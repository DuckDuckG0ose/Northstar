import os
import configparser
import subprocess
import ctypes

def ltweakval():
    # The default directory for Valorant GameUserSettings.ini file
    default_dir = os.path.expanduser("~\\AppData\\Local\\VALORANT\\Saved\\Config")

    # Check if the directory exists
    if not os.path.exists(default_dir):
        print("The default directory does not exist. Please make sure Valorant is installed correctly.")
        return

    # Path to the GameUserSettings.ini file
    config_path = os.path.join(default_dir, "GameUserSettings.ini")

    # Check if the GameUserSettings.ini file exists
    if not os.path.isfile(config_path):
        print("The GameUserSettings.ini file does not exist in the default directory.")
        return

    # Ask for user confirmation
    MessageBox = ctypes.windll.user32.MessageBoxW
    result = MessageBox(None, 'Are you sure you want to lower the Valorant settings for better performance? NOTE THAT THIS WILL LOWER THE GAME QUALITY. THE ONLY WAY TO UNDO THIS TWEAK IS TO REINSTALL VALORANT!!! ARE YOU SURE?', 'Confirmation', 1)
    if result == 1:
        # Create a config parser object
        config = configparser.ConfigParser()
        config.read(config_path)

        # Lower the settings
        if 'ScalabilityGroups' in config:
            config['ScalabilityGroups']['sg.ResolutionQuality'] = '70'
            config['ScalabilityGroups']['sg.ViewDistanceQuality'] = '1'
            config['ScalabilityGroups']['sg.AntiAliasingQuality'] = '1'
            config['ScalabilityGroups']['sg.ShadowQuality'] = '1'
            config['ScalabilityGroups']['sg.PostProcessQuality'] = '1'
            config['ScalabilityGroups']['sg.TextureQuality'] = '1'
            config['ScalabilityGroups']['sg.EffectsQuality'] = '1'
            config['ScalabilityGroups']['sg.FoliageQuality'] = '1'

        # Save the changes back to the file
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    try:
        subprocess.run(['./valorant'], shell=True)
    except FileNotFoundError:
        print("The 'valorant' batch file was not found in the current directory.")
        print("The settings have been successfully lowered for better performance.")
    else:
        print("Operation cancelled by user.")


