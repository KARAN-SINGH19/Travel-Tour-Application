from django.contrib import admin
from home.models import *


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('memberID', 'amount', 'username')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('couponCode', 'discountPercentage', 'validFor')


class feedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback', 'username')


admin.site.register(offers, OfferAdmin)
admin.site.register(Member, MembershipAdmin)
admin.site.register(feedback, feedbackAdmin)
