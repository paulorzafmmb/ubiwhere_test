# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-28 21:17:30
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-30 16:46:38
from django.test import TestCase
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from .models import RoadSegment, RoadSpeed
from .serializers import RoadSegmentSerializer


class Tests(TestCase):
    def test_create_road_segment(self):
        road_segment = RoadSegment.objects.create(lat_start=1, lat_end=2, long_start=3, long_end=4, length=5)
        self.assertEqual(road_segment.lat_start, 1)
        self.assertEqual(road_segment.lat_end, 2)
        self.assertEqual(road_segment.long_start, 3)
        self.assertEqual(road_segment.long_end, 4)
        self.assertEqual(road_segment.length, 5)

    def test_create_temperature_reading(self):
        road_segment = RoadSegment.objects.create(lat_start=2, lat_end=2, long_start=3, long_end=4, length=5)
        road_speed = RoadSpeed.objects.create(road=road_segment, speed=50, timestamp=timezone.now())
        self.assertEqual(road_speed.road, road_segment)
        self.assertEqual(road_speed.speed, 50)

    def test_duplicate_road_segments(self):
        RoadSegment.objects.create(lat_start=3, lat_end=2, long_start=3, long_end=4, length=5)
        with self.assertRaises(Exception):
            RoadSegment.objects.create(lat_start=3, lat_end=2, long_start=3, long_end=4, length=5)

    def test_traffic_intensity(self):
        road_segment = RoadSegment.objects.create(lat_start=5, lat_end=2, long_start=3, long_end=4, length=5)
        RoadSpeed.objects.create(road=road_segment, speed=50, timestamp=timezone.now())
        serializer = RoadSegmentSerializer(road_segment)
        self.assertEqual(serializer.data['traffic_intensity'], 'média')


class APITests(APITestCase):
    def setUp(self):
        self.road_segment_1 = RoadSegment.objects.create(lat_start=1, lat_end=2, long_start=3, long_end=4, length=5)
        self.road_segment_2 = RoadSegment.objects.create(lat_start=6, lat_end=7, long_start=8, long_end=9, length=10)
        RoadSpeed.objects.create(road=self.road_segment_1, speed=50, timestamp=timezone.now())
        RoadSpeed.objects.create(road=self.road_segment_2, speed=10, timestamp=timezone.now())

    def test_get_sensors_by_temp_label_hot(self):
        url = '/api/segments/by-traffic-intensity/?traffic_intensity=elevada'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['lat_start'], self.road_segment_2.lat_start)

    def test_get_sensors_by_temp_label_invalid(self):
        url = '/api/segments/by-traffic-intensity/?traffic_intensity=qualquer'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)




