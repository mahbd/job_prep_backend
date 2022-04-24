from django.test import TestCase, Client
from django.urls import reverse

from constants import DIFFICULTY_CHOICES, STATUS_CHOICES
from users.models import User
from problems.models import Problem, Tag, Company, Status

c = Client()


class ProblemAPITestCase(TestCase):
    def setUp(self):
        self.problem1 = Problem.objects.create(
            name='Test Problem',
            acceptance=0.99,
            difficulty=DIFFICULTY_CHOICES[0][0],
            question_html='<p>Test Question</p>',
            solution_html='<p>Test Solution</p>',
        )
        self.problem2 = Problem.objects.create(
            name='Test Problem 2',
            acceptance=0.99,
            difficulty=DIFFICULTY_CHOICES[0][0],
            question_html='<p>Test Question 2</p>',
            solution_html='<p>Test Solution 2</p>',
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.staff = User.objects.create_user(
            username='teststaff',
            password='testpassword',
            is_staff=True,
        )
        self.base_url = reverse('api:problems-list')

    def test_problem_creation_ann(self):
        res = c.post(self.base_url, {
            'name': 'Test Problem 3',
            'acceptance': 0.99,
            'difficulty': DIFFICULTY_CHOICES[0][0],
            'question_html': '<p>Test Question 3</p>',
            'solution_html': '<p>Test Solution 3</p>',
        })
        self.assertEqual(res.status_code, 403)

    def test_problem_creation_regular_user(self):
        c.force_login(self.user)
        res = c.post(self.base_url, {
            'name': 'Test Problem 3',
            'acceptance': 0.99,
            'difficulty': DIFFICULTY_CHOICES[0][0],
            'question_html': '<p>Test Question 3</p>',
            'solution_html': '<p>Test Solution 3</p>',
        }, follow=True)
        self.assertEqual(res.status_code, 403)

    def test_problem_creation_staff(self):
        c.force_login(self.staff)
        res = c.post(self.base_url, {
            'name': 'Test Problem 3',
            'acceptance': 0.99,
            'difficulty': DIFFICULTY_CHOICES[0][0],
            'question_html': '<p>Test Question 3</p>',
            'solution_html': '<p>Test Solution 3</p>',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201, res.json())
        # check number of problems
        self.assertEqual(Problem.objects.count(), 3)

    def test_problem_creation_staff_invalid_data(self):
        c.force_login(self.staff)
        res = c.post(self.base_url, {
            'name': 'Test Problem 3',
            'acceptance': 0.99,
            'difficulty': 'invalid',
            'question_html': '<p>Test Question 3</p>',
            'solution_html': '<p>Test Solution 3</p>',
        }, follow=True)
        self.assertEqual(res.status_code, 400)
        # check number of problems
        self.assertEqual(Problem.objects.count(), 2)

    def test_problem_creation_staff_missing_data(self):
        c.force_login(self.staff)
        res = c.post(self.base_url, {
            'name': 'Test Problem 3',
            'acceptance': 0.99,
            'difficulty': DIFFICULTY_CHOICES[0][0],
            'question_html': '<p>Test Question 3</p>',
        }, follow=True)
        self.assertEqual(res.status_code, 400)
        # check number of problems
        self.assertEqual(Problem.objects.count(), 2)

    def test_get_problems(self):
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)

    def test_get_problem(self):
        res = c.get(f"{self.base_url}{self.problem1.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], self.problem1.name)

    def test_get_problem_invalid(self):
        res = c.get(f"{self.base_url}999/")
        self.assertEqual(res.status_code, 404)

    def test_update_problem_staff(self):
        c.force_login(self.staff)
        res = c.patch(f"{self.base_url}{self.problem1.id}/", {
            'name': 'Test Problem 1',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], 'Test Problem 1')

    def test_update_problem_regular_user(self):
        c.force_login(self.user)
        res = c.patch(f"{self.base_url}{self.problem1.id}/", {
            'name': 'Test Problem 1',
        })
        self.assertEqual(res.status_code, 403)

    def test_update_problem_ann(self):
        res = c.patch(f"{self.base_url}{self.problem1.id}/", {
            'name': 'Test Problem 1',
        })
        self.assertEqual(res.status_code, 403)

    def test_delete_problem_staff(self):
        c.force_login(self.staff)
        res = c.delete(f"{self.base_url}{self.problem1.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Problem.objects.count(), 1)

    def test_delete_problem_regular_user(self):
        c.force_login(self.user)
        res = c.delete(f"{self.base_url}{self.problem1.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Problem.objects.count(), 2)

    def test_delete_problem_ann(self):
        res = c.delete(f"{self.base_url}{self.problem1.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Problem.objects.count(), 2)


class TagAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.staff = User.objects.create_user(
            username='teststaff',
            password='testpassword',
            is_staff=True,
        )
        self.tag1 = Tag.objects.create(name='Test Tag 1')
        self.tag2 = Tag.objects.create(name='Test Tag 2')
        self.base_url = reverse('api:tags-list')

    def test_tag_creation_staff(self):
        c.force_login(self.staff)
        res = c.post(self.base_url, {
            'name': 'Test Tag 3',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Tag.objects.count(), 3)

    def test_tag_creation_regular_user(self):
        c.force_login(self.user)
        res = c.post(self.base_url, {
            'name': 'Test Tag 3',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Tag.objects.count(), 2)

    def test_tag_creation_ann(self):
        res = c.post(self.base_url, {
            'name': 'Test Tag 3',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Tag.objects.count(), 2)

    def test_get_tags_staff(self):
        c.force_login(self.staff)
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)

    def test_get_tags_regular_user(self):
        c.force_login(self.user)
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)

    def test_get_tags_ann(self):
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)

    def test_get_tag_staff(self):
        c.force_login(self.staff)
        res = c.get(f"{self.base_url}{self.tag1.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], 'Test Tag 1')

    def test_get_tag_regular_user(self):
        c.force_login(self.user)
        res = c.get(f"{self.base_url}{self.tag1.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], 'Test Tag 1')

    def test_get_tag_ann(self):
        res = c.get(f"{self.base_url}{self.tag1.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['name'], 'Test Tag 1')

    def test_update_tag_staff(self):
        c.force_login(self.staff)
        res = c.patch(f"{self.base_url}{self.tag1.id}/", {
            'name': 'Test Tag 1 Updated',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Tag.objects.get(id=self.tag1.id).name, 'Test Tag 1 Updated')

    def test_update_tag_regular_user(self):
        c.force_login(self.user)
        res = c.patch(f"{self.base_url}{self.tag1.id}/", {
            'name': 'Test Tag 1 Updated',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Tag.objects.get(id=self.tag1.id).name, 'Test Tag 1')

    def test_update_tag_ann(self):
        res = c.patch(f"{self.base_url}{self.tag1.id}/", {
            'name': 'Test Tag 1 Updated',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Tag.objects.get(id=self.tag1.id).name, 'Test Tag 1')

    def test_delete_tag_staff(self):
        c.force_login(self.staff)
        res = c.delete(f"{self.base_url}{self.tag1.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Tag.objects.count(), 1)

    def test_delete_tag_regular_user(self):
        c.force_login(self.user)
        res = c.delete(f"{self.base_url}{self.tag1.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Tag.objects.count(), 2)

    def test_delete_tag_ann(self):
        res = c.delete(f"{self.base_url}{self.tag1.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Tag.objects.count(), 2)


# noinspection DuplicatedCode
class CompanyAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.staff = User.objects.create_user(
            username='teststaff',
            password='testpassword',
            is_staff=True,
        )
        self.company1 = Company.objects.create(name='Test Company 1')
        self.company2 = Company.objects.create(name='Test Company 2')
        self.base_url = reverse('api:companies-list')

    def test_get_companies_staff(self):
        c.force_login(self.staff)
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)
        self.assertEqual(res.json()['results'][0]['name'], 'Test Company 1')

    def test_get_companies_regular_user(self):
        c.force_login(self.user)
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)
        self.assertEqual(res.json()['results'][0]['name'], 'Test Company 1')

    def test_get_companies_ann(self):
        res = c.get(self.base_url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)
        self.assertEqual(res.json()['results'][0]['name'], 'Test Company 1')

    def test_create_company_staff(self):
        c.force_login(self.staff)
        res = c.post(self.base_url, {
            'name': 'Test Company 3',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Company.objects.count(), 3)

    def test_create_company_regular_user(self):
        c.force_login(self.user)
        res = c.post(self.base_url, {
            'name': 'Test Company 3',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Company.objects.count(), 2)

    def test_create_company_ann(self):
        res = c.post(self.base_url, {
            'name': 'Test Company 3',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Company.objects.count(), 2)

    def test_update_company_staff(self):
        c.force_login(self.staff)
        res = c.patch(f"{self.base_url}{self.company1.id}/", {
            'name': 'Test Company 1 Updated',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Company.objects.count(), 2)
        self.assertEqual(Company.objects.get(id=self.company1.id).name, 'Test Company 1 Updated')

    def test_update_company_regular_user(self):
        c.force_login(self.user)
        res = c.patch(f"{self.base_url}{self.company1.id}/", {
            'name': 'Test Company 1 Updated',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Company.objects.get(id=self.company1.id).name, 'Test Company 1')

    def test_update_company_ann(self):
        res = c.patch(f"{self.base_url}{self.company1.id}/", {
            'name': 'Test Company 1 Updated',
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Company.objects.get(id=self.company1.id).name, 'Test Company 1')

    def test_delete_company_staff(self):
        c.force_login(self.staff)
        res = c.delete(f"{self.base_url}{self.company1.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Company.objects.count(), 1)

    def test_delete_company_regular_user(self):
        c.force_login(self.user)
        res = c.delete(f"{self.base_url}{self.company1.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Company.objects.count(), 2)

    def test_delete_company_ann(self):
        res = c.delete(f"{self.base_url}{self.company1.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Company.objects.count(), 2)


# noinspection DuplicatedCode
class StatusTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
        )
        self.staff = User.objects.create_user(
            username='teststaff',
            password='testpassword',
            is_staff=True,
        )
        self.problem1 = Problem.objects.create(
            name='Test Problem',
            acceptance=0.99,
            difficulty=DIFFICULTY_CHOICES[0][0],
            question_html='<p>Test Question</p>',
            solution_html='<p>Test Solution</p>',
        )
        self.problem2 = Problem.objects.create(
            name='Test Problem 2',
            acceptance=0.99,
            difficulty=DIFFICULTY_CHOICES[0][0],
            question_html='<p>Test Question 2</p>',
            solution_html='<p>Test Solution 2</p>',
        )
        self.status1 = Status.objects.create(problem=self.problem1, user=self.user, status=STATUS_CHOICES[0][0])
        self.status2 = Status.objects.create(problem=self.problem2, user=self.user, status=STATUS_CHOICES[0][0])
        self.base_url = reverse('api:statuses-list')

    def test_get_status_list_staff(self):
        c.force_login(self.staff)
        res = c.get(f"{self.base_url}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)

    def test_get_status_list_user(self):
        c.force_login(self.user)
        res = c.get(f"{self.base_url}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 2)

    def test_get_status_list_user2(self):
        c.force_login(self.user2)
        res = c.get(f"{self.base_url}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()['results']), 0)

    def test_get_status_list_ann(self):
        res = c.get(f"{self.base_url}")
        self.assertEqual(res.status_code, 403)

    def test_create_status_user(self):
        c.force_login(self.user)
        res = c.post(f"{self.base_url}", {
            'problem': self.problem1.id,
            'status': STATUS_CHOICES[0][0],
        }, content_type='application/json')
        status_id = res.json()['id']
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Status.objects.count(), 3)
        self.assertEqual(Status.objects.get(id=status_id).user_id, self.user.id)

    def test_create_status_ann(self):
        res = c.post(f"{self.base_url}", {
            'problem': self.problem1.id,
            'status': STATUS_CHOICES[0][0],
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Status.objects.count(), 2)

    def test_update_status_staff(self):
        c.force_login(self.staff)
        res = c.patch(f"{self.base_url}{self.status1.id}/", {
            'status': STATUS_CHOICES[1][0],
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Status.objects.get(id=self.status1.id).status, STATUS_CHOICES[1][0])

    def test_update_status_user(self):
        c.force_login(self.user)
        res = c.patch(f"{self.base_url}{self.status1.id}/", {
            'status': STATUS_CHOICES[1][0],
        }, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Status.objects.get(id=self.status1.id).status, STATUS_CHOICES[1][0])

    def test_update_status_user2(self):
        c.force_login(self.user2)
        res = c.patch(f"{self.base_url}{self.status1.id}/", {
            'status': STATUS_CHOICES[1][0],
        }, content_type='application/json')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(Status.objects.get(id=self.status1.id).status, STATUS_CHOICES[0][0])

    def test_update_status_ann(self):
        res = c.patch(f"{self.base_url}{self.status1.id}/", {
            'status': STATUS_CHOICES[1][0],
        }, content_type='application/json')
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Status.objects.get(id=self.status1.id).status, STATUS_CHOICES[0][0])

    def test_delete_status_staff(self):
        c.force_login(self.staff)
        res = c.delete(f"{self.base_url}{self.status1.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Status.objects.count(), 1)

    def test_delete_status_user(self):
        c.force_login(self.user)
        res = c.delete(f"{self.base_url}{self.status1.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Status.objects.count(), 1)

    def test_delete_status_user2(self):
        c.force_login(self.user2)
        res = c.delete(f"{self.base_url}{self.status1.id}/")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(Status.objects.count(), 2)
