from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from .models import LogEntry
from .serializers import LogEntrySerializer

import logging 
logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'logs/index.html'

class LogEntryUnifiedView(View):

    def get(self, request):
        tags_params = self.request.GET.get('tags')
        logs = LogEntry.objects.order_by("-created_at")

        if tags_params:
            tags = tags_params.split(",")
            # Fetch all logs and filter in Python
            logs = [log for log in logs if any(tag in log.tags for tag in tags)]

        # HTMX Requests
        if request.headers.get("HX-Request") == "true":
            logger.info("HTMX is requesting logs. return render")
            return render(request, "logs/partials/log_list.html", {"logs": logs})
        
        # CLI Requests
        logger.info("API is requesting logs. return JSON")
        serializer = LogEntrySerializer(logs, many=True)
        return JsonResponse(serializer.data, safe=False)

class LogEntryCreateView(CreateAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer


class LogEntryDeleteView(DestroyAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
