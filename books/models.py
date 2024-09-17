from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from datetime import datetime

def default_due_date():
    return timezone.now() + timedelta(days=14)

class Author(models.Model):
    name = models.CharField(max_length=100)
    biography = models.TextField()
    nationality = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13)
    category = models.CharField(max_length=100)
    publication_date = models.DateField()

    def __str__(self):
        return self.title

    def average_score(self):
        scores = self.scores.all()
        if scores.exists():
            return sum([score.score for score in scores]) / scores.count()
        return 0

class BookScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'book')

class Borrowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=default_due_date)
    return_date = models.DateTimeField(null=True, blank=True)

    def is_overdue(self):
        today = timezone.now().date()
        if self.return_date is None:
            return today > self.due_date  
        return False  

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reserved_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reserved {self.book.title}"
