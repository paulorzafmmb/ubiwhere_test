# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-30 14:12:32
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-30 14:43:26

import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from traffic.models import RoadSegment, RoadSpeed


class Command(BaseCommand):
    help = "Import traffic segment speed data from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file.')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        success_count = 0
        error_count = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    road_segment_data = {
                        'lat_start': float(row['Lat_start']),
                        'lat_end': float(row['Lat_end']),
                        'long_start': float(row['Long_start']),
                        'long_end': float(row['Long_end']),
                        'length': float(row['Length'])
                    }
                    road_speed_data = {
                        'speed': float(row['Speed']),
                        'timestamp': timezone.now()
                    }

                    road_segment = RoadSegment.objects.get_or_create(**road_segment_data)
                    RoadSpeed.objects.create(road=road_segment[0], **road_speed_data)
                    success_count += 1
                except Exception as e:
                    self.stderr.write(f"Error importing row {row}: {e}")
                    error_count += 1

        self.stdout.write(self.style.SUCCESS(f"Import complete: {success_count} added, {error_count} errors."))
