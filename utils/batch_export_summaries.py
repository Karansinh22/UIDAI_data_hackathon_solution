import os
import subprocess
import sys

def run_all_analysis():
    analysis_dir = "notebooks/analysis"
    results_dir = "analysis_results"
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    notebooks = sorted([f for f in os.listdir(analysis_dir) if f.endswith(".ipynb")])
    
    python_exe = sys.executable
    
    for nb in notebooks:
        nb_path = os.path.join(analysis_dir, nb)
        output_name = nb.replace(".ipynb", "_summary.txt")
        output_path = os.path.join(results_dir, output_name)
        
        print(f"Generating summary for {nb}...")
        
        # We use our run_notebook.py to execute and capture stdout
        try:
            result = subprocess.run(
                [python_exe, "utils/run_notebook.py", nb_path],
                capture_output=True,
                text=True,
                check=True
            )
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"=== {nb} Analytical Insights ===\n\n")
                f.write(result.stdout)
                
            print(f"Successfully saved to {output_path}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error running {nb}: {e.stderr}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"=== {nb} Run Error ===\n\n")
                f.write(e.stdout)
                f.write("\nERROR:\n")
                f.write(e.stderr)

if __name__ == "__main__":
    run_all_analysis()
