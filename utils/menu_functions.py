import os, bluetooth, re, subprocess, time
import logging as log
from utils.AnsiColorCode import AnsiColorCode

##########################
# UI Redesign by Lamento #
##########################

def get_target_address():
    print(f"\nWhat is the target address?")

    # Load known devices
    known_devices = load_known_devices()
    if known_devices:
        print(f"\nYou can also select one of the below known devices")
        for idx, (addr, name) in enumerate(known_devices):
            print(f"{AnsiColorCode.BLUE}{idx + 1}{AnsiColorCode.RESET}: Device Name: {AnsiColorCode.BLUE}{name}, Address: {AnsiColorCode.BLUE}{addr}{AnsiColorCode.RESET}")

    print(f"\nLeave blank and we will scan for you{AnsiColorCode.BLUE}!{AnsiColorCode.RESET}")
    target_address = None
    text_input = input(f"\n {AnsiColorCode.BLUE}> ")

    if text_input == "":
        devices = scan_for_devices()

        # Save the scanned devices only if they are not already in known devices
        new_devices = [device for device in devices if device not in known_devices]
        save_known_devices(new_devices)

        if devices:
            # Show list of scanned devices for user selection
            for idx, (addr, name) in enumerate(devices):
                print(f"{AnsiColorCode.RESET}[{AnsiColorCode.BLUE}{idx + 1}{AnsiColorCode.RESET}] {AnsiColorCode.BLUE}Device Name{AnsiColorCode.RESET}: {AnsiColorCode.BLUE}{name}, {AnsiColorCode.BLUE}Address{AnsiColorCode.RESET}: {AnsiColorCode.BLUE}{addr}")
            selection = int(input(f"\n{AnsiColorCode.RESET}Select a device by number{AnsiColorCode.BLUE}: {AnsiColorCode.BLUE}")) - 1
            if 0 <= selection < len(devices):
                target_address = devices[selection][0]
            else:
                print("\nInvalid selection. Exiting.")
                return None
        else:
            return None
    else:
        if is_valid_mac_address(text_input):
            print('yes')
            target_address = text_input.strip()
        elif known_devices:
            # Check if input is an index for known devices
            try:
                target_address = known_devices[int(text_input) - 1][0]
            except:
                pass
        else:
            print("\nInvalid Input.")
            return None

    return target_address

def restart_bluetooth_daemon():
    run(["sudo", "service", "bluetooth", "restart"])
    time.sleep(0.5)

def run(command):
    assert(isinstance(command, list))
    log.info("executing '%s'" % " ".join(command))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result

def print_fancy_ascii_art():

    print(f"""
    {AnsiColorCode.BLUE}
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠄⠒⠒⠒⠒⠒⠒⠂⠠⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠴⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠞⠁⠀⠀⠀⠀⣀⡤⠴⠒⠒⠒⠒⠦⠤⣀⠀⠀⠀⠙⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⢰⠋⠀⠀⠀⣠⠖⠋⢀⣄⣀⡀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀⠈⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⢀⡼⠁⠀⣴⣿⡛⠻⣿⣧⡀⠀⠀⠀⠀⠀⠀⠈⠳⡄⡿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⣼⣀⣀⣀⡜⠀⠀⠀⣿⣿⣿⣿⣿⣿⡧⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⣀⡤⠟⠁⠀⠈⠙⡶⣄⡀⠈⠻⢿⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
	⣤⣤⠖⠖⠛⠉⠈⣀⣀⠀⠴⠊⠀⠀⣹⣷⣶⡏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⣀⡀⠀⠀
	⠘⠿⣿⣷⣶⣶⣶⣶⣤⣶⣶⣶⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⠤⠖⠒⠋⠉⠁⠙⣆⠀
	⠀⠀⠀⠀⠉⠉⠉⠉⠙⠿⣍⣩⠟⠋⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣖⣶⣶⢾⠯⠽⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡄
	⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠚⠁⠀⠀⠀⠀⠈⠓⠤⠀⠀⠀⠀⠀⠀⠐⠒⠚⠉⠉⠁⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⣀⢀⠀⠀⠀⠀⠀⠀⠀⣇
	⠀⠀⠀⠀⠀⠀⠀⡴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠤⠤⠖⠒⠚⠉⠉⠁⠀⠀⠀⢸⢸⣦⠀⠀⠀⠀⠀⠀⢸
	⠀⠀⠀⠀⠀⢠⠎⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠤⠴⠒⠒⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⣸⡏⠇⠀⠀⠀⠀⠀⢸
	⠀⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠞⢠⡿⠀⠀⠀⠀⠀⠀⠀⢸
	⠀⠀⠀⠀⣾⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀⡏
	⠀⠀⠀⠀⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠖⠉⢀⣴⠏⠠⠀⠀⠀⠀⠀⠀⠀⣸⠁
	⠀⠀⠀⠀⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠒⠒⠢⠤⠄⠀⠀⠀⠀⠀⠈⠁⠀⣠⣶⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢠⠃⠀
	⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠃⠀⠀
	⠀⠀⠀⠀⠀⠈⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⡶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠳⣄⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠖⣪⡵⠋⠀⠀⠀⠀⠀
	⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠫⠭⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣭⣭⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⡴⠶⠛⠉⠀⠀⠀⠀⠀⠀⠀
{AnsiColorCode.RESET}
""")

def clear_screen():
    os.system('clear')

# Function to append discovered devices to a file
def save_known_devices(devices, filename='known_devices.txt'):
    with open(filename, 'a') as file:
        for addr, name in devices:
            file.write(f"{addr},{name}\n")

# Function to scan for devices
def scan_for_devices():
    main_menu()

    # Normal Bluetooth scan
    print(f"\n{AnsiColorCode.RESET}Attempting to scan now{AnsiColorCode.BLUE}...")
    try:
        nearby_devices = bluetooth.discover_devices(duration=6, lookup_names=True, flush_cache=True)
    except OSError as e:
        log.error(f"{AnsiColorCode.RED}Couldn't scan for Bluetooth devices!\n{AnsiColorCode.RESET}Is your Bluetooth activated?\n{e}")
        exit(1)

    device_list = []
    if len(nearby_devices) == 0:
        print(f"\n{AnsiColorCode.RESET}[{AnsiColorCode.RED}+{AnsiColorCode.RESET}] No nearby devices found.")
    else:
        print(f"\nFound {len(nearby_devices)} nearby device(s):")
        for _, (addr, name) in enumerate(nearby_devices):
            device_list.append((addr, name))

    return device_list

def getterm():
    size = os.get_terminal_size()
    return size.columns

def print_menu():
    title = "BlueDucky - Bluetooth Device Attacker"
    vertext = "Ver 2.1"
    motd1 = f"Remember, you can still attack devices without visibility.."
    motd2 = f"If you have their MAC address.."
    terminal_width = getterm()
    separator = "=" * terminal_width

    print(AnsiColorCode.BLUE + separator)  # Blue color for separator
    print(AnsiColorCode.RESET + title.center(len(separator)))  # Centered Title in blue
    print(AnsiColorCode.BLUE + vertext.center(len(separator)))  # Centered Version
    print(AnsiColorCode.BLUE + separator + AnsiColorCode.RESET)  # Blue color for separator
    print(motd1.center(len(separator)))# used the same method for centering
    print(motd2.center(len(separator)))# used the same method for centering
    print(AnsiColorCode.BLUE + separator + AnsiColorCode.RESET)  # Blue color for separator

def main_menu():
    clear_screen()
    print_fancy_ascii_art()
    print_menu()


def is_valid_mac_address(mac_address):
    # Regular expression to match a MAC address in the form XX:XX:XX:XX:XX:XX
    mac_address_pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return mac_address_pattern.match(mac_address) is not None

# Function to read DuckyScript from file
def read_duckyscript(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        log.warning(f"File {filename} not found. Skipping DuckyScript.")
        return None

# Function to load known devices from a file
def load_known_devices(filename='known_devices.txt'):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [tuple(line.strip().split(',')) for line in file]
    else:
        return []


title = "BlueDucky - Bluetooth Device Attacker"
vertext = "Ver 2.1"
terminal_width = getterm()
separator = "=" * terminal_width

print(AnsiColorCode.BLUE + separator)  # Blue color for separator
print(AnsiColorCode.RESET + title.center(len(separator)))  # White color for title
print(AnsiColorCode.BLUE + vertext.center(len(separator)))  # White blue for version number
print(AnsiColorCode.BLUE  + separator + AnsiColorCode.RESET)  # Blue color for separator
print(f"{AnsiColorCode.RESET}Remember, you can still attack devices without visibility{AnsiColorCode.BLUE}..{AnsiColorCode.RESET}")
print(f"{AnsiColorCode.BLUE}If you have their {AnsiColorCode.RESET}MAC address{AnsiColorCode.BLUE}..{AnsiColorCode.RESET}")
print(AnsiColorCode.BLUE + separator + AnsiColorCode.RESET)  # Blue color for separator
