# Generated by Django 5.1.2 on 2025-07-06 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enciclopedia', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enciclopedia',
            name='categoria',
            field=models.CharField(blank=True, choices=[('Fisica', 'Física'), ('Quimica', 'Química'), ('Matematica', 'Matemática'), ('Biologia', 'Biología')], max_length=50, null=True),
        ),
    ]
