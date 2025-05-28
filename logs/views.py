from rest_framework.generics import CreateAPIView, ListAPIView
from .models import LogEntry
from .serializers import LogEntrySerializer

class LogEntryListView(ListAPIView):
    serializer_class = LogEntrySerializer
    
    def get_queryset(self) : #type: ignore[override]
        queryset = LogEntry.objects.all().order_by("-created_at")
        tags_params = self.request.GET.get('tags')

        if tags_params:
            tags = tags_params.split(",")
            # Fetch all logs and filter in Python
            logs = LogEntry.objects.all().order_by("-created_at")
            filtered_logs = [log for log in logs if any(tag in log.tags for tag in tags)]
            return filtered_logs


        return queryset

class LogEntryCreateView(CreateAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
