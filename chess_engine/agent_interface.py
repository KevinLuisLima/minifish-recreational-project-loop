#=============================================================
# File: chess_engine/agent_interface.py
# Description: Abstract Base Class (Template Method Pattern) for all AI Agents.
# Dependencies: Requires definitions from compiled C structures (BoardState, Move, MoveStatus).
#=============================================================

from abc import ABC, abstractmethod
# We assume bindings are now available and correctly mapped from the updated chess_engine/chess.c
# from .api_c_layer import BoardState # Placeholder: Actual binding will be here
from typing import TYPE_CHECKING # Use this for type hinting complex C structures

if TYPE_CHECKING:
    # These types must match the definition in chess_engine/chess.c
    class MoveStatus:
        SUCCESS: int = 0
        ILLEGAL_STATE: int = 1
        RULE_VIOLATION: int = 2
        CHECK_FAILURE: int = 3
        NO_MOVES_FOR_TURN: int = 4

    class BoardState:
        player_color: str # e.g., "WHITE", "BLACK"
        turn_count: int
        last_move: 'Move'
        is_checkmate: bool
        is_stalemate: bool
        # ... other state fields ...

    class Move:
        start_sq: str # e.g., "a1"
        end_sq: str   # e.g., "b2"
        is_capture: bool
        promotion_type: int

else:
    # Mock implementation for non-type checking environments
    class MoveStatus:
        SUCCESS = 0
        ILLEGAL_STATE = 1
        RULE_VIOLATION = 2
        CHECK_FAILURE = 3
        NO_MOVES_FOR_TURN = 4

    class BoardState:
        def __init__(self):
            pass

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
        The core decision method (Template Method).
        Takes a BoardState object/structure and returns an optimal Move object.
        Concrete agents override this to implement their specific strategy.
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
        # Re-using the mock constructor based on new definitions
        print("Dummy Agent: Returning hardcoded dummy move a1->b2.")
        return Move(start_sq="a1", end_sq="b2")

# Note: We must ensure that 'Move', 'BoardState' classes/structs are properly exposed
# or bound correctly before the full system can compile.
