#=============================================================
# File: setup.py
# Description: Python setup script to package the library and handle C bindings.
# Note: For a true cross-language binding (C -> Python), we typically use pybind11
# or set up ctypes bindings after the core C library is compiled via CMake.
# This file serves as the primary entry point for installation/compilation setup.
#=============================================================

from setuptools import setup, find_packages
from subprocess import CalledProcessError, PIPE, STDOUT

# Define required dependencies (e.g., pybind11, torch)
install_requires=[
    'numpy>=1.20',
    # 'torch' # Placeholder for actual ML/Tensor library
]

setup(
    name='chess-ai-platform',
    version='0.1.0',
    packages=find_packages(),
    package_dir={"": "chess_engine"}, # Assuming modules are in chess_engine
    install_requires=install_requires,
    # We use a minimal build step here; the complex C binding (like pybind11)
    # should be managed by invoking CMake explicitly before 'python setup.py install'.
    cmdclass={
        'build_bindings': build_c_binding_script
    }
)

def build_c_binding_script(build_py, epoch, run_command):
    """Custom command class to force running cmake/compilation before package installation."""
    print("\n--- Running Cross-Language Binding Build ---")
    print("Attempting to compile 'chesscore' C library using CMake...")

    # Check if the build directory exists and clean up old artifacts (optional)
    try:
        import os
        if os.path.exists("./build"):
             os.system("rm -rf ./build") # Unix command, needs adaptation for Windows or use subprocess
        os.makedirs("./build", exist_ok=True)
        print("Cleaned build directory.")

        # 1. Configure CMake (Assumes cmake is in PATH)
        cmake_cmd = ["cmake", "..", f"-DCMAKE_BUILD_TYPE=Debug"]
        print(f"-> Executing: {' '.join(cmake_cmd)}")
        subprocess.run(cmake_cmd, check=True, capture_output=PIPE, text=True)

        # 2. Build the core engine library
        build_cmd = ["make", "all"]
        print(f"-> Executing: {' '.join(build_cmd)}")
        subprocess.run(build_cmd, check=True, capture_output=PIPE, text=True)

        print("===============================================")
        print("SUCCESS: Core C Library ('libchesscore') compiled successfully.")
    except CalledProcessError as e:
        raise RuntimeError(f"CMAKE BUILD FAILED:\n{e.stdout}\n{e.stderr}") from e
    except FileNotFoundError:
         # Handle case where cmake or make is not installed on the system PATH
         print("WARNING: CMake or Make command not found. Cannot fully build C bindings.")

    return build_py(build_py, epoch, run_command)

