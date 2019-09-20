# Generated by Django 2.2.4 on 2019-09-20 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jersey', '0002_auto_20190918_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jersey',
            name='shirt_size',
            field=models.CharField(choices=[('XS', 'Extra Small'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('XXL', 'Double Extra Large')], max_length=3),
        ),
    ]
