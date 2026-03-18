#!/usr/bin/env python3
import platform, psutil, subprocess, os, readline, shutil, random, socket, requests

# --- ASCII Art & Config ---
ICONS = {
    "pyramid": [
        "                '                ", "               /=\\               ",
        "              /===\ \            ", "             /=====\' \           ",
        "            /=======\'' \         ", "           /=========\ ' '\      ",
        "          /===========\''   \    ", "         /=============\ ' '  \  ",
        "        /===============\   ''  \ ", "       /=================\' ' ' ' \ ",
        "      /===================\' ' '  ' \ ", "     /=====================\' '   ' ' \ ",
        "    /=======================\  '   ' /", "   /=========================\   ' /  ",
        "  /===========================\'  /   ", " /=============================\/    "
    ],
    "computer": [
        "     _________________________      ", "    |.-----------------------.|     ",
        "    ||                       ||     ", "    ||       PYTHON 3.x      ||     ",
        "    ||                       ||     ", "    ||                       ||     ",
        "    ||                       ||     ", "    |'-----------------------'|     ",
        "     [_______________________]      ", "     |_______________________|      ",
        "      |                     |       ", "      |       _______       |       ",
        "      |      |_______|      |       ", "      |_____________________|       ",
        "     /                       \      ", "    /_________________________\     "
    ],
    "saturn": [

        "                                    ", "                _..._               ",

        "              .'     '.             ", "             /    _    \            ",

        "       __..-/:  _( )_   \           ", "  _..-'      \ '     '  /_..-''-._  ",

        " '._          '._____.'          _.'", "    '.._                      _..'  ",

        "        '-._              _.-'      ", "            '-..____...-''          ",

        "                                    ", "           THE DATA SPACE           ",

        "                                    ", "                                    ",

        "                                    ", "                                    "

    ]

}

CURRENT_ICON = "pyramid"
ART_WIDTH = 40
RAINBOW = [196, 202, 208, 214, 220, 226, 190, 154, 118, 82, 46, 47, 48, 49, 50, 51]
RESET, BOLD, GREEN, BLUE, YELLOW, RED = "\033[0m", "\033[1m", "\033[1;32m", "\033[1;34m", "\033[1;33m", "\033[1;31m"

# --- Helper Functions ---

def get_weather(city=None):
    """Fetches weather using Open-Meteo. Defaults to IP-based location."""
    try:
        # 1. Get Lat/Lon
        if city:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_data = requests.get(geo_url).json()
            if not geo_data.get('results'): return "City not found"
            lat, lon, name = geo_data['results'][0]['latitude'], geo_data['results'][0]['longitude'], geo_data['results'][0]['name']
        else:
            # Auto-detect location via IP
            ip_data = requests.get("https://ipapi.co/json/").json()
            lat, lon, name = ip_data['latitude'], ip_data['longitude'], ip_data['city']

        # 2. Get Weather
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_data = requests.get(w_url).json()
        temp = w_data['current_weather']['temperature']
        return f"{name}: {temp}°C"
    except:
        return "Weather Offline"

def get_detailed_sys_info():
    # 1. Initialize a default value FIRST
    ip = "N/A"
    mem = psutil.virtual_memory()
    load = psutil.cpu_percent()
    disk = psutil.disk_usage('/')
    fmt = lambda label, val: f"{BOLD}{label.ljust(12)}{RESET} {val}"
    
    return [
        f"{BOLD}{platform.node()}@{platform.system()}{RESET}",
        "-------------------------------------",
        fmt("OS:", f"{platform.system()} {platform.release()}"),
        fmt("Kernel:", platform.version().split()[0]),
        fmt("CPU:", f"{platform.processor()[:20]}..."),
        fmt("CPU Load:", f"{load}%"),
        fmt("Memory:", f"{round(mem.used/1024**3, 1)}G / {round(mem.total/1024**3, 1)}G"),
        # Now 'disk' is defined and safe to use!
        fmt("Disk Usage:", f"{disk.percent}%"),
        fmt("Local IP:", ip),
        fmt("Python:", platform.python_version()),
        fmt("Uptime:", f"{round((psutil.time.time() - psutil.boot_time())/3600, 1)} hrs"),
        "",
        f"{YELLOW}Banner:{RESET} {CURRENT_ICON}",
        "\033[41m  \033[42m  \033[43m  \033[44m  \033[45m  \033[46m  \033[47m  " + RESET
    ]

def draw_fetch(specific_icon=None):
    global CURRENT_ICON
    if specific_icon in ICONS: CURRENT_ICON = specific_icon
    art = ICONS[CURRENT_ICON]
    sys_info = get_detailed_sys_info()
    os.system('clear')
    print("")
    for i, line in enumerate(art):
        color = f"\033[38;5;{RAINBOW[i % len(RAINBOW)]}m"
        info = sys_info[i] if i < len(sys_info) else ""
        print(f"{color}{line.ljust(ART_WIDTH)}{RESET}{info}")
    print("")

def main():
    draw_fetch()
    while True:
        try:
            cwd = os.getcwd().replace(os.path.expanduser("~"), "~")
            user_input = input(f"{GREEN}cub@cub-inspiron-2350:{RESET}:{BLUE}{cwd}{RESET}$ ").strip()
            if not user_input: continue
            parts = user_input.split()
            cmd = parts[0]

            if cmd in ["exit", "quit"]: break
            elif cmd == "help":
                print(f"\n{YELLOW}--- Commands ---{RESET}")
                print(f"weather [city] : Check specific city weather")
                print(f"banner [name]  : Change art (pyramid, computer)")
                print(f"housekeeper    : Sort files in current folder")
                print(f"clear          : Refresh all info")
                print("-" * 20)
            elif cmd == "weather":
                city = parts[1] if len(parts) > 1 else None
                print(f"🌤  {get_weather(city)}")
            elif cmd == "banner":
                draw_fetch(parts[1] if len(parts) > 1 else "pyramid")
            elif cmd == "clear":
                draw_fetch()
            elif cmd == "housekeeper":
                # (Housekeeper logic from previous step)
                print("Cleaning...")
            elif cmd == "cd":
                try: os.chdir(os.path.expanduser(parts[1] if len(parts) > 1 else "~"))
                except: print("Path not found")
            else:
                subprocess.run(user_input, shell=True)
        except KeyboardInterrupt: print("\nUse 'exit' to quit.")
        except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    main()
