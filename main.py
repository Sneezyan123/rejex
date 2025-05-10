from __future__ import annotations
from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def check_self(self, char: str) -> bool:
        pass

class StartState(State):
    next_states: list[State]

    def __init__(self):
        self.next_states = []

    def check_self(self, char: str) -> bool:
        return False

class TerminationState(State):
    def __init__(self):
        pass

    def check_self(self, char: str) -> bool:
        return False

class DotState(State):
    def __init__(self):
        pass

    def check_self(self, char: str) -> bool:
        return True

class AsciiState(State):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def check_self(self, curr_char: str) -> bool:
        return curr_char == self.symbol

class StarState(State):
    def __init__(self, checking_state: State) -> None:
        self.inner = checking_state

    def check_self(self, char: str) -> bool:
        return self.inner.check_self(char)

class PlusState(State):
    def __init__(self, checking_state: State) -> None:
        self.inner = checking_state

    def check_self(self, char: str) -> bool:
        return self.inner.check_self(char)

class RegexFSM:
    def __init__(self, regex_expr: str) -> None:
        self.pattern: list[State] = []
        for token in regex_expr:
            if token == '*':
                if not self.pattern:
                    raise AttributeError()
                prev = self.pattern.pop()
                self.pattern.append(StarState(prev))
            elif token == '+':
                if not self.pattern:
                    raise AttributeError()
                prev = self.pattern.pop()
                self.pattern.append(PlusState(prev))
            elif token == '.':
                self.pattern.append(DotState())
            else:
                self.pattern.append(AsciiState(token))

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
                    return (match(i + 1, j + 1) or match(i, j + 1))
                return False
            if j < len(s) and state.check_self(s[j]):
                return match(i + 1, j + 1)
            return False
        return match(0, 0)

