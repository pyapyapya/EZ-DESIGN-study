from abc import ABC, abstractmethod

class Memory(ABC):
    @abstractmethod
    def make_memory(self, data: list[int]|None = None, size: int|None = None):
        pass

    def read(self, address: int):
        pass

    def write(self, address: int, value: int):
        pass


class RamFactory(Memory):
    def __init__(self, size: int):
        self.size = size
        self.ram_data = [0] * size

    @classmethod
    def make_memory(cls, data: list[int]|None = None, size: int|None = None):
        if data is not None:
            raise ValueError("RAM data must not given when creating RAM")
        if isinstance(size, int):
            return cls(size)

    def read(self, address: int):
        return self.ram_data[address]

    def write(self, address: int, value: int):
        self.ram_data[address] = value


class RomFactory(Memory):
    def __init__(self, data: list[int]):
        self.rom_data = data
        self.size = len(data)

    @classmethod
    def make_memory(cls, data: list[int]|None = None, size: int|None = None):
        if size is not None:
            raise ValueError("ROM size must be given when creating ROM")
        if isinstance(data, list):
            return cls(data)

    def read(self, address: int):
        return self.rom_data[address]

    def write(self, address: int, value: int):
        raise ValueError("ROM cannot be written to directly")
