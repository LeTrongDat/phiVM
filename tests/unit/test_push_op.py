import unittest

from src.pvm.configuration import Configuration
from src.pvm.instructions import Instruction
from src.pvm.types import Word
from src.pvm.vm import PhiVM


class TestPushOp(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration(
            memory_size=Word(2048), stack_start=Word(1024), stack_size=Word(512)
        )
        self.vm = PhiVM(self.config)

    def test_push_instruction(self) -> None:
        # Create a program with the PUSH instruction
        program = [(Instruction.PUSH, [Word(100)])]

        # Run the program
        self.vm.run(program)

        # Check if the value is correctly pushed onto the stack
        expected_stack_position = self.config.stack_start + 1
        expected_value_at_stack = 100
        self.assertEqual(self.vm.stack_pointer, expected_stack_position)
        self.assertEqual(
            self.vm.memory[self.config.stack_start], expected_value_at_stack
        )


if __name__ == "__main__":
    unittest.main()
