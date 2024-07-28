import sys
from cx_Freeze import setup, Executable

sys.setrecursionlimit(1500)

build_exe_options = {
    "packages": ["pygame", "cv2", "mediapipe"],
    "include_files": ["Chico.jpg", "egg.jpg", "golden_egg.jpg", "bomb.png", "forest.jpg"],
}

setup(
    name="Catch the Eggs",
    version="0.1",
    description="Catch the Eggs Game",
    options={"build_exe": build_exe_options},
    executables=[Executable("my_script.py")]
)
