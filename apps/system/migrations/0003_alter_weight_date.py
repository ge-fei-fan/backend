# Generated by Django 4.1 on 2022-08-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weight',
            name='date',
            field=models.DateField(blank=True, help_text='记录体重时间', null=True, verbose_name='记录体重时间'),
        ),
    ]
