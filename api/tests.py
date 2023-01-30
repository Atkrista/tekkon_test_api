from django.test import TestCase, Client
from .models import Bay, Customer, Booking
from datetime import date, timedelta
from django.utils import timezone

# Create your tests here.


class BookingTestCase(TestCase):
    def setUp(self):
        # Initial data will be populated in the test db from initial migration
        # 1 Park with 4 bays, and 4 customers
        self.client = Client()
        self.valid_future_date = (date.today() + timedelta(days=3)).isoformat()

    def test_early_reservation(self):
        invalid_date = (timezone.now() + timedelta(hours=23, minutes=59)).date()
        response = self.client.post(
            "/bookings/",
            {
                "reservation_date": invalid_date.isoformat(),
                "customer": 1,
                "bay": 1,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_customer_daily_limit(self):
        customer = Customer.objects.all().first()
        response = self.client.post(
            "/bookings/",
            {
                "reservation_date": self.valid_future_date,
                "bay": 1,
                "customer": customer.id,
            },
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            "/bookings/",
            {
                "reservation_date": self.valid_future_date,
                "bay": 2,
                "customer": customer.id,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_all_bookings(self):
        bookings = [
            Booking.objects.create(
                customer_id=i, bay_id=i, reservation_date=self.valid_future_date
            )
            for i in range(1, 4)
        ]
        response = self.client.get(
            f"/bookings/valid_bookings/?date={self.valid_future_date}"
        )
        self.assertEqual(response.status_code, 200)
        # Verify that all bookings are returned
        self.assertEqual(len(response.data["results"]), 3)
        # Verify that customer data is in response
        self.assertTrue("customer" in response.data["results"][0])
