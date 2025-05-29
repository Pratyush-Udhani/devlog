import json
from django.http import JsonResponse, QueryDict
from django.shortcuts import render
from django.views.generic import TemplateView, View
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.parsers import FormParser, JSONParser
from .models import LogEntry
from .serializers import LogEntrySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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

class LogEntryFormView(View):
    def get(self, request):
        return render(request, "logs/partials/create_log_form.html")

@method_decorator(csrf_exempt, name='dispatch')
class LogEntryCreateView(View):
    def post(self, request):
        if request.headers.get("Content-Type") == "application/json":
            data = json.loads(request.body)
            title = data.get("title", "").strip()
            body = data.get("body", "").strip()
            tags = data.get("tags", [])
        else:
            title = request.POST.get("title", "").strip()
            body = request.POST.get("body", "").strip()
            tags_raw = request.POST.get("tags", "")
            tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]

        LogEntry.objects.create(title=title, body=body, tags=tags)

        # Return HTML for HTMX or JSON for CLI
        if request.headers.get("HX-Request") == "true":
            logs = LogEntry.objects.order_by("-created_at")
            return render(request, "logs/partials/log_list.html", {"logs": logs})

        return JsonResponse({"message": "Log created"}, status=201)

class LogEntryDeleteView(DestroyAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
