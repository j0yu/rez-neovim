# -*- coding: utf-8 -*-
import inspect
import os

# Force calculate current file path from source file of dummy function
__file__ = os.path.abspath(inspect.getsourcefile(lambda: None))
__dir__ = os.path.dirname(__file__)

name = "neovim"

# Vendor packages: <vendor_version>+local.<our_version>
__version__ = "0.4.3"
version = __version__ + "+local.1.0.0"

description = "Vim-fork focused on extensibility and usability."

authors = ["Joseph Yu"]

variants = [
    ["platform-linux", "arch-x86_64"],
    ["platform-osx", "arch-x86_64"],
    ["platform-windows", "arch-x86"],
    ["platform-windows", "arch-x86_64"],
]

tools = ["nvim-qt.exe" if os.name == "nt" else "nvim"]
# @late()
# def tools():
#     import os
#     bin_path = os.path.join(str(this.root), 'bin')
#     executables = []
#     for item in os.listdir(bin_path):
#         path = os.path.join(bin_path, item)
#         if os.access(path, os.X_OK) and not os.path.isdir(path):
#             executables.append(item)
#     return executables

build_requires = ["requests"]

build_command = [os.sys.executable, os.path.join(__dir__, "install.py")]


def commands():
    """Commands to set up environment for ``rez env neovim``"""
    import os
    env.PATH.append(os.path.join("{root}", "bin"))
    # env.XDG_DATA_DIRS.append(os.path.join("{root}", "share"))
