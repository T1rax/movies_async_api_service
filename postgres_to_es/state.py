import abc
import json
from typing import Any


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: str | None):
        self.file_path = file_path
                    
    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {}
        return data or {}

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as outfile:
            json.dump(state, outfile)


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        self.storage.save_state(state={key: value})

    def get_state(self, key: str) -> Any:
        return self.storage.retrieve_state().get(key)
