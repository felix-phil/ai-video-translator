from uuid import uuid4
import uuid
from moviepy.editor import AudioFileClip, VideoFileClip
from django.core.files import File
from translator.models import Translator
import os


def extract_audio(object_id):
    """This function extracts audio from video"""
    # Get the object
    translator_object = Translator.objects.get(pk=object_id)
    old_audio_file_path = ''
    if translator_object.source_audio:
        old_audio_file_path = translator_object.source_audio.path

    # raise exceptions
    if not translator_object:
        raise Exception("Object not found")
    if not translator_object.source_video:
        raise Exception(
            "Video file not available, try again!")

    if not os.path.isfile(translator_object.source_video.path):
        raise Exception(
            "Video file not available, try again!")

    video_clip = VideoFileClip(translator_object.source_video.path)

    new_audio_file_path = str(uuid4())+'.wav'
    video_clip.audio.write_audiofile(new_audio_file_path)

    translator_object.source_audio = File(open(new_audio_file_path, "rb"))
    translator_object.save()

    try:
        os.unlink(new_audio_file_path)
        if os.path.isfile(old_audio_file_path):
            os.unlink(old_audio_file_path)
    except:
        print('Deleting error..')
