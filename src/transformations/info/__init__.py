"""
Info panel specific transformations
"""
from .artist import transform_info_artist
from .label import transform_info_label
from .format import transform_info_format
from .notes import transform_info_notes
from .url import transform_info_url
from .tracklist import transform_info_tracklist

__all__ = [
    'transform_info_artist',
    'transform_info_label',
    'transform_info_format',
    'transform_info_notes',
    'transform_info_url',
    'transform_info_tracklist'
]
