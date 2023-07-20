import os
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

# Function to print text with "#" and specified words replaced by orange color
def print_colored_ascii(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    with open(file_path, "r") as file:
        ascii_text = file.read()

    colored_ascii = (
        ascii_text.replace("#", f"{Fore.YELLOW}#{Style.RESET_ALL}")
                  .replace("Hone", f"{Fore.YELLOW}Hone{Style.RESET_ALL}")
                  .replace("AuraSide I.N.C.", f"{Fore.YELLOW}AuraSide I.N.C.{Style.RESET_ALL}")
    )

    print(colored_ascii)

def sponsor():
    # Replace "hone.txt" with the actual filename of your ASCII file
    file_name = "hone.txt"
    print_colored_ascii(file_name)
