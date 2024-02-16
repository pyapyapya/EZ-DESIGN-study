from abc import ABC, abstractmethod

from week1.cpu import CPUFactory
from week1.memory import RamFactory, RomFactory

class Computer:
    def __init__(self):
        self.cpu_process = None
        self.ram = None
        self.rom = None

    def bootstrap(self):
        state = {}
        state["cpu_processed"] = self.cpu_process
        state["ram_data"] = self.ram
        state["rom_data"] = self.rom
        return state

class ComputerBuilder(ABC):
    def __init__(self):
        self.computer = Computer()

    @staticmethod
    def build_computer(type: str) -> Computer:
        if type == "laptop":
            builder: LaptopBuilder = LaptopBuilder()
        elif type == "desktop":
            builder: DesktopBuilder = DesktopBuilder()
        else:
            raise ValueError("Unknown computer type")
        
        builder.set_cpu()
        builder.set_ram()
        builder.set_rom()
        return builder.get_computer()

    @abstractmethod
    def set_cpu(self, type: str):
        pass

    @abstractmethod
    def set_ram(self, size: int):
        pass

    @abstractmethod
    def set_rom(self, data: list[int]):
        pass

    def get_computer(self) -> Computer:
        return self.computer


class LaptopBuilder(ComputerBuilder):    
    def set_cpu(self):
        cpu = CPUFactory.make_cpu(type="single")
        self.computer.cpu_process = cpu.process(data=[1, 2, 3, 4])
    
    def set_ram(self):
        self.computer.ram = RamFactory.make_memory(size=8).ram_data
    
    def set_rom(self):
        self.computer.rom = RomFactory.make_memory(data=[1, 2, 3, 4]).rom_data



class DesktopBuilder(ComputerBuilder):
    def set_cpu(self):
        cpu = CPUFactory.make_cpu(type="dual")
        self.computer.cpu_process = cpu.process(data=[1, 2, 3, 4, 5, 6, 7, 8])
    
    def set_ram(self):
        self.computer.ram = RamFactory.make_memory(size=16).ram_data
    
    def set_rom(self):
        self.computer.rom = RomFactory.make_memory(data=[1, 2, 3, 4, 5, 6, 7, 8]).rom_data
