import os
def minecraft_tweak():
    # Set the Minecraft directory
    mc_dir = os.path.join(os.getenv('APPDATA'), '.minecraft')

    # Check if Minecraft directory exists
    if not os.path.exists(mc_dir):
        print("Minecraft directory not found. Are you sure you have minecraft installed?")
        exit()

    # Check if options.txt exists
    options_file = os.path.join(mc_dir, 'options.txt')
    if not os.path.exists(options_file):
        print("options.txt not found.")
        exit()

    # Make a backup of the original options.txt
    os.system(f'copy {options_file} {os.path.join(mc_dir, "options.txt.bak")}')

    # Change settings in options.txt
    with open(options_file, 'r') as file:
        lines = file.readlines()

    with open(options_file, 'w') as file:
        for line in lines:
            if line.startswith('renderDistance'):
                file.write('renderDistance:4\n')
            else:
                file.write(line)
