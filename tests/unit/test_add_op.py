import unittest
import numpy as np
from src.pvm.vm import PhiVM
from src.pvm.configuration import Configuration
from src.pvm.instructions import Instruction
from src.pvm.types import Word


class TestAddOperation(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration(
            memory_size=Word(2048), stack_start=Word(1024), stack_size=Word(512)
        )

    def test_add_basic(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(5)]),
            (Instruction.PUSH, [Word(10)]),
            (Instruction.ADD, []),
        ]
        vm.run(program)
        result = vm.memory[vm.stack_pointer - 1]
        self.assertEqual(result, Word(15))

    def test_add_overflow(self) -> None:
        vm = PhiVM(self.config)
        max_int64 = np.iinfo(np.int64).max
        program = [
            (Instruction.PUSH, [Word(max_int64)]),
            (Instruction.PUSH, [Word(1)]),
            (Instruction.ADD, []),
        ]
        vm.run(program)
        # Check the overflow flag
        self.assertTrue(vm.overflow_flag, "Overflow flag should be set")

    def test_add_sign_flag(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(-5)]),
            (Instruction.PUSH, [Word(-10)]),
            (Instruction.ADD, []),
        ]
        vm.run(program)
        # Check the sign flag
        self.assertTrue(vm.sign_flag, "Sign flag should be set")


if __name__ == "__main__":
    unittest.main()
