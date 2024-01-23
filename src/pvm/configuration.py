"""
Defines the Configuration class for PhiVM, handling the setup of VM parameters.
"""


from src.pvm.errors import ConfigurationError
from src.pvm.types import Word


class Configuration:
    """
    Manages the configuration settings for PhiVM.

    Holds and validates the configuration parameters such as memory size, stack start,
    and stack size for the virtual machine.
    """

    def __init__(self, memory_size: Word, stack_start: Word, stack_size: Word) -> None:
        """
        Initialize the VM configuration.

        Args:
            memory_size (Word): The total size of the VM's memory.
            stack_start (Word): The starting position of the stack in the memory.
            stack_size (Word): The size of the stack.
        """
        self.memory_size = memory_size
        self.stack_start = stack_start
        self.stack_size = stack_size
        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validates the VM configuration.

        Raises:
            ConfigurationError: If any configuration parameter is invalid.
        """
        if self.memory_size <= 0:
            raise ConfigurationError("memory_size must be a positive integer")

        if self.stack_start < 0:
            raise ConfigurationError("stack_start must be a non-negative integer")

        if self.stack_size <= 0:
            raise ConfigurationError("stack_size must be a positive integer")

        if self.stack_start + self.stack_size > self.memory_size:
            raise ConfigurationError("Stack exceeds allocated memory size")
