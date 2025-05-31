# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-28 21:36:29
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 01:04:39

from rest_framework import serializers

from .models import RoadSegment, RoadSpeed, Car, Sensor, SensorReadings


class RoadSpeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadSpeed
        fields = '__all__'


class RoadSegmentSerializer(serializers.ModelSerializer):
    speed = RoadSpeedSerializer(many=True, read_only=True)
    traffic_intensity = serializers.SerializerMethodField()
    speed_readings_count = serializers.SerializerMethodField()

    class Meta:
        model = RoadSegment
        fields = '__all__'

    def get_traffic_intensity(self, obj):
        latest_speed = obj.speed.order_by('-timestamp').first()
        return self.check_traffic_intensity(latest_speed.speed) if latest_speed else None

    def check_traffic_intensity(self, speed):
        if speed > 50:
            return 'baixa'
        elif speed > 20:
            return 'média'
        else:
            return 'elevada'

    def get_speed_readings_count(self, obj):
        return obj.speed.count()


class SensorReadingsSerializer(serializers.ModelSerializer):
    road_segment = serializers.IntegerField(required=True, write_only=True)
    sensor__uuid = serializers.CharField(required=True, write_only=True)
    car__license_plate = serializers.CharField(required=True, write_only=True)
    car = serializers.CharField(source='car.license_plate', read_only=True)
    road = serializers.IntegerField(source='road.id', read_only=True)
    sensor = serializers.UUIDField(source='sensor.uuid', read_only=True)

    class Meta:
        model = SensorReadings
        fields = ['road_segment', 'sensor__uuid', 'car__license_plate', 'timestamp', 'car', 'road', 'sensor']

    def validate(self, attrs):
        road_segment_id = int(attrs.pop('road_segment', 0))
        if not road_segment_id:
            raise serializers.ValidationError('Missing road_segment')

        try:
            road_segment = RoadSegment.objects.get(id=int(road_segment_id))
        except RoadSegment.DoesNotExist:
            raise serializers.ValidationError("Road Segment id is not valid")

        attrs['road'] = road_segment

        sensor_uuid = attrs.pop('sensor__uuid', None)
        if not sensor_uuid:
            raise serializers.ValidationError('Missing sensor__uuid')

        try:
            sensor = Sensor.objects.get(uuid=sensor_uuid)
        except Sensor.DoesNotExist:
            raise serializers.ValidationError("Sensor uuid is not valid")

        attrs['sensor'] = sensor

        car_license_plate = attrs.pop('car__license_plate', None)
        if not car_license_plate.strip():
            raise serializers.ValidationError("Car license plate cannot be empty.")

        attrs['car'] = car_license_plate

        return attrs

    def create(self, validated_data):
        car_license_plate = validated_data.pop('car')
        car, _ = Car.objects.get_or_create(license_plate=car_license_plate)
        return SensorReadings.objects.create(car=car, **validated_data)


class SensorSerializer(serializers.ModelSerializer):
    readings = SensorReadingsSerializer(many=True, read_only=True)

    class Meta:
        model = Sensor
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    readings = SensorReadingsSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = '__all__'
