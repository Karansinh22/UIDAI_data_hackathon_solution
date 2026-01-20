import nbformat
import sys
import os

def run_notebook(notebook_path):
    print(f"Executing notebook: {notebook_path}")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Change directory to the notebook's directory so relative paths work
    original_cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(notebook_path)))
    
    # Global namespace for execution
    globals_dict = {}
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            print(f"Running cell {i+1}...")
            source = "".join(cell.source)
            try:
                exec(source, globals_dict)
            except Exception as e:
                print(f"Error in cell {i+1}: {e}")
                os.chdir(original_cwd)
                return False
    
    os.chdir(original_cwd)
    print("Notebook execution completed successfully.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_notebook.py <path_to_notebook>")
        sys.exit(1)
    
    success = run_notebook(sys.argv[1])
    sys.exit(0 if success else 1)
