import os
import sys

paths = [".agent/logs", "docs/adr"]

for path in paths:
    print(f"Checking {path}...")
    if os.path.exists(path):
        print(f"  Exists: True")
        print(f"  Is dir: {os.path.isdir(path)}")
        try:
            print(f"  Contents: {os.listdir(path)}")
        except Exception as e:
            print(f"  ListDir Error: {e}")
        
        try:
            test_file = os.path.join(path, "test_write.tmp")
            with open(test_file, "w") as f:
                f.write("test")
            print(f"  Write: Success")
            os.remove(test_file)
        except Exception as e:
            print(f"  Write Error: {e}")
    else:
        print(f"  Exists: False")
