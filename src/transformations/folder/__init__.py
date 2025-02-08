"""
Folder name specific transformations
"""
from .artist import transform_artist
from .catalog import transform_catalog
from .label import transform_label
from .title import transform_title

__all__ = [
    'transform_artist',
    'transform_catalog',
    'transform_label',
    'transform_title'
]
