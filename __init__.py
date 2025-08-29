"""
File Mapper Package
"""

# Use absolute imports to avoid pytest issues
try:
    from filemapper import main, process_json_file, parse_data, do_action
except ImportError:
    # Fallback for when running as a module
    from .filemapper import main, process_json_file, parse_data, do_action

__all__ = ["main", "process_json_file", "parse_data", "do_action"]
