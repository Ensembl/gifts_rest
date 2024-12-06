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
from django.db import connection, transaction

class Command(BaseCommand):
    help = "Update user_stamp column in multiple tables and convert it to INTEGER"

    def handle(self, *args, **kwargs):
        # List of tables to update
        tables = [
            "ue_mapping_comment",
            "ue_mapping_label",
            "ue_mapping_status",
            "ue_unmapped_entry_comment",
            "ue_unmapped_entry_label",
            "ue_unmapped_entry_status",
        ]

        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    for table in tables:
                        self.stdout.write(f"Processing table: {table}")

                        # Update user_stamp values using PostgreSQL-compatible syntax
                        update_query = f"""
                            UPDATE {table} AS uec
                            SET user_stamp = uc.id
                            FROM users_customuser AS uc
                            WHERE uec.user_stamp = uc.elixir_id;
                        """
                        self.stdout.write(f"Running update query for {table}...")
                        cursor.execute(update_query)

                        # Change column type to INTEGER
                        alter_query = f"""
                            ALTER TABLE {table}
                            ALTER COLUMN user_stamp TYPE INTEGER USING user_stamp::INTEGER;
                        """
                        self.stdout.write(f"Changing column type for {table}...")
                        cursor.execute(alter_query)

                        self.stdout.write(f"Table {table} processed successfully!")

        except Exception as e:
            self.stderr.write(f"Error occurred: {e}")
            raise
