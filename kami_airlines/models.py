from django.db import models

from db.base_models import BaseModel

# Create your models here.


class Airplanes(BaseModel):
    passenger_assumptions = models.PositiveIntegerField()

    class Meta:
        db_table = "airplanes"
        ordering = ["id"]
