from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Subject, Chapter, Exercise_Page
from .forms import SubjectForm, ChapterForm, ExerciseForm


class TestAdminpageIndex(TestCase):
    def create_subject(self, code, name, pfname, plname, pemail):
        return Subject.objects.create(subject_code=code, subject_name = name, professor_firstname = pfname, professor_lastname = plname, professor_email = pemail )

    def create_chapter(self, number, name, subject):
        return Chapter.objects.create(chapter_number = number, chapter_name = name, subject = subject)

    def create_exercise_page(self, chapter, youtube, title, explanation, easyq, easya, easyp, medq, meda, medp, hardq, harda, hardp):
        return Exercise_Page.objects.create(chapter = Chapter.objects.get(chapter), youtube_id = youtube, headline = title, explanation = explanation,
                                            easy_question = easyq, easy_answer = easya, easy_points = easyp, medium_question = medq, meadium_answer = meda,
                                            medium_points = medp, hard_question = hardq, hard_answer = harda, hard_points = hardp)

    #Testing the forms.py with creation and checking if the excist
    def test_subject_form(self):
        Fluidmek = self.create_subject("TEP4100", "Fluidmekanikk", "Reidar", "Kristoffersen", "reidarkri@prof.ntnu.no")
        Form = SubjectForm(self.create_subject("TEP4140", "Fluidmekanikk", "Reidar", "Kristoffersen", "reidarkri@prof.ntnu.no"))

        self.assertEqual(Fluidmek, Subject.objects.get(pk = "TEP4100"))
        self.assertIsNotNone(Form)
        self.assertNotEqual(Fluidmek, Form)

    def test_chapter_form(self):
        Fluidmek = self.create_subject("TEP4100", "Fluidmekanikk", "Reidar", "Kristoffersen", "reidarkri@prof.ntnu.no")
        NavierStokes = ChapterForm(1, "Navier-Stokes")

        self.assertNotEqual(NavierStokes, self.create_chapter(1, "Navier-Stokes", Fluidmek))
        self.assertIsNotNone(NavierStokes)

    def test_exercise_page_form(self):
        Fluidmek = self.create_subject("TEP4100", "Fluidmekanikk", "Reidar", "Kristoffersen", "reidarkri@prof.ntnu.no")
        Euler = ExerciseForm(1, "Eulers Metode")

        self.assertIsNotNone(Euler)

    def test_index_view(self):
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.is_staff = True
        user.save()
        self.client.login(username='Hans', password='123zxc')
        index = '/adminpage/'

        resp = self.client.get(index)
        self.assertEqual(resp.status_code, 200)

    def test_reports_view(self):
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.is_staff = True
        user.save()
        self.client.login(username='Hans', password='123zxc')
        reports = '/adminpage/tilbakemeldinger/'
        resp = self.client.get(reports)
        self.assertEqual(resp.status_code, 200)


    def test_subjects_view(self):
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.is_staff = True
        user.save()
        self.client.login(username='Hans', password='123zxc')
        url = '/adminpage/subjects/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)


    def test_statistics_view(self):
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.is_staff = True
        user.save()
        self.client.login(username='Hans', password='123zxc')
        url = '/adminpage/statistics/'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_user_not_authenticated(self):
        url = '/adminpage/statistics/'
        response = self.client.get(url)
        
        # check that the status-code is correct (redirect_code, which is 302)
        self.assertEqual(response.status_code, 302)

    def test_user_authenticated(self):
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.save()

        logged_in = self.client.login(username='Hans', password='123zxc')

        url = '/adminpage/subjects/'
        resp = self.client.get(url)

        # check that the status-code is correct
        self.assertEqual(resp.status_code, 200)

        # check that the user is logged in
        self.assertTrue(logged_in)

        # check that the context from the view is correct
        context = resp.context['subjects']
        self.assertIsNotNone(context)

class TestAdminpageOverview(TestCase):

    def setUp(self):
        subject1 = Subject(subject_code='TMT4100', subject_name='Matte',
                professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        chapter1 = Chapter(chapter_number = 1, chapter_name = "Integrasjon", subject = Subject.objects.get(pk = "TMT4100"))
        chapter1.save()
        exercise = Exercise_Page(chapter = chapter1, headline = "Oppgave 1", easy_question = "Hvorfor funker dette?",
                                 easy_answer = "Because Django", easy_points = 3 )
        exercise.save()

    def test_subjects_overview(self):
        url = '/adminpage/subjects/'
        response = self.client.get(url)

        # response should give 200
        self.assertEqual(response.status_code, 200)

        # check if the view render the correct subject to the template
        subjects = response.context['subjects']
        self.assertIsNotNone(subjects)
        self.assertIn(Subject.objects.get(pk="TMT4100"), subjects)

    def test_chapters_overview(self):
        subject = Subject.objects.get(pk = "TMT4100")
        url = '/adminpage/subjects/' + str(subject.pk) + '/'
        response = self.client.get(url)

        # response should give 200
        self.assertEqual(response.status_code, 200)

        integrasjon = Chapter.objects.get(chapter_number = 1, chapter_name = "Integrasjon")
        context = response.content.decode('UTF-8')

        self.assertIn(subject.pk, context)
        self.assertIn(integrasjon.chapter_name, context)

    def test_exercise_overview(self):
        subject = Subject.objects.get(pk = "TMT4100")
        chapter = Chapter.objects.get(chapter_name = "Integrasjon")
        exercise = Exercise_Page.objects.get(headline = "Oppgave 1")
        url = '/adminpage/subjects/' + str(subject.pk) + '/' + str(chapter.pk) +'/'

        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertIn(exercise.headline, self.client.get(url).content.decode('UTF-8'))

class TestCreationDeletion(TestCase):
    def setUp(self):
        subject1 = Subject(subject_code='TMT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        subject2 = Subject(subject_code='TMT4140', subject_name='Matte 2',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject2.save()
        chapter1 = Chapter(chapter_number=1, chapter_name="Integrasjon", subject=Subject.objects.get(pk="TMT4100"))
        chapter1.save()
        chapter2 = Chapter(chapter_number=1, chapter_name="Diff lign", subject=Subject.objects.get(pk="TMT4140"))
        chapter2.save()
        exercise = Exercise_Page(chapter=chapter1, headline="Oppgave 1", easy_question="Hvorfor funker dette?",
                                 easy_answer="Because Django", easy_points=3)
        exercise.save()

    def test_delete_subject(self):
        subject1 = Subject.objects.get(pk = "TMT4100")
        url = '/adminpage/subjects/' + str(subject1.pk) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        subject1.delete()
        newUrl = self.client.get('/adminpage/subjects/').context['subjects']

        self.assertNotEqual(newUrl, subject1)

    def test_delete_chapter(self):
        chapter = Chapter.objects.get(chapter_name = "Integrasjon")
        delete_chapter = chapter.delete()
        response = self.client.get('/adminpage/subjects/')
        context = response.content.decode('UTF-8')

        self.assertNotIn(chapter.chapter_name, context)

    def test_delete_exercise(self):
        subject = Subject.objects.get(pk = "TMT4100")
        exercise = Exercise_Page.objects.get(headline = "Oppgave 1")
        chapter = Chapter.objects.get(chapter_name = "Integrasjon")
        exercise.delete()
        url = '/adminpage/subjects/' + str(subject.pk) + '/' + str(chapter.pk) + '/'

        self.assertNotIn(exercise.headline, self.client.get(url).content.decode('UTF-8'))
