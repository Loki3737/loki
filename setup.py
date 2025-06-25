# setup.py per cx_Freeze

from cx_Freeze import setup, Executable

# Path to your script
script = "CopyTrack.py"

# Icon path
icon_path = "C:\\Users\\melaa\\Desktop\\icon.ico"

build_exe_options = {
    "packages": ["pyperclip", "time", "datetime", "re", "winreg", "os", "sys"],
    "include_files": [],  # se hai file extra da includere
}

exe = Executable(
    script=script,
    base="Console",   # Console perché hai output su terminale
    icon=icon_path,
    target_name="CopyTrack.exe"
)

setup(
    name="CopyTrack",
    version="1.5",
    description="Clipboard tracker",
    options={"build_exe": build_exe_options},
    executables=[exe]
)