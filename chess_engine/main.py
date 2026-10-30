//=============================================================
// File: chess_engine/main.py
// Description: The main entry point and orchestrator of the entire loop.
// Dependencies: Depends on classes in agent_interface.py and functions in api_c_layer.h (via bindings).
//=============================================================

import sys
# Assuming chess_engine is installed or accessible in PYTHONPATH
from .agent_interface import DummyAgent, MoveStatus # Import our updated MoveStatus enum/class

# --- SIMULATED BINDINGS LAYER ---
# In a real scenario, this would involve ctypes or pybind11 declarations
# linking directly to functions compiled from chess.c.

def run_c_apply_move(current_state: 'BoardState', move: 'Move', next_state: 'BoardState') -> bool:
    """
    Simulates calling the compiled C function apply_move from chess_engine/chess.c.
    This is the critical binding layer.
    """
    print("\n[PYTHON] Calling bound C function: apply_move()...")

    # Simulate passing structures to C (assuming correct memory layout matching C)
    // bool success = apply_move(current_state, move, &next_state);

    # For now, we mock the expected behavior based on our successful rewrite of chess.c
    if MoveStatus.SUCCESS > 0: # If success status is non-zero in C (as per placeholder)
        print("[PYTHON] Binding Success: C engine processed move and returned true.")
        return True
    else:
        print(f"[PYTHON] Binding Failure: C engine failed to process the move. Status code received: {MoveStatus.ILLEGAL_STATE}")
        return False

# --- Main Orchestration Logic ---

def run_simulation(agents, num_turns=1):
    """
    Runs the full simulation loop (The Mission Loop).
    Orchestrates interaction between agents and the C game engine.
    """
    print("=============================================================")
    print("STARTING CHESS AI SIMULATION LOOP (FIDE Rules Integrated)")
    print("=============================================================")

    # 1. Initialize Agents
    initialized_agents = {}
    for agent in agents:
        agent.initialize() # Calls the AgentInterface method
        initialized_agents[type(agent).__name__] = agent

    print("\n--- Simulation Ready ---")

    # Dummy Board State Initialization for MVP Test - MUST BE UPDATED TO USE ACTUAL CLASSES
    current_state = {"pieces": "Initial setup", "turn": 1} # Use actual BoardState class instance here
    next_state = {"pieces": "", "turn": 0}

    for turn in range(num_turns):
        print(f"\n--- Turn {turn + 1}/{num_turns}: Determining Moves ---")

        # Agent A decides the move based on current state
        agent_a = initialized_agents['DummyAgent'] # Replace with real Agent A class
        try:
            move_a: 'Move' = agent_a.get_move(current_state)
            print(f"Move determined by {agent_a.name}: {move_a.start_sq} -> {move_a.end_sq}")

            # 2. Execute Move via C Layer (Core Game Engine interaction)
            success = run_c_apply_move(current_state, &move_a, next_state)

            if not success:
                print("CRITICAL ERROR: C Engine failed to apply move or validation failed. Simulation halted.")
                return False # Critical failure path

            # Update state for the next turn/agent
            current_state = next_state
        except Exception as e:
            print(f"CRITICAL FAILURE DURING LOOP ITERATION {turn+1}: {e}")
            return False # Critical failure path

    return True


def main():
    """Main entry point function."""
    agent_a = DummyAgent("AlphaZero")
    agent_b = DummyAgent("BulletPolicy")

    # We run for 1 turn to test the full cycle: Get Move -> Apply Move
    run_simulation([agent_a, agent_b], num_turns=1)
    print("\n--- Simulation Cycle Complete ---")


if __name__ == "__main__":
    # Attempt to run the main orchestrator function.
    main()
