from django.test import TestCase
from django.test.client import RequestFactory
from stats import views
from main.models import Subject, Chapter, Exercise_Page, StudentConnectSubject, StudentConnectExercise
from django.contrib.auth.models import User


class TestMySubjectsView(TestCase):

    def setUp(self):
        # create a subject
        subject = Subject(subject_code='TDT4100', subject_name='Matte',
                          professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject.save()
        # create a chapter
        chapter = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject)
        chapter.save()

        # create some exercises
        ex1 = Exercise_Page(chapter=chapter, easy_points=1, medium_points=4, hard_points=5)
        ex2 = Exercise_Page(chapter=chapter, easy_points=2, medium_points=3, hard_points=5)
        ex1.save(), ex2.save()

        # create a user
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.save()

        # let user follow subject
        user.userprofile.add_subject(subject.pk)


    # test that the subject-view gives the correct status_code
    def test_subject_view(self):
        self.client.login(username='Hans', password='123zxc')
        url = '/my_subjects/TDT4100/'
        response = self.client.get(url)

        # response should give 200 status-code
        self.assertEqual(response.status_code, 200)

        # test that when a user is logged in, the correct user is rendered to the template
        self.client.login(username='Hans', password='123zxc')
        response = self.client.get(url)
        context = response.context
        self.assertEqual(context['user'].username, 'Hans')


    def test_all_exercises_view(self):
        self.client.login(username='Hans', password='123zxc')
        url = '/my_subjects/TDT4100/1/'
        response = self.client.get(url)

        # check that status_code is correct
        self.assertEqual(response.status_code, 200)

        # check that the correct chapter_name is rendered
        chapter = Chapter.objects.get(pk=1)
        correct_chapter_name = 'Multiplikasjon'
        self.assertEqual(chapter.chapter_name, correct_chapter_name)

        # there should be rendered two StudentExercise-connections, check if this is true
        self.assertTrue(len(response.context['connections'])==2)


    def test_exercise_view(self):
        self.client.login(username='Hans', password='123zxc')
        url = '/my_subjects/TDT4100/1/1/'
        response = self.client.get(url)

        # check that the status-code is correct
        self.assertEqual(response.status_code,200)

        # check that the rendered context is correct
        context = response.context
        self.assertEqual(context['info_easy'], '(Not completed)')
        self.assertEqual(context['info_medium'], '(Not completed)')

        # assume that the user answered correct to the hard question
        conn = StudentConnectExercise.objects.get(user=User.objects.get(username='Hans'), exercise=Exercise_Page.objects.get(pk=1))
        conn.completed_hard = True
        conn.save()

        response = self.client.get(url)
        context = response.context
        self.assertEqual(context['info_hard'], '(Completed)')
