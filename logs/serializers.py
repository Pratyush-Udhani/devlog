from rest_framework import serializers
from .models import LogEntry

import logging
logger = logging.getLogger(__name__)

class LogEntrySerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = LogEntry
        fields = ['id', 'title', 'body', 'tags', 'created_at']
