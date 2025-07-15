from rest_framework import generics
from django.db import models
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ExchangeProposalSerializer, ExchangeProposalCreateSerializer, ExchangeProposalUpdateSerializer
from .permissions import IsOwnerOrReadOnly, IsSenderOrReceiver


class APIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000



class AdAPIList(generics.ListCreateAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = APIListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category', 'condition']
    search_fields = ['title', 'description']
    

class AdAPIUpdateOrDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (IsOwnerOrReadOnly, )

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("Объявление с указанным ID не найдено.")


class ExchangeProposalList(generics.ListAPIView):
    serializer_class = ExchangeProposalSerializer
    pagination_class = APIListPagination
    def get_queryset(self):
        user = self.request.user
        return ExchangeProposal.objects.filter(
            models.Q(ad_sender__user=user) | models.Q(ad_receiver__user=user)
        ).distinct().order_by('-created_at')
    
    permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ad_sender', 'status']


class ExchangeProposalCreateView(generics.CreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalCreateSerializer
    permission_classes = (IsAuthenticated, )



class ExchangeProposalUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ExchangeProposalUpdateSerializer
    permission_classes = [IsAuthenticated, IsSenderOrReceiver]

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound("Предложение с указанным ID не найдено.")


# class AdAPIDestroy(generics.RetrieveDestroyAPIView):
#     queryset = Ad.objects.all()
#     serializer_class = AdSerializer
#     permission_classes = (IsOwnerOrReadOnly, )

