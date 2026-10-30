#=============================================================
# File: README.md
# Description: Project overview and build instructions.
#=============================================================

## ♟️ Chess AI Agent Platform (TCC Project)

### 🎯 Goal
To create a robust, modular platform for comparing multiple specialized AI chess agents by managing their complex interactions across different technology stacks (C core logic and Python ML orchestration).

### 🧱 Architecture Overview
The system adheres to the **Template Method** design pattern, separating concerns into:
1.  **Core Game Logic (C):** The single source of truth for move validation and state transitions (`chess_engine/chess.c`). This part is platform-independent (FIDE rules).
2.  **Orchestration & ML (Python):** Manages the overall loop, loads weights via API (`chess_engine/agent_interface.py`), calls the C core functions, and aggregates performance metrics (`chess_engine/main.py`).

### ⚙️ Build System Setup (Required!)
This project requires a cross-language build process managed by CMake and Python's setuptools.

**Dependencies:**
1.  `cmake`: For configuring the build system.
2.  `make`: To compile the compiled artifacts.
3.  Python: With necessary libraries (numpy, etc.).

**Execution Steps:**

1.  **Setup Build Directory:** Navigate to the `build_system/` folder.
    ```bash
    cd build_system
    mkdir build
    cd build
    ```
2.  **Configure CMake:** Run CMake against the root directory to detect headers and sources.
    ```bash
    cmake .. -DCMAKE_BUILD_TYPE=Debug 
    # Note: The '..' points back to the folder containing chess_engine/ and setup.py
    ```
3.  **Compile Core Engine (C):** Compile the C source files into a reusable library.
    ```bash
    make all
    ```

### 🧪 Running the System (MVP Test)
After successful compilation, you can set up Python bindings and run the simulation:

1.  **Install Packages:** Install project dependencies using the setup file. This step will trigger the custom `build_c_binding_script` defined in `setup.py`.
    ```bash
    # Run this command from the root directory of the project
    pip install -e . 
    ```
2.  **Execute Simulation:** Once installed, run the main orchestrator script:
    ```bash
    python chess_engine/main.py
    ```

### 📝 Next Steps / Focus Areas
1.  Implement full FIDE rules within `chess_engine/chess.c`.
2.  Refine `AgentInterface` to correctly wrap the compiled C functions for Python access.
3.  Develop the detailed testing suite in `src/test/`.