# Generated by Django 5.1.5 on 2025-01-30 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0021_alter_size_unique_together_remove_size_school'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='size',
            unique_together={('size', 'category')},
        ),
    ]
