"""
File Mapper Package

A utility for mapping files from source directories to ''destination'' directories
via symbolic links. Primarily used to re-arrange a dataset into a different structure
without incurring an addtitional storage cost
"""

__version__ = "0.1.0"

# Use absolute imports to avoid pytest issues
try:
    from filemapper import main, process_json_file, parse_data, do_action
except ImportError:
    # Fallback for when running as a module
    from .filemapper import main, process_json_file, parse_data, do_action

__all__ = ["main", "process_json_file", "parse_data", "do_action"]
