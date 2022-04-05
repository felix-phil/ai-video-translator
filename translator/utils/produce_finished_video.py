from moviepy.editor import AudioClip, AudioFileClip, VideoClip, VideoFileClip
from translator.models import Translator
import os
from uuid import uuid4
from django.core.files import File


def produce_finished_video(object_id):
    translator_object = Translator.objects.get(pk=object_id)

    if not translator_object:
        raise Exception("Object not found")
    if not os.path.isfile(translator_object.source_video.path):
        raise Exception(
            "Video file does not exist")
    if not os.path.isfile(translator_object.translated_audio.path):
        raise Exception(
            "Translated audio does not exist")

    video_file_path = translator_object.source_video.path
    audio_file_path = translator_object.translated_audio.path

    video_clip = VideoFileClip(video_file_path)
    audio_clip = AudioFileClip(audio_file_path)
    video_current_fps = video_clip.fps

    # Joining the video with translated audio
    final_clip = video_clip.set_audio(audio_clip)
    temp_file_name = str(translator_object.id)+"-"+str(uuid4())+".mp4"
    final_clip.write_videofile(
        filename=temp_file_name, fps=video_current_fps, threads=40)
    # Save Audio to DB
    translator_object.translated_video_audio = File(open(temp_file_name, "rb"))
    translator_object.save()

    # Remove temp file
    os.unlink(temp_file_name)
