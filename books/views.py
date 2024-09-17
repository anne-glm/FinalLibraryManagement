from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import Author, Book, Borrowing, Reservation, BookScore
from .serializers import AuthorSerializer, BookSerializer, BorrowingSerializer, ReservationSerializer, UserRegistrationSerializer, BookScoreSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Generate JWT token for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            "message": "User created successfully.",
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)

class BorrowedBooksListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)

class ReservedBooksListView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]  # Only admin can create authors

class AuthorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]  # Only admin can update/delete authors


class BookScoreCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user  
        book_id = request.data.get('book')
        score = request.data.get('score')

        if not book_id or not score:
            return Response({'detail': 'Book ID and score are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user already scored this book
        if BookScore.objects.filter(user=user, book=book).exists():
            return Response({'detail': 'You have already scored this book.'}, status=status.HTTP_400_BAD_REQUEST)

        book_score = BookScore(user=user, book=book, score=score)
        book_score.save()

        serializer = BookScoreSerializer(book_score)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]  

class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]  

class BorrowBookView(generics.CreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        user = self.request.user
        book = serializer.validated_data['book']

        # Check how many books the user currently has borrowed and not returned
        current_borrowed_books = Borrowing.objects.filter(user=user, return_date__isnull=True).count()
        if current_borrowed_books >= 5:
            raise ValidationError("You cannot borrow more than 5 books at a time.")

        # Check if the book is already borrowed by another user
        if Borrowing.objects.filter(book=book, return_date__isnull=True).exists():
            raise ValidationError("This book is already borrowed by another user.")

        # Check if the book is reserved by another user
        if Reservation.objects.filter(book=book).exclude(user=user).exists():
            raise ValidationError("This book is reserved by another user.")

        # If the book is not borrowed or reserved, allow borrowing
        serializer.save(user=user)

class ReserveBookView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        book = serializer.validated_data['book']

        # Prevent reservation if the book is already reserved by another user
        if Reservation.objects.filter(book=book).exists():
            raise ValidationError("This book is already reserved by another user.")

        
        serializer.save(user=self.request.user)


class ReturnBookView(generics.DestroyAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.return_date:
            # If the book is already returned, raise an exception
            raise ValidationError("This book has already been returned.")
        instance.return_date = timezone.now()
        instance.save()

    def delete(self, request, *args, **kwargs):
        try:
          
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'status': 'success', 'message': 'Book returned successfully'}, status=status.HTTP_200_OK)
        except Borrowing.DoesNotExist:
            # Return a 404 error if the borrowing doesn't exist
            return Response({'status': 'error', 'message': 'Borrowing record not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log unexpected errors for debugging purposes
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)