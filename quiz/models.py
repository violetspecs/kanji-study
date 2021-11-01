from django.db import models
from django.contrib.auth.models import User

class Kanji(models.Model):
    kanji = models.CharField(max_length=20)
    onyomi = models.CharField(max_length=200)
    kunyomi = models.CharField(max_length=200)
    english = models.CharField(max_length=200)

    def __str__(self):
        return self.kanji

class UserKanji(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE)
    times_correct_english = models.IntegerField(default = 0)
    times_answered_english = models.IntegerField(default = 0)
    times_correct_onyomi = models.IntegerField(default = 0)
    times_answered_onyomi = models.IntegerField(default = 0)
    times_correct_kunyomi = models.IntegerField(default = 0)
    times_answered_kunyomi = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username + " for " + self.kanji.kanji + ": " + str(self.times_correct_english) + " out of " + str(self.times_answered_english)