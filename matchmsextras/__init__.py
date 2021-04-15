import logging
from .__version__ import __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Netherlands eScience Center"
__email__ = 'f.huber@esciencecenter.nl'
__all__ = [
    "__version__"
]