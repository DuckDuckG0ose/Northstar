import crayons
from Main import logo, selectionmenu, countdown_timer
import subprocess
import time
import os

def create_restore_point(name, restore_type=7):
    try:
        command = f'wmic.exe /namespace:\\\\root\\default Path SystemRestore Call CreateRestorePoint "{name}", 100, {restore_type}'
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def restore_to_restore_point(restore_point_sequence_number):
    try:
        command = f'wmic.exe /Namespace:\\\\root\\default Path SystemRestore Call Restore "{restore_point_sequence_number}"'
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def check_restore_point():
    try:
        command = 'wmic.exe /Namespace:\\\\root\\default Path SystemRestore get SequenceNumber'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip()
        if "SequenceNumber" in output:
            print(crayons.green("A existing restore point is already found."))
        else:
            print(crayons.red("No restore point"))
    except subprocess.CalledProcessError:
        print(crayons.red("Error occurred while checking restore points."))

def RestorePoint():
    while True:

        logo()
        print(crayons.green("""

                    ██████╗░███████╗░██████╗████████╗░█████╗░██████╗░███████╗  ██████╗░░█████╗░██╗███╗░░██╗████████╗
                    ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██╔══██╗██║████╗░██║╚══██╔══╝
                    ██████╔╝█████╗░░╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░  ██████╔╝██║░░██║██║██╔██╗██║░░░██║░░░
                    ██╔══██╗██╔══╝░░░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░  ██╔═══╝░██║░░██║██║██║╚████║░░░██║░░░
                    ██║░░██║███████╗██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗  ██║░░░░░╚█████╔╝██║██║░╚███║░░░██║░░░
                    ╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝  ╚═╝░░░░░░╚════╝░╚═╝╚═╝░░╚══╝░░░╚═╝░░░
"""))
        try:
            print(crayons.blue("                      [1.] Create                                          [2.] Restore"))
            print(f"\n")
            check_restore_point()
            print(f"\n")
            rp_action = input(int(crayons.green("                   What action would you like to perform: ")))

            if rp_action == 9:
                os.system("cls")
                selectionmenu()
            
            elif rp_action == 1:
                print("Creating a restore point...")
                create_restore_point()
            
            elif rp_action ==2:
                print("Restoring...")
                restore_to_restore_point()


        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)
                



    

