import ctypes

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

