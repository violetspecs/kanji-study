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
    print(quiz_type)
    if quiz_type == 'kunyomi':
        userkanji_list = UserKanji.objects.filter(user=user).annotate(correct_percent=F('times_correct_kunyomi')*100/F('times_answered_kunyomi')*100).order_by(F('correct_percent').asc())[:20]
        kanji_list = Kanji.objects.filter(userkanji__in=userkanji_list).exclude(kunyomi__exact='くんよみ')
    elif quiz_type == 'onyomi':
        userkanji_list = UserKanji.objects.filter(user=user).annotate(correct_percent=F('times_correct_onyomi')*100/F('times_answered_onyomi')*100).order_by(F('correct_percent').asc())[:20]
        kanji_list = Kanji.objects.filter(userkanji__in=userkanji_list).exclude(onyomi__exact='オンヨミ')
    else:
        quiz_type = 'default'
        userkanji_list = UserKanji.objects.filter(user=user).annotate(correct_percent=F('times_correct_english')*100/F('times_answered_english')*100).order_by(F('correct_percent').asc())[:20]
        kanji_list = Kanji.objects.filter(userkanji__in=userkanji_list)
    
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
            userkanji = UserKanji(user=user, kanji=kanji)
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
        if quiz_type == "kunyomi":
            userkanji.times_correct_kunyomi = userkanji.times_correct_kunyomi + 1
            userkanji.times_answered_kunyomi = userkanji.times_answered_kunyomi + 1
        elif quiz_type == "onyomi":
            userkanji.times_correct_onyomi = userkanji.times_correct_onyomi + 1
            userkanji.times_answered_onyomi = userkanji.times_answered_onyomi + 1
        else:
            userkanji.times_correct_english = userkanji.times_correct_english + 1
            userkanji.times_answered_english = userkanji.times_answered_english + 1
        
        userkanji.save()

    for answer in wrong_answers:
        kanji = Kanji.objects.get(id=answer)
        print(kanji)
        userkanji = UserKanji.objects.get(user=user, kanji=kanji)
        if quiz_type == "kunyomi":
            userkanji.times_answered_kunyomi = userkanji.times_answered_kunyomi + 1
        elif quiz_type == "onyomi":
            userkanji.times_answered_onyomi = userkanji.times_answered_onyomi + 1
        else:
            userkanji.times_answered_english = userkanji.times_answered_english + 1

        userkanji.save()

    total_correct = len(correct_answers)
    total_answered = len(correct_answers) + len(wrong_answers)
    results = Kanji.objects.filter(id__in = wrong_answers)
    
    return render(request, 'quiz/result.html', {'type': quiz_type, 'kanji_list': results, 'kanji_list_json': json.dumps(list(results.values()), cls=DjangoJSONEncoder), 'total_correct': total_correct, 'total_answered': total_answered})