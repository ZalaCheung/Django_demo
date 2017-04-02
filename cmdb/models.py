from django.db import models

class Users(models.Model):
    ID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)

class Tests(models.Model):
    ID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(Users,on_delete=models.CASCADE)
    Problem = models.CharField(max_length=50)
    Score = models.IntegerField()

class IndividualProblemResult(models.Model):
    ID = models.AutoField(primary_key=True)
    TestID = models.ForeignKey(Tests,on_delete=models.CASCADE)
    ProblemNo = models.IntegerField()
    Operand1 = models.IntegerField()
    Operand2 = models.IntegerField()
    Operation = models.CharField(max_length=10)
    AnswerCorrectly = models.BooleanField()
# Create your models here.
