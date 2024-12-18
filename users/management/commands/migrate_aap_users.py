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
from django.contrib.auth.hashers import make_password
from django.db import connection
from users.models import CustomUser


class Command(BaseCommand):
    help = (
        "Migrate users from aap_auth_aapuser to Django users_customuser table \n"
        "Usage: python manage.py migrate_aap_users --email user@example.com"
    )

    def add_arguments(self, parser):
        # Add an optional argument for email
        parser.add_argument(
            '--email',
            type=str,
            help='Email of the user to migrate (optional)'
        )

    def handle(self, *args, **options):
        email = options.get('email')

        if email:
            # Migrate a single user by email
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT elixir_id, full_name, email FROM aap_auth_aapuser WHERE email = %s",
                    [email]
                )
                user = cursor.fetchone()

                if user:
                    elixir_id, full_name, user_email = user
                    print(f"elixir_id --> {elixir_id}")
                    print(f"elixir_id[4:] --> {elixir_id[4:]}")
                    print(f"full_name --> {full_name}")
                    print(f"user_email --> {user_email}")
                    if not CustomUser.objects.filter(email=user_email).exists():
                        CustomUser.objects.create(
                            elixir_id=elixir_id,
                            full_name=full_name,
                            email=user_email,
                            password=make_password(elixir_id[4:])
                        )
                        self.stdout.write(f"User {email} migrated successfully.")
                    else:
                        self.stdout.write(f"User {email} already exists in the system.")
                else:
                    self.stdout.write(f"No user found with email {email}.")
        # This part is dangerous, I'll leave it commented
        # else:
        #     # Migrate all users if no email is provided
        #     with connection.cursor() as cursor:
        #         cursor.execute("SELECT elixir_id, full_name, email FROM aap_auth_aapuser")
        #         users = cursor.fetchall()
        #
        #         for elixir_id, user_email in users:
        #             if not CustomUser.objects.filter(username=elixir_id).exists():
        #                 CustomUser.objects.create(
        #                     username=elixir_id,
        #                     email=user_email,
        #                     password=make_password("temporary_password")
        #                 )
        #         self.stdout.write("All users migrated successfully.")
