from django.shortcuts import render, redirect
from adminPanel.models import *
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, reverse


def adminHome(request):
    return render(request, 'adminPanel.html')


def addHotels(request):
    hotelData = Hotel.objects.all()
    context = {'hotelData': hotelData}
    if request.method == 'POST':
        if request.POST.get('submitBtn') == 'hotelDetails':
            hotelId = request.POST['hotelId']
            hotelName = request.POST['hotelName']
            hotelLocation = request.POST['hotelLocation']
            startingPrice = request.POST['startingPrice']
            hotelRating = request.POST['ratings']
            hotelImage = request.FILES['hotelImage']

            hotelData = Hotel.objects.create(
                hotel_id=hotelId,
                hotel_name=hotelName,
                hotel_location=hotelLocation,
                starting_price=startingPrice,
                ratings=hotelRating,
                hotel_image=hotelImage
            )
            hotelData.save()
            messages.success(request, "Hotel Details Added Successfully")
            return redirect('adminPanel:addHotel')

        elif request.POST.get('submitBtn') == 'roomDetails':
            room_id = request.POST['roomId']
            room_type = request.POST['roomType']
            room_capacity=request.POST['roomCapacity']
            room_price = request.POST['roomPrice']
            hotel_id = request.POST['hotelId']

            hotelData = Hotel.objects.get(hotel_id=hotel_id)

            roomData = hotelRoomtype.objects.create(
                room_id=room_id,
                room_type=room_type,
                room_capacity=room_capacity,
                room_price=room_price,
                hotel_id=hotelData
            )
            roomData.save()
            messages.success(request, "Room Details Added Successfully")
            return redirect('adminPanel:addHotel')

    return render(request, 'addHotel.html', context)


def addResorts(request):
    resortData = Resort.objects.all()
    context = {'resortData': resortData}

    if request.method == 'POST':
        if request.POST.get('submitBtn') == 'addResort':
            resortId = request.POST['resortId']
            resortName = request.POST['resortName']
            resortLocation = request.POST['resortLocation']
            startingPrice = request.POST['startingPrice']
            resortRating = request.POST['ratings']
            resortImage = request.FILES['resortImage']

            resortData = Resort.objects.create(
                resort_id=resortId,
                resort_name=resortName,
                resort_location=resortLocation,
                starting_price=startingPrice,
                ratings=resortRating,
                resort_image=resortImage
            )

            resortData.save()
            messages.success(request, "Resort Details Added Successfully")
            return redirect('adminPanel:addResort')

        elif request.POST.get('submitBtn') == 'addRoom':
            roomId = request.POST['roomId']
            roomName = request.POST['roomName']
            room_capacity=request.POST['roomCapacity']
            roomPrice = request.POST['roomPrice']
            resortId = request.POST['resortId']

            resortData = Resort.objects.get(resort_id=resortId)

            roomData = resortRoomtype.objects.create(
                room_id=roomId,
                room_type=roomName,
                room_capacity=room_capacity,
                room_price=roomPrice,
                resort_id=resortData,
            )

            roomData.save()
            messages.success(request, "Room Details Added Successfully")
            return redirect('adminPanel:addResort')

    return render(request, 'addResort.html', context)


def addFlights(request):
    if request.method == 'POST':
        flightId = request.POST['flightId']
        airlineName = request.POST['airlineName']
        airplaneName = request.POST['airplaneName']
        originCode = request.POST['originCode']
        destinationCode = request.POST['destinationCode']
        deptCity = request.POST['depCity']
        arrivalCity = request.POST['arrivalCity']
        price = request.POST['price']
        trip = request.POST['trip']
        flight_class = request.POST['class']
        deptDate = request.POST['deptDate']
        returnDate = request.POST.get('returnDate', None)
        deptTime = request.POST['deptTime']
        arrivalTime = request.POST['arrivalTime']
        flightDuration = request.POST['flightDuration']
        airlineImage = request.FILES['airlineImage']

        if not returnDate:
            returnDate = None

        flightData = Flight.objects.create(
            flight_id=flightId,
            airline_name=airlineName,
            airplane_name=airplaneName,
            origin_code=originCode,
            destination_code=destinationCode,
            departure_city=deptCity,
            arrival_city=arrivalCity,
            departure_date=deptDate,
            return_date=returnDate,
            departure_time=deptTime,
            arrival_time=arrivalTime,
            flight_trip=trip,
            flight_class=flight_class,
            price=price,
            flight_duration=flightDuration,
            airline_image=airlineImage,
        )

        flightData.save()
        messages.success(request, "Flight Details Added Successfully")
        return redirect('adminPanel:addFlight')

    return render(request, 'addFlight.html')


def viewHotel(request):
    hotelData = Hotel.objects.all()
    context = {'hotelData': hotelData}
    return render(request, 'viewHotel.html', context)


def viewResort(request):
    resortData = Resort.objects.all()
    context = {'resortData': resortData}
    return render(request, 'viewResort.html', context)


def viewFlight(request):
    flightData = Flight.objects.all()
    context = {'flightData': flightData}
    return render(request, 'viewFlight.html', context)


def editHotel(request):
    hotelData = Hotel.objects.all()
    context = {'hotelData': hotelData}
    return render(request, 'editHotel.html', context)


def deleteHotel(request, id):
    if request.method == 'POST':
        data = Hotel.objects.filter(hotel_id=id)
        data.delete()
        return redirect('adminPanel:editHotel')
    return render('editHotel.html')


def editResort(request):
    resortData = Resort.objects.all()
    context = {'resortData': resortData}
    return render(request, 'editResort.html', context)


def deleteResort(request, id):
    if request.method == 'POST':
        data = Resort.objects.filter(resort_id=id)
        data.delete()
        return redirect('adminPanel:editResort')
    return render('editResort.html')


def editFlight(request):
    flightData = Flight.objects.all()
    context = {'flightData': flightData}
    return render(request, 'editFlight.html', context)


def deleteFlight(request, id):
    if request.method == 'POST':
        data = Flight.objects.filter(flight_id=id)
        data.delete()
        return redirect('adminPanel:editFlight')
    return render('editFlight.html')


def updateHotel(request, id):
    hotelData = Hotel.objects.get(hotel_id=id)
    context = {'hotelData': hotelData}
    return render(request, 'updateHotelDetails.html', context)


def updateHotelDetails(request, id):
    if request.method == 'POST':
        hotel_id = request.POST['hotelId']
        hotel_name = request.POST['hotelName']
        hotel_location = request.POST['hotelLocation']
        starting_price = request.POST['startingPrice']
        ratings = request.POST['ratings']
        data = Hotel.objects.get(hotel_id=id)

        data.hotel_id = hotel_id
        data.hotel_name = hotel_name
        data.hotel_location = hotel_location
        data.starting_price = starting_price
        data.ratings = ratings
        data.save()
        return redirect('adminPanel:editHotel')
    return render('editHotel')


def updateResort(request, id):
    resortData = Resort.objects.get(resort_id=id)
    context = {'resortData': resortData}
    return render(request, 'updateResortDetails.html', context)


def updateResortDetails(request, id):
    if request.method == 'POST':
        resort_id = request.POST['hotelId']
        resort_name = request.POST['hotelName']
        resort_location = request.POST['hotelLocation']
        starting_price = request.POST['startingPrice']
        ratings = request.POST['ratings']
        data = Resort.objects.get(resort_id=id)

        data.resort_id = resort_id
        data.resort_name = resort_name
        data.resort_location = resort_location
        data.starting_price = starting_price
        data.ratings = ratings
        data.save()
        return redirect('adminPanel:editResort')
    return render('editResort')


def updateFlight(request, id):
    flightData = Flight.objects.get(flight_id=id)
    context = {'flightData': flightData}
    return render(request, 'updateFlightDetails.html', context)


def updateFlightDetails(request, id):
    if request.method == 'POST':
        flight_id = request.POST['flightId']
        airline_name = request.POST['airlineName']
        deptCity = request.POST['deptCity']
        arrivalCity = request.POST['arrivalCity']
        flightClass = request.POST['flightClass']
        price = request.POST['price']
        deptDateTime = request.POST['deptDateTime']
        arrivalDateTime = request.POST['arrivalDateTime']
        data = Flight.objects.get(flight_id=id)

        data.flight_id = flight_id
        data.airline_name = airline_name
        data.departure_city = deptCity
        data.arrival_city = arrivalCity
        data.flight_class = flightClass
        data.price = price
        data.departure_dateTime = deptDateTime
        data.arrival_dateTime = arrivalDateTime
        data.save()
        return redirect('adminPanel:editFlight')
    return render('editFlight')


def logout_user(request):
    logout(request)
    return redirect(reverse('landingPage:login_user'))
