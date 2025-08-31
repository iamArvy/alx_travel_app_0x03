from rest_framework import viewsets, filters, status
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .payment_utils import chapa
from django.http import Http404
from .tasks import send_booking_confirmation

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
    
    def perform_create(self, serializer):
        booking = serializer.save()

        # Trigger async email task if user has email
        if booking.user and booking.user.email:
            send_booking_confirmation.delay(
                booking.user.email, booking.id
            )

class InitiatePaymentView(APIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
            
            # Check if payment already exists
            if hasattr(booking, 'payment'):
                return Response(
                    {"error": "Payment already initiated for this booking"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Initiate payment with Chapa
            payment_response = chapa.initiate_payment(booking=booking)
            
            if not payment_response or 'status' not in payment_response or payment_response['status'] != 'success':
                return Response(
                    {"error": "Failed to initiate payment"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
            
            # Create payment record
            payment = Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                transaction_id=payment_response['data']['tx_ref'],
                chapa_response=payment_response
            )
            
            return Response({
                "status": "success",
                "checkout_url": payment_response['data']['checkout_url'],
                "transaction_id": payment.transaction_id
            })
            
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class VerifyPaymentView(APIView):
    def get(self, request):
        transaction_id = request.query_params.get('tx_ref')
        
        if not transaction_id:
            return Response(
                {"error": "Transaction reference required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            raise Http404("Payment not found")
        
        data = chapa.verify_payment(transaction_id)

        if not data or data.get('status') != 'success':
            payment.status = "failed"
            payment.save(update_fields=["status"])
            return Response({"status": "failed"}, status=status.HTTP_200_OK)
            
        payment.status = "completed"
        payment.chapa_response = data
        payment.save(update_fields=["status", "chapa_response"])

        send_booking_confirmation.delay(payment.booking.id)

        return Response({"status": "completed"}, status=status.HTTP_200_OK)