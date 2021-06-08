# Generated by Django 2.2.6 on 2021-04-29 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0006_auto_20210429_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dayname',
            name='days',
        ),
        migrations.AddField(
            model_name='dayname',
            name='name',
            field=models.CharField(default='Poniedziałek', max_length=16),
        ),
        migrations.AlterField(
            model_name='dayname',
            name='order',
            field=models.IntegerField(unique=True),
        ),
    ]