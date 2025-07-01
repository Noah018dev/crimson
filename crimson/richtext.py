from collections.abc import Generator
from rich.live import Live
from rich.spinner import Spinner
from shutil import get_terminal_size
from PIL.Image import Image
import climage
import rich
import rich.console
import rich.markdown
import builtins

from .ai.ai_types import StreamingChunk


console = rich.console.Console()

def print(text : str, use_markdown : bool = True) -> None :
    if use_markdown :
        console.print(markdown(text))
    else :
        console.print(text)
        
def markdown(text : str) -> rich.markdown.Markdown :
    return rich.markdown.Markdown(text)

def display_streaming_generator(generator : Generator[StreamingChunk, StreamingChunk, StreamingChunk]) -> str :
    all_text = ''
    spinner = Spinner('dots10', 'Processing...')
    
    initial_live_content = rich.console.Group(
        markdown(all_text),
        spinner
    )
    
    with Live(initial_live_content, console=console, refresh_per_second=30, transient=False) as live :
        for chunk in generator :
            match chunk.chunk_type :
                case 'END' :
                    break
                case 'THINKING' :
                    spinner.text = markdown(f'{chunk.content}...')
                    
                    live.update(rich.console.Group(
                        markdown(all_text),
                        spinner
                    ))
                case 'RESPONSE' :
                    all_text += chunk.content
                    spinner.text = 'Generating...'
                    
                    live.update(rich.console.Group(
                        markdown(all_text),
                        spinner
                    ))
                case 'ATTACHMENT' :
                    ... 
        
        live.update(markdown(all_text))
    
    return all_text