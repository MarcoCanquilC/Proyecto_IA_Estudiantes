# Generated by Django 5.1.4 on 2025-06-28 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorito',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='favorito',
            name='tema',
        ),
        migrations.RemoveField(
            model_name='favorito',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='tema',
        ),
        migrations.DeleteModel(
            name='favorito',
        ),
    ]
