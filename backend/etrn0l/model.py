from typing import List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class FlashLoop():
    tags: List[str]
    id: Optional[str] = None
    number: Optional[int] = None
    source_audio: Optional[str] = None
    source_video: Optional[str] = None
    file_url: Optional[str] = None
