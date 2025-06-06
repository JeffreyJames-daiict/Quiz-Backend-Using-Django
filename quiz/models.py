from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
import pandas as pd

class Category(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name       

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    #sets one to one relationship with the another table Category and on delete cascade
    file = models.FileField(upload_to='quiz/')
    #Special Field used to extract the File
    created_at = models.DateTimeField(auto_now_add=True)
    #DateTimeField autonowadd means saves the date and time of the field when it was created first time
    updated_at = models.DateTimeField(auto_now=True)
    #DatetimeField autonow means saves the last updated time of the change

    class Meta:
        verbose_name_plural = 'Quizzes'

    def __str__(self):
        return self.title    
    

    # runs when quiz is saved    
    #call the function on quiz save
    def save(self,*args, **kwargs):
        super().save(*args,**kwargs)
        if self.file:
            self.import_quiz_from_excel()

    #function to extract Excel File
    def import_quiz_from_excel(self):
        #read the excel file
        df = pd.read_excel(self.file.path)
        
        #iterate over each row
        for index,row in df.iterrows():
            #extract question text, choices and correct answer from the row
            question_text = row['Question']
            choice1 = row['A']
            choice2 = row['B']
            choice3 = row['C']
            choice4 = row['D']

            correct_answer = row['Answer']
            #create the question object
            question = Question.objects.get_or_create(quiz = self,text = question_text)
            #create the choices object
            choice_1 = Choice.objects.get_or_create(question =question[0],text = choice1, is_correct = correct_answer == 'A')
            choice_2 = Choice.objects.get_or_create(question =question[0],text = choice2, is_correct = correct_answer == 'B')
            choice_3 = Choice.objects.get_or_create(question =question[0],text = choice3, is_correct = correct_answer == 'C')
            choice_4 = Choice.objects.get_or_create(question =question[0],text = choice4, is_correct = correct_answer == 'A')

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text =  models.TextField()

    def __str__(self):
        return self.text[:50]
    
class Choice(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)    
    text = models.TextField(max_length=255)

    is_correct = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.question.text[:50]},{self.text[:20]}'
    

class QuizSubmission(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
    score = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}, {self.quiz.title}"
    

class UserRank(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    rank = models.IntegerField(null = True,blank=True)
    total_score = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.rank},{self.user.username}"
    
@receiver(post_save, sender= QuizSubmission)
def update_leaderboard(sender, instance, created, **kwargs):
    if created:
        update_leaderboard()

def update_leaderboard():

    #Count the sum of scores of all users
    user_scores = (QuizSubmission.objects.values('user').annotate(total_score = Sum('score')).order_by('-total_score')) # Returns in the format of the list
    # Took the Users from the QuizSubmission which is linked with the User Function Objects
    # Here the Annotate takes the Unique user and total_score = Summation of the Score 

    #Update rank based on the sorted list
    rank = 1
    for entry in user_scores:
        user_id = entry['user']
        total_score = entry['total_score']

        user_rank,created = UserRank.objects.get_or_create(user_id = user_id)
        #getorcreate return two values in the tuple format first the user_id and the Boolean Value whether the return is the Truw of False 
        user_rank.rank = rank
        user_rank.total_score = total_score
        user_rank.save()
        rank+=1
