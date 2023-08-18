import os
def servicetweak():
    # Define the path to the file
    file_path = "sysservicetweak.txt"

    # Read the file and process each line
    with open(file_path, "r") as file:
        for line in file:
            command = line.strip()  # Remove leading/trailing whitespace and newline
            if command:
                os.system(command)
                print(f"Executed: {command}")
            else:
                print("Empty line")

    print("Script finished")