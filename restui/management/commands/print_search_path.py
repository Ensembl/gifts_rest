"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = """
        Prints the current search path
        Usage:
        $ python manage.py print_search_path
    """

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SHOW search_path;")
            search_path = cursor.fetchone()
            self.stdout.write(self.style.SUCCESS(f'Search path: {search_path}'))
            self.stdout.write(self.style.SUCCESS(f'Connection: {connection.settings_dict}'))
