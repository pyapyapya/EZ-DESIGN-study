from abc import ABC, abstractmethod


class CPUFactory(ABC):
    @classmethod
    def make_cpu(self, type: str):
        if type == "single":
            return SingleCoreCPU()
        elif type == "dual":
            return DualCoreCPU()
        else:
            raise ValueError("Unknown CPU type")
    
    @abstractmethod
    def process(self, data: list[int]):
        pass


class SingleCoreCPU(CPUFactory):
    def process(self, data: list[int]):
        cpu_processed = data
        return [cpu_processed]


class DualCoreCPU:
    def process(self, data: list[int]):
        cpu_processed = [data[::2], data[1::2]]
        return cpu_processed