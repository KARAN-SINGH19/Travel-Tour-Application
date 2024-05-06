from django.shortcuts import render, redirect
from adminPanel.models import *
from hotelBooking.models import *
from django.utils import timezone
import stripe
from django.core.mail import send_mail, EmailMessage
import os
from home.models import *
from django.contrib import messages
import requests


def get_exchange_rate(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data['result'] == 'success':
        rate_usd_aed = data['conversion_rates']['AED']
        rate_aed_usd = 1 / rate_usd_aed
        return rate_aed_usd
    else:
        print("Failed to fetch exchange rate.")
        return None


def bookResort(request, id, name, location, image):
    roomData = resortRoomtype.objects.filter(resort_id=id)
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
            print(price)
        prices.append(price)
    zipped_data = zip(roomData, prices)
    context = {'id': id, 'name': name,
               'location': location, 'image': image, 'zipped_data': zipped_data, 'currencySelected': currencySelected}
    return render(request, 'bookResort.html', context)


def confirmBooking(request, id, name, location, roomType, roomPrice):
    roomData = resortRoomtype.objects.filter(resort_id=id)
    logged_in_user = request.user
    members = Member.objects.filter(username=logged_in_user)
    couponCodes = offers.objects.values_list('couponCode', flat=True)
    username = request.user
    if request.method == 'POST':
        reservationType = request.POST['resortName']
        reservationRoom = request.POST['roomType']
        reservationAmt = request.POST['price']
        reservationDuration = request.POST['bookingDuration']
        
        if 'couponCode' in request.POST:
            couponCode = request.POST['couponCode']
        else:
            couponCode = ''

        if couponCode == '':
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
            discountPercentage = offer.discountPercentage  # DISCOUNT PERCENTAGE
            reservationAmt = int(reservationAmt) * \
                int(reservationDuration)  # AMOUNT B4 DISCOUNT
            # DISCOUNT AMOUNT
            discountAmt = (int(reservationAmt)*int(discountPercentage))/100
            reservationFinalamt = reservationAmt-discountAmt  # FINAL AMOUNT
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
            return render(request, 'confirmResortbooking.html', context)
        return redirect('resortBooking:generateReceipt')

    context = {'roomData': roomData, 'name': name, 'location': location,
               'roomType': roomType, 'roomPrice': roomPrice, 'members': members}
    return render(request, 'confirmResortbooking.html', context)


def generateReceipt(request):
    currencySelected = request.session.get('currency')
    username = request.user
    firstname = username.first_name
    email = username.email
    lastname = username.last_name
    current_datetime = timezone.now()
    obj = Reservation.objects.last()
    finalAmount = obj.reservation_amount
    hotelName = obj.reservation_type
    roomType = obj.reservation_room
    duration = obj.reservation_duration
    discount = request.session.get('discount')
    amount = request.session.get('amount')
    context = {'firstname': firstname, 'lastname': lastname, 'reservationFinalamt': finalAmount, 'current_datetime': current_datetime, 'reservation_type': hotelName,
               'reservation_room': roomType, 'userEmail': email, 'obj': obj, 'reservationDuration': duration, 'discount': discount, 'amount': amount, 'currencySelected': currencySelected}
    return render(request, 'generateReceipt.html', context)


stripe.api_key = "sk_test_51NxBhTEWwd2L3hVcqKggRsddgVdE7Q2gO7tkapbEzMRINxkLf9twyWTIbMv0K9cpkieEAfGXRHTsoyClzt7yhQwX007TC5uy2q"


def checkout_session(request, id):
    data = Reservation.objects.get(reservation_id=id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'aed',
                'product_data': {
                    'name': data.reservation_type,
                },
                'unit_amount': (data.reservation_amount)*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/hotelBooking/success/',
        cancel_url='http://127.0.0.1:8000/hotelBooking/error/',
    )
    return redirect(session.url, code=303)


def success(request):
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'error.html')
