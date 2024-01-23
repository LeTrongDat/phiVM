import unittest

from src.pvm.configuration import Configuration
from src.pvm.errors import DivisionByZeroError
from src.pvm.instructions import Instruction
from src.pvm.types import Word
from src.pvm.vm import PhiVM


class TestDivOperation(unittest.TestCase):
    def setUp(self) -> None:
        self.config = Configuration(
            memory_size=Word(2048), stack_start=Word(1024), stack_size=Word(512)
        )

    def test_div_basic(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(20)]),
            (Instruction.PUSH, [Word(5)]),
            (Instruction.DIV, []),
        ]
        vm.run(program)
        result = vm.memory[vm.stack_pointer - 1]
        self.assertEqual(result, Word(4))  # Expect 20 / 5 = 4

    def test_div_by_zero(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(5)]),
            (Instruction.PUSH, [Word(0)]),
            (Instruction.DIV, []),
        ]
        with self.assertRaises(DivisionByZeroError):
            vm.run(program)

    def test_div_sign_flag_positive_dividend_negative_divisor(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(10)]),
            (Instruction.PUSH, [Word(-2)]),
            (Instruction.DIV, []),
        ]
        vm.run(program)
        self.assertTrue(
            vm.sign_flag,
            "Sign flag should be set for positive dividend and negative divisor",
        )

    def test_div_sign_flag_negative_dividend_positive_divisor(self) -> None:
        vm = PhiVM(self.config)
        program = [
            (Instruction.PUSH, [Word(-10)]),
            (Instruction.PUSH, [Word(2)]),
            (Instruction.DIV, []),
        ]
        vm.run(program)
        self.assertTrue(
            vm.sign_flag,
            "Sign flag should be set for negative dividend and positive divisor",
        )


if __name__ == "__main__":
    unittest.main()
