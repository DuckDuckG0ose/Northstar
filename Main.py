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


os.system("title PerfCTRL - When your preformance falls, We rise.")


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

def selectionmenu():
    while True:
        os.system("cls")
        logo()

        print(f'\n \n')
        print(crayons.blue("                         [1.] SoftReboot                                                  [2.] Restore Point Center"))
        print("                         Use this if your pc has been                                                   Need to vreate or restore to a restore point?")
        print("                         running for a while and you want a boost                                                  Use this!")
        print(f'\n \n')
        print(f'\n \n')
        try:
            print(crayons.red("                                                                                    [0.] EXIT         [9.] BACK"))
            action = int(input(crayons.green("                                                                   What action would you like to perform: ")))


            if action == 0:
                print("Exiting...")
                time.sleep(3)
                break  # Exit the loop and end the program

            elif action == 1:
                softreboot()

            elif 2:
                display_menu()
                main_menu()

            else:
                print(crayons.red("Hmmm, seems like that action was invalid."))
                countdown_timer(15)
    
        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)

countdown_timer(15)

agree = input(str(" Type 'i agree' without the quotation marks to comtinue: "))

if agree.strip().lower() == 'i agree':
    print("Resuming...")
    selectionmenu()
else:
    print("You must agree to use this program...")
    input("Press any key to continue...")



    