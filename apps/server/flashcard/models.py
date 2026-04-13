from django.db import models
# Create your models here.


class Flashcard(models.Model):
    # key of a flashcard
    # set_id = models.AutoField(foreign_key=True)
    set_id = models.ForeignKey('Set', on_delete=models.CASCADE)
    flashcard_id = models.AutoField(primary_key=True)
    # algorithm parameters
    EFactor = models.FloatField()
    interval = models.FloatField()
    repetition = models.IntegerField()
    # card information and front/back
    nextPractice = models.DateTimeField(null=True)
    lastPractice = models.DateTimeField(null=True)
    question = models.TextField()
    answer = models.TextField()


class Set(models.Model):
    nearest_practice = models.DateTimeField(null=True)
    set_id = models.AutoField(primary_key=True)
    set_name = models.CharField(max_length=100)
    # flashcards = models.ManyToManyField(Flashcard)
