# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-28 21:17:30
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 00:58:49

import secrets

from django.db import models


class RoadSegment(models.Model):
    lat_start = models.FloatField()
    lat_end = models.FloatField()
    long_start = models.FloatField()
    long_end = models.FloatField()
    length = models.FloatField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lat_start', 'lat_end', 'long_start', 'long_end', 'length'], name='unique_road_segment')
        ]

    def __str__(self):
        return f"Lat {self.lat_start} - {self.lat_end}, Long {self.long_start} - {self.long_end}"

class RoadSpeed(models.Model):
    road = models.ForeignKey(RoadSegment, on_delete=models.CASCADE, related_name='speed')
    speed = models.FloatField()
    timestamp = models.DateTimeField()
    
    def __str__(self):
        return f"Road {self.road}, Speed {self.speed}"

class Car(models.Model):
    license_plate = models.CharField(unique=True)
    registration_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Plate: {self.license_plate}'

class Sensor(models.Model):
    name = models.CharField()
    uuid = models.UUIDField()

    def __str__(self):
        return f'Sensor: {self.name}'

class SensorReadings(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings')
    road = models.ForeignKey(RoadSegment, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='readings')
    timestamp = models.DateTimeField()

class AuthToken(models.Model):
    token = models.CharField(max_length=64, unique=True, default=secrets.token_hex)

    @property
    def is_authenticated(self):
        return True
