from django.contrib import admin
from translator.models import Translator, Contributor
from translator.utils.extract_audio import extract_audio
from translator.utils.extract_text import extract_text
from translator.utils.translate_text import translate_text
from translator.utils.produce_speech_audio import produce_speech_audio
from translator.utils.produce_finished_video import produce_finished_video


def extract_audios(modeladmin, request, queryset):
    for t in queryset:
        extract_audio(t.id)


def extract_texts(modeladmin, request, queryset):
    for t in queryset:
        extract_text(t.id)


def translate_texts(modeladmin, request, queryset):
    for t in queryset:
        translate_text(t.id)


def produce_speech_audios(modeladmin, request, queryset):
    for t in queryset:
        produce_speech_audio(t.id)


def finish_task(modeladmin, request, queryset):
    for t in queryset:
        produce_finished_video(t.id)


class TranslatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'source_language',
                    'destination_language', 'translated_video_audio']
    ordering = ['id']
    actions = [extract_audios, extract_texts,
               translate_texts, produce_speech_audios, finish_task]


admin.site.register(Translator, TranslatorAdmin)
admin.site.register(Contributor)
# Register your models here.
