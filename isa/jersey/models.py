from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.TextField()
    SHIRT_SIZES = (
        ('XS', "Extra Small"),
        ('S', "Small"),
        ('M', "Medium"),
        ('L', "Large"),
        ('XL', "Extra Large"),
        ('XXL', "Double Extra Large"),
    )
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES)

    def __str__(self):
        return "{}, {} {}".format(self.email, self.first_name, self.last_name)

class Authenticator(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    authenticator = models.CharField(max_length=64, primary_key=True)
    date_created = models.DateField(auto_now=True)

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
    shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES)
    primary_color = models.CharField(max_length=60)
    secondary_color = models.CharField(max_length=60)

    def __str__(self):
        return "{}, Number {} for {}".format(self.player, self.number, self.team)
