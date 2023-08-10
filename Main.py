import subprocess
import crayons
import time
from time import sleep
import os
import logging
import sys
import ctypes
import shutil
import requests
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

def update(repo_url):
    local_version_file = "version.txt"
    repo_version_url = f"{repo_url}/raw/master/version.txt"

    # Read the local version file
    with open(local_version_file, "r") as f:
        local_version = f.readline().strip()

    # Fetch the version file from the GitHub repository
    try:
        response = requests.get(repo_version_url)
        response.raise_for_status()  # Check for any request errors
        repo_version = response.text.strip()
    except requests.exceptions.RequestException as e:
        print(crayons.red(f"Error fetching version file from GitHub: {e}"))
        print("Resuming with the code...")
        return

    # Check if the remote version is higher than the local version
    if repo_version > local_version:
        # Download and update all files from the GitHub repository
        try:
            repo_url_raw = f"{repo_url}/raw/master/"
            response = requests.get(repo_url_raw)
            response.raise_for_status()

            for filename in response.text.splitlines():
                file_url = f"{repo_url_raw}{filename}"
                response = requests.get(file_url)
                response.raise_for_status()

                with open(filename, "wb") as f:
                    f.write(response.content)

            print(crayons.green("Update successful."))
        except requests.exceptions.RequestException as e:
            print(crayons.red(f"Error downloading files from GitHub: {e}"))
    else:
        print(crayons.green("Local version is up to date."))
    input("Press enter to continue...")



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
    command = 'powershell.exe "(Get-AppxPackage Microsoft.MicrosoftEdge).Version"'
    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    # Extract the version number from the output
    msversion = result.stdout.strip()
    # Change the path to the Edge installer directory according to your system
    edge_installer_path = fr'%PROGRAMFILES(X86)%\Microsoft\Edge\Application\{msversion}\Installer'
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
    print(crayons.blue("                                                                              Welcome to "), crayons.green("Frontier"), crayons.blue(". Uncover the power within. Put it to use."))

def logo_red():
    os.system("cls")
    f = open('logo.txt', 'r')
    print(crayons.red(f.read()))
    f.close()


def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r                                                                                                                            Proceeding in in {i} seconds")
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

def thirdpage():
    while True:
        os.system("cls")
        logo()
#                                       .             /                                                 .                  /                                                  .                 /
        print(f'\n \n')
        print(crayons.cyan("                         [1.] Max SYN Retransmissions                                    [2.] Chimney PacketCoalescing                                         [3.] TCP Receive Window"))
        print("                         Alters the registry in order to increase                        disables the Chimney Offload feature in the Windows                   disables TCP Receive Window Auto-Tuning")
        print("                         The number of attempts to reestablish a connection              networking stack, which can boost internet performance                for the specified InternetCustom setting ")
        print(f'\n \n')
        print(crayons.cyan("                         [4.] Restrict Autotuning                                        [5.] Network direct memory acess                                           [6.] Set IPV4 IPV6 RSC for Adapters"))
        print("                          sets the TCP Receive Window Auto-Tuning                        Doesn't work together with Chimney Offload                            Enables the Windows operating system's")
        print("                         level to 'Restricted' in the Windows TCP/IP stack               but Chimney Offload is out since Windows 10.                          autotuning feature for the TCP/IP stack")
        print(f'\n \n')
        print(f'\n \n')

        print()
        try:
            print(crayons.magenta("                                                                                                   [99.] DISCORD   |    [10.] Page 2 "))
            action = int(input(crayons.green("                                                                                             What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                sys.exit()  # Exit the loop and end the program

            elif action == 1:
                os.system("powershell.exe Set-NetTCPSetting -SettingName InternetCustom -MaxSynRetransmissions 3")
            
            elif action == 2:
                os.system("powershell.exe Set-NetOffloadGlobalSetting -Chimney Disabled")
            
            elif action == 3:
                os.system("powershell.exe Set-NetTCPSetting -SettingName InternetCustom -ScalingHeuristics Disabled")
            
            elif action == 4:
                os.system("netsh int tcp set global autotuninglevel=Restricted")
            
            elif action == 5:
                os.system("netsh int tcp set global netdma=enabled")
            elif action == 6:
                os.system("powershell.exe Set-NetAdapterRsc -Name * -IncludeHidden -IPv4Enabled $True -IPv6Enabled $True")
            
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
        print(crayons.cyan("                         [4.] Enable Teredo tecnologie                                   [5.] Clear DNS client cache                                           [6.] Enable WinStock"))
        print("                         Enables Teredo Options to allocate more                         Refreshes DNS resolutions  and clears out                             Enables the Windows operating system's")
        print("                         resources to the network adapters                               Old , unused and/or broken ones.                                      autotuning feature for the TCP/IP stack")
        print(f'\n \n')
        print(crayons.cyan("                         [7.] Non Sack Rtt Resiliency                                    [8.] TCP memory pressure protection                                   [9.] SYN Retransmissions"))
        print("                         enhances internet performance by improving                      helps ensure that a computer continues normal operation               Sets the number of times to attempt to")
        print("                         congestion control and recovery from packet loss                when low on memory due to denial of service attacks.                  reestablish a connection with SYN packets.")
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
            elif action == 4:
                os.system("netsh interface teredo set state client")
            elif action == 5:
                os.system("powershell.exe Clear-DnsClientCache")
            elif action == 6:
                os.system("netsh winsock set autotuning on")
            elif action == 7:
                os.system("netsh int tcp set global nonsackrttresiliency=enabled")
            elif action == 8:
                os.system("powershell.exe Set-NetTCPSetting -MemoryPressureProtection Enabled")
            elif action == 9:
                os.system("powershell.exe Set-NetTCPSetting -SettingName InternetCustom -MaxSynRetransmissions 3")
            
            elif action == 10:
                selectionmenu()
                break
            elif action == 11:
                thirdpage()
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
                os.system('call %systemroot%\System32\SystemPropertiesProtection.exe')  
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


try:
    github_repo_url = "https://github.com/VisualDeVenture/Frontier"
    update(github_repo_url)
    check_admin()
except Exception as e:
    print("An error occurred:")
    print(e)
    input("Press any key to continue...")

# Just a small update