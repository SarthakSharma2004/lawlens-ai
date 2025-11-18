from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import get_settings


class TextToSpeech :
    settings = get_settings()

    client = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash-preview-tts" , 
        google_api_key = settings.GOOGLE_API_KEY
    )

    @staticmethod
    def text_to_speech(summary_text : str , language : str = "en") -> bytes :
        """
        Converts summary text into speech using Google Gemini TTS
        and returns audio bytes in WAV format.
        """

        try :
            response = TextToSpeech.client.invoke(
                f"say this in a clear and professional voice in {language} : {summary_text}" , 
                generation_config = {"response_modalities": ["AUDIO"]}
            )

            if "audio" in response.additional_kwargs :
                audio_bytes = response.additional_kwargs['audio']
                return audio_bytes
            
            else :
                raise ValueError("Audio not found in response")
            
        except Exception as e :
            raise RuntimeError(f"Error converting text to speech: {e}")



