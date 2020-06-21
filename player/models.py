from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Player(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, related_name='player', on_delete=models.CASCADE)
    strength = models.IntegerField(verbose_name='Strength', default=1)
    intelligence = models.IntegerField(verbose_name='Intelligence', default=1)
    education = models.IntegerField(verbose_name='Education', default=1)
    dexterity = models.IntegerField(verbose_name='Dexterity', default=1)
    accuracy = models.IntegerField(verbose_name='Accuracy', default=1)
    agility = models.IntegerField(verbose_name='Agility', default=1)

    def __str__(self):
        return self.user.username
