# Generated by Django 5.1.4 on 2025-02-06 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_price_service_stock_alter_service_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='stock',
        ),
        migrations.AddField(
            model_name='service',
            name='available',
            field=models.BooleanField(default=True, verbose_name='Disponible'),
        ),
        migrations.AlterField(
            model_name='service',
            name='content',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='service',
            name='subtitle',
            field=models.CharField(max_length=200, verbose_name='Subtítulo'),
        ),
        migrations.AlterField(
            model_name='service',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Título'),
        ),
    ]
