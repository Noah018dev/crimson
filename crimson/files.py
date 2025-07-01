from typing import Literal
from .ai.generative import client
from io import BytesIO
from google.genai.types import File
import httpx


type UploadSource = Literal['FILE', 'URI', 'RAW']

def upload_from_file(file : str | bytes, source : UploadSource = 'FILE') -> File :
    match source :
        case 'FILE' :
            return client.files.upload(file=file)
        case 'RAW' :
            return client.files.upload(file=BytesIO(source))
        case 'URI' :
            return upload_from_file(httpx.get(file).content, 'RAW')