# Generated by Django 2.2.4 on 2019-10-19 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jersey', '0008_auto_20191019_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.TextField(),
        ),
    ]
