"""
Defines types used in PhiVM including Word, Program, InstOperands, and Memory.
"""


from numpy import int64

# from src.pvm.instructions import Instruction

Word = int64
InstOperands = list[Word]
# Program = list[(Instruction, InstOperands)]
Memory = list[Word]
