from crimson.ai.generative import Chat, Tools
from crimson.richtext import console, display_streaming_generator, print
from PIL.Image import Image
from crimson import intro
from rich import panel


chat = Chat(functions=[Tools.generate_image])
running = True

print(intro.display(), use_markdown=False)

while running :
    prompt = console.input('[magenta][bold]>>>[/bold][/magenta] ')
    
    generator = chat.send_message_stream(prompt)
    
    display_streaming_generator(generator)