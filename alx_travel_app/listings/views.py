from rest_framework import viewsets, filters
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['available', 'location']
    search_fields = ['name', 'description']

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'listing', 'user', 'start_date', 'end_date']

    def get_queryset(self):
      queryset = super().get_queryset()
      listing_id = self.kwargs.get('listing_pk')
      if listing_id:
          queryset = queryset.filter(listing_id=listing_id)
      return queryset
