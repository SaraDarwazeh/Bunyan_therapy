# Generated by Django 5.0.7 on 2024-08-28 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BunyanApp', '0013_remove_userassessment_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userassessment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
