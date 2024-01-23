"""
Implements the PhiVM class for executing a stack-based virtual machine's instructions.
"""


from src.pvm.configuration import Configuration
from src.pvm.errors import InvalidInstructionError, StackOverflowError
from src.pvm.types import InstOperands, Memory, Word
from src.pvm.instructions import Instruction


class PhiVM:
    """
    Represents a stack-based virtual machine.

    Manages the execution of instructions and maintains the state of the VM,
    including memory and stack.
    """

    def __init__(self, config: Configuration) -> None:
        """
        Initializes the PhiVM with the given configuration.

        Args:
            config (Configuration): The configuration settings for the VM.
        """
        self.memory: Memory = [Word(0)] * config.memory_size
        self.stack_pointer: Word = config.stack_start
        self.stack_start: Word = config.stack_start
        self.stack_size: Word = config.stack_size

    def execute_instruction(
        self, instruction: Instruction, operands: InstOperands
    ) -> None:
        """
        Executes a single instruction with the given operands.

        Args:
            instruction (Instruction): The instruction to execute.
            operands (InstOperands): The operands for the instruction.

        Raises:
            InvalidInstructionError: If the instruction is not supported.
        """
        if instruction == Instruction.PUSH:
            self._push(operands)
            return
        raise InvalidInstructionError("Instruction not supported")

    def run(self, program: list) -> None:
        """
        Runs a sequence of instructions (a program).

        Args:
            program (Program): The program to run, as a list of instructions and operands.
        """
        for instruction, operands in program:
            self.execute_instruction(instruction, operands)

    def _push(self, operands: InstOperands) -> None:
        """
        Pushes a value onto the stack.

        Args:
            operands (InstOperands): The operands for the push instruction; expects one operand.

        Raises:
            StackOverflowError: If pushing the value would exceed the stack size.
        """
        if self.stack_pointer >= self.stack_start + self.stack_size:
            raise StackOverflowError("Stack overflow")
        self.memory[self.stack_pointer] = operands[0]
        self.stack_pointer += 1
