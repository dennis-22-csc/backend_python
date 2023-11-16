"""Instantiates a storage object.
Instantiates a file storage engine (FileStorage).
"""

from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()
