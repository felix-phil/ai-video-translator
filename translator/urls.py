from django.urls import path
from .api import (TranslatorCreateView, TranslatorListView,
                  StartTranslationWorker, AllTasks, CancelTask, ContributorsListView)

urlpatterns = [
    path('api/translations/create',
         TranslatorCreateView.as_view(), name='create-trans'),
    path('api/translations', TranslatorListView.as_view(), name='get-all-trans'),
    path('api/translations/translate',
         StartTranslationWorker.as_view(), name='start-trans'),
    path('api/contributors',
         ContributorsListView.as_view(), name='contributors'),
    path('celery-progress',
         AllTasks.as_view(), name='all-tasks'),
    path('celery/cancel',
         CancelTask.as_view(), name='cancel-tasks'),
]
