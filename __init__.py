"""
File Mapper Package

A utility for mapping files from source directories to destination directories
with support for copying, moving, and creating symbolic links.
"""

__version__ = "0.1.0"
__author__ = "NDA Team"

from .file_mapper_script import main, process_json_file, parse_data, do_action

__all__ = ["main", "process_json_file", "parse_data", "do_action"]
