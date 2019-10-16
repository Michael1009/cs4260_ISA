# Generated by Django 2.2.4 on 2019-10-10 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jersey', '0005_auto_20191007_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('authenticator', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('date_created', models.DateField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jersey.User')),
            ],
        ),
    ]
