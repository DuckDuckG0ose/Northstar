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
from modules import maximize_command_prompt, boostdiscord, webbrowser
import json
from powerplan import powerplan


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
        print(crayons.blue("                         [3.] Powerplan                                                  [4.] Boost Discord"))
        print("                         Not reccomended using on a laptop                                                   Using this tweak makes your Discord")
        print("                         Boosts your pc's preformance by using out custom power plan                               client use less resources and goes brrrr")
        print(f'\n \n')
        try:
            print(crayons.red("                                                                                    [0.] EXIT         [9.] BACK         [10.] DISCORD"))
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
            elif action == 3:
                powerplan()
                print(crayons.green("Power Plan applied."))
                countdown_timer(5)
            elif action == 4:
                boostdiscord()
                print(crayons.green("I boosted Discord"))
                countdown_timer(5)
            elif action == 10:
                    discord_url = "https://discord.gg/GkhwF53JbF"
                    os.system(f'start {discord_url}')
            else:
                print(crayons.red("Hmmm, seems like that action was invalid."))
                countdown_timer(5)
    
        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)



def firstlaunch():
    # Read the content of the config.json file
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    # Check the value of the first_launch key
    first_launch = config_data.get('first_launch', False)

    print(f"First Launch: {first_launch}")

    # Call the appropriate function based on the first_launch value
    if first_launch:
        # After showing the warning menu, update the first_launch value to False
        config_data['first_launch'] = False
        # Write the updated data back to the config.json file
        with open('config.json', 'w') as file:
            json.dump(config_data, file, indent=4)
        print("Updated 'first_launch' to False")
        warningmenu()

    else:
        selectionmenu()

firstlaunch()
