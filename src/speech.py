from elevenlabs import ElevenLabs
from core.config import get_settings


class TextToSpeech :
    settings = get_settings()
    client = ElevenLabs(settings.ELEVENLABS_API_KEY)

    @staticmethod
    def text_to_speech(summary_text : str) -> bytes :
        """
        Converts summary text into speech using ElevenLabs
        and returns MP3 bytes.
        """

        audio = TextToSpeech.client.text_to_speech.convert(
            text = summary_text , 
            voice_id = TextToSpeech.settings.ELEVENLABS_VOICE_ID ,
            model_id = "eleven_multilingual_v2" ,
            output_format = "mp3_44100_12" ,
            voice_settings={
                "stability": 0.4,
                "similarity_boost": 0.9,
                "speaking_rate": 0.9,
            }
        )

        audio_bytes = b"".join(audio)
        return audio_bytes

