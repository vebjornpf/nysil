from django.test import TestCase, RequestFactory, Client
from stats import views
from main.models import Subject, Chapter, Exercise_Page, StudentConnectSubject
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from django.contrib.auth import authenticate, login




# Testing statistics_index
class TestStatisticsIndex(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.client = Client()

    def test_user_not_authenticated(self):
        request = self.factory.get('stats:statistics_index')
        request.user = AnonymousUser()
        response = views.statistics_index(request)
        self.assertEqual(response.status_code,200)


    def test_user_authenticated(self):
        pass











# testing the views help-methods and make sure that the logic is correct
class TestHelpMethods(TestCase):

    # testing the numbers of students in a subject
    def test_get_number_of_students(self):

        # -------- SETUP ------------------
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        user1 = User(username='Hans', password='123zxc')
        user2 = User(username='Grete', password='123zxc')
        user3 = User(username='Peter', password='123zxc')

        subject1.save(), user1.save(), user2.save(), user3.save()
        # -------------------------------------

        self.assertEqual(views.get_number_of_students(subject1),0)

        user1.userprofile.add_subject(subject1.pk)
        user2.userprofile.add_subject(subject1.pk)
        user3.userprofile.add_subject(subject1.pk)

        self.assertEqual(views.get_number_of_students(subject1),3)


    # testing the max points in a subject
    def test_get_max_points(self):

        # ---------- SETUP -------------------
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        chapter1 = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject1)
        chapter1.save()
        ex1 = Exercise_Page(chapter=chapter1, easy_points=1, medium_points=4, hard_points=5)
        ex2 = Exercise_Page(chapter=chapter1, easy_points=2, medium_points=3, hard_points=5)
        ex1.save(), ex2.save()

        # ----------------------------------

        self.assertEqual(views.get_max_points(subject1), 20)


    # testing that the fix_highscore_info is on the correct format
    def test_fix_highscore_info(self):

        # ----------- SETUP --------------
        # Subject
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()

        # students
        user1 = User(username='Hans', password='123zxc')
        user2 = User(username='Grete', password='123zxc')
        user1.save(), user2.save()

        # connects students to
        user1.userprofile.add_subject(subject1.pk)
        user2.userprofile.add_subject(subject1.pk)

        # fix the users points in the subject
        StudentConnectSubject.objects.get(user=user1, subject=subject1).points = 10
        StudentConnectSubject.objects.get(user=user2, subject=subject1).points = 5

        # ----------------------------------------------

        highscore_info = views.fix_highscore_info(subject1)

        # testing the length of highscore_info
        self.assertEqual(len(highscore_info),2)

        # testing that the ranks is in the correct order
        self.assertTrue(highscore_info[0][0]==1)
        self.assertTrue(highscore_info[1][0]==2)

        # testing that user1 has rank=1 (first)
        self.assertTrue(highscore_info[0][1].user==user1)

        # testing that the value of the last index is in the correct format
        self.assertTrue(highscore_info[1][2]=="0 %")