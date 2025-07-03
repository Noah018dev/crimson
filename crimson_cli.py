from crimson.ai.generative import Chat, Tools
from crimson.richtext import console, display_streaming_generator, print
from crimson.data import crimson_default_instructions
from crimson import intro


chat = Chat(functions=[Tools.generate_image], instructions=crimson_default_instructions)
running = True

print(intro.display(), use_markdown=False)

while running :
    prompt = console.input('[magenta][bold]>>>[/bold][/magenta] ')
    
    generator = chat.send_message_stream(prompt)
    
    display_streaming_generator(generator)