# Generated by Django 3.0.4 on 2020-03-20 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('list_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='search',
            new_name='search_text',
        ),
    ]