from pymupdf import pymupdf
from enum import Enum

class DocState(str,Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    PARTIALLY_INDEXED = "PARTIALLY_INDEXED"
    INDEXED = "INDEXED"
    FAILED = "FAILED"
    