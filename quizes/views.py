from django.shortcuts import render
from django.http import JsonResponse
from .models import Quiz
from questions.models import Question,Answer
from results.models import Result
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'index.html'
    context_object_name = 'quizes'
    
def quiz_view(request, id):
    quiz = Quiz.objects.get(pk=id)
    context = {
        'quiz': quiz,
    }
    return render(request, 'quiz.html',context)


def quiz_data_view(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse( {'data': questions, 'time': quiz.time})









def save_quiz_view(request, id):
        questions = []
        data = request.POST
        print(data)
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')  # This removes the 'csrfmiddlewaretoken' key, if it exists
        
        for k in data_.keys():
            print('key: ', k) 
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)
        
        user = request.user
        quiz = Quiz.objects.get(pk=id)
        
        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        # correct_answer = None
        
        for q in questions:
            a_selected  = request.POST.get(q.text)
            
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                correct_answer = None
                for a in question_answers:
                    
                    if a_selected == a.text:
                        if a.correct:
                            score += 1 
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                        
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})
                
            
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)
        
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})
    
            
            
    