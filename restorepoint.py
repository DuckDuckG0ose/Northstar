import crayons
import subprocess
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
            print(crayons.green("An existing restore point is already found."))
        else:
            print(crayons.red("No restore point available."))
    except subprocess.CalledProcessError:
        print(crayons.red("Error occurred while checking restore points."))

def display_menu():
    print(crayons.green("""
                  ██████╗░███████╗░██████╗████████╗░█████╗░██████╗░███████╗  ██████╗░░█████╗░██╗███╗░░██╗████████╗
                  ██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██╔══██╗██║████╗░██║╚══██╔══╝
                  ██████╔╝█████╗░░╚█████╗░░░░██║░░░██║░░██║██████╔╝█████╗░░  ██████╔╝██║░░██║██║██╔██╗██║░░░██║░░░
                  ██╔══██╗██╔══╝░░░╚═══██╗░░░██║░░░██║░░██║██╔══██╗██╔══╝░░  ██╔═══╝░██║░░██║██║██║╚████║░░░██║░░░
                  ██║░░██║███████╗██████╔╝░░░██║░░░╚█████╔╝██║░░██║███████╗  ██║░░░░░╚█████╔╝██║██║░╚███║░░░██║░░░
                  ╚═╝░░╚═╝╚══════╝╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚══════╝  ╚═╝░░░░░░╚════╝░╚═╝╚═╝░░╚══╝░░░╚═╝░░░
"""))
    print(crayons.blue("                      [1.] Create                                          [2.] Restore"))
    print("                                                      [0.] Exit")
    check_restore_point()
    print("\n")

def create_restore_point_menu():
    print("Creating a restore point...")
    name = input(crayons.green("(If you forget the name of the restore point you will not be able to get it back)Enter a name for the restore point: "))
    create_restore_point(name)
    print(crayons.green("Restore point created successfully."))

def restore_menu():
    check_restore_point()
    value = input(crayons.green("Enter the desired restore point's ID: "))
    print("Restoring...")
    restore_to_restore_point(value)
    print(crayons.green("System restored successfully."))

def main_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        display_menu()
        try:
            rp_action = int(input(crayons.green("What action would you like to perform: ")))

            if rp_action == 1:
                create_restore_point_menu()
            elif rp_action == 2:
                restore_menu()
            else:
                print(crayons.red("Invalid option. Please choose from the available options."))

        except ValueError:
            print(crayons.red("Please use numbers only."))

