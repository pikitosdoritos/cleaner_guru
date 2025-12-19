from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Photo:
    path: str
    size_bytes: int
    width: Optional[int]
    height: Optional[int]
    sha256: Optional[str] = None
    phash: Optional[str] = None
    timestamp: Optional[datetime] = None