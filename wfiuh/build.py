import os.path

from PyInstaller.__main__ import run as py_installer_run


def run():
    py_installer_run(
        [
            os.path.join(__package__, "main.py"),
            "--onefile",
            "--name",
            "wfiuh",
            "--collect-all",
            __package__,
        ]
    )
