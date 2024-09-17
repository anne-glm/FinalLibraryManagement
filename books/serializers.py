from rest_framework import serializers
from .models import Author, Book, Borrowing, Reservation, BookScore
from django.contrib.auth.models import User


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'nationality', 'date_of_birth']

class BookScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookScore
        fields = ['id', 'user', 'book', 'score']
        extra_kwargs = {'user': {'read_only': True}}
        
class BookSerializer(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'isbn', 'category', 'publication_date', 'average_score']

    def get_average_score(self, obj):
        return obj.average_score()

class BorrowingSerializer(serializers.ModelSerializer):
    borrow_date = serializers.ReadOnlyField()
    due_date = serializers.ReadOnlyField()
    return_date = serializers.ReadOnlyField(required=False)  

    class Meta:
        model = Borrowing
        fields = ['id', 'book', 'borrow_date', 'due_date', 'return_date']


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'book', 'reserved_date']
        

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
       
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
