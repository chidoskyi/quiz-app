from django.urls import path
from .views import QuizListView, quiz_view,quiz_data_view,save_quiz_view  # Change the import statement

app_name = 'quizes'

urlpatterns = [
    path('', QuizListView.as_view(), name='main-view'),
    path('<int:id>/', quiz_view, name="quiz-view"),
    path('<int:id>/save', save_quiz_view, name="save-view"),
    path('<int:id>/data', quiz_data_view, name="quiz-data-view"),
]
