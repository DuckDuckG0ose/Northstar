import ctypes
import re
import subprocess
import psutil
import os
import time
import webbrowser
import shutil
import crayons

def windowssearch():
    os.system('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Search" /v "BingSearchEnabled" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Search" /v "CortanaEnabled" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Search" /v "SearchboxTaskbarMode" /t REG_DWORD /d "1" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowCloudSearch" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "ConnectedSearchUseWeb" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKLM\Software\Policies\Microsoft\Windows\Windows Search" /v "ConnectedSearchUseWebOverMeteredConnections" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "DisableWebSearch" /t REG_DWORD /d "1" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowCortanaAboveLock" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\services\TermServicentVersion\Search" /v "AllowCortana" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowCortana" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\Windows Search" /v "AllowSearchToUseLocation" /t REG_DWORD /d "0" /f')

def run_robloxtweaks_cmd():
    try:
        subprocess.run(["robloxtweak.cmd"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        from Main import logger
        print(f"An error occurred: {str(e)}")
        logger.critical("UNABLE TO BOOST ROBLOX: ", e)

def maximize_command_prompt():
    try:
        # Constants for Windows API functions and attributes
        SW_MAXIMIZE = 3
        HWND = 0
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001

        # Load the Windows User32.dll library
        user32 = ctypes.windll.user32

        # Get the handle of the command prompt window
        hwnd = user32.GetForegroundWindow()

        # Maximize the command prompt window
        user32.ShowWindow(hwnd, SW_MAXIMIZE)

        # Set the position of the window to fill the screen (optional)
        user32.SetWindowPos(hwnd, HWND, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    except Exception as e:
        from Main import logger
        print(f"An error occurred: {str(e)}")
        logger.critical("UNABLE TO RESIZE WINDOW: ", e)

def boostdiscord():
    # Get the current username of the logged-in user
    current_user = os.getlogin()
    
    # Close Discord if it's running
    for proc in psutil.process_iter(['pid', 'name']):
        if 'Discord.exe' in proc.info['name']:
            pid = proc.info['pid']
            discord_process = psutil.Process(pid)
            discord_process.terminate()
            discord_process.wait()

    reg_command = f'Reg.exe add "HKU\\{current_user}\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\Discord.exe" /v "UseLargePages" /t REG_DWORD /d "1" /f'
    subprocess.run(reg_command, shell=True)
    print("Attempting to kill Discord...")
    time.sleep(3)

    # Reopen Discord (you may need to change the path to Update.exe if it's not in the system PATH)
    subprocess.Popen(f'C:\\Users\\{current_user}\\AppData\\Local\\Discord\\Update.exe --processStart Discord.exe')
    print("Reopening Discord...")
    print("If the console said invalid parameter it means discord was already closed. Dont worry.")
    time.sleep(3)

def open_browser_with_url(url):
    # On Windows, use 'start' command
    if os.name == 'nt':
        os.system(f'start {url}')


def center(text):
    console_width = shutil.get_terminal_size().columns
    padding = (console_width - len(text)) // 2
    centered_text = ' ' * padding + text
    return centered_text

def iprenew():
    os.system("ipconfig /renew")

def spicetify():
    try:
        print("Please wait while spice things up :P")
        # First PowerShell command
        command1 = "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-cli/master/install.ps1 | iex"
        subprocess.run(["powershell", "-Command", command1], check=True)

        # Second PowerShell command
        command2 = "iwr -useb https://raw.githubusercontent.com/spicetify/spicetify-marketplace/main/resources/install.ps1 | iex"
        subprocess.run(["powershell", "-Command", command2], check=True)

        command3 = "spicetify apply"
        subprocess.run(["powershell", "-Command", command3], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running PowerShell command: {e}")
        from Main import logger
        logger.critical("UNABLE TO ACCESS POWERSHELL: ", e)
    from Main import countdown_timer
    print(crayons.green("We spiced things up, to use spicetify open relaunch spotify. There will be a tab under your search button called Marketplace, we reccomend using the marketplace to install a plugin called 'adblock'. Thank you for using Northstar."))
    countdown_timer(15)
    exit(1)

def mssuninstall():
    try:
        print("Deleting the shitty ass ms store")
        # First PowerShell command
        command1 = "Get-AppxPackage -alluser *WindowsStore* | Remove-Appxpackage"
        subprocess.run(["powershell", "-Command", command1], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error running PowerShell command: {e}")
        from Main import logger
        logger.critical("UNABLE TO RUN POWERSHELL COMMAND: ", e)
        exit(1)


def defrag():
    try:
        # Run the "defrag" command with subprocess
        subprocess.run("defrag C:", shell=True, check=True)

        print("Defragmentation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running defrag: {e}")
        from Main import logger
        print(f"An error occurred: {str(e)}")
        logger.error("Unable to defrag: ", e)
    except FileNotFoundError:
        print("The 'defrag' command was not found. Make sure you are running on a Windows OS.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        from Main import logger
        print(f"An error occurred: {str(e)}")
        logger.critical("UNABLE TO ACCESS DEFRAGER: ", e)


def get_edge_version():
    try:
        result = subprocess.check_output('reg query "HKEY_CURRENT_USER\Software\Microsoft\Edge\BLBeacon" /v version', shell=True)
        output = result.decode("utf-8")
        version_match = re.search(r"version\s+REG_SZ\s+(\d+\.\d+\.\d+\.\d+)", output)
        if version_match:
            edge_version = version_match.group(1)
            return edge_version
        else:
            print("Error: Microsoft Edge version not found in the output.")
            return None
    except subprocess.CalledProcessError as e:
        print("Error:", e)
        from Main import logger
        print(f"An error occurred: {str(e)}")
        logger.critical("ERROR: ", e)
        return None

if __name__ == "__main__":
    edge_version = get_edge_version()
    if edge_version:
        from Main import logger
        print(f"Microsoft Edge version: {edge_version}")
        logger.info(f"Microsoft Edge version: {edge_version}")
        


def msedge():
    get_edge_version()
    print("Please wait while we uninstall ms edge")
    os.system(f"C:\Program Files (x86)\Microsoft\Edge\Application\{edge_version}\Installer")
    os.system("setup.exe –uninstall –system-level –verbose-logging –force-uninstall")
    print("We got rid of MS edge. Try searching for it.")

def smrtscrdisable():
    os.system('reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" /v "SmartScreenEnabled" /t REG_SZ /d "Off" /f')
    os.system('reg add "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Explorer" /v "SmartScreenEnabled" /t REG_SZ /d "Off" /f')
    os.system('reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppHost" /v "EnableWebContentEvaluation" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\AppHost" /v "EnableWebContentEvaluation" /t REG_DWORD /d "0" /f')
    os.system('reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\System" /v "EnableSmartScreen" /t REG_DWORD /d "0" /f')


def smartscreen():
    from Main import countdown_timer
    while True:
        print(crayons.red(" BE AWARE. YOU ARE ABOUT TO DISABLE WINDOWS SMARTSCREEN! DISABLING IT MAKES ANY PROGRAM RAN WILL IMMEDIATELY GET THEM. YOU WILL NOT RECEIVE THE 'Windows protected your PC' POPUP WHEN RUNNING POSSIBLY MALICIOUS FILES."))
        
        try:
            decision = input(crayons.blue("Use 1 [Yes] and 2 [No]"))
            if decision == 1:
                smrtscrdisable()

            elif decision == 2:
                print("As you wish.")
                countdown_timer(4)
                break
        except ValueError:
            print("Please use numbers only.")
            countdown_timer(10)

