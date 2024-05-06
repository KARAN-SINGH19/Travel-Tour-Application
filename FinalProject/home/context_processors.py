from home.models import *


def userDetails(request):
    userDetails = {}
    if request.user.is_authenticated:
        username = request.user
        email = username.email
        userDetails = {'username': username, 'email': email}
    return {'userDetails': userDetails}


def members(request):
    membersData = {}
    #CHECKING WHETHER THE USE IS LOGGED IN OR NO
    if request.user.is_authenticated:
        #RERIEVIG THE LOGGED IN USER'S USERNAME 
        logged_in_user = request.user
        #CHECKING IF THE USER IS A MEMBER
        members = Member.objects.filter(username=logged_in_user)
        membersData = {'members': members}
    return membersData



