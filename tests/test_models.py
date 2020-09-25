from django.test import TestCase
from quiz.models import UserScore, Question, config

# Create your tests here.

class QuestionTest(TestCase):
    def setUp(self):
        u=Question(question='question', day = '1', question_no = '1', answer = 'ans')
        # Question.objects.create(question='q2', day = '1', question_no = '2', answer = 'ans2')
        # Question.objects.create(question='question', day = '2', question_no = '1', answer = 'ans11')
        # Question.objects.create(question='q22', day = '2', question_no = '2', answer = 'ans22')
        u.save()
        
        
    def testGetQuestion(self):
        q1 = Question.objects.filter(day = '1', question_no = '1')       
        # q2 = Question.objects.get(day = '1', question_no = '2')
        # q3 = Question.objects.get(day = '2', question_no = '1')
        # q4 = Question.objects.get(day = '2', question_no = '2')
        
        self.assertEqual(
            Question.check_ans(Question,'ans',q1), True
        )
        self.assertEqual(
            Question.check_ans(Question,'ans2',q1), False
        )
