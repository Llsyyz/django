from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .project.douyin import dingdan_combine

def home(request):
    return render(request, 'app/home.html')

def index(request):
    question = {
        'question_text': 'What is your favorite programming language?',
        'choice_set': [
            {'choice_text': 'Python'},
            {'choice_text': 'JavaScript'},
            {'choice_text': 'Java'},
            {'choice_text': 'C++'},
        ]
    }
    content = {"question": question}
    return render(request, "app/deal.html", content)


def deal(request):
    if request.method == "POST":
        response = request.POST
        print(response)
        dir_from = response['dir_from']
        file_sort = response['file_sort']
        file_to = response['file_to']
        project = response['project']
        print(dir_from, file_sort, file_to, project)
        dingdan_combine.order_combine(dir_from, file_sort, file_to, project)
        return render(request, "app/deal.html", response)
