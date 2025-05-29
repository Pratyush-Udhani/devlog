from django.shortcuts import render
from django.views.generic import TemplateView, View
from rest_framework.generics import DestroyAPIView
from .models import LogEntry
from .serializers import LogEntrySerializer

import logging 
logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    template_name = 'logs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_tags = self.request.GET.getlist("tags")
        all_logs = LogEntry.objects.order_by("-created_at")

        if selected_tags:
            all_logs = [log for log in all_logs if any(tag in log.tags for tag in selected_tags)]

        all_tags = set(tag for log in LogEntry.objects.all() for tag in log.tags)
        
        context["logs"] = all_logs
        context["all_tags"] = sorted(all_tags)
        context["selected_tags"] = selected_tags
        return context

        """ context = super().get_context_data(**kwargs)
        all_logs = LogEntry.objects.all()
        all_tags = set(tag for log in all_logs for tag in log.tags)
        context["logs"] = LogEntry.objects.order_by("-created_at")
        context["all_tags"] = sorted(all_tags)
        context["selected_tags"] = self.request.GET.getlist("tags")
        return context """

class LogEntryUnifiedView(View):
    def get(self, request):
        tags_params = request.GET.getlist('tags')
        logs = LogEntry.objects.order_by("-created_at")

        if tags_params:
            logs = [log for log in logs if any(tag in log.tags for tag in tags_params)]

        if request.headers.get("HX-Request") == "true":
            return render(
                request,
                "logs/partials/log_list.html",
                {
                    "logs": logs,
                    "selected_tags": tags_params,
                })

        # In case it's not HTMX, fallback (optional)
        return render(
            request,
            "logs/index.html",
            {
                "logs": logs,
                "all_tags": sorted(set(tag for log in logs for tag in log.tags)),
                "selected_tags": tags_params,
            }
        )

class LogEntryFormView(View):
    def get(self, request):
        return render(request, "logs/partials/create_log_form.html")

class LogEntryCreateView(View):
    def post(self, request):
        title = request.POST.get("title", "").strip()
        body = request.POST.get("body", "").strip()
        tags_raw = request.POST.get("tags", "")
        tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]

        LogEntry.objects.create(title=title, body=body, tags=tags)

        # Return HTML for HTMX or JSON for CLI
        if request.headers.get("HX-Request") == "true":
            logs = LogEntry.objects.order_by("-created_at")
            return render(request, "logs/partials/log_list.html", {"logs": logs})

class LogEntryDeleteView(DestroyAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
