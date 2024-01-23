import unittest
import numpy as np
from src.pvm.vm import PhiVM
from src.pvm.configuration import Configuration
from src.pvm.instructions import Instruction
from src.pvm.types import Word


class TestSubOperation(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration(
            memory_size=Word(2048), stack_start=Word(1024), stack_size=Word(512)
        )

    def test_sub_basic(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(10)]),
            (Instruction.PUSH, [Word(5)]),
            (Instruction.SUB, []),
        ]
        vm.run(program)
        result = vm.memory[vm.stack_pointer - 1]
        self.assertEqual(result, Word(5))  # Expect 10 - 5 = 5

    def test_sub_negative_result(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(5)]),
            (Instruction.PUSH, [Word(10)]),
            (Instruction.SUB, []),
        ]
        vm.run(program)
        result = vm.memory[vm.stack_pointer - 1]
        self.assertEqual(result, Word(-5))  # Expect 5 - 10 = -5

    def test_sub_sign_flag(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(5)]),
            (Instruction.PUSH, [Word(10)]),
            (Instruction.SUB, []),
        ]
        vm.run(program)
        self.assertTrue(vm.sign_flag, "Sign flag should be set for negative result")

    def test_sub_overflow_flag(self) -> None:
        vm = PhiVM(self.config)
        min_int64 = np.iinfo(np.int64).min
        program = [
            (Instruction.PUSH, [Word(min_int64)]),
            (Instruction.PUSH, [Word(1)]),
            (Instruction.SUB, []),
        ]
        vm.run(program)
        self.assertTrue(
            vm.overflow_flag, "Overflow flag should be set for overflow result"
        )


if __name__ == "__main__":
    unittest.main()
