import crayons
import subprocess
import os

def onstartup(batch_file_path):
    batch_code = """@echo off
start "" "C:\\PathToTool\\TimerTool.exe" -t 0.5 -minimized
exit
"""
    with open(batch_file_path, 'w') as file:
        file.write(batch_code)

def add_to_startup(startup_folder, batch_file_path):
    startup_file_path = os.path.join(startup_folder, "TimerTool_Startup.bat")
    try:
        os.makedirs(startup_folder, exist_ok=True)
        os.rename(batch_file_path, startup_file_path)
        print("The batch file has been added to the user's startup folder.")
    except Exception as e:
        print(f"Error: {e}")


def timerresolution(start):
    os.system("")
    if start:
        onstartup()
    else:
        os.system("Frontier.exe -t 0.5 -minimized")


def timerr():
    while True:
        choice = input("Do you want to start Timer Resolution on startup? (y/n): ").lower()

        if choice == 'y':
            timerresolution(True)
            break
        elif choice == 'n':
            timerresolution(False)
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")