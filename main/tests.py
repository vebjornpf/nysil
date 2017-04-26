from django.test import TestCase
from .models import Subject, Chapter, User


class LoginLogoutTest(TestCase):
    def setUp(self):
        User.objects.create_user('Grete', 'grete@test.no', '123zxc')

    def test_login_user(self):
        user = User.objects.create_user(username = 'Hans', password = '123zxc')
        user.save()
        logged_in = self.client.login(username = 'Hans', password = '123zxc')
        url = '/main/'
        resp = self.client.get(url)
        context = resp.content.decode('UTF-8')

        self.assertTrue(logged_in)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(user.username, context)

    def test_login_prof(self):
        user = User.objects.create_user(username='Hans', password='123zxc')
        user.is_staff = True
        user.save()
        url = '/main/'
        resp = self.client.get(url)
        context = resp.content.decode('UTF-8')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(user.username, context)

    def test_add_subject(self):
        user = User.objects.create_user(username = 'Hans', password = '123zxc')
        user.save()
        self.client.login(username = 'Hans', password = '123zxc')
        subject = Subject.objects.create(subject_code = "TDT4120", subject_name = "Matte 3")
        subject.save()
        user.userprofile.add_subject("TDT4120")
        url = '/my_subjects/' + str(subject.pk) +'/'
        resp = self.client.get(url)
        context = resp.content.decode('UTF-8')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(subject.pk, context)

    def test_logout_user(self):
        user = User.objects.create_user(username='Hans', password='123zxc')
        user.save()
        self.client.login(username='Hans', password='123zxc')
        logged_out = self.client.logout()
        url = '/main/login_user/'

        self.assertFalse(logged_out)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertIn("Username", self.client.get(url).content.decode('UTF-8'))

    def test_register_user(self):
        url = '/main/userregister/'
        resp = self.client.get(url)

        self.assertTrue(resp.status_code, 200)

    def test_register_prof(self):
        url = '/main/professorregister/'
        resp = self.client.get(url)

        self.assertTrue(resp.status_code, 200)

class AdminPageTest(TestCase):
    def setUp(self):
        Subject.objects.create(subject_code = "TDT4100", subject_name = "DatDat")
        Subject.objects.create(subject_code="TMA4100", subject_name="Matte 1")
        Subject.objects.create(subject_code="TEP4100", subject_name="FLuidmekanikk")
        Chapter.objects.create(chapter_number = 1, chapter_name = "ER-modeller", subject = Subject.objects.get(pk="TDT4100"))
        Chapter.objects.create(chapter_number = 1, chapter_name = "Integrasjon", subject = Subject.objects.get(pk="TMA4100"))
        Chapter.objects.create(chapter_number = 2, chapter_name = "Euler", subject = Subject.objects.get(pk="TMA4100"))
        Chapter.objects.create(chapter_number = 1, chapter_name = "Integrasjon", subject = Subject.objects.get(pk="TEP4100"))

    #Test if the subject is created, and possible to call upon with get()
    def test_subject_creation(self):
        Datdat = Subject.objects.get(pk="TDT4100")
        Matte = Subject.objects.get(subject_code ="TMA4100")
        self.assertIsNotNone(Matte)
        self.assertIsNotNone(Datdat)
        self.assertEqual(Datdat,Subject.objects.get(subject_name="DatDat"))
        self.assertEqual(Matte,Subject.objects.get(pk="TMA4100"))

    # Test if the chapter is created, and possible to call upon with get()
    def test_chapter_creation(self):
        ER = Chapter.objects.get(chapter_name = "ER-modeller")
        self.assertIsNotNone(ER)
        self.assertEqual(ER, Chapter.objects.get(chapter_name="ER-modeller"))



    #Checking if duplicate is allowed for different subject. chapter_number & name is equal, but the chapter in whole is not
    def test_chapter_equality(self):
        IntegrasjonMatte = Chapter.objects.get(chapter_name = "Integrasjon", subject = Subject.objects.get(pk ="TMA4100"))
        IntegrasjonFluid = Chapter.objects.get(chapter_name = "Integrasjon", subject = Subject.objects.get(pk = "TEP4100"))
        self.assertNotEqual(IntegrasjonMatte,IntegrasjonFluid)
        self.assertEqual(IntegrasjonMatte.chapter_number, IntegrasjonFluid.chapter_number)
        self.assertEqual(IntegrasjonMatte.chapter_name, IntegrasjonFluid.chapter_name)
