from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import User, Booking, Listing, Review
from .serializers import UserSerializer, BookingSerializer, ListingSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Provides CRUD operations for user data.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']

    def get_queryset(self):
        return self.queryset.order_by('first_name')


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking model.
    Provides CRUD operations for booking data.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['listing__name', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        return self.queryset.order_by('start_date')
    

class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Listing model.
    Provides CRUD operations for listing data.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'location']

    def get_queryset(self):
        return self.queryset.order_by('name')
    

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review model.
    Provides CRUD operations for review data.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['listing__name', 'user__first_name', 'user__last_name']

    def get_queryset(self):
        return self.queryset.order_by('created_at')
