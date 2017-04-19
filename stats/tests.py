from django.test import TestCase, Client
from stats import views
from main.models import Subject, Chapter, Exercise_Page, StudentConnectSubject, StudentConnectExercise
from django.contrib.auth.models import User





# Testing statistics_index
class TestStatisticsIndex(TestCase):
    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()
        Subject(subject_code='TDT4110', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()

    def test_user_not_authenticated(self):

        url = '/adminpage/statistics/'
        response = self.client.get(url)
        body = response.content.decode('UTF-8')

        # check that we get the correct template when a user is not logged in
        self.assertIn("Please sign in", body)

        # check that the status-code is correct
        self.assertEqual(response.status_code, 200)


    def test_user_authenticated(self):
        user = User.objects.create_user('Hans', 'hans@test.no', '123zxc')
        user.save()

        logged_in = self.client.login(username='Hans', password='123zxc')

        url = '/adminpage/statistics/'
        resp = self.client.get(url)


        # check that the status-code is correct
        self.assertEqual(resp.status_code, 200)

        # check that the user is logged in
        self.assertTrue(logged_in)

        # check that the context from the view is correct
        context = resp.context['subjects']
        self.assertEqual(context[0], Subject.objects.get(subject_code='TDT4100'))
        self.assertEqual(context[1], Subject.objects.get(subject_code='TDT4110'))
        self.assertTrue(len(context) == 2)

class TestStatisticsSubject(TestCase):

    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()

    def test_statistics_subject(self):

        url = '/adminpage/statistics/TDT4100/'
        response = self.client.get(url)

        # response should give 200
        self.assertEqual(response.status_code,200)

        # check if the view render the correct subject to the template
        subject_code = response.context['subject'].subject_code
        self.assertEqual(subject_code, 'TDT4100')


class TestSubjectOverview(TestCase):

    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()

        User.objects.create_user('Hans', 'hans@test.no', '123zxc').save()
        User.objects.create_user('Grete', 'grete@test.no', '123zxc').save()

    def test_subject_overview(self):
        url = '/adminpage/statistics/TDT4100/overview/'
        response = self.client.get(url)

        # response should give 200
        self.assertEqual(response.status_code, 200)

        # testing the view-context
        self.assertEqual((response.context['num_students']),0)

        User.objects.get(username='Hans').userprofile.add_subject('TDT4100')
        User.objects.get(username='Grete').userprofile.add_subject('TDT4100')
        response = self.client.get(url)

        self.assertEqual((response.context['num_students']),2)

class TestSubjectHighscore(TestCase):

    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()




    def test_subject_highscore(self):
        # only have to test that the responses status_code is 200 because the context
        # is tested through the TestHelpMethods-class

        url = '/adminpage/statistics/TDT4100/highscore/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# the subject_chapters-view is more like an inheritance-view for other views, so
# we only have to test that the status_code is correct
class TestSubjectChapters(TestCase):


    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                            professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()

    def test_subject_chapters(self):
        # only have to test that the responses status_code is 200 because the context
        # is tested through the TestHelpMethods-class

        url = '/adminpage/statistics/TDT4100/chapters/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


# the subject_exervise-view is also a help/inheritance-view for other views
# enough to thst that the status_code is correct
class TestSubjectExercise(TestCase):
    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()


    def test_subject_chapters(self):


        url = '/adminpage/statistics/TDT4100/exercises/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class TestChapterPlot(TestCase):

    def setUp(self):
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        chapter1 = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject1)
        chapter1.save()
        ex1 = Exercise_Page(chapter=chapter1, easy_points=1, medium_points=4, hard_points=5)
        ex2 = Exercise_Page(chapter=chapter1, easy_points=2, medium_points=3, hard_points=5)
        ex1.save(), ex2.save()

        # most of the context that is rendered are tested in the class TestHelpMethods, so
        # we only test the context that is not already tested

    def test_chapter_plot(self):
        chapter = Chapter.objects.get(chapter_number=1, chapter_name="Multiplikasjon")

        url = '/adminpage/statistics/TDT4100/chapter_plot/' + str(chapter.pk) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test that the view render the correct chapter
        self.assertEqual(response.context['chapter'].pk, chapter.pk)

# only have to test that the status_code is correct because the context is tested in the TestHelpMethods-class
class TestExerciseBargraph(TestCase):
    def test_exercise_bargraph(self):
        subject = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject.save()
        chapter = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject)
        chapter.save()
        ex = Exercise_Page(chapter=chapter, easy_points=2, medium_points=3, hard_points=5)
        ex.save()
        url = '/adminpage/statistics/TDT4100/graph/' + str(ex.pk) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

# only have to test that the status_code is correct because the context is tested in the TestHelpMethods-class
class TestSubjectPieGraph(TestCase):

    def setUp(self):
        Subject(subject_code='TDT4100', subject_name='Matte',
                professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no').save()

    def test_subject_pie_graph(self):
        url = '/adminpage/statistics/TDT4100/graph/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

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

    def test_create_chapter_graph(self):

        # ----------- SETUP --------------
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        chapter1 = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject1)
        chapter1.save()
        ex1 = Exercise_Page(chapter=chapter1, easy_points=1, medium_points=4, hard_points=5)
        ex2 = Exercise_Page(chapter=chapter1, easy_points=2, medium_points=3, hard_points=5)
        ex1.save(), ex2.save()

        user1 = User(username='Hans', password='123zxc')
        user2 = User(username='Grete', password='123zxc')
        user1.save(), user2.save()

        user1.userprofile.add_subject(subject1.pk)
        user2.userprofile.add_subject(subject1.pk)
        # --------------------------------

        connection = StudentConnectExercise(user=user1, exercise=ex1)
        connection.completed_easy=True
        connection.completed_medium=True
        connection.completed_hard=True
        connection.save()

        data = views.create_chapter_graph(chapter1)
        correct_data = [[1,1],[2,0]]
        self.assertEqual(data, correct_data)


    def test_create_means(self):
        # ----------- SETUP --------------
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        chapter1 = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject1)
        chapter1.save()
        ex1 = Exercise_Page(chapter=chapter1, easy_points=1, medium_points=4, hard_points=5)
        ex1.save()

        user1 = User(username='Hans', password='123zxc')
        user2 = User(username='Grete', password='123zxc')
        user1.save(), user2.save()

        user1.userprofile.add_subject(subject1.pk)
        user2.userprofile.add_subject(subject1.pk)
        # --------------------------------

        connection1 = StudentConnectExercise(user=user1, exercise=ex1)
        connection1.completed_easy=True
        connection1.completed_hard= True
        connection1.save()

        connection2 = StudentConnectExercise(user=user2, exercise=ex1)
        connection2.completed_easy=True
        connection2.completed_medium= True
        connection2.save()

        data = views.create_means(ex1)
        correct_data = (2,1,1)

        self.assertEqual(data, correct_data)

    def test_create_subject_graph_values(self):
        # ----------- SETUP --------------
        subject1 = Subject(subject_code='TDT4100', subject_name='Matte',
                           professor_firstname='Jan', professor_lastname='Teigen', professor_email='jan@teigen.no')
        subject1.save()
        chapter1 = Chapter(chapter_number=1, chapter_name="Multiplikasjon", subject=subject1)
        chapter1.save()
        ex1 = Exercise_Page(chapter=chapter1, easy_points=1, medium_points=4, hard_points=5)
        ex2 = Exercise_Page(chapter=chapter1, easy_points=1, medium_points=4, hard_points=5)

        ex1.save(), ex2.save()

        user1 = User(username='Hans', password='123zxc')
        user2 = User(username='Grete', password='123zxc')
        user3 = User(username='Peter', password='123zxc')

        user1.save(), user2.save(), user3.save()

        user1.userprofile.add_subject(subject1.pk)
        user2.userprofile.add_subject(subject1.pk)
        user3.userprofile.add_subject(subject1.pk)

        # --------------------------------

        connection1 = StudentConnectSubject.objects.get(user=user1, subject=subject1)
        connection2 = StudentConnectSubject.objects.get(user=user2, subject=subject1)
        connection3 = StudentConnectSubject.objects.get(user=user3, subject=subject1)

        connection1.points = 20
        connection2.points = 1
        connection3.points = 10


        connection1.save(), connection2.save(), connection3.save()

        data = views.create_subject_graph_values(subject1)
        correct_data = [1,0,0,0,1,0,0,0,0,1]

        self.assertEqual(data, correct_data)

