from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet)

# Nested router
listings_router = routers.NestedDefaultRouter(router, r'listings', lookup='listing')
listings_router.register(r'bookings', BookingViewSet, basename='listing-bookings')
# router = DefaultRouter()
# router.register(r'listings', ListingViewSet)
# router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(listings_router.urls)),
]
