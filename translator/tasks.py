from celery import shared_task
from celery_progress.backend import ProgressRecorder
from .utils.extract_audio import extract_audio
from .utils.extract_text import extract_text
from .utils.translate_text import translate_text
from .utils.produce_speech_audio import produce_speech_audio
from .utils.produce_finished_video import produce_finished_video
from translator.models import Translator
from celery.exceptions import TaskError
from celery import states


@shared_task(bind=True)
def translate_video(self, object_id):
    translator_object = Translator.objects.get(pk=object_id)
    try:
        translator_object.status = 'LOADING'
        translator_object.save()

        progress_recorder = ProgressRecorder(self)

        # Extract Audio from Video
        progress_recorder.set_progress(0, 5, 'preparing..')
        extract_audio(object_id)
        progress_recorder.set_progress(1, 5, 'extracting audio')

        # Extract Text
        extract_text(object_id)
        progress_recorder.set_progress(2, 5, 'transcribing audio to text')

        # Traslate text
        translate_text(object_id)
        progress_recorder.set_progress(3, 5, 'translating text')

        # produce audio from speech
        produce_speech_audio(object_id)
        progress_recorder.set_progress(4, 5, 'producing translated audio')

        # combine video and translated audio
        produce_finished_video(object_id)
        progress_recorder.set_progress(5, 5, 'producing translated video')

        translator_object.status = 'COMPLETED'
        translator_object.save()

        return 'Completed'

    except:
        translator_object.status = 'FAILED'
        translator_object.save()
        self.update_state(state=states.FAILURE, meta={})
        raise TaskError()
        # return 'Failed'
