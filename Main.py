import subprocess
import crayons
import time
from time import sleep
import os
import sys
import ctypes
from honesponsor import sponsor
from softreboot import softreboot
from restorepoint import display_menu, main_menu
from modules import maximize_command_prompt
import json


os.system("title PerfCTRL - When your preformance falls, We rise.")
maximize_command_prompt()


def logo():
    os.system("cls")
    f = open('logo.txt', 'r')
    print(crayons.yellow(f.read()))
    f.close()
    print(crayons.blue("                                                       Welcome to "), crayons.green("PerfCTRL"), crayons.blue(". When your friends call out your aim and you blame it on your fps..."))

def logo_red():
    os.system("cls")
    f = open('logo.txt', 'r')
    print(crayons.red(f.read()))
    f.close()


def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r                                                                           Proceeding in in {i} seconds")
        sys.stdout.flush()
        time.sleep(1)

    sys.stdout.write("\r" + " " * 20 + "\r")
    sys.stdout.flush()




def warningmenu():
    os.system("cls")
    logo_red()
    print(crayons.red(f"""

    ░██╗░░░░░░░██╗░█████╗░██████╗░███╗░░██╗██╗███╗░░██╗░██████╗░██╗
    ░██║░░██╗░░██║██╔══██╗██╔══██╗████╗░██║██║████╗░██║██╔════╝░██║
    ░╚██╗████╗██╔╝███████║██████╔╝██╔██╗██║██║██╔██╗██║██║░░██╗░██║
    ░░████╔═████║░██╔══██║██╔══██╗██║╚████║██║██║╚████║██║░░╚██╗╚═╝
    ░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║██║░╚███║██║██║░╚███║╚██████╔╝██╗
    ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝░░╚══╝░╚═════╝░╚═╝


    WE ARE NOT RESPONSIABLE FOR ANY DAMAGES DONE TO YOUR MACHINE. WE STRONGLY SUGGEST ON MAKING A RESTORE POINT. PERFCTRL IS STILL NOT PERFECT AND WE DONT HAVE A AUTOMATIC RESTORE POINT SYSTEM IN PLACE. \n THIS PROGRAM CANT KNOW IF ITS BEING RUN AS AN ADMIN OR NOT. IF YOU ARE NOT RUNNING IT AS AN AMIN IT MAY HAVE A CHANCE OF BRICKING YOUR SYSTEM.
    """))
    countdown_timer(9)
    selectionmenu()






def selectionmenu():
    while True:
        os.system("cls")
        logo()

        print(f'\n \n')
        print(crayons.blue("                         [1.] SoftReboot                                                  [2.] Restore Point Center"))
        print("                         Use this if your pc has been                                                   Need to create or restore to a restore point?")
        print("                         running for a while and you want a boost                                                  Use this!")
        print(f'\n \n')
        print(f'\n \n')
        try:
            print(crayons.red("                                                                                    [0.] EXIT         [9.] BACK"))
            action = int(input(crayons.green("                                                                   What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                time.sleep(3)
                sys.exit()  # Exit the loop and end the program

            elif action == 1:
                softreboot()
                break

            elif action == 2:
                display_menu()
                main_menu()
                break

            else:
                print(crayons.red("Hmmm, seems like that action was invalid."))
                countdown_timer(5)
    
        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)



def checkjson(file_path):
    try:
        with open(file_path, 'r+') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                # If the JSON file is empty or invalid, initialize with a default value
                data = {'first_launch': False}

            first_launch = data.get('first_launch', False)

            if first_launch:
                    # If value is True, call the menu() function
                warningmenu()
                    # Set the value to False and write it back to the JSON file
                data['first_launch'] = False
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
            else:
                selectionmenu()
                # If value is False, skip the menu() function and continue with code
    except (FileNotFoundError, IOError) as e:
        print(f"Error while handling JSON file: {str(e)}")


file_path = "config.json"
checkjson(file_path)