from django.db import models
from django.urls import reverse
from datetime import date, timedelta

FERTILIZERS = (
    ('1', '4-4-4'),
    ('2', '4-8-12'),
    ('N', 'None')
)


class Plant(models.Model):
    name = models.CharField(max_length=100)
    varietal = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    light_requirement = models.IntegerField()
    water_requirement = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("detail", kwargs={"plant_id": self.id})

    def watered(self):
        date_last_watered = self.watering_set.latest('date').date
        today = date.today()
        days_since_watered = (today - (date_last_watered)).days
        print(f"{days_since_watered}")
        return days_since_watered.days < water_requirement


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
