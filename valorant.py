import subprocess

def tweakval():
    try:
        subprocess.run(['./valorant'], shell=True)
    except FileNotFoundError:
        print("The 'valorant' batch file was not found in the current directory.")
