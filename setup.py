import os
from cx_Freeze import setup, Executable
from src.data.constant import __version__

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'
main_file = os.path.abspath('src\main.py')


executables = [
    Executable(main_file, base=base, targetName = 'leaf.exe')
]

setup(name='Leaf',
      version = __version__,
      description = 'Simple text-based farming game for the bored developer.',
      options = dict(build_exe = buildOptions),
      executables = executables)
