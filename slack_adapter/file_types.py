import enum


class FileTypes(enum.Enum):
    Posts = 1,
    Snippets = 2,
    Images = 4,
    Gdocs = 8,
    Zips = 16,
    Pdfs = 32,
    All = 63