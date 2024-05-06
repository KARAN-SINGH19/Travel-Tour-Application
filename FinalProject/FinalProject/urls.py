from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', include('landingPage.urls')),
    path('home/', include('home.urls')),
    path('adminPanel/', include('adminPanel.urls')),
    path('flightBooking/', include('flightBooking.urls')),
    path('hotelBooking/', include('hotelBooking.urls')),
    path('resortBooking/', include('resortBooking.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
