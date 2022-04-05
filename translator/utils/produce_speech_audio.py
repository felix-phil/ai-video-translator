import os
from gtts import gTTS
from translator.models import Translator
from django.core.files import File
from uuid import uuid4
from translator.utilities import get_chunks


def produce_speech_audio(object_id):
    """This function produces a speech in the destination lang specified"""
    # Get the object
    translator_object = Translator.objects.get(pk=object_id)

    # raise exceptions
    if not translator_object:
        raise Exception("Object not found")
    if not translator_object.translated_text:
        raise Exception(
            "Audio has not been tranlated, please translate audio and try again!")

    old_audio_path = ''
    if translator_object.translated_audio:
        old_audio_path = translator_object.translated_audio.path

    text = translator_object.translated_text
    # text_chunks = get_chunks(text=text, maxlength=500)

    file_to_write = str(uuid4())+".wav"

    with open(file_to_write, "wb") as fp:
        # for chunk in text_chunks:
        tts = gTTS(text, lang=translator_object.destination_language)
        tts.write_to_fp(fp)

        #  Save to DB
    translated_audio = File(open(file_to_write, "rb"))
    translator_object.translated_audio = translated_audio
    translator_object.save()

    try:
        os.unlink(file_to_write)
        if os.path.isfile(old_audio_path):
            os.unlink(old_audio_path)
    except:
        print('Deleting error')
