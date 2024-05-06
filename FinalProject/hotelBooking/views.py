from django.shortcuts import render, redirect
from adminPanel.models import *
from hotelBooking.models import *
from django.utils import timezone
import stripe
from django.core.mail import send_mail, EmailMessage
import os
from home.models import *
from django.contrib import messages
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from itertools import zip_longest
import requests


def get_exchange_rate(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    # requests library to fetch the data from api/server
    response = requests.get(url)
    # json function of requests library to convert josn data into pytjon dict
    data = response.json()
    if response.status_code == 200 and data['result'] == 'success':
        rate_usd_aed = data['conversion_rates']['AED']
        rate_aed_usd = 1 / rate_usd_aed
        return rate_aed_usd
    else:
        print("Failed to fetch exchange rate.")
        return None


def bookHotel(request, id, name, location, image):
    roomData = hotelRoomtype.objects.filter(hotel_id=id)
    prices = []
    currencySelected = request.session.get('currency')
    exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')
    print(exchange_rate_aed_usd)

    for x in roomData:
        if (currencySelected == 'USD'):
            coversion = int(x.room_price) * exchange_rate_aed_usd
            price = round(coversion)
        else:
            price = x.room_price
        prices.append(price)
    zipped_data = zip(roomData, prices)

    context = {'id': id, 'name': name,
               'location': location, 'image': image, 'zipped_data': zipped_data, 'currencySelected': currencySelected}
    return render(request, 'bookHotel.html', context)


def confirmBooking(request, id, name, location, roomType, roomPrice):
    roomData = hotelRoomtype.objects.filter(hotel_id=id)
    username = request.user  # REQUEST.USER WILL GIVE ME THE LOGGED IN USER'S USERNAME
    # CHECKING WHEATHER THE LOGGED IN USER IS A MEMNER OR NO
    members = Member.objects.filter(username=username)
    # SPEICIFALLY RETIEVING THE VALUES UNDER couponCode COLUMN OF OFFERS TABLE
    couponCodes = offers.objects.values_list('couponCode', flat=True)
    if request.method == 'POST':
        reservationType = request.POST['hotelName']
        reservationRoom = request.POST['roomType']
        reservationAmt = request.POST['price']
        reservationDuration = request.POST['bookingDuration'] 

        if 'couponCode' in request.POST:
            couponCode = request.POST['couponCode']
        else:
            couponCode = ''

        if couponCode == '':
            print("hello")
            current_datetime = timezone.now()
            reservationAmt = int(reservationAmt)*int(reservationDuration)

            obj = Reservation.objects.create(
                reservation_type=reservationType,
                reservation_room=reservationRoom,
                reservation_amount=reservationAmt,
                reservation_dateTime=current_datetime,
                reservation_duration=reservationDuration,
                reservation_location=location,
                username=username
            )
            request.session['amount'] = reservationAmt
            request.session['discount'] = 0
            obj.save()

        elif couponCode in couponCodes:
            offer = offers.objects.get(couponCode=couponCode)

            # DISCOUNT PERCENTAGE
            discountPercentage = offer.discountPercentage

            # AMOUNT B4 DISCOUNT
            reservationAmt = int(reservationAmt) * int(reservationDuration)

            # DISCOUNT AMOUNT
            discountAmt = (int(reservationAmt)*int(discountPercentage))/100

            # FINAL AMOUNT
            reservationFinalamt = reservationAmt-discountAmt

            request.session['discount'] = discountAmt
            request.session['amount'] = reservationAmt

            current_datetime = timezone.now()

            obj = Reservation.objects.create(
                reservation_type=reservationType,
                reservation_room=reservationRoom,
                reservation_amount=reservationFinalamt,
                reservation_dateTime=current_datetime,
                reservation_duration=reservationDuration,
                reservation_location=location,
                username=username
            )
            obj.save()
        else:
            messages.error(request, "Invalid Coupon Code!")
            context = {'name': name, 'location': location,
                       'roomType': roomType, 'roomPrice': roomPrice, 'members': members}
            return render(request, 'confirmHotelbooking.html', context)
        return redirect('hotelBooking:generateReceipt')

    context = {'roomData': roomData, 'name': name, 'location': location,
               'roomType': roomType, 'roomPrice': roomPrice, 'members': members}
    return render(request, 'confirmHotelbooking.html', context)


def generateReceipt(request):
    currencySelected = request.session.get('currency')
    loggedUser = request.user

    # RETEVING USER DETAILS
    firstname = loggedUser.first_name
    email = loggedUser.email
    lastname = loggedUser.last_name

    # GETTING CURRENT DATE TIME
    current_datetime = timezone.now()

    # GETTING THE LATEST RESERVATION MADE WITH LAST FUNCTION
    obj = Reservation.objects.last()

    # RETREIVING THE AMPUN DETAILS, HOTEL NAME, ROOM TYPE AND DURATION OF BOOKING FROM obj WHICH CONTAINS ALL THE INFO REGARDING THE RESERVATION MADE
    finalAmount = obj.reservation_amount
    hotelName = obj.reservation_type
    roomType = obj.reservation_room
    duration = obj.reservation_duration

    # ACCESSING THE DISCOUNT AND RESERVATION AMT FROM SESSION VARIABLE
    discount = request.session.get('discount')
    amount = request.session.get('amount')

    # MAKING CONTEXT VARIABLE
    context = {'firstname': firstname, 'lastname': lastname, 'reservationFinalamt': finalAmount, 'current_datetime': current_datetime, 'reservation_type': hotelName,
               'reservation_room': roomType, 'userEmail': email, 'obj': obj, 'reservationDuration': duration, 'discount': discount, 'amount': amount, 'currencySelected': currencySelected}
    return render(request, 'generateReceipt.html', context)


stripe.api_key = "sk_test_51NxBhTEWwd2L3hVcqKggRsddgVdE7Q2gO7tkapbEzMRINxkLf9twyWTIbMv0K9cpkieEAfGXRHTsoyClzt7yhQwX007TC5uy2q"


def checkout_session(request, id):
    data = Reservation.objects.get(reservation_id=id)
    currencySelected = request.session.get('currency')
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currencySelected,
                'product_data': {
                    'name': data.reservation_type,
                },
                'unit_amount': (data.reservation_amount)*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/hotelBooking/hotelPass/'
    )
    return redirect(session.url, code=303)


def hotelPass(request):
    current_datetime = timezone.now()
    reservationData = Reservation.objects.last()
    return render(request, 'hotelPass.html', {'reservationData': reservationData, 'current_datetime': current_datetime})


def sendEmail(request, id, type):
    if request.method == 'POST':
        username = request.user
        email = username.email
        fileName = f'{type}Pass_{id}.pdf'  # CREATING THE FILE NAME
        downloadsFolder = os.path.expanduser("~/Downloads")  # SAVING THE FILE
        # CREATING THE PATH WHERE THE FILE WILL IS STORED
        filePath = os.path.join(downloadsFolder, fileName)
        senderEmail = 'tripcanvas30@gmail.com'
        receiverEmail = email
        email = EmailMessage(
            subject=f'{type} Pass PDF',
            body="""We are thrilled to confirm your reservation for your upcoming travel plans. Whether you are jetting off to your dream destination or unwinding in a luxurious resort, your [Flight/Hotel/Resort] booking is now secured.
            Please find attached your [Flight Ticket/Hotel Pass/Resort Voucher] for easy access during your trip. Should you have any questions or require further assistance, feel free to reach out to our dedicated customer support team.
            Safe travels, and we look forward to providing you with an exceptional experience!
            Warm regards""",
            from_email=senderEmail,
            to=[receiverEmail],
        )
        email.attach_file(filePath)
        email.send()
    return render(request, 'success.html')


def invalidCode(request):
    return render(request, 'invalidCode.html')
