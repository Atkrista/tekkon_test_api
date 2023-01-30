from .models import Bay, Booking, Customer
from rest_framework import serializers
import datetime
from django.utils import timezone


class BaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bay
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        validators = [
            # A bay can be booked once a day.
            serializers.UniqueTogetherValidator(
                queryset=Booking.objects.all(),
                fields=["reservation_date", "bay"],
                message="Bay has already been booked for the date.",
            ),
            serializers.UniqueTogetherValidator(
                queryset=Booking.objects.all(),
                fields=["reservation_date", "customer"],
                message="Max one bookings per customer per day.",
            ),
        ]

    def validate_reservation_date(self, value):
        # Check that booking is done 24 hours in advance.
        reservation_date = datetime.datetime.combine(
            value, datetime.time.min, tzinfo=datetime.timezone.utc
        )
        if not reservation_date > (timezone.now() + datetime.timedelta(hours=24)):
            raise serializers.ValidationError("Booking must take 24 hours in advance.")

        return value


class BookingCustomerDetailedSerializer(BookingSerializer):
    customer = CustomerSerializer()
