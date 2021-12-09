from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)
    avg_rating = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    rates_number = models.IntegerField(default=0)

    class Meta:
        unique_together = ["make", "model"]

    def update_avg_rating(self):
        ratings = self.car_ratings.all()
        self.rates_number = ratings.count()
        self.avg_rating = ratings.aggregate(models.Avg("rating")).get("rating__avg")
        self.save(update_fields=["avg_rating", "rates_number"])


class CarRatings(models.Model):
    rating = models.IntegerField()
    car = models.ForeignKey(Car, related_name="car_ratings", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.car.update_avg_rating()
