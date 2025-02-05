"""
Info panel specific transformations
"""
from .artist import transform_info_artist
from .format import transform_info_format
from .notes import transform_info_notes_label

__all__ = [
    'transform_info_artist',
    'transform_info_format',
    'transform_info_notes_label'
]
