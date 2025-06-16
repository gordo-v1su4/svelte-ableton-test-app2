import py_compile
import os

script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataExportScript')

files_to_compile = ['__init__.py', 'DataExportScript.py']

for filename in files_to_compile:
    file_path = os.path.join(script_dir, filename)
    try:
        py_compile.compile(file_path, cfile=None, doraise=True)
        print(f"✓ {filename} compiled successfully")
    except py_compile.PyCompileError as e:
        print(f"✗ Compilation error in {filename}: {e}")
    except FileNotFoundError as e:
        print(f"✗ File not found: {file_path}")