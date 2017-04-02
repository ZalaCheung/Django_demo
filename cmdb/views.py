from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from cmdb import models
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
# Create your views here.
@csrf_exempt
def index(request):
    # return HttpResponse('hello world!')
    if request.method == 'GET':
        return JsonResponse({'desheng':'superzala'})
    if request.method == 'POST':
        json_str = (request.body).decode('utf-8')
        body = json.loads(json_str)
        data = models.Users(Username = body['user'],Password = body['pwd'],FirstName = body['first'],LastName=body['last'])
        data.save();
        return JsonResponse({'result':'true'})
    # return render(request,"index.html",)
@csrf_exempt
def login(request):
    if request.method == 'POST':
        json_str = (request.body).decode('utf-8')
        body = json.loads(json_str)
        try:
            user = models.Users.objects.get(Username=body['user'])

        except:
            return JsonResponse({'result':"User doesn't exist" })
        if user.Password == body['pwd']:
            return JsonResponse({'result':'ok','id':user.ID})
        else:
            return JsonResponse({'result':'Wrong password'})
@csrf_exempt
def loginTest(request):
    #body_unicode = request.body.decode('utf-8')
    #print(request.body)
    json_str = ((request.body).decode('utf-8'))
    body = json.loads(json_str)
    username = body['UserName']
    password = body['PassWord']
    #username = request.GET.get("name", None)
    #password = request.GET.get("password", None)
    userPassJudge = models.Users.objects.filter(Username=username, Password=password)
    print(userPassJudge.get(Username=username).ID)
    if userPassJudge:
        return JsonResponse({'result': "true","UserID": userPassJudge.get(Username=username).ID})
    else:
        return JsonResponse({'result': "false"})
@csrf_exempt
def singleTest(request):
  if request.method == 'POST':
      json_str = (request.body).decode('utf-8')
      body = json.loads(json_str)
      user = models.Users.objects.get(ID = body['UserID'])
      data = models.Tests(UserID = user,Problem = body['Problem'],Score = body['Score'])
      data.save()
      return JsonResponse({'TestID': data.ID})

@csrf_exempt
def singleProblem(request):
    if request.method == 'POST':
        json_str = (request.body).decode('utf-8')
        body = json.loads(json_str)
        test = models.Tests.objects.get(ID=body['TestID'])
        data = models.IndividualProblemResult(TestID=test,ProblemNo=body['ProblemNum'],Operand1=body['Operand1'],
                                              Operand2=body['Operand2'],Operation = body['Operation'],
                                              AnswerCorrectly=body['AnswerCorrectly'])
        data.save()
        return JsonResponse({'result':'true'})
@csrf_exempt
def update(request):
    if request.method == 'POST':
        json_str = (request.body).decode('utf-8')
        body = json.loads(json_str)
        models.Tests.objects.filter(ID=body['TestID']).update(Score=body['Score'])
        return JsonResponse({'result':'true'})

@csrf_exempt
def top5user(request):
    if request.method == 'GET':
        data = models.Tests.objects.values("UserID").annotate(totalScore =Max("Score")).order_by("-totalScore").all()[:5]
        size = min(len(data),5)
        datas = []
        for i in range(size):
            datas.append({"username":models.Users.objects.get(ID = data[i]['UserID']).Username,"score":data[i]['totalScore']})
        # print(data[0]['totalScore'])
        return JsonResponse({'result': 'true',"topusers":datas})
