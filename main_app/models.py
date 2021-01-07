from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta

FERTILIZERS = (
    ('1', '4-4-4'),
    ('2', '4-8-12'),
    ('N', 'None')
)


class Fertilizer(models.Model):
    fertilizer = models.CharField(
        max_length=1,
        choices=FERTILIZERS,
        default=FERTILIZERS[0][0]
    )
    quantity = models.IntegerField()

    def __str__(self):
        return self.fertilizer

    def get_absolute_url(self):
        return reverse('fertilizers_detail', kwargs={'pk': self.id})


class Plant(models.Model):
    name = models.CharField(max_length=100)
    varietal = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    light_requirement = models.IntegerField()
    water_requirement = models.PositiveIntegerField()
    fertilizers = models.ManyToManyField(Fertilizer)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"plant_id": self.id})

    def watered(self):
        date_last_watered = self.watering_set.latest('date').date
        today = date.today()
        days_since_watered = (today - (date_last_watered)).days
        days_to_next_water = self.water_requirement - days_since_watered
        return days_to_next_water


class Watering(models.Model):
    date = models.DateField('date watered')
    fertilizer = models.CharField(
        max_length=1,
        choices=FERTILIZERS,
        default=FERTILIZERS[0][0]
    )

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_fertilizer_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
