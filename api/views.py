# from django.shortcuts import render
import datetime
from rest_framework import viewsets, response, decorators
from .models import Bay, Booking, Customer
from .serializers import (
    BaySerializer,
    BookingSerializer,
    CustomerSerializer,
    BookingCustomerDetailedSerializer,
)

# Create your views here.


class BayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read endpoint for bays
    """

    queryset = Bay.objects.all()
    serializer_class = BaySerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoint for bookings
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @decorators.action(methods=["GET"], detail=False)
    def valid_bookings(self, request):
        queried_date = request.query_params.get("date", "")
        if not queried_date:
            return response.Response(
                data={
                    "message": "Please pass a date as query_parameter `date`. ex: ?date=2023-01-30."
                },
                status=400,
            )
        try:
            queried_date = datetime.datetime.strptime(queried_date, "%Y-%m-%d").date()
        except Exception as e:
            return response.Response(
                data={
                    "message": "Invalid date. Query parameter `date` must be a valid date of format YYYY-DD-MM"
                },
                status=400,
            )
        return response.Response(
            data={
                "results": [
                    BookingCustomerDetailedSerializer(booking).data
                    for booking in Booking.objects.filter(reservation_date=queried_date)
                ]
            }
        )


class CustomerViewSet(viewsets.ModelViewSet):
    """
    CRUD endpoint for customers
    """

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
