import threading
import queue
import logging
from config import settings

logger = logging.getLogger("construction_safety.voice")

class VoiceAlertService:
    _instance = None

    def __init__(self):
        self.speech_queue = queue.Queue(maxsize=10)
        self.is_running = True
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = VoiceAlertService()
        return cls._instance

    def speak(self, text: str, language: str = "en"):
        if not settings.VOICE_ENABLED or not text:
            return
        try:
            # Don't overload the queue if voice messages pile up
            if not self.speech_queue.full():
                self.speech_queue.put_nowait((text, language))
        except queue.Full:
            pass

    def _speech_worker(self):
        """
        Background worker thread running offline TTS engine.
        Ensures camera frame rate and CV inference are not blocked.
        """
        engine = None
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", settings.VOICE_RATE)
            engine.setProperty("volume", settings.VOICE_VOLUME)
        except Exception as e:
            logger.warning(f"Could not initialize offline pyttsx3 engine: {e}. Voice will be simulated.")

        while self.is_running:
            try:
                item = self.speech_queue.get(timeout=1.0)
                if item is None:
                    break
                text, lang = item
                logger.info(f"[VOICE ALERT - {lang.upper()}]: {text}")

                if engine:
                    try:
                        engine.say(text)
                        engine.runAndWait()
                    except Exception as err:
                        logger.error(f"Error executing speech: {err}")
                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Voice worker exception: {e}")

    def shutdown(self):
        self.is_running = False
        try:
            self.speech_queue.put_nowait(None)
        except:
            pass
