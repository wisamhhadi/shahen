import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shahen.settings")
django.setup()

from django.apps import apps
from django.db import connection

M = apps.get_model("deliverycompany", "DeliveryCompany")
table = M._meta.db_table

with connection.cursor() as c:
    c.execute("""
        SELECT data_type, character_maximum_length
        FROM information_schema.columns
        WHERE table_name=%s AND column_name=%s
    """, [table, "phone"])
    rows = c.fetchall()

print("TABLE:", table)
print("PHONE_COLUMN:", rows)

if rows and rows[0][0] in ("integer", "bigint", "smallint", "numeric"):
    with connection.cursor() as c:
        c.execute(
            f'ALTER TABLE "{table}" ALTER COLUMN "phone" TYPE varchar(20) USING "phone"::varchar(20);'
        )
    print("CONVERTED_TO_VARCHAR_20")
else:
    print("NO_CONVERSION_NEEDED")
