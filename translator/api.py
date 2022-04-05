import imp
import json
from translator.models import Translator, Contributor
from translator.serializers import TranslatorSerializer, ContributorSerializer
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK)

from django_celery_results.models import TaskResult
from server.celery import app
from celery import states
from .tasks import translate_video


class TranslatorListView(ListAPIView):
    serializer_class = TranslatorSerializer
    queryset = Translator.objects.all()
    permission_classes = [permissions.AllowAny]


class TranslatorCreateView(CreateAPIView):
    serializer_class = TranslatorSerializer
    queryset = Translator.objects.all()
    permission_classes = [permissions.AllowAny]

    # def perform_create(self, serializer, *args, **kwargs):

    #     serializer.save()
    #     data = serializer.data
    #     id = data.get('id')
    # source_video = data['source_video']

    # perform background tasks

    # 0. Etract thumbnail image file from video
    # 1. Extract audio from uploaded video
    # extract_audio(
    #     id, data.get('name') or id
    # )

    # 3. Convert audio to text
    # extract_text(id)
    # 4. Convert text to another language
    # 5. Convert translated text to another language
    # 6. Use TTS
    # 7. Join Speech with video


class StartTranslationWorker(APIView):
    def post(self, request, *args, **kwargs):
        try:
            object_id = request.data['object_id']

            translator_object = Translator.objects.get(pk=object_id)
            task_id = ''
            if not translator_object.current_task:
                task = translate_video.delay(object_id)
                task_id = task.task_id
                translator_object.current_task = task.task_id
                translator_object.save()
            else:
                task_id = translator_object.current_task
                translate_video.apply_async(
                    args=(object_id,), task_id=translator_object.current_task)
            return Response({"message": "Job has been added to task", "task_id": task_id},
                            HTTP_200_OK)

        except KeyError:
            return Response({"error": "translation object_id is required"}, HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": "something went wrong"}, HTTP_500_INTERNAL_SERVER_ERROR)


class AllTasks(APIView):
    def get(self, request, *args, **kwargs):
        tasks = TaskResult.objects.all()
        serialized_tasks = []
        for task in tasks:
            result = json.loads(task.result)
            serialized_tasks.append(
                {'id': task.task_id,
                 'status': task.status,
                 'result': result,
                 'date_created': task.date_created,
                 'date_done': task.date_done
                 })
        return Response(serialized_tasks, HTTP_200_OK)


class CancelTask(APIView):
    def post(self, request, *args, **kwargs):
        try:
            task_id = request.data['task_id']
            app.control.revoke(task_id, terminate=True)
            return Response({"message": 'Task cancelled'}, HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, HTTP_500_INTERNAL_SERVER_ERROR)


class ContributorsListView(ListAPIView):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    permission_classes = [permissions.AllowAny]
