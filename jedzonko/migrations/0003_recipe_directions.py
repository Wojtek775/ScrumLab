# Generated by Django 2.2.6 on 2021-04-28 15:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0002_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='directions',
            field=models.TextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]