from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book, BookScore, Borrowing, Reservation
from .serializers import AuthorSerializer, BookSerializer
from .tasks import send_due_date_reminder
from django.core import mail
from datetime import timedelta
from django.core import mail
from books.tasks import send_due_date_reminder




class AuthorModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )

    def test_author_str(self):
        self.assertEqual(str(self.author), "John Doe")


class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), "Sample Book")

    def test_average_score(self):
        self.assertEqual(self.book.average_score(), 0)  # No scores yet

class BookScoreModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.book_score = BookScore.objects.create(
            user=self.user,
            book=self.book,
            score=4
        )

    def test_book_score_unique_together(self):
        with self.assertRaises(Exception):
            BookScore.objects.create(
                user=self.user,
                book=self.book,
                score=5
            )


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book
        )

    def test_is_overdue(self):
        self.borrowing.due_date = timezone.now().date() - timedelta(days=1)
        self.borrowing.save()
        self.assertTrue(self.borrowing.is_overdue())


class ReservationModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.reservation = Reservation.objects.create(
            user=self.user,
            book=self.book
        )

    def test_reservation_str(self):
        self.assertEqual(str(self.reservation), "testuser reserved Sample Book")


class AuthorSerializerTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.serializer = AuthorSerializer(instance=self.author)

    def test_author_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['name'], 'John Doe')
        self.assertEqual(data['biography'], 'Biography of John Doe')


class BookSerializerTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.serializer = BookSerializer(instance=self.book)

    def test_book_serializer(self):
        data = self.serializer.data
        self.assertEqual(data['title'], 'Sample Book')
        self.assertEqual(data['description'], 'Description of Sample Book')


class UserRegistrationViewTest(APITestCase):
    def test_user_registration(self):
        url = '/api/register/'
        data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)


class BorrowBookViewTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.client.force_authenticate(user=self.user)

    def test_borrow_book(self):
        url = '/api/borrow/'
        data = {'book': self.book.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Borrowing.objects.filter(user=self.user, book=self.book).exists())


class BookListViewTest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)  # Ensure the user is authenticated

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('title', response.data[0])



class JWTAuthenticationTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.token_url = '/api/token/'

    def test_obtain_jwt_token(self):
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)




'''
class SendDueDateReminderTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            name="John Doe",
            biography="Biography of John Doe",
            nationality="American",
            date_of_birth="1980-01-01"
        )
        self.user = User.objects.create_user(username="testuser", password="password")
        self.book = Book.objects.create(
            title="Sample Book",
            description="Description of Sample Book",
            author=self.author,
            isbn="1234567890123",
            category="Fiction",
            publication_date="2024-01-01"
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            due_date=timezone.now().date()  # Ensure it's overdue
        )

    def test_send_due_date_reminder(self):
        # Ensure no emails are sent before the task runs
        self.assertEqual(len(mail.outbox), 0)
        
        # Run the task directly
        send_due_date_reminder.apply()

        # Check if an email has been sent
        self.assertEqual(len(mail.outbox), 1)
        if mail.outbox:
            self.assertEqual(mail.outbox[0].subject, 'Book Due Date Reminder')