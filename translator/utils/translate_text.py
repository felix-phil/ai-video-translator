from typing import List
from translator.models import Translator
from threading import Thread
from queue import Queue
from translator.utilities import get_chunks


def translate_thread(q: Queue, result: List):
    while not q.empty():
        work_args = q.get()
        try:
            from deep_translator import GoogleTranslator
            translated = GoogleTranslator(
                source="auto", target=work_args[2]).translate(work_args[1])
            result[work_args[0]] = str(translated)
        except:
            # result[work_args[0]] = '....'
            # print(f"failed to transcribe '{work_args[1]}'")
            raise Exception(f"failed to transcribe '{work_args[1]}'")
        q.task_done()
        return True


def translate_text(object_id):
    """ Translates into another language """
    translator_object = Translator.objects.get(pk=object_id)
    # raise exceptions
    if not translator_object:
        raise Exception("Object not found")
    if not translator_object.extracted_text:
        raise Exception(
            "Transciption has not been extracted from audio, extract text and try again")

    text_to_translate = translator_object.extracted_text
    sentence_list = []
    # Split text to chunks if text is greater than 4500 and split it into chunks
    if len(text_to_translate) > 4500:
        chunks = get_chunks(text_to_translate, 4500)
        for text in chunks:
            sentence_list.append(text)
    else:
        sentence_list.append(text_to_translate)

    queue = Queue(maxsize=0)
    num_threads = min(50, len(sentence_list))

    tranlated_sentence_list = ['' for sentence in sentence_list]

    for i in range(len(sentence_list)):
        queue.put(
            (i, sentence_list[i], translator_object.destination_language))

    for thread in range(num_threads):
        worker = Thread(target=translate_thread, args=(
            queue, tranlated_sentence_list))
        worker.setDaemon(True)
        worker.start()

    queue.join()
    translated_text = " ".join(tranlated_sentence_list)

    # Save to DB
    translator_object.translated_text = translated_text
    translator_object.save()
