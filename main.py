from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occurred character is handled by current state
        """
        pass

    def check_next(self, next_char: str) -> State | Exception:
        for state in getattr(self, 'next_states', []):
            if state.check_self(next_char):
                return state
        raise NotImplementedError("rejected string")

class StartState(State):
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char: str) -> bool:
        return False

class TerminationState(State):
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char: str) -> bool:
        return False

class DotState(State):
    """
    state for . character (any character accepted)
    """
    next_states: list[State] = []

    def __init__(self):
        super().__init__()

    def check_self(self, char: str) -> bool:
        return True

class AsciiState(State):
    """
    state for alphabet letters or numbers
    """
    next_states: list[State] = []

    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.curr_sym = symbol

    def check_self(self, curr_char: str) -> bool:
        return curr_char == self.curr_sym

class StarState(State):
    next_states: list[State] = []

    def __init__(self, checking_state: State):
        super().__init__()
        self.state = checking_state

    def check_self(self, char: str) -> bool:
        return self.state.check_self(char)

class PlusState(State):
    next_states: list[State] = []

    def __init__(self, checking_state: State):
        super().__init__()
        self.state = checking_state

    def check_self(self, char: str) -> bool:
        return self.state.check_self(char)

class RegexFSM:
    curr_state: State = StartState()

    def __init__(self, regex_expr: str) -> None:
        self.pattern: list[State] = []
        for token in regex_expr:
            new_state = self.__init_next_state(token)
            self.pattern.append(new_state)

    def __init_next_state(
        self, next_token: str
    ) -> State:
        if next_token == ".":
            return DotState()
        if next_token == "*":
            if not self.pattern:
                raise AttributeError("it is not possible!")
            prev = self.pattern.pop()
            return StarState(prev)
        if next_token == "+":
            if not self.pattern:
                raise AttributeError("it is not possible!")
            prev = self.pattern.pop()
            return PlusState(prev)
        if next_token.isascii():
            return AsciiState(next_token)
        raise AttributeError("char is not supported")

    def check_string(self, s: str) -> bool:
        def match(i: int, j: int) -> bool:
            if i == len(self.pattern):
                return j == len(s)
            state = self.pattern[i]
            if isinstance(state, StarState):
                if match(i + 1, j):
                    return True
                if j < len(s) and state.check_self(s[j]):
                    return match(i, j + 1)
                return False
            if isinstance(state, PlusState):
                if j < len(s) and state.check_self(s[j]):
                    return match(i + 1, j + 1) or match(i, j + 1)
                return False
            if j < len(s) and state.check_self(s[j]):
                return match(i + 1, j + 1)
            return False
        return match(0, 0)

if __name__ == "__main__":
    regex_pattern = "a*4.+hi"
    regex_compiled = RegexFSM(regex_pattern)
    print(regex_compiled.check_string("aaaaaa4uhi"))  # True
    print(regex_compiled.check_string("4uhi"))       # True
    print(regex_compiled.check_string("meow"))       # False
