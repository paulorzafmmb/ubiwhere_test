# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-28 21:17:30
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 00:26:36

import datetime

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import OuterRef, Subquery
from django.utils import timezone

from .models import RoadSegment, RoadSpeed, Car, Sensor, SensorReadings
from .permissions import IsAdminOrReadOnly
from .serializers import RoadSegmentSerializer, RoadSpeedSerializer, CarSerializer, SensorSerializer, SensorReadingsSerializer
from .authentication import SensorTokenAuthentication


INTENSITIES = {
    'baixa': [50, None],
    'média': [20, 50],
    'elevada': [None, 20]
}

class RoadSegmentViewSet(viewsets.ModelViewSet):
    serializer_class = RoadSegmentSerializer
    queryset = RoadSegment.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'traffic_intensity', openapi.IN_QUERY,
                description="Traffic Intensity (baixa, média, elevada)",
                type=openapi.TYPE_STRING,
                required=True,
                enum=list(INTENSITIES.keys())
            )
        ],
        responses={200: RoadSegmentSerializer(many=True)}
    )
    @action(detail=False, methods=['GET'], url_path='by-traffic-intensity')
    def get_by_traffic_intensity(self, request):
        traffic_intensity = request.query_params.get('traffic_intensity', '')
        if traffic_intensity not in INTENSITIES:
            return Response(
                {'detail': f'Invalid traffic intensity param. Must be one of {list(INTENSITIES.keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        latest_readings = RoadSpeed.objects.filter(
            road=OuterRef('pk')
        ).order_by('-timestamp')

        roads = RoadSegment.objects.annotate(
            last_temp=Subquery(latest_readings.values('speed')[:1])
        )

        limits = INTENSITIES[traffic_intensity]
        if  limits[0] is not None:
            roads = roads.filter(last_temp__gte=limits[0])
        if limits[1] is not None:
            roads = roads.filter(last_temp__lt=limits[1])

        serializer = RoadSegmentSerializer(roads, many=True)
        return Response(serializer.data)


class RoadSpeedViewSet(viewsets.ModelViewSet):
    serializer_class = RoadSpeedSerializer
    queryset = RoadSpeed.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class CarViewSet(viewsets.ModelViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'license_plate', openapi.IN_QUERY,
                description="License Plate",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: CarSerializer()}
    )
    @action(detail=False, methods=['GET'], url_path='recent-readings')
    def get_recent_readings(self, request):
        license_plate = request.query_params.get('license_plate')
        if not license_plate:
            return Response(
                {'detail': 'Missing license plate'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            car = Car.objects.get(license_plate=license_plate)
        except Car.DoesNotExist:
            return Response(
                {'detail': 'License plate no registered'},
                status=status.HTTP_404_NOT_FOUND
            )

        time_threshold = timezone.now() - datetime.timedelta(hours=24)
        readings = car.readings.filter(timestamp__gte=time_threshold).order_by("timestamp")
        car.readings_cached = readings

        serializer = CarSerializer(car)
        return Response(serializer.data)


class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class SensorReadingsViewSet(viewsets.ModelViewSet):
    serializer_class = SensorReadingsSerializer
    queryset = SensorReadings.objects.all()
    authentication_classes = [SensorTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        is_bulk = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_bulk)
        serializer.is_valid(raise_exception=True)

        if is_bulk:
            instances = [serializer.child.create(item) for item in serializer.validated_data]
        else:
            instances = serializer.save()

        return Response(self.get_serializer(instances, many=is_bulk).data, status=201)

