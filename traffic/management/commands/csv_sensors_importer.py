# -*- coding: utf-8 -*-
# @Author: Paulo Barbosa
# @Date:   2025-05-30 14:12:32
# @Last Modified by:   Paulo Barbosa
# @Last Modified time: 2025-05-31 01:10:09

import csv
from django.core.management.base import BaseCommand
from django.utils import timezone
from traffic.models import Sensor


class Command(BaseCommand):
    help = "Import sensors from a CSV file."

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
                    Sensor.objects.create(name=row['name'], uuid=row['uuid'])
                    success_count += 1
                except Exception as e:
                    self.stderr.write(f"Error importing row {row}: {e}")
                    error_count += 1

        self.stdout.write(self.style.SUCCESS(f"Import complete: {success_count} added, {error_count} errors."))
