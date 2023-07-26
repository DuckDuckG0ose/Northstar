import os
import requests

def debloat():
    url = 'https://raw.githubusercontent.com/VisualDeVenture/Debloat/main/Debloat.bat'
    
    # Download the batch script content from GitHub
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the batch script content to a temporary file
        with open('debloat_script.bat', 'w') as file:
            file.write(response.text)
        
        # Run the batch script using os.system
        os.system('debloat_script.bat')
        
        # Remove the temporary batch file
        os.remove('debloat_script.bat')
    else:
        print(f"I couldnt debloat your pc. Something must be wrong.")
    input("Thank you for choosing Frontier. Press any key to continue...")