"""
This module defines custom exception classes used by the PhiVM virtual machine.
"""


class StackOverflowError(Exception):
    """Exception raised for stack overflow errors."""


class StackUnderflowError(Exception):
    """Exception raised for popping from an empty stack."""


class ConfigurationError(Exception):
    """Exception raised for invalid VM configuration."""


class InvalidInstructionError(Exception):
    """Exception raised for invalid VM instruction."""
