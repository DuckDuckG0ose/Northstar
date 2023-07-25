import subprocess
import crayons
import time
from time import sleep
import os
import sys
import ctypes
import shutil
from honesponsor import sponsor
from softreboot import softreboot
from restorepoint import display_menu, main_menu
from modules import maximize_command_prompt, boostdiscord, webbrowser, iprenew, spicetify, mssuninstall
from modules import defrag
import json
from debloat import debloat
from powerplan import powerplan
from TimerResolution import timerr


os.system("title Frontier - When your preformance falls, We rise.")
maximize_command_prompt()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_admin():
    if is_admin():
        firstlaunch()
    else:
        noadmin()

def noadmin():
    os.system("cls")
    print(crayons.red('''

███╗░░██╗░█████╗░  ░█████╗░██████╗░███╗░░░███╗██╗███╗░░██╗
████╗░██║██╔══██╗  ██╔══██╗██╔══██╗████╗░████║██║████╗░██║
██╔██╗██║██║░░██║  ███████║██║░░██║██╔████╔██║██║██╔██╗██║
██║╚████║██║░░██║  ██╔══██║██║░░██║██║╚██╔╝██║██║██║╚████║
██║░╚███║╚█████╔╝  ██║░░██║██████╔╝██║░╚═╝░██║██║██║░╚███║
╚═╝░░╚══╝░╚════╝░  ╚═╝░░╚═╝╚═════╝░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝

██████╗░███████╗██████╗░███╗░░░███╗██╗░██████╗░██████╗██╗░█████╗░███╗░░██╗░██████╗
██╔══██╗██╔════╝██╔══██╗████╗░████║██║██╔════╝██╔════╝██║██╔══██╗████╗░██║██╔════╝
██████╔╝█████╗░░██████╔╝██╔████╔██║██║╚█████╗░╚█████╗░██║██║░░██║██╔██╗██║╚█████╗░
██╔═══╝░██╔══╝░░██╔══██╗██║╚██╔╝██║██║░╚═══██╗░╚═══██╗██║██║░░██║██║╚████║░╚═══██╗
██║░░░░░███████╗██║░░██║██║░╚═╝░██║██║██████╔╝██████╔╝██║╚█████╔╝██║░╚███║██████╔╝
╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝╚═════╝░╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░


Hey there! We are sorry, but you are not running the script with admin permissions. 
We truly don't want to brick your pc. That's why we are asking you to relaunch the script
with admin permissions. Thank you.
'''))
    input("Press enter to exit...")

def uninstall_edge():
    # Change the path to the Edge installer directory according to your system
    edge_installer_path = r'%PROGRAMFILES(X86)%\Microsoft\Edge\Application\xxx\Installer'
    cmd1 = f'cd "{edge_installer_path}"'
    cmd2 = 'setup.exe -uninstall -system-level -verbose-logging -force-uninstall'

    try:
        # Run the first command to change the directory
        subprocess.run(cmd1, shell=True, check=True)
        # Run the second command to uninstall Edge
        subprocess.run(cmd2, shell=True, check=True)
        print("Microsoft Edge has been uninstalled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    

def logo():
    os.system("cls")
    f = open('logo.txt', 'r')
    print(crayons.yellow(f.read()))
    f.close()
    print(crayons.blue("                                                                Welcome to "), crayons.green("Frontier"), crayons.blue(". When your friends call out your aim and you blame it on your fps..."))

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


    WE ARE NOT RESPONSIABLE FOR ANY DAMAGES DONE TO YOUR MACHINE. WE STRONGLY SUGGEST ON MAKING A RESTORE POINT. FRONTIER IS STILL NOT PERFECT AND WE DONT HAVE A AUTOMATIC RESTORE POINT SYSTEM IN PLACE. \n THIS PROGRAM CANT KNOW IF ITS BEING RUN AS AN ADMIN OR NOT. IF YOU ARE NOT RUNNING IT AS AN AMIN IT MAY HAVE A CHANCE OF BRICKING YOUR SYSTEM.
    """))
    countdown_timer(9)
    selectionmenu()

def secondpage():
    while True:
        os.system("cls")
        logo()
#                                       .             /                                                 .                  /                                                  .                 /
        print(f'\n \n')
        print(crayons.cyan("                         [1.] Uninstall Edge                                             [2.] Defrag Disk                                                      [3.] Timer Resolution"))
        print("                         Its useless basically                                           Computer crashing? Use this option to try                             Sets your CPU Timer Rsolution")
        print("                         Might aswell uninstall it                                       and fix the corrupted stuff inside your C: drive                      to a custom value to boost the speed")
        print(f'\n \n')
        print()
        try:
            print(crayons.magenta("                                                                                          [99.] DISCORD   |    [10.] Page 1 [11.] Page 3"))
            action = int(input(crayons.green("                                                                                             What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                sys.exit()  # Exit the loop and end the program

            elif action == 1:
                uninstall_edge()
            
            elif action == 2:
                defrag()
            
            elif action == 3:
                timerr()

            elif action == 10:
                selectionmenu()
                break
            elif action == 99:
                    discord_url = "https://discord.gg/GkhwF53JbF"
                    os.system(f'start {discord_url}')
            else:
                print(crayons.red("Hmmm, seems like that action was invalid."))
                countdown_timer(5)
        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)


def selectionmenu():
    while True:
        os.system("cls")
        logo()

        print(f'\n \n')
        print(crayons.cyan("                         [1.] SoftReboot                                                  [2.] Restore Point Center                                             [3.] Debloat"))
        print("                         Use this if your pc has been                                     Need to create or restore to a restore point?                         Removes bloatware from your PC")
        print("                         running for a while and you want a boost                         Use this!                                                             In order to speed it up")
        print(f'\n \n')
        print(crayons.cyan("                         [4.] Powerplan                                                   [5.] Boost Discord                                                    [6.]Renew your IP"))
        print("                         Not reccomended using on a laptop                                Using this tweak makes your Discord                                   Most internet problems come from")
        print("                         Boosts your pc's preformance by using our custom power plan      client use less resources and goes brrrr                              a old ip. Renew it now.")
        print(f'\n \n')
        print(crayons.cyan("                         [7.] DNS flush                                                   [8.] Spicetify                                                       [9.]Uninstall MS store"))
        print("                         Flush your DNS configuration                                     Installs a modded version of spotify                                   The most annoying bloatware on windows")
        print("                         Could boost browser speeds.                                      that allows you to block ads & etc.                                    Just uninstall it. Its useless.")
        print("\n \n")
        try:
            print(crayons.magenta("                                                                                          [0.] EXIT       [99.] DISCORD   |   [10.] Page 2"))
            action = int(input(crayons.green("                                                                                             What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                sys.exit()  # Exit the loop and end the program

            elif action == 1:
                softreboot()
                break

            elif action == 2:
                display_menu()
                main_menu()
                break
            elif action == 3:
                debloat()
            elif action == 4:
                powerplan()
                print(crayons.green("Power Plan applied."))
                countdown_timer(5)
            elif action == 5:
                boostdiscord()
                print(crayons.green("I boosted Discord"))
                countdown_timer(5)
            elif action == 6:
                iprenew()
            elif action == 7:
                os.system("ipconfig /flushdns")
            elif action == 8:
                spicetify()
            elif action == 9:
                mssuninstall()
            elif action == 10:
                secondpage()
                break
            elif action == 99:
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

check_admin()