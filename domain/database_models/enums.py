from enum import Enum

class Source(Enum):
    WEB = "web"
    TG = "tg"
    FB = "fb"


class SearchStatus(Enum):
    NEW = "new"
    PARSING = "parsing"
    PARSED = "parsed"

class AnalizeStatus(Enum):
    UNANALIZED = "unanalized"
    ANALIZED = "analized"
    FAILED = "failed"

