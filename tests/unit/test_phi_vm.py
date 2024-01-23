import unittest
from src.pvm.vm import PhiVM
from src.pvm.configuration import Configuration
from src.pvm.instructions import Instruction
from src.pvm.types import Word


class TestPhiVM(unittest.TestCase):
    def test_push_instruction(self) -> None:
        # Create a VM configuration
        config = Configuration(
            memory_size=Word(2048), stack_start=Word(1024), stack_size=Word(512)
        )

        # Initialize the VM with the configuration
        vm = PhiVM(config)

        # Execute the PUSH instruction
        vm.execute_instruction(
            Instruction.PUSH,
            [Word(100)],
        )

        # Check if the value is correctly pushed onto the stack
        expected_stack_position = config.stack_start + 1
        expected_value_at_stack = 100
        self.assertEqual(vm.stack_pointer, expected_stack_position)
        self.assertEqual(vm.memory[config.stack_start], expected_value_at_stack)


if __name__ == "__main__":
    unittest.main()
