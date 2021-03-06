# Generated by Django 2.2.4 on 2019-12-08 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jersey', '0011_auto_20191021_0426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recommended_items', models.CharField(max_length=50)),
                ('item_being_viewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jersey.Jersey')),
            ],
        ),
    ]
