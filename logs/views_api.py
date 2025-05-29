
from rest_framework.parsers import JSONParser
from .models import LogEntry
from .serializers import LogEntrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogEntryAPIListView(APIView):
    def get(self, request):
        tags_params = request.GET.get("tags")
        logs = LogEntry.objects.order_by("-created_at")
        if tags_params:
            tags = tags_params.split(",")
            logs = [log for log in logs if any(tag in log.tags for tag in tags)]
        serializer = LogEntrySerializer(logs, many=True)
        return Response(serializer.data)

class LogEntryAPICreateView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        serializer = LogEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
