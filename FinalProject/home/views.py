from django.shortcuts import render
from adminPanel.models import *
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.contrib import messages
from hotelBooking.models import *
from flightBooking.models import *
from datetime import datetime
import stripe
from home.models import *
from itertools import zip_longest
from django.http import HttpResponse
import requests
from django.core.paginator import Paginator


def get_exchange_rate(api_key):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    response = requests.get(url)  # SENDING GET REQUEST TO THE URL
    data = response.json()  # COVERTING THE DATA INTO JSON FORMAT
    if response.status_code == 200 and data['result'] == 'success':
        rate_usd_aed = data['conversion_rates']['AED']
        rate_aed_usd = 1 / rate_usd_aed
        return rate_aed_usd
    else:
        print("Failed to fetch exchange rate.")
        return None


def home(request):
    onewayDeptdata = []
    onewayArrdata = []
    roundwayDeptdata = []
    roundwayArrdata = []

    onewayData = Flight.objects.filter(flight_trip__contains='One Way')
    roundTripData = Flight.objects.filter(
        flight_trip__contains='Round Trip').exclude(return_date=None)

    # flat=true is used to get a list of values instead of list of tuples
    onewayDept = onewayData.values_list('departure_city', flat=True).distinct()
    onewayArr = onewayData.values_list('arrival_city', flat=True).distinct()
    roundtripDept = roundTripData.values_list(
        'departure_city', flat=True).distinct()
    roundtripArr = roundTripData.values_list(
        'arrival_city', flat=True).distinct()

    for i in roundtripDept:
        roundwayDeptdata.append(i)

    for i in roundtripArr:
        roundwayArrdata.append(i)

    for i in onewayDept:
        onewayDeptdata.append(i)

    for i in onewayArr:
        onewayArrdata.append(i)

    context = {'onewayData': onewayData, 'roundwayDeptdata': roundwayDeptdata,
               'roundwayArrdata': roundwayArrdata, 'onewayDeptdata': onewayDeptdata, 'onewayArrdata': onewayArrdata}
    return render(request, 'homePage.html', context)


def hotelHome(request):
    hotelData = Hotel.objects.filter(starting_price__gt=1000)
    exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')

    prices = []
    currencySelected = request.session.get('currency')
    for x in hotelData:
        if currencySelected == 'USD':
            conversion = int(x.starting_price) * exchange_rate_aed_usd
            price = round(conversion)
        else:
            price = x.starting_price
        prices.append(price)

    # ZIP FUNCTION ALLOWS US TO SEND TWI VARIBALES TOGTHER IN A SINGLE ITERATABLE VARIABLE
    zipped_data = zip(hotelData, prices)

    return render(request, 'hotelHome.html', {'zipped_data': zipped_data, 'currencySelected': currencySelected})


def hotels(request):
    hotelData = Hotel.objects.all()
    exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')

    prices = []
    currencySelected = request.session.get('currency')
    for x in hotelData:
        if (currencySelected == 'USD'):
            coversion = round(int(x.starting_price)*exchange_rate_aed_usd)
            price = round(coversion)
        else:
            price = x.starting_price
        prices.append(price)

    zipped_data = zip(hotelData, prices)

    context = {'zipped_data': zipped_data,
               'currencySelected': currencySelected}
    return render(request, 'hotels.html', context)


def hotelSearch(request):
    if request.method == "GET":
        currencySelected = request.session.get('currency')
        exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')
        prices = []
        searchData = request.GET.get('search', '')
        print(searchData)
        if searchData:
            hotelData = Hotel.objects.filter(
                Q(hotel_name__icontains=searchData) |
                Q(hotel_location__icontains=searchData) |
                Q(starting_price__icontains=searchData)
            )
            print(hotelData)
            for x in hotelData:
                if (currencySelected == 'USD'):
                    coversion = round(int(x.starting_price)
                                      * exchange_rate_aed_usd)
                    price = round(coversion)
                else:
                    price = x.starting_price
                prices.append(price)
            zipped_data = zip(hotelData, prices)
    return render(request, 'hotels.html', {'zipped_data': zipped_data, 'currencySelected': currencySelected})


def checkCurrency(request):
    if request.method == 'POST':
        if request.POST.get('currency') == 'USD':
            request.session['currency'] = 'USD'
        elif request.POST.get('currency') == 'AED':
            request.session['currency'] = 'AED'
    return redirect('home:home')


def resortHome(request):
    resortData = Resort.objects.filter(starting_price__gt=1500)
    exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')

    prices = []
    currencySelected = request.session.get('currency')
    for x in resortData:
        if currencySelected == 'USD':
            conversion = int(x.starting_price) * exchange_rate_aed_usd
            price = round(conversion)
        else:
            price = x.starting_price
        prices.append(price)

    zipped_data = zip(resortData, prices)

    context = {'zipped_data': zipped_data,
               'currencySelected': currencySelected}
    return render(request, 'resortHome.html', context)


def resorts(request):
    resortData = Resort.objects.all()
    exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')

    prices = []
    currencySelected = request.session.get('currency')
    for x in resortData:
        if (currencySelected == 'USD'):
            coversion = round(int(x.starting_price)*exchange_rate_aed_usd)
            price = round(coversion)
        else:
            price = x.starting_price
        prices.append(price)

    zipped_data = zip_longest(resortData, prices)

    context = {'zipped_data': zipped_data,
               'currencySelected': currencySelected}
    return render(request, 'resorts.html', context)


def resortSearch(request):
    if request.method == "GET":
        currencySelected = request.session.get('currency')
        exchange_rate_aed_usd = get_exchange_rate('8f16f9cb77815e97e5c6ffe2')
        prices = []
        searchData = request.GET.get('search', '')
        print(searchData)
        if searchData:
            resortData = Resort.objects.filter(
                Q(resort_name__icontains=searchData) |
                Q(resort_location__icontains=searchData) |
                Q(starting_price__icontains=searchData)
            )
            print(resortData)
            for x in resortData:
                if (currencySelected == 'USD'):
                    coversion = round(int(x.starting_price)
                                      * exchange_rate_aed_usd)
                    price = round(coversion)
                else:
                    price = x.starting_price
                prices.append(price)
            zipped_data = zip(resortData, prices)
    return render(request, 'resorts.html', {'zipped_data': zipped_data, 'currencySelected': currencySelected})


def reservations(request):
    currencySelected = request.session.get('currency')
    logged_in_user = request.user
    hotelresort_Reservations = Reservation.objects.filter(
        username=logged_in_user)
    onewayflight_Reservations = singleFlightreservations.objects.filter(
        username=logged_in_user)
    roundtripflight_Reservations = doubleFlightreservations.objects.filter(
        username=logged_in_user)
    return render(request, 'reservations.html', {'currencySelected': currencySelected, 'hotelresort_Reservations': hotelresort_Reservations, 'onewayflight_Reservations': onewayflight_Reservations, 'roundtripflight_Reservations': roundtripflight_Reservations})


def deleteReservations(request, id):
    reservation = Reservation.objects.get(reservation_id=id)
    reservation.delete()
    return redirect('home:reservations')


def delete_oneway_Reservations(request, id):
    reservation = singleFlightreservations.objects.get(reservation_id=id)
    reservation.delete()
    return redirect('home:reservations')


def delete_roundtrip_Reservations(request, id):
    reservation = doubleFlightreservations.objects.get(reservation_id=id)
    reservation.delete()
    return redirect('home:reservations')


def updateProfile(request):
    loggedUser = request.user
    username = loggedUser.username
    email = loggedUser.email
    context = {'username': username, 'email': email}
    if request.method == 'POST':
        
        #ASSUMING THAT THE FIELD WILL EITHER HAVE THE NEW DETAILS OR AN EMPTY STRING
        newFname = request.POST.get('fname', '')
        newLname = request.POST.get('lname', '')
        newEmail = request.POST.get('email', '')
        newUsername = request.POST.get('username', '')
        newPassword = request.POST.get('password', '')
        
        #RETRIEVING THE LOGGED IN USER'S DETAILS
        user = User.objects.get(username=username)

        #IF DETAILS ARE SPECIFIED WE WILL UPDATE THE EXISTING DETAILS
        if newFname:
            user.first_name = newFname
        if newLname:
            user.last_name = newLname
        if newEmail:
            user.email = newEmail
        if newUsername:
            user.username = newUsername
        if newPassword:
            user.set_password(newPassword)
        user.save()

    return render(request, 'updateProfile.html', context)


def membership(request):
    return render(request, 'membership.html')


def userFeedback(request):
    logged_in_user = request.user
    if request.method == 'POST':
        # WE CAN USE request.POST() AS WELL AS request.POST.get()
        userFeedback = request.POST.get('userFeedback')
        obj = feedback.objects.create(
            feedback=userFeedback, username=logged_in_user)
        obj.save()
    context = {'logged_in_user': logged_in_user}
    return render(request, 'feedback.html', context)


def payment(request, price, name):
    currencySelected = request.session.get('currency')
    logged_in_user = request.user
    firstname = logged_in_user.first_name
    lastname = logged_in_user.last_name
    email = logged_in_user.email
    username = logged_in_user.username
    current_datetime = datetime.now()
    context = {'firstname': firstname, 'lastname': lastname, 'amt': price,
               'type': name, 'userEmail': email, 'current_datetime': current_datetime, 'username': username, 'currencySelected': currencySelected}
    return render(request, 'payment.html', context)


stripe.api_key = "sk_test_51NxBhTEWwd2L3hVcqKggRsddgVdE7Q2gO7tkapbEzMRINxkLf9twyWTIbMv0K9cpkieEAfGXRHTsoyClzt7yhQwX007TC5uy2q"


def checkout_session(request, price):
    username = request.user
    currencySelected = request.session.get('currency')
    if request.method == 'POST':
        exist = Member.objects.filter(username=username)
        if exist:
            return redirect('home:error')
        else:
            member = Member.objects.create(username=username, amount=price)
            member.save()
            data = Member.objects.last()
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currencySelected,
                        'product_data': {
                            'name': data.memberID,
                        },
                        'unit_amount': int(data.amount)*100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='http://127.0.0.1:8000/home/success2/'
            )
            return redirect(session.url, code=303)


def success2(request):
    return render(request, 'success2.html')


def error(request):
    return render(request, 'error.html')


def offer(request):
    offerList = offers.objects.all()
    return render(request, 'offers.html', {'offerList': offerList})
