from django.test import TestCase, Client
from django.urls import reverse

from constants import DIFFICULTY_CHOICES
from problems.models import Problem
from users.models import User

c = Client()


# noinspection DuplicatedCode
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

    def test_problem_creation_staff_with_companies(self):
        c.force_login(self.staff)
        res = c.post(self.base_url, {
            'name': 'Test Problem 3',
            'acceptance': 0.99,
            'difficulty': DIFFICULTY_CHOICES[0][0],
            'question_html': '<p>Test Question 3</p>',
            'solution_html': '<p>Test Solution 3</p>',
            'companies': ["Google", "Facebook"],
        }, content_type='application/json')
        self.assertEqual(res.status_code, 201, res.json())
        self.assertEqual(Problem.objects.count(), 3)
        # check number of companies
        self.assertEqual(len(Problem.objects.get(id=res.json()['id']).companies), 2)

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
