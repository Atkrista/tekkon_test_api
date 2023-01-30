from django.db import models

# Create your models here.


class Bay(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __repr__(self):
        return f"<Bay: {self.id}>"


class Booking(models.Model):
    reservation_date = models.DateField()
    booking_timestamp = models.DateTimeField(auto_now_add=True)

    bay = models.ForeignKey(
        to="Bay", on_delete=models.CASCADE, related_name="bay_bookings"
    )
    customer = models.ForeignKey(
        to="Customer", on_delete=models.CASCADE, related_name="customer_bookings"
    )

    def __repr__(self):
        return f"<Booking: {self.id}>"


class Customer(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    license_plate = models.CharField(
        max_length=50, blank=False, null=False, unique=True
    )

    def __repr__(self):
        return f"<Customer: {self.name}>"
