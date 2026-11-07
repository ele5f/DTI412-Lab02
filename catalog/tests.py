from django.test import TestCase
from django.urls import reverse


class CatalogRouteTests(TestCase):
    """Automated version of the lab's Step 7.1 verification checklist."""

    def test_home_shows_metrics(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_courses'], 3)
        self.assertContains(response, 'DTI412')

    def test_course_list_shows_all_courses(self):
        response = self.client.get(reverse('catalog:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['courses']), 3)

    def test_course_detail_found(self):
        response = self.client.get(reverse('catalog:course_detail', args=[101]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Special Topic in Application Development')

    def test_course_detail_missing_returns_404(self):
        response = self.client.get('/courses/999/')
        self.assertEqual(response.status_code, 404)

    def test_inquiry_get(self):
        response = self.client.get(reverse('catalog:inquiry'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_inquiry_post_validation_errors(self):
        response = self.client.post(reverse('catalog:inquiry'), {
            'student_name': '', 'email': 'not-an-email', 'message': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['errors']), 3)
        self.assertIsNone(response.context['submitted_data'])

    def test_inquiry_post_success(self):
        response = self.client.post(reverse('catalog:inquiry'), {
            'student_name': 'Jane Doe', 'email': 'jane@example.com',
            'course_code': 'DTI412', 'message': 'What are the prerequisites?',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errors'], [])
        self.assertContains(response, 'Inquiry Processed Successfully!')

    def test_inquiry_post_rejected_without_csrf_token(self):
        from django.test import Client
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post(reverse('catalog:inquiry'), {
            'student_name': 'Jane', 'email': 'jane@example.com', 'message': 'Hi',
        })
        self.assertEqual(response.status_code, 403)


class CourseSearchTests(TestCase):
    """Step 7.2 extension challenge: ?q= search filter."""

    def test_search_by_code(self):
        response = self.client.get(reverse('catalog:course_list'), {'q': 'dti305'})
        codes = [c['code'] for c in response.context['courses']]
        self.assertEqual(codes, ['DTI305'])

    def test_search_by_title(self):
        response = self.client.get(reverse('catalog:course_list'), {'q': 'Database'})
        codes = [c['code'] for c in response.context['courses']]
        self.assertEqual(codes, ['DTI201'])

    def test_search_no_match(self):
        response = self.client.get(reverse('catalog:course_list'), {'q': 'zzz'})
        self.assertEqual(response.context['courses'], [])
        self.assertContains(response, 'No courses match')
