import subprocess
import crayons
import re
import time
from time import sleep
import os
import logging
import sys
import ctypes
import shutil
import threading
import requests
from honesponsor import sponsor
from softreboot import softreboot
from modules import maximize_command_prompt, boostdiscord, webbrowser, iprenew, spicetify, mssuninstall, run_robloxtweaks_cmd
from modules import defrag
import json
from debloat import debloat
from servicetweak import servicetweak
from powerplan import powerplan
from TimerResolution import timerr
from pypresence import Presence
from valorant import tweakval

def set_cmd_font_size(size):
    LF_FACESIZE = 32
    STD_OUTPUT_HANDLE = -11

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

    font_info = CONSOLE_FONT_INFOEX()
    font_info.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font_info.nFont = 0
    font_info.dwFontSize.X = 0
    font_info.dwFontSize.Y = size
    font_info.FontFamily = 54  # Modern
    font_info.FontWeight = 400  # Normal
    font_info.FaceName = "Consolas"

    hndl = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(hndl, ctypes.c_long(False), ctypes.pointer(font_info))

def fontsize():
    font_size = int(input("Enter font size: "))
    set_cmd_font_size(font_size)
    print(f"Font size updated to {font_size}")
    selectmode()





def setup_logging(log_file='logs.txt'):
    # Create a logger
    logger = logging.getLogger('file_logger')
    logger.setLevel(logging.DEBUG)

    # Create a file handler for writing logs to the file
    file_handler = logging.FileHandler(log_file, mode='w')  # 'w' mode overwrites existing file
    file_handler.setLevel(logging.DEBUG)

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

def update_rich_presence():
    client_id = '1065733264842690570'
    RPC = Presence(client_id)
    RPC.connect()

    details = "Uncover your PC's full potential"
    state = "The best PC optimization tool out there"
    start_time = time.time()

    presence_data = {
        "details": details,
        "state": state,
        "start": start_time,
        "large_image": "https://i.imgur.com/dNwR4F6.png",
        "small_image": "small_image_key",
        "buttons": [{"label": "Github", "url": "https://github.com/VisualDeVenture/Frontier"},
                    {"label": "Discord", "url": "https://discord.gg/GkhwF53JbF"}            
                    ]
    }

    try:
        while True:
            RPC.update(**presence_data)
            time.sleep(15)  # Update the presence every 15 seconds
    except KeyboardInterrupt:
        RPC.close()



os.system("title Project Frontier - Uncover your PC's full potential.")
maximize_command_prompt()
logger = setup_logging()
logger.info("Changed the window title.")
lightmode = False
presence_thread = threading.Thread(target=update_rich_presence)
presence_thread.daemon = True
presence_thread.start()
logger.info("Started rich presence.")

def update(repo_url):
    local_version_file = "version.txt"
    repo_version_url = f"{repo_url}/raw/master/version.txt"
    logger.info("Starting version checking squence")

    # Read the local version file
    with open(local_version_file, "r") as f:
        local_version = f.readline().strip()

    # Fetch the version file from the GitHub repository
    try:
        response = requests.get(repo_version_url)
        response.raise_for_status()  # Check for any request errors
        repo_version = response.text.strip()
        logger.warning("Possible error while checking for version. Unsure.")

    except requests.exceptions.RequestException as e:
        print(crayons.red(f"Error fetching version file from GitHub: {e}"))
        logger.error(e)
        print("Resuming with the code...")
        return

    # Check if the remote version is higher than the local version
    if repo_version > local_version:
        # Download and update all files from the GitHub repository
        try:
            repo_url_raw = repo_url
            response = requests.get(repo_url_raw)
            response.raise_for_status()
            logger.info("")
            for filename in response.text.splitlines():
                file_url = f"{repo_url_raw}{filename}"
                response = requests.get(file_url)
                response.raise_for_status()

                with open(filename, "wb") as f:
                    f.write(response.content)

            print(crayons.green("Update successful."))
            logger.info("Updated an outdated version.")
        except requests.exceptions.RequestException as e:
            print(crayons.red(f"Error downloading files from GitHub: {e}"))
            logger.error("Error while trying to download files from github", e)
    else:
        print(crayons.green("Local version is up to date."))
        logger.info("Latest version is being used.")
    logger.info("Ending version checking sequence.")
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
    logger.critical("YOU ARE MISSING ADMIN PERMISSIONS. THIS IS NOT AN ERROR. DO NOT REPORT THIS TO FRONTIER DEVS.")
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
        logger.info("User uninstalled MS Edge")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the command: {e}")
        logger.error("Error while trying to run commands. (MS EDGE): ", e)
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error("An error occured while uninstalling Microsoft Edge:", e)

    

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


    WE ARE NOT RESPONSIABLE FOR ANY DAMAGES DONE TO YOUR MACHINE. WE STRONGLY SUGGEST ON MAKING A RESTORE POINT.
    FRONTIER IS STILL NOT PERFECT AND WE DONT HAVE A AUTOMATIC RESTORE POINT SYSTEM IN PLACE. \n THIS PROGRAM CANT KNOW IF ITS BEING RUN AS AN ADMIN OR NOT. IF YOU ARE NOT RUNNING IT AS AN AMIN IT MAY HAVE A CHANCE OF BRICKING YOUR SYSTEM.
    """))
    countdown_timer(9)
    logger.info("This was users first launch. Take some stuff with a grain of salt.")
    selectionmenu()

def selectmode():
    lightmode = False
    while True:

        logo()                                       #                                                                                                                                     #
        print(f'\n \n')
        print(crayons.cyan("                         [1.] General Purpose Tweak Menu                                                                                                       [2.] Game Tweaks"))
        print("                         Menu of all General Purpose Input/Output                                                                                              Game tweaks hand picked by the Frontier")
        print("                         Tweaks made by the Frontier Devs                                                                                                      team to get you the most performance when gaming ")
        print(f'\n \n')

        try:
            print(crayons.magenta("                                                                    [100.] Edit Screen size |    [99.] light mode enable/disable |    [10.] Discord "))
            action = int(input(crayons.green("                                                                                             What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                break  # Exit the loop and end the program

            elif action == 1:
                selectionmenu()
                logger.info("Selected GPTW")
            elif action == 2:
                gametweaks()

            elif action == 100:
                fontsize()
                break
                selectmode()

            elif action == 99:
                    if lightmode == False:
                        os.system("color f0")
                        lightmode = True
                    elif lightmode == True:
                        os.system("color 0f")
            else:
                print(crayons.red("Hmmm, seems like that action was invalid."))
                countdown_timer(5)
        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)

def gametweaks():
    lightmode = False
    while True:

        logo()                                       #                                                                                                                                     #
        print(f'\n \n')
        print(crayons.cyan("                         [1.] Roblox Tweaks                                                                                                                    [2.] Valorant tweak"))
        print("                         You must use this tweak every time roblox                                                                                             Boost your fps in Valorant using this tweak")
        print("                         Updates to keep using it.                                                                                                             this tweak must be ran every update to have effects")
        print(f'\n \n')

        try:
            print(crayons.magenta("                                                                                       [99.] back |    [10.] Discord "))
            action = int(input(crayons.green("                                                                                             What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                break  # Exit the loop and end the program

            elif action == 1:
                run_robloxtweaks_cmd()
                logger.info("Tweaked Roblox.")
            elif action == 2:
                print("Not enabled yet")

            elif action == 99:
                break
            else:
                print(crayons.red("Hmmm, seems like that action was invalid."))
                countdown_timer(5)
        except ValueError:
            print(crayons.red("Please use numbers only."))
            countdown_timer(4)



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
        print(crayons.cyan("                         [4.] Restrict Autotuning                                        [5.] Network direct memory access                                     [6.] Set IPV4 IPV6 RSC for Adapters"))
        print("                         sets the TCP Receive Window Auto-Tuning                         Doesn't work together with Chimney Offload                            Enables the Windows operating system's")
        print("                         level to 'Restricted' in the Windows TCP/IP stack               but Chimney Offload is out since Windows 10.                          autotuning feature for the TCP/IP stack")
        print(f'\n \n')
        print(crayons.cyan("                         [7.] Better Wallpaper                                           [8.] Windows visual effects                                           [9.] Set compatibility services"))
        print("                         Increases the quality of your wallapaper                        I have 0 idea on what this does. Did a benchmark                      Enables windows's compatibility services")
        print("                         Does NOT work with lively wallpeper/wallpaper engine            check and it gave me like 10 more fps.                                and disables the non-used ones")
        print(f'\n \n')
        print(f'\n \n')

        print()
        try:
            print(crayons.magenta("                                                                                                   [99.] DISCORD   |    [10.] Page 2 "))
            action = int(input(crayons.green("                                                                                             What action would you like to perform: ")))

            if action == 0:
                print("Exiting...")
                break  # Exit the loop and end the program

            elif action == 1:
                os.system("powershell.exe Set-NetTCPSetting -SettingName InternetCustom -MaxSynRetransmissions 3")
                logger.info("Tweak used: Max SYN Retransmissions")
            
            elif action == 2:
                os.system("powershell.exe Set-NetOffloadGlobalSetting -Chimney Disabled")
                logger.info("Tweak used: Chimney PacketCoalescing")

            elif action == 3:
                os.system("powershell.exe Set-NetTCPSetting -SettingName InternetCustom -ScalingHeuristics Disabled")
                logger.info("Tweak used: TCP Receive Window")
            
            elif action == 4:
                os.system("netsh int tcp set global autotuninglevel=Restricted")
                logger.info("Tweak used: Restrict Autotuning")

            elif action == 5:
                os.system("netsh int tcp set global netdma=enabled")
                logger.info("Tweak used: Network direct memory access")

            elif action == 6:
                os.system("powershell.exe Set-NetAdapterRsc -Name * -IncludeHidden -IPv4Enabled $True -IPv6Enabled $True")
                logger.info("Tweak used: Set IPV4 IPV6 RSC for Adapters")

            elif action == 7:
                os.system('reg add "HKCU\Control Panel\Desktop" /v "JPEGImportQuality" /t "REG_DWORD" /d "100" /f')
                logger.info("Tweak used: Better Wallpaper")

            elif action == 8:
                print(crayons.green("Idk what you just did. Hope you made a restore point if something goes wrong. :P"))
                logger.info("Tweak used: Windows visual effects")
                countdown_timer(4)
            
            elif action == 9:
                servicetweak()
                logger.info("Tweak used: Set compatibiltity services")

            elif action == 10:
                secondpage()
                break
            elif action == 99:
                    discord_url = "https://discord.gg/GkhwF53JbF"
                    os.system(f'start {discord_url}')
                    logger.info("User joined the Discord server.")
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
                break  # Exit the loop and end the program

            elif action == 1:
                uninstall_edge()
                logger.info("Tweak used: uninstall edge")
            elif action == 2:
                defrag()
                logger.info("Tweak used: Defrag disk")
            elif action == 3:
                timerr()
                logger.info("Tweak used: Set timer resolution")
            elif action == 4:
                os.system("netsh interface teredo set state client")
                logger.info("Tweak used: Terado Tweak")
            elif action == 5:
                os.system("powershell.exe Clear-DnsClientCache")
                logger.info("Tweak used: Cleared DNS cache")
            elif action == 6:
                os.system("netsh winsock set autotuning on")
                logger.info("Tweak used: winstock autotuning")
            elif action == 7:
                os.system("netsh int tcp set global nonsackrttresiliency=enabled")
                logger.info("Tweak used: Non sack tweak")
            elif action == 8:
                os.system("powershell.exe Set-NetTCPSetting -MemoryPressureProtection Enabled")
                logger.info("Tweak used: Memory pressure protection")
            elif action == 9:
                os.system("powershell.exe Set-NetTCPSetting -SettingName InternetCustom -MaxSynRetransmissions 3")
                logger.info("Tweak used: SYN Retransmissions")
            
            elif action == 10:
                selectionmenu()
                break
            elif action == 11:
                thirdpage()
                break
            elif action == 99:
                    discord_url = "https://discord.gg/GkhwF53JbF"
                    os.system(f'start {discord_url}')
                    logger.info("Joined the Discord server.")
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
                break  # Exit the loop and end the program

            elif action == 1:
                softreboot()
                break

            elif action == 2:
                os.system('call %systemroot%\System32\SystemPropertiesProtection.exe')
                logger.info("Opened the restore point center.")  
            elif action == 3:
                debloat()
            elif action == 4:
                powerplan()
                print(crayons.green("Power Plan applied."))
                logger.info("Tweak used: Set the power plan")
                countdown_timer(5)
            elif action == 5:
                boostdiscord()
                print(crayons.green("I boosted Discord"))
                logger.info("Tweak used: Boosted discord")
                countdown_timer(5)
            elif action == 6:
                iprenew()
                logger.info("Tweak used: Renewed ip")
            elif action == 7:
                os.system("ipconfig /flushdns")
                logger.info("Tweak used: Flushed DNS")
            elif action == 8:
                spicetify()
                logger.info("Tweak used: Spiced up spotify")
            elif action == 9:
                mssuninstall()
                logger.info("Tweak used: uninstalled Microsoft Store")
            elif action == 10:
                secondpage()
                break
            elif action == 99:
                    discord_url = "https://discord.gg/GkhwF53JbF"
                    os.system(f'start {discord_url}')
                    logger.info("Tweak used: Joined the discord server")
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
        selectmode()


def main():
    os.system("cls")
    try:
        # Create the log file if it doesn't exist
        logger.info("Sucesfully started the script. Checking the version number...")
        github_repo_url = "https://github.com/VisualDeVenture/Frontier"
        update(github_repo_url)
        check_admin()
    
    except Exception as e:
        logger.critical(e)
        print("An error occurred:")
        print(e)
        input("Press any key to continue...")

main()