import os
import time
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from adminPanel.models import *
from django.db.models import Q
from datetime import datetime
from flightBooking.models import *
import stripe
from django.contrib import messages
from django.utils import timezone
from django.utils.dateparse import parse_time
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage
import pdfkit
from pathlib import Path
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


def selectSingleflight(request):
    if request.method == 'POST':
        context = {}
        tripType = 'One Way'

        # RERIEVING THE DETAILS ENTERED BY THE USER
        deptCity = request.POST['deptCity']
        arrivalCity = request.POST['arrivalCity']
        passengers = request.POST['passengers']
        flightClass = request.POST['flight_class']
        deptDate_str = request.POST['deptDate']

        # COVERTING THE DATE INTO PYTHON DATE OBJECT SO THAT WE CAN COMPARE THE DATES IF NECESSARY
        deptDate = datetime.strptime(deptDate_str, '%Y-%m-%d').date()

        flightData = Flight.objects.filter(arrival_city=arrivalCity,   flight_trip=tripType,
                                           departure_city=deptCity, departure_date=deptDate, flight_class=flightClass)

        if flightData:
            exchange_rate_aed_usd = get_exchange_rate(
                '8f16f9cb77815e97e5c6ffe2')
            prices = []
            currencySelected = request.session.get('currency')
            for x in flightData:
                if (currencySelected == 'USD'):
                    conversion = int(x.price) * exchange_rate_aed_usd
                    price = round(conversion)
                else:
                    price = x.price
                prices.append(price)
            zipped_data = zip(flightData, prices)
        else:
            return redirect('flightBooking:notFound')

        context = {'zipped_data': zipped_data,
                   'passengers': passengers, 'currencySelected': currencySelected}
    return render(request, 'selectSingleflight.html', context)


def selectDoubleflight(request):
    currencySelected = request.session.get('currency')
    if request.method == 'POST':
        context = {}
        tripType = 'Round Trip'

        # RERIEVING THE DETAILS ENTERED BY THE USER
        deptCity = request.POST['deptCity']
        arrivalCity = request.POST.get('arrivalCity')
        flight_class = request.POST['flight_class']
        passengers = request.POST['passengers']
        deptDate_str = request.POST['deptDate']
        returnDate_str = request.POST['returnDate']

        # COVERTING THE DATE INTO PYTHON DATE OBJECT SO THAT WE CAN COMPARE THE DATES IF NECESSARY
        deptDate = datetime.strptime(deptDate_str, '%Y-%m-%d').date()
        returnDate = datetime.strptime(returnDate_str, '%Y-%m-%d').date()

        # SEGEMTING THE DATA INTO 2 SECTIONS [OUTBOUND DATA AND INBOUND DATA]
        outboundData = Flight.objects.filter(arrival_city=arrivalCity,   flight_trip=tripType,
                                             departure_city=deptCity, departure_date=deptDate, return_date=returnDate, flight_class=flight_class)
        inboundData = Flight.objects.filter(departure_city=arrivalCity, arrival_city=deptCity,
                                            flight_trip=tripType, flight_class=flight_class, departure_date=returnDate)

        exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')
        outboundPrices = []
        currencySelected = request.session.get('currency')
        for x in outboundData:
            if (currencySelected == 'USD'):
                coversion = int(x.price) * exchange_rate_aed_usd
                price = round(coversion)
            else:
                price = x.price
            outboundPrices.append(price)
            print(outboundPrices)

        inboundPrices = []
        currencySelected = request.session.get('currency')
        for x in inboundData:
            if (currencySelected == 'USD'):
                coversion = int(x.price) * exchange_rate_aed_usd
                price = round(coversion)
            else:
                price = x.price
            inboundPrices.append(price)
            print(inboundPrices)

        outboundprices = zip(outboundData, outboundPrices)
        inboundprices = zip(inboundData, inboundPrices)

        context = {'currencySelected': currencySelected, 'outboundprices': outboundprices, 'inboundprices': inboundprices,
                   'passengers': passengers, 'outboundData': outboundData, 'inboundData': inboundData}
    return render(request, 'selectDoubleflight.html', context)


def confirmSingleflight(request, origincode, destinationcode, airline, id, duration, passengers, price, finalFare, image, deptDate, returnDate, deptTime, arrTime, deptCity, arrCity, airlineName, flightId, flightClass):
    passengerscount = []
    passenger_details = []
    passenger_names = []
    passenger_age = []
    passenger_gender = []

    # LOGGED IN USER DETAILS
    user_instance = request.user

    # CALCULATING THE FINAL FARE
    finalFare = int(passengers)*int(price)

    if request.method == 'POST':

        # RETRIEVIENG THE PASSENGER DETAILS FROM THE FORM
        for i in range(passengers):
            name = request.POST.get(f'name{i}')
            age = request.POST.get(f'age{i}')
            gender = request.POST.get(f'gender{i}')
            passenger_details2 = {
                'Name': name,
                'Age': age,
                'Gender': gender
            }
            passenger_details.append(passenger_details2)

        # ADDING THE PASSENGER NAME,AGE AND GENDER INTO THE LIST AND STORING INTO SESSION VARIBEL SO THAT I CAN USE THEM IN THE TICKET PAGE TO DISPLAY THE PASSENGER DETAILS
        for i in range(passengers):
            names = passenger_details[i]['Name']
            age = passenger_details[i]['Age']
            gender = passenger_details[i]['Gender']
            passenger_names.append(names)
            passenger_age.append(age)
            passenger_gender.append(gender)

        # STROING THESE ARRAYS IN SESSION VARIABLE
        request.session['names'] = passenger_names
        request.session['age'] = passenger_age
        request.session['gender'] = passenger_gender

        print(passenger_names)
        print(passenger_age)
        print(passenger_gender)

        flightReservation = singleFlightreservations.objects.create(
            flight_id=id,
            airline=airline,
            origin_code=origincode,
            destination_code=destinationcode,
            flight_duration=duration,
            departure=deptCity,
            arrival=arrCity,
            passenger_details=passenger_details,
            departure_date=deptDate,
            departure_time=deptTime,
            arrival_time=arrTime,
            flight_class=flightClass,
            price=finalFare,
            username=user_instance
        )
        flightReservation.save()
        return redirect('flightBooking:generateFlightreceipt1')

    # CREATING A LIST SO THAT ACCORDING TO THE PASSENGERS I CAN RENDER THE FORM OF THE CONFIRM FLIGHT PAGE
    for i in range(0, passengers, 1):
        passengerscount.append(i)

    deptTime = datetime.strptime(deptTime, '%H:%M:%S')
    arrTime = datetime.strptime(arrTime, '%H:%M:%S')

    context = {
        'passengers': passengers,
        'finalFare': finalFare,
        'price': price,
        'image': image,
        'deptDate': deptDate,
        'destinationcode': destinationcode,
        'origincode': origincode,
        'returnDate': returnDate,
        'deptTime': deptTime,
        'arrTime': arrTime,
        'deptCity': deptCity,
        'arrCity': arrCity,
        'airlineName': airlineName,
        'flightId': flightId,
        'flightClass': flightClass,
        'passengerscount': passengerscount,
    }

    return render(request, 'confirmSingleflight.html', context)


def confirmDoubleflight(request, return_date, departure_date, flightClass, passengers, image):
    request.session['passengers'] = passengers
    passengersCount = []
    logged_in_user = request.user

    if request.method == 'POST':

        # INBOUND DATA
        InboundDepartureCity = request.POST['InboundDepartureCity']
        InboundArrivalCity = request.POST['InboundArrivalCity']
        InboundDepartureTime = request.POST['InboundDepartureTime']
        InboundArrivalTime = request.POST['InboundArrivalTime']
        InboundAirline = request.POST['InboundAirline']
        InboundPrice = request.POST['InboundPrice']
        InboundFlightid = request.POST['InboundFlightid']
        InboundFinalfare = int(passengers)*int(InboundPrice)

        # OUTBOUND DATA
        OutboundDepartureCity = request.POST['OutboundDepartureCity']
        OutboundArrivalCity = request.POST['OutboundArrivalCity']
        OutboundDepartureTime = request.POST['OutboundDepartureTime']
        OutboundArrivalTime = request.POST['OutboundArrivalTime']
        OutboundAirline = request.POST['OutboundAirline']
        OutboundPrice = request.POST['OutboundPrice']
        OutboundFlightid = request.POST['OutboundFlightid']
        OutboundFinalfare = int(passengers)*int(OutboundPrice)

        Inbounddata = Flight.objects.get(flight_id=InboundFlightid)
        Outbounddata = Flight.objects.get(flight_id=OutboundFlightid)

        # RETRIEVING THE INBOUND DETAILS FROM THE Inbounddata OBJECT SO THAT I CAN STORE THEM UNDER THE OutboundFlightDetails TABLE
        InboundOriginCode = Inbounddata.origin_code
        InboundDestinationCode = Inbounddata.destination_code
        InboundDuration = Inbounddata.flight_duration

        # RETRIEVING THE OUTBOUND DETAILS FROM THE Outbounddata OBJECT SO THAT I CAN STORE THEM UNDER THE InboundFlightDetails TABLE
        OutboundOriginCode = Outbounddata.origin_code
        OutboundDestinationCode = Outbounddata.destination_code
        OutboundDuration = Outbounddata.flight_duration

        # CALCULATING THE TOTAL AMT AS I NEED TO STORE THIS UNDER doubleFlightreservations TABLE
        Totalamt = int(InboundFinalfare)+int(OutboundFinalfare)

        # SAVING DATA INTO doubleFlightreservations TABLE
        roundTripreservations = doubleFlightreservations.objects.create(
            departure_date=departure_date,
            return_date=return_date,
            origin_code=OutboundOriginCode,
            destination_code=OutboundDestinationCode,
            total_amount=Totalamt,
            username=logged_in_user
        )
        roundTripreservations.save()

        # RETRIEVING THE RESERVATION OBJECT RECENTLY CREATED SINCE I HAVE USED IT AS FOREIGN KEY IN OutboundFlightDetails AND InboundFlightDetails
        firstReservation = doubleFlightreservations.objects.filter().last()

        # SAVING DATA INTO OutboundFlightDetails TABLE
        outboundDetails = OutboundFlightDetails.objects.create(
            reservation_id=firstReservation,
            flight_duration=OutboundDuration,
            origin_code=OutboundOriginCode,
            departure_city=OutboundDepartureCity,
            destination_code=OutboundDestinationCode,
            arrival_city=OutboundArrivalCity,
            airline=OutboundAirline,
            flight_id=OutboundFlightid,
            flight_class=flightClass,
            price=OutboundPrice,
            departure_time=Outbounddata.departure_time,
            arrival_time=Outbounddata.arrival_time
        )
        outboundDetails.save()

        # SAVING DATA INTO InboundFlightDetails TABLE
        inboundDetails = InboundFlightDetails.objects.create(
            reservation_id=firstReservation,
            flight_duration=InboundDuration,
            origin_code=InboundOriginCode,
            departure_city=InboundDepartureCity,
            destination_code=InboundDestinationCode,
            arrival_city=InboundArrivalCity,
            airline=InboundAirline,
            flight_id=InboundFlightid,
            flight_class=flightClass,
            price=InboundPrice,
            departure_time=Inbounddata.departure_time,
            arrival_time=Inbounddata.arrival_time
        )
        inboundDetails.save()

        for i in range(0, passengers, 1):
            passengersCount.append(i)

        context = {'InboundDepartureCity': InboundDepartureCity, 'InboundArrivalCity': InboundArrivalCity, 'InboundDepartureTime': InboundDepartureTime, 'InboundArrivalTime': InboundArrivalTime, 'InboundAirline': InboundAirline, 'InboundPrice': InboundPrice, 'InboundFlightid': InboundFlightid, 'InboundOriginCode': InboundOriginCode, 'InboundDestinationCode': InboundDestinationCode, 'InboundFinalfare': InboundFinalfare,
                   'OutboundDepartureCity': OutboundDepartureCity, 'OutboundArrivalCity': OutboundArrivalCity, 'OutboundDepartureTime': OutboundDepartureTime, 'OutboundArrivalTime': OutboundArrivalTime, 'OutboundAirline': OutboundAirline, 'OutboundPrice': OutboundPrice, 'OutboundFlightid': OutboundFlightid, 'OutboundOriginCode': OutboundOriginCode, 'OutboundDestinationCode': OutboundDestinationCode, 'OutboundFinalfare': OutboundFinalfare,
                   'departure_date': departure_date, 'return_date': return_date, 'flightClass': flightClass, 'passengersCount': passengersCount, 'passengers': passengers, 'Totalamt': Totalamt, 'image': image}

    return render(request, 'confirmDoubleflight.html', context)


def generateFlightreceipt1(request):
    currencySelected = request.session.get('currency')
    print(currencySelected)
    username = request.user
    firstname = username.first_name
    email = username.email
    lastname = username.last_name
    current_datetime = timezone.now()
    data = singleFlightreservations.objects.filter().last()
    return render(request, 'generateFlightreceipt1.html', {'data': data, 'current_datetime': current_datetime, 'firstname': firstname, 'lastname': lastname, 'email': email, 'currencySelected': currencySelected})


def generateFlightreceipt2(request, passengers, Totalamt, InboundFinalfare, OutboundFinalfare):
    currencySelected = request.session.get('currency')

    passenger_details = []
    passenger_names = []
    ages = []
    genders = []

    # LOGGED IN USER DETAILS
    username = request.user
    firstname = username.first_name
    email = username.email
    lastname = username.last_name
    current_datetime = timezone.now()

    reservation = doubleFlightreservations.objects.filter().last()
    inboundata = InboundFlightDetails.objects.filter().last()
    outboundata = OutboundFlightDetails.objects.filter().last()

    # RETRIEVIENG THE PASSENGER DETAILS FROM THE FORM
    if request.method == 'POST':
        for i in range(passengers):
            name = request.POST[f'name{i}']
            age = request.POST[f'age{i}']
            gender = request.POST[f'gender{i}']
            passenger_details2 = {
                'Name': name,
                'Age': age,
                'Gender': gender
            }
            passenger_details.append(passenger_details2)

    # ADDING THE PASSENGER NAME,AGE AND GENDER INTO THE LIST AND STORING INTO SESSION VARIBEL SO THAT I CAN USE THEM IN THE TICKET PAGE TO DISPLAY THE PASSENGER DETAILS
        for i in range(passengers):
            names = passenger_details[i]['Name']
            age = passenger_details[i]['Age']
            gender = passenger_details[i]['Gender']
            passenger_names.append(names)
            ages.append(age)
            genders.append(gender)

    # STROING THESE ARRAYS IN SESSION VARIABLE
        request.session['passenger_names'] = passenger_names
        request.session['passenger_ages'] = ages
        request.session['passenger_genders'] = genders

        print(passenger_names)
        print(ages)
        print(genders)

    # BASICALLY HERE I AM UPDATING (ADDING THE PASSENGER DETAILS AS I DIDNT ADD THEM IN confirmDoubleflight VIEW FUNC ) THE INBOUND AND OUTBOUND DATA DETAILS
        outboundata.passenger_details = passenger_details
        inboundata.passenger_details = passenger_details
        outboundata.save()
        inboundata.save()

    return render(request, 'generateFlightreceipt2.html', {'reservation': reservation, 'inboundata': inboundata, 'outboundata': outboundata, 'Totalamt': Totalamt, 'current_datetime': current_datetime, 'firstname': firstname, 'lastname': lastname, 'email': email, 'InboundFinalfare': InboundFinalfare, 'OutboundFinalfare': OutboundFinalfare, 'currencySelected': currencySelected})


stripe.api_key = "sk_test_51NxBhTEWwd2L3hVcqKggRsddgVdE7Q2gO7tkapbEzMRINxkLf9twyWTIbMv0K9cpkieEAfGXRHTsoyClzt7yhQwX007TC5uy2q"


def checkout_session1(request):
    currencySelected = request.session.get('currency')
    data = singleFlightreservations.objects.filter().last()
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currencySelected,
                'product_data': {
                    'name': data.departure+" "+data.arrival,
                },
                'unit_amount': (data.price)*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/flightBooking/ticket/',
        cancel_url='http://127.0.0.1:8000/flightBooking/error/',
    )
    return redirect(session.url, code=303)


def checkout_session2(request, Totalamt):
    currencySelected = request.session.get('currency')
    outboundata = OutboundFlightDetails.objects.filter().last()
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': currencySelected,
                'product_data': {
                    'name': outboundata.departure_city+" "+outboundata.arrival_city,
                },
                'unit_amount': (Totalamt)*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://127.0.0.1:8000/flightBooking/ticket2/',
        cancel_url='http://127.0.0.1:8000/flightBooking/error/',
    )
    return redirect(session.url, code=303)


def ticket(request):
    currencySelected = request.session.get('currency')
    current_datetime = timezone.now()
    username = request.user
    email = username.email

    # RETRIEVING THE LATEST RESERVATIONS ADDED INTO THE DB SO THAT CAN SHOW THEIR DETAILS IN THE TICKET
    reservationData = singleFlightreservations.objects.filter().last()

    # RETRIEVING THE PASSENGER DETAILS FROM THE SESSION
    passenger_names = request.session.get('names')
    passenger_age = request.session.get('age')
    passenger_gender = request.session.get('gender')

    # MAKING THESE PASSENGER DETAILS AS A SINGLE ITERATBALE VARIABLE WITH ZIP FUNCTION
    passenger_details = zip(passenger_names, passenger_age, passenger_gender)

    return render(request, 'ticket1.html', {'currencySelected': currencySelected, 'reservationData': reservationData, 'email': email, 'username': username, 'current_datetime': current_datetime, 'passenger_details': passenger_details})


def sendEmail(request, id):
    if request.method == 'POST':
        username = request.user
        email = username.email
        fileName = f'OnewayTicket_{id}.pdf'
        downloadsFolder = os.path.expanduser("~/Downloads")
        filePath = os.path.join(downloadsFolder, fileName)
        senderEmail = 'tripcanvas30@gmail.com'
        receiverEmail = email
        email = EmailMessage(
            subject='Flight Ticket PDF',
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


def sendEmail2(request, id):
    if request.method == 'POST':
        username = request.user
        email = username.email
        fileName = f'RoundwayTicket_{id}.pdf'
        downloadsFolder = os.path.expanduser("~/Downloads")
        filePath = os.path.join(downloadsFolder, fileName)
        senderEmail = 'tripcanvas30@gmail.com'
        receiverEmail = email
        email = EmailMessage(
            subject='Flight Ticket PDF',
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


def ticket2(request):
    currencySelected = request.session.get('currency')

    current_datetime = timezone.now()
    username = request.user
    email = username.email

    # RETRIEVING THE LATEST RESERVATIONS ADDED INTO THE DB SO THAT CAN SHOW THEIR DETAILS IN THE TICKET
    reservationData = doubleFlightreservations.objects.filter().last()
    inboundData = InboundFlightDetails.objects.filter().last()
    outboundData = OutboundFlightDetails.objects.filter().last()

    # RETRIEVING THE PASSENGER DETAILS FROM THE SESSION
    passenger_names = request.session.get('passenger_names')
    passenger_ages = request.session.get('passenger_ages')
    passenger_genders = request.session.get('passenger_genders')

    # MAKING THESE PASSENGER DETAILS AS A SINGLE ITERATBALE VARIABLE WITH ZIP FUNCTION
    passenger_details = zip(passenger_names, passenger_ages, passenger_genders)

    # CALCALATING THE TOTAL AMT FOR INBOUND AND OUTBOUND DATA BY MULTIPLYING THE NO OF PASSESNGERS * THE PRICE PER PERSON
    passengerCount = len(passenger_names)
    totalamtOutbound = int(outboundData.price)*int(passengerCount)
    totalamtInbound = int(inboundData.price)*int(passengerCount)

    return render(request, 'ticket2.html', {'currencySelected': currencySelected, 'reservationData': reservationData, 'email': email, 'username': username, 'current_datetime': current_datetime, 'inboundData': inboundData, 'outboundData': outboundData, 'passenger_details': passenger_details, 'totalamtOutbound': totalamtOutbound, 'totalamtInbound': totalamtInbound})


def notFound(request):
    return render(request, 'flightNF.html')
