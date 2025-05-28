from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import LogEntry
from .serializers import LogEntrySerializer
# Create your views here.
#

class LogEntryListView(ListAPIView):
    queryset = LogEntry.objects.all().order_by("-created_at")
    serializer_class = LogEntrySerializer

class LogEntryCreateView(CreateAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
