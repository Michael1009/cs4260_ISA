from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    SHIRT_SIZES = (
        ('XS', "Extra Small"),
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Double Extra Large"),
    )
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

    def __str__(self):
        return self.email


class Jersey(models.Model):
    team = models.CharField(max_length=60)
    number = models.PositiveIntegerField()
    player = models.CharField(max_length=60)
    SHIRT_SIZES = (
        ('XS', "Extra Small"),
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Double Extra Large"),
    )
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
    primary_color = models.CharField(max_length=60)
    secondary_color = models.CharField(max_length=60)
