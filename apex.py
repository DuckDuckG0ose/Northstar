import os
import configparser
import ctypes

def apextweaks():
    # The default directory for Apex Legends settings.cfg file
    default_dir = os.path.expanduser("~\\Saved Games\\Respawn\\Apex\\local")

    # Check if the directory exists
    if not os.path.exists(default_dir):
        print("The default directory does not exist. Please make sure Apex Legends is installed correctly.")
        return

    # Path to the settings.cfg file
    config_path = os.path.join(default_dir, "settings.cfg")

    # Check if the settings.cfg file exists
    if not os.path.isfile(config_path):
        print("The settings.cfg file does not exist in the default directory.")
        return

    # Ask for user confirmation
    MessageBox = ctypes.windll.user32.MessageBoxW
    result = MessageBox(None, 'Are you sure you want to lower the Apex Legends settings for better performance?', 'Confirmation', 1)
    if result == 1:
        # Create a config parser object
        config = configparser.ConfigParser()
        config.read(config_path)

        # Lower the settings
        if 'VideoConfig' in config:
            config['VideoConfig']['setting.cl_gib_allow'] = '0'
            config['VideoConfig']['setting.cl_particle_fallback_base'] = '0'
            config['VideoConfig']['setting.cl_particle_fallback_multiplier'] = '0'
            config['VideoConfig']['setting.cl_ragdoll_maxcount'] = '0'
            config['VideoConfig']['setting.mat_depthfeather_enable'] = '0'
            config['VideoConfig']['setting.mat_forceaniso'] = '1'
            config['VideoConfig']['setting.particle_cpu_level'] = '0'
            config['VideoConfig']['setting.r_createmodeldecals'] = '0'
            config['VideoConfig']['setting.r_decals'] = '0'
            config['VideoConfig']['setting.shadow_enable'] = '0'

        # Save the changes back to the file
        with open(config_path, 'w') as configfile:
            config.write(configfile)

        print("The settings have been successfully lowered for better performance.")
    else:
        print("Operation cancelled by user.")
