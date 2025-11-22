from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from accounts.authentication import CsrfExemptSessionAuthentication

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        tasks = self.get_queryset()
        total = tasks.count()
        completed = tasks.filter(status='completed').count()
        in_progress = tasks.filter(status='in_progress').count()
        return Response({
            'total': total,
            'completed': completed,
            'inProgress': in_progress,
            'completionRate': (completed/total*100) if total else 0
        })
