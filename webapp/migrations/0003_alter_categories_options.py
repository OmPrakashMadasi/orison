# Generated by Django 5.1.5 on 2025-01-22 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_rename_category_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
