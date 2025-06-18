from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, BookingViewSet, ListingViewSet, ReviewViewSet
from rest_framework_nested.routers import NestedDefaultRouter, DefaultRouter


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)

nested_router = NestedDefaultRouter(router, r'listings', lookup='listing')
nested_router.register(r'bookings', BookingViewSet, basename='listing-bookings')
nested_router.register(r'reviews', ReviewViewSet, basename='listing-reviews')
nested_router.register(r'users', UserViewSet, basename='listing-users')
nested_router.register(r'listings', ListingViewSet, basename='listing-listings')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
