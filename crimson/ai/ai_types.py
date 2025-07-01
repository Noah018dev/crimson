from dataclasses import dataclass
from typing import Literal, Optional


type StreamingChunkType = Literal['THINKING', 'RESPONSE', 'END', 'ATTACHMENT']
type AttachmentType = Literal['IMAGE']

@dataclass
class StreamingChunk() :
    chunk_type : StreamingChunkType
    content : 'Optional[str | Attachment]'
    
@dataclass
class Attachment() :
    attachment_type : AttachmentType
    data : object