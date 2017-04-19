from django.test import TestCase
from progress import views
from main.models import Subject, Chapter, Exercise_Page, StudentConnectSubject, StudentConnectExercise
from django.contrib.auth.models import User


# when testing the views, we only have to test that the status_code is correct, because all the context we render to
# the template has been tested in th TestHelpMethods-class
class TestProgressViews(TestCase):

    def setUp(self):
        # create a user
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.save()

        # create s subject the user can add
        subject = Subject(subject_code='TDT4100', subject_name='Matte',
                    professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject.save()

        user.userprofile.add_subject(subject)


    def test_my_progress_view(self):
        # log in a user
        self.client.login(username='Hans', password='123zxc')
        url = '/progress/'
        response = self.client.get(url)

        # response should give 200
        self.assertEqual(response.status_code, 200)

    def test_highscore_view(self):
        url = '/progress/TDT4100/highscore/'
        response = self.client.get(url)

        # response should give 200
        self.assertEqual(response.status_code, 200)


# a class for testing all the help-methods in the progress-view
class TestHelpMethods(TestCase):

    def setUp(self):
        # create some users
        hans = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        hans.save()
        grete = User.objects.create_user('Grete', 'grete@test.no', '123zxc')
        grete.save()
        peder = User.objects.create_user('Peder', 'peder@test.no', '123zxc')
        peder.save()

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

        # make the users follow the subject
        hans.userprofile.add_subject(subject.pk)
        grete.userprofile.add_subject(subject.pk)
        peder.userprofile.add_subject(subject.pk)

        # fix the user points
        grete_conn = StudentConnectSubject.objects.get(user=grete, subject=subject)
        hans_conn =StudentConnectSubject.objects.get(user=hans, subject=subject)
        peder_conn = StudentConnectSubject.objects.get(user=peder, subject=subject)

        grete_conn.points = 20
        hans_conn.points = 7
        peder_conn.points = 3
        grete_conn.save(), hans_conn.save(), peder_conn.save()

    def test_max_points(self):
        points = views.get_max_points(Subject.objects.get(pk='TDT4100'))
        correct_points = 20
        self.assertEqual(points, correct_points)


    def test_find_rank(self):

        # grete shoud have rank=1 on the format "1 of 3"
        grete_rank = views.find_rank(Subject.objects.get(pk='TDT4100'), User.objects.get(username='Grete'))
        correct_rank = "1 of 3"
        self.assertEqual(grete_rank, correct_rank)

        # hans shoud have rank=2 on the format "2 of 3"
        hans_rank = views.find_rank(Subject.objects.get(pk='TDT4100'), User.objects.get(username='Hans'))
        correct_rank = "2 of 3"
        self.assertEqual(hans_rank, correct_rank)

        # hans shoud have rank=2 on the format "2 of 3"
        peder_rank = views.find_rank(Subject.objects.get(pk='TDT4100'), User.objects.get(username='Peder'))
        correct_rank = "3 of 3"
        self.assertEqual(peder_rank, correct_rank)

    def test_set_view_context(self):
        # create some more subjects
        subject1 = Subject(subject_code='TDT4101', subject_name='Matte',
                          professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        subject2 = Subject(subject_code='TDT4102', subject_name='Matte',
                          professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject2.save()

        grete = User.objects.get(username='Grete')
        grete.userprofile.add_subject(subject1.pk)
        grete.userprofile.add_subject(subject2.pk)

        grete_subjects = StudentConnectSubject.objects.filter(user=grete)
        context = views.set_view_context(grete_subjects, grete)

        self.assertTrue(context[0][0][2] == "100.0%")
        self.assertTrue(context[1][0][2] == "0 %")
        self.assertTrue(context[2][0][2] == "0 %")

    def test_split_subjects(self):

        # because grete follows three subjects, all the lists should have length 1 because the subjects are divided by three
        # create some more subjects
        subject1 = Subject(subject_code='TDT4101', subject_name='Matte',
                          professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        subject2 = Subject(subject_code='TDT4102', subject_name='Matte',
                          professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject2.save()

        grete = User.objects.get(username='Grete')
        grete.userprofile.add_subject(subject1.pk)
        grete.userprofile.add_subject(subject2.pk)
        grete_subjects = StudentConnectSubject.objects.filter(user=grete)

        split = views.split_subjects(grete_subjects)

        self.assertTrue(len(split[0]) == 1)
        self.assertTrue(len(split[1]) == 1)
        self.assertTrue(len(split[2]) == 1)