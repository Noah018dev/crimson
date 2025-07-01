from collections.abc import Callable, Generator
from google import genai
from google.genai import types
from google.genai import chats
from .ai_types import StreamingChunk, Attachment


client = genai.Client()
attachments = []

class UserDenied() :
    def __init__(self) :
        pass

class Chat() :
    def __init__(self, model : str = 'gemini-2.5-flash', functions : list[Callable] = []) :
        self.chat : chats.Chat = client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    include_thoughts=True
                ),
                temperature=1,
                top_p=0.95,
                top_k=64,
                tools=functions
            )
        )
        
        self.model = model
    
    def send_message_stream(self, prompt : str) -> Generator[StreamingChunk, StreamingChunk, StreamingChunk] :
        first_text_append = '\n\n'
        
        for chunk in self.chat.send_message_stream(prompt) :
            if chunk is None :
                continue
            
            for part in chunk.candidates[0].content.parts :
                if not part.text :
                    continue
                elif part.thought :
                    yield StreamingChunk('THINKING', part.text.splitlines()[0])
                else :
                    yield StreamingChunk('RESPONSE', first_text_append + part.text)
                    first_text_append = ''
                
                if attachments :
                    while attachments :
                        yield StreamingChunk('ATTACHMENT', attachments.pop(0))
            
        return StreamingChunk('END', None)

class Tools() :
    def generate_image(prompt : str) -> None :
        '''Generates an image from the prompt, returns None, and nothing else.
        
        prompt : str
        '''
        
        response = client.models.generate_images(
            model='imagen-4.0-generate-preview-06-06',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            )
        )

        response.generated_images[0].image.show()
  
        return None