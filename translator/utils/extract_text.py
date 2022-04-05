from translator.models import Translator
import speech_recognition as sr
import os
import contextlib
import wave
import math
from queue import Queue
from threading import Thread
from translator.utilities import get_audio_duration


def recognize_thread(q: Queue, result):
    while not q.empty():
        work_args_tuple = q.get()
        r = sr.Recognizer()
        _audio = sr.AudioFile(work_args_tuple[1])
        try:
            with _audio as source:
                r.adjust_for_ambient_noise(source)
                audio = r.record(
                    source, offset=work_args_tuple[0]*work_args_tuple[2], duration=work_args_tuple[2])

                # Using Google Speech Recognizer
                text = r.recognize_google(audio, language="en-GB")
                result[work_args_tuple[0]] = text
        except:
            # result[work_args_tuple[0]] = '...'
            # print(f"Failed to transcribe task {work_args_tuple[0]}")
            raise Exception(f"Failed to transcribe task {work_args_tuple[0]}")

        q.task_done()
    return True


def extract_text(object_id):
    """Transcribes audio file to text and saves it to the object"""
    # Get the object
    translator_object = Translator.objects.get(pk=object_id)

    # raise exceptions
    if not translator_object:
        raise Exception("Object not found")
    if not os.path.isfile(translator_object.source_audio.path):
        raise Exception("No source audio exists in the specified path")

    duration = 10
    audio_source_file_path = translator_object.source_audio.path
    total_duration = get_audio_duration(audio_source_file_path) / duration
    total_duration = math.ceil(total_duration)

    # Create queue
    queue = Queue(maxsize=0)
    num_theads = min(50, int(total_duration))

    # Create array to share to store transcriptions in each threads
    transcriptions_list = ['' for x in range(0, total_duration)]
    for task_index in range(0, total_duration):
        queue.put((task_index, audio_source_file_path, duration))

    # Recognize speech
    for thread_index in range(num_theads):
        worker = Thread(target=recognize_thread,
                        args=(queue, transcriptions_list))
        worker.setDaemon(True)
        worker.start()
    queue.join()

    # Joint transcriptions_list into a single string
    transcribed_text = ""
    for text in transcriptions_list:
        transcribed_text += text+" "

    # Save transcribed text to DB
    translator_object.extracted_text = transcribed_text
    translator_object.save()
