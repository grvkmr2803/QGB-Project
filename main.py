import os
import sys

def run_analysis(script_name: str):
    
    module_path = f"analysis.{script_name}"
    print(f"\n{'='*20} RUNNING: {module_path} {'='*20}")
    
    result = os.system(f'"{sys.executable}" -m {module_path}')
    
    if result != 0:
        print(f"\nERROR: An error occurred while running {module_path}. Please check the output above")
        sys.exit(1) 
        
    print(f"\n{'='*20} FINISHED: {module_path} {'='*20}")


if __name__ == "__main__":
  
    run_analysis("ideal_and_validation")
    run_analysis("noisy_simulation")
    run_analysis("error_mitigation")

   