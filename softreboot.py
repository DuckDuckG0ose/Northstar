import os
import crayons
import time
import sys

def softreboot():
    print(crayons.red("YOUR SCREEN WILL FLICKER FOR A BIT AND THERE WILL BE MULTIPLE ADMIN PRIVILAGES POPUPS. ALLOW ALL OF THEM."))

    def countdown_timer(seconds):
        for i in range(seconds, 0, -1):
            sys.stdout.write(f"\rProceeding in {i} seconds")
            sys.stdout.flush()
            time.sleep(1)

        sys.stdout.write("\r" + " " * 20 + "\r")
        sys.stdout.flush()
    countdown_timer(7)


    # Change directory to %TEMP%
    os.chdir(os.environ['TEMP'])

    # Download NSudo.exe if it doesn't exist
    if not os.path.exists("NSudo.exe"):
      os.system('curl -g -L -# -o "NSudo.exe" "https://github.com/auraside/HoneCtrl/raw/main/Files/NSudo.exe"')

    # Run NSudo commands to modify the registry and start TrustedInstaller service
    os.system('NSudo.exe -U:S -ShowWindowMode:Hide cmd /c "reg add \\"HKLM\\SYSTEM\\CurrentControlSet\\Services\\TrustedInstaller\\" /v "Start" /t Reg_DWORD /d "3" /f" >nul 2>&1')
    os.system('NSudo.exe -U:S -ShowWindowMode:Hide cmd /c "sc start \\"TrustedInstaller\\"" >nul 2>&1')

    # Download restart64.exe if it doesn't exist
    if not os.path.exists("Restart64.exe"):
        os.system('curl -g -L -# -o "Restart64.exe" "https://github.com/auraside/HoneCtrl/raw/main/Files/restart64.exe"')

    # Download EmptyStandbyList.exe if it doesn't exist
    if not os.path.exists("EmptyStandbyList.exe"):
        os.system('curl -g -L -# -o "EmptyStandbyList.exe" "https://github.com/auraside/HoneCtrl/raw/main/Files/EmptyStandbyList.exe"')

    # Kill the explorer.exe process
    os.system('taskkill /f /im explorer.exe >nul 2>&1')

    # Change directory to %SYSTEMROOT%
    os.chdir(os.environ['SYSTEMROOT'])

    # Start explorer.exe
    os.system('start explorer.exe >nul 2>&1')

    # Change directory back to %TEMP%
    os.chdir(os.environ['TEMP'])

    # Create the RefreshNet.bat file
    with open("RefreshNet.bat", "w") as bat_file:
        bat_file.write("netsh advfirewall reset\n")
        bat_file.write("ipconfig /release\n")
        bat_file.write("ipconfig /renew\n")
        bat_file.write("nbtstat -R\n")
        bat_file.write("nbtstat -RR\n")
        bat_file.write("ipconfig /flushdns\n")
        bat_file.write("ipconfig /registerdns\n")

    # Run RefreshNet.bat using NSudo
    os.system('NSudo -U:T -P:E -M:S -ShowWindowMode:Hide -wait cmd /c "%TEMP%\\RefreshNet.bat"')

    # Run Restart64.exe and EmptyStandbyList.exe
    os.system('Restart64.exe')
    os.system('EmptyStandbyList.exe standbylist')
