# Generated by Django 5.1.4 on 2025-01-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Airplanes",
            fields=[
                (
                    "id",
                    models.BigAutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("uuid", models.BigIntegerField(editable=False, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("passenger_assumptions", models.PositiveIntegerField()),
            ],
            options={
                "db_table": "airplanes",
                "ordering": ["id"],
            },
        ),
    ]
