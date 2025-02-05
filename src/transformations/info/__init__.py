"""
Info panel specific transformations
"""
from .artist import transform_info_artist
from .label import transform_info_label
from .format import transform_info_format
from .notes import transform_info_notes

__all__ = [
    'transform_info_artist',
    'transform_info_label',
    'transform_info_format',
    'transform_info_notes'
]
