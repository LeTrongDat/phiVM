"""
Defines the Instruction enum for PhiVM. It enumerates all possible PhiVM instructions.
"""

from enum import Enum


class Instruction(Enum):
    """
    Enumerates PhiVM instructions. Extendable for additional VM instructions.
    """

    PUSH = "PUSH"
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    # Additional instructions can be added here as needed
