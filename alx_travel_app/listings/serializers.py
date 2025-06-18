"""
serializers module for the messaging app's chat functionality.
This module contains serializers for handling chat-related data,
including user, conversation, and message data.
"""

from rest_framework import serializers
from .models import User, Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles serialization and deserialization of user data.
    Includes full name via SerializerMethodField.
    """
    full_name = serializers.SerializerMethodField()
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'full_name']
        read_only_fields = ['user_id']
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'phone_number': {'required': True, 'allow_blank': False}
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 8:
            raise serializers.ValidationError("Phone number must be at least 8 digits long.")
        return value


class ListingSerializer(serializers.ModelSerializer):
    """
    Serializer for Listing model.
    Handles serialization and deserialization of listing data.
    Includes host information via nested UserSerializer.
    """
    host = UserSerializer(read_only=True)

    class Meta:
        model = Listing
        fields = ['listing_id', 'host', 'name', 'description', 'location', 'price_per_night', 'created_at', 'updated_at']
        read_only_fields = ['listing_id', 'created_at', 'updated_at']

    def validate_price_per_night(self, value):
        if value < 0:
            raise serializers.ValidationError("Price per night must be a positive number.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model.
    Handles serialization and deserialization of booking data.
    Includes listing and user information via nested serializers.
    """
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['booking_id', 'listing', 'user', 'start_date', 'end_date', 'total_price', 'status', 'created_at', 'updated_at']
        read_only_fields = ['booking_id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return attrs
    

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    Handles serialization and deserialization of review data.
    Includes listing and user information via nested serializers.
    """
    listing = ListingSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['review_id', 'listing', 'user', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['review_id', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    def validate_comment(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Comment must be at least 10 characters long.")
        return value
    


