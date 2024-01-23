import unittest

import numpy as np

from src.pvm.configuration import Configuration
from src.pvm.instructions import Instruction
from src.pvm.types import Word
from src.pvm.vm import PhiVM


class TestMulOperation(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration(
            memory_size=Word(2048), stack_start=Word(1024), stack_size=Word(512)
        )

    def test_mul_basic(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(6)]),
            (Instruction.PUSH, [Word(7)]),
            (Instruction.MUL, []),
        ]
        vm.run(program)
        result = vm.memory[vm.stack_pointer - 1]
        self.assertEqual(result, Word(42))  # Expect 6 * 7 = 42

    def test_mul_overflow(self) -> None:
        vm = PhiVM(self.config)
        large_number = np.iinfo(np.int64).max // 2
        program = [
            (Instruction.PUSH, [Word(large_number)]),
            (Instruction.PUSH, [Word(3)]),
            (Instruction.MUL, []),
        ]
        vm.run(program)
        self.assertTrue(
            vm.overflow_flag, "Overflow flag should be set for overflow result"
        )

    def test_mul_sign_flag(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(-3)]),
            (Instruction.PUSH, [Word(4)]),
            (Instruction.MUL, []),
        ]
        vm.run(program)
        result = vm.memory[vm.stack_pointer - 1]
        self.assertEqual(result, Word(-12))  # Expect -3 * 4 = -12
        self.assertTrue(vm.sign_flag, "Sign flag should be set for negative result")


if __name__ == "__main__":
    unittest.main()
