"""
Contains util functions
"""
import os


def get_hostname() -> str:
    return os.getenv('HOSTNAME', 'unknown')
