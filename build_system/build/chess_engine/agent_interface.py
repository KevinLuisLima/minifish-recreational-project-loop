#=============================================================
# File: chess_engine/agent_interface.py
# Description: Abstract Base Class (Template Method Pattern) for all AI Agents.
# Dependencies: Must now rely on the canonical MoveStatus and BoardState definitions from api_c_layer.h via Python bindings.
#=============================================================

from abc import ABC, abstractmethod
# NOTE: Actual python type imports will happen when pybind11/ctypes bindings are available.
# We mock the types here to ensure Python code compiles against the known contract.
class MockMoveStatus:
    SUCCESS = 0
    ILLEGAL_STATE = 1
    RULE_VIOLATION = 2
    CHECK_FAILURE = 3
    NO_MOVES_FOR_TURN = 4

# Using simplified definitions for compilation success in this step
class BoardState:
    def __init__(self): pass

class Move:
    def __init__(self, start_sq: str, end_sq: str, is_capture: bool=False, promotion_type: int=0):
        self.start_sq = start_sq
        self.end_sq = end_sq
        self.is_capture = is_capture
        self.promotion_type = promotion_type

class AgentInterface(ABC):
    """
    Abstract Base Class defining the template method for an AI agent's decision cycle.
    All concrete agents must inherit from this class.
    """
    def __init__(self, name: str):
        self.name = name
        print(f"Initialized Agent: {self.name}")

    @abstractmethod
    def initialize(self):
        """Initializes the agent's model weights and local state."""
        pass

    @abstractmethod
    def get_move(self, board_state: BoardState) -> Move:
        """
        The core decision method (Template Method). Returns an optimal move based on calculation.
        """
        raise NotImplementedError("Subclass must implement abstract method 'get_move'.")

    def get_evaluation(self, board_state: BoardState) -> float:
        """Utility method for evaluating the current state beyond just predicting a move."""
        return 0.0

    @staticmethod
    def load_weights(hf_dataset_api):
        """Handles model weight retrieval from HuggingFace API wrapper."""
        print(f"[{AgentInterface.__name__}] Connecting to HF API and loading weights...")
        return f"MODEL_WEIGHTS_FOR_{'ABC'}"

class DummyAgent(AgentInterface):
    """A simple placeholder agent for MVP testing purposes."""
    def initialize(self):
        pass

    def get_move(self, board_state: BoardState) -> Move:
        print("Dummy Agent: Returning hardcoded dummy move a1->b2.")
        return Move(start_sq="a1", end_sq="b2")
