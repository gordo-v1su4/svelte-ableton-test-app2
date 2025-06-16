# Ableton Live Data Export Script
# Entry point for the control surface

from .DataExportScript import create_instance

# Metadata
__version__ = '1.0.0'
__author__ = 'Your Name'
__description__ = 'Exports comprehensive Ableton Live song data to JSON'

# This makes the create_instance function available to Ableton Live
__all__ = ['create_instance']