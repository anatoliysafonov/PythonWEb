from abc import ABC, abstractmethod

class BotInterface(ABC):
    @abstractmethod
    def log():
        pass

    @abstractmethod    
    def add():
        pass

    @abstractmethod
    def save():
        pass

    @abstractmethod
    def load():
        pass

    @abstractmethod
    def search():
        pass

    @abstractmethod
    def edit():
        pass

    @abstractmethod
    def remove():
        pass

    @abstractmethod
    def congratulate():
        pass

    @abstractmethod
    def hello():
        pass

