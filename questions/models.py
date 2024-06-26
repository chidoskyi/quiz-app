from django.db import models
from quizes.models import Quiz

# Create your models here.

class Question(models.Model):
    text = models.CharField(max_length=250)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    created = models.DateTimeField( auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.text)
    
    def get_answers(self):
        return self.answer_set.all()  # Access the related answers through the Answer model
    

class Answer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'question: {self.question.text}, answer: {self.text}, correct: {self.correct}'
    