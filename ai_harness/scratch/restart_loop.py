import subprocess
import os
import time

def restart_loop():
    root_dir = r"c:\Users\rchos\Desktop\Studio_Loop"
    bat_file = os.path.join(root_dir, "run_gemma_e4b_vulkan.bat")
    
    print(f"Running {bat_file}...")
    # Using start to run the batch file in a new window as it's interactive/long-running
    subprocess.Popen(f'start cmd /c "{bat_file}"', shell=True, cwd=root_dir)
    print("Restart command sent.")

if __name__ == "__main__":
    restart_loop()
