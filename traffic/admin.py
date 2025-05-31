# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-28 21:17:30
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 00:50:54

from django.contrib import admin

from .models import RoadSegment, RoadSpeed, Car, Sensor, SensorReadings, AuthToken

admin.site.register(RoadSegment)
admin.site.register(RoadSpeed)
admin.site.register(Car)
admin.site.register(Sensor)
admin.site.register(SensorReadings)
admin.site.register(AuthToken)