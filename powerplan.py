import os

def powerplan():
    os.system("cd C:\\Windows\\")
    os.system('powershell -c "Invoke-WebRequest -Uri \'https://cdn.discordapp.com/attachments/741471786486464585/1102253173680390204/Venix.pow\' -OutFile \"C:\\Windows\\Venix.pow\""')
    GUID = "99999999-9999-9999-9999-999999999999"
    os.system("powercfg /setactive %s" % GUID)
    os.system("powercfg -import \"C:\\Windows\\Venix.pow\" %s" % GUID)
    os.system("powercfg -s %s" % GUID)