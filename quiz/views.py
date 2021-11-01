from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Kanji, UserKanji
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, F, Value, Case, When
from types import SimpleNamespace
from django.views.decorators.csrf import csrf_exempt
import json

@login_required(login_url='/login/')
def index(request):
    return render(request, 'quiz/index.html')

@login_required(login_url='/login/')
def answer(request):
    user = request.user
    quiz_type = request.GET.get('quiz')

    if quiz_type == 'kunyomi':
        userkanji_list = UserKanji.objects.filter(user=user).annotate(correct_percent=Case(When(times_answered_kunyomi=0, then=0),default=(F('times_correct_kunyomi')*100/F('times_answered_kunyomi')*100))).order_by(F('correct_percent').asc())
        kanji_list = Kanji.objects.filter(userkanji__in=userkanji_list).exclude(kunyomi__exact='くんよみ')[:20]
    elif quiz_type == 'onyomi':
        userkanji_list = UserKanji.objects.filter(user=user).annotate(correct_percent=Case(When(times_answered_onyomi=0, then=0),default=(F('times_correct_onyomi')*100/F('times_answered_onyomi')*100))).order_by(F('correct_percent').asc())
        kanji_list = Kanji.objects.filter(userkanji__in=userkanji_list).exclude(onyomi__exact='オンヨミ')[:20]
    else:
        quiz_type = 'default'
        userkanji_list = UserKanji.objects.filter(user=user).annotate(correct_percent=Case(When(times_answered_english=0, then=0),default=(F('times_correct_english')*100/F('times_answered_english')*100))).order_by(F('correct_percent').asc())
        kanji_list = Kanji.objects.filter(userkanji__in=userkanji_list)[:20]
    
    return render(request, 'quiz/answer.html', {'type': quiz_type, 'kanji_list': kanji_list, 'kanji_list_json': json.dumps(list(kanji_list.values()), cls=DjangoJSONEncoder)})

@csrf_exempt
def register(request):
    kanji_list = json.loads(request.POST['kanji_list'])
    users = User.objects.all()
    for kanji_json in kanji_list:
        kunyomi = "くんよみ"
        onyomi = "オンヨミ"
        english = "english"

        if "kunyomi" in kanji_json:
            kunyomi = kanji_json['kunyomi']
        if "onyomi" in kanji_json:
            onyomi = kanji_json['onyomi']
        if "meanings" in kanji_json:
            english = kanji_json['meanings']

        kanji = Kanji(kanji=kanji_json['character'], english=english, onyomi=onyomi, kunyomi=kunyomi)
        kanji.save()
        for user in users:
            userkanji = UserKanji(user=user, kanji=kanji, times_correct=0, times_answered=0)
            userkanji.save()

    return HttpResponse("Successfully added " + str(len(kanji_list)) + " kanji")


@login_required(login_url='/login/')
def result(request):
    correct_answers = request.POST['correctAnswers'].split()
    wrong_answers = request.POST['wrongAnswers'].split()
    quiz_type = request.POST['quizChoiceType']
    print(correct_answers)
    print(wrong_answers)

    user = request.user

    for answer in correct_answers:
        kanji = Kanji.objects.get(id=answer)
        print(kanji)
        userkanji = UserKanji.objects.get(user=user, kanji=kanji)
        userkanji.times_correct = userkanji.times_correct + 1
        userkanji.times_answered = userkanji.times_answered + 1
        userkanji.save()

    for answer in wrong_answers:
        kanji = Kanji.objects.get(id=answer)
        print(kanji)
        userkanji = UserKanji.objects.get(user=user, kanji=kanji)
        userkanji.times_answered = userkanji.times_answered + 1
        userkanji.save()

    total_correct = len(correct_answers)
    total_answered = len(correct_answers) + len(wrong_answers)
    results = Kanji.objects.filter(id__in = wrong_answers)

    isKunyomi = False
    if quiz_type == 'kunyomi':
        isKunyomi = True
    
    return render(request, 'quiz/result.html', {'type': quiz_type, 'kanji_list': results, 'kanji_list_json': json.dumps(list(results.values()), cls=DjangoJSONEncoder), 'total_correct': total_correct, 'total_answered': total_answered})