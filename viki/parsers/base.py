from abc import ABC, abstractmethod

class BaseIntentParser(ABC):
    """Абстрактный класс для всех будущих парсеров (Anthropic, OpenAI, Llama)."""
    @abstractmethod
    def parse(self, raw_input: str) -> dict:
        pass
