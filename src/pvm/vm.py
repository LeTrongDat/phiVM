"""
Implements the PhiVM class for executing a stack-based virtual machine's instructions.
"""

import numpy as np

from src.pvm.configuration import Configuration
from src.pvm.errors import (
    DivisionByZeroError,
    InvalidInstructionError,
    StackOverflowError,
    StackUnderflowError,
)
from src.pvm.instructions import Instruction
from src.pvm.types import InstOperands, Memory, Word


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

        self.sign_flag = 0  # 1 if result is negative
        self.overflow_flag = 0  # 1 if there's an arithmetic overflow

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
        elif instruction == Instruction.ADD:
            self._add()
        elif instruction == Instruction.SUB:
            self._sub()
        elif instruction == Instruction.MUL:
            self._mul()
        elif instruction == Instruction.DIV:
            self._div()
        else:
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

    def _add(self) -> None:
        """
        Executes the ADD instruction which pops the top two elements from the stack,
        adds them together, and pushes the result back onto the stack.

        Raises:
            StackUnderflowError: If there are fewer than two elements on the stack.
            StackOverflowError: If the result cannot be pushed onto the stack because it is full.
        """
        if self.stack_pointer < self.stack_start + 2:
            raise StackUnderflowError("Not enough elements on the stack to perform add")

        # Pop the top two elements and add them
        self.stack_pointer -= 1
        operand2 = self.memory[self.stack_pointer]
        self.stack_pointer -= 1
        operand1 = self.memory[self.stack_pointer]

        # Convert to native Python ints for flag calculations
        result = operand1 + operand2

        # Update flags
        self.sign_flag = 1 if result < 0 else 0
        self.overflow_flag = (
            1
            if (operand1 > 0 and operand2 > 0 > result)
            or (operand1 < 0 and operand2 < 0 < result)
            else 0
        )

        if self.stack_pointer >= self.stack_start + self.stack_size:
            raise StackOverflowError("Stack overflow on add")
        self.memory[self.stack_pointer] = result
        self.stack_pointer += 1

    def _sub(self) -> None:
        """
        Executes the SUB instruction, which subtracts the top stack element from the next top
        element.

        The result is pushed back onto the stack. This method updates the VM flags
        based on the result of the subtraction.

        Raises:
            StackUnderflowError: If there are not enough elements on the stack to perform
            the operation.
            StackOverflowError: If the result cannot be pushed onto the stack because it is full.
        """
        if self.stack_pointer < self.stack_start + 2:
            raise StackUnderflowError(
                "Not enough elements on the stack to perform subtract"
            )

        # Pop the top two elements from the stack
        self.stack_pointer -= 1
        operand2 = self.memory[self.stack_pointer]
        self.stack_pointer -= 1
        operand1 = self.memory[self.stack_pointer]

        # Perform the subtraction
        result = operand1 - operand2

        self.sign_flag = 1 if result < 0 else 0
        self.overflow_flag = (
            1
            if (operand1 < 0 < result and operand2 > 0)
            or (operand1 > 0 > result and operand2 < 0)
            else 0
        )

        if self.stack_pointer >= self.stack_start + self.stack_size:
            raise StackOverflowError("Stack overflow on subtract")
        self.memory[self.stack_pointer] = result
        self.stack_pointer += 1

    def _mul(self) -> None:
        """
        Executes the MUL instruction, which multiplies the top two elements on the stack.

        The result of the multiplication is pushed back onto the stack. This method also
        updates the VM flags based on the result of the multiplication.

        Raises:
            StackUnderflowError: If there are not enough elements on the stack to perform
            the operation.
            StackOverflowError: If the result cannot be pushed onto the stack because it is full.
        """

        if self.stack_pointer < self.stack_start + 2:
            raise StackUnderflowError(
                "Not enough elements on the stack to perform multiply"
            )

        # Pop the top two elements from the stack
        self.stack_pointer -= 1
        operand2 = self.memory[self.stack_pointer]
        self.stack_pointer -= 1
        operand1 = self.memory[self.stack_pointer]

        # Convert operands to Python's native int for overflow checking
        python_int_result = int(operand1) * int(operand2)

        # Check for overflow
        max_int64 = np.iinfo(np.int64).max
        min_int64 = np.iinfo(np.int64).min
        self.overflow_flag = not min_int64 <= python_int_result <= max_int64

        # Perform the multiplication
        result = operand1 * operand2

        # Update VM flags based on the result
        self.sign_flag = 1 if result < 0 else 0

        # Push the result back onto the stack, if space permits
        if self.stack_pointer >= self.stack_start + self.stack_size:
            raise StackOverflowError("Stack overflow on multiply")
        self.memory[self.stack_pointer] = result
        self.stack_pointer += 1

    def _div(self) -> None:
        """
        Executes the DIV instruction, which divides the second top element on the stack
        by the top element.

        The result of the division is pushed back onto the stack. In case of division
        by zero, a DivisionByZeroError is raised. This method also updates the VM
        flags based on the result of the division.

        Raises:
            StackUnderflowError: If there are not enough elements on the stack to perform division.
            DivisionByZeroError: If the division operation attempts to divide by zero.
            StackOverflowError: If the result cannot be pushed onto the stack because it is full.
        """
        if self.stack_pointer < self.stack_start + 2:
            raise StackUnderflowError(
                "Not enough elements on the stack to perform division"
            )

        # Pop the top two elements for division
        self.stack_pointer -= 1
        divisor = self.memory[self.stack_pointer]
        self.stack_pointer -= 1
        dividend = self.memory[self.stack_pointer]

        # Check for division by zero
        if divisor == 0:
            raise DivisionByZeroError("Attempted division by zero")

        # Perform the division
        result = dividend // divisor

        # Update VM flags based on the result (update as needed)
        self.sign_flag = 1 if result < 0 else 0
        self.overflow_flag = 0  # Overflow is not typically an issue in integer division

        # Push the result back onto the stack, if space permits
        if self.stack_pointer >= self.stack_start + self.stack_size:
            raise StackOverflowError("Stack overflow on division")
        self.memory[self.stack_pointer] = result
        self.stack_pointer += 1
