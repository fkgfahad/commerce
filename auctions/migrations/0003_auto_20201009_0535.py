# Generated by Django 3.1.2 on 2020-10-09 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20201008_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auctions', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='auction',
            name='date',
            field=models.CharField(default='October 09, 2020 05:35', max_length=64),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.CharField(default='October 09, 2020 05:35', max_length=64),
        ),
    ]
