# Generated by Django 4.2.5 on 2023-10-21 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saedah', '0004_alter_deal_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='link',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='deal',
            name='latitude',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='deal',
            name='longitude',
            field=models.FloatField(blank=True),
        ),
    ]
