import time
import whois
import threading
import subprocess
import paramiko
import requests
import socket
import hashlib

logo = r"""
___________            __               .__        __          
\_   _____/___   _____/  |______________|__| _____/  |_  ______
 |    __)/  _ \ /  _ \   __\____ \_  __ \  |/    \   __\/  ___/
 |     \(  <_> |  <_> )  | |  |_> >  | \/  |   |  \  |  \___ \ 
 \___  / \____/ \____/|__| |   __/|__|  |__|___|  /__| /____  >
     \/                    |__|                 \/          \/ 
"""

lock = threading.Lock()
found = None


def pause():
    input("Press Enter to continue...")


def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, text=True)
    except Exception as e:
        print("Command failed:", e)


def clear():
    subprocess.call("clear", shell=True)


# -----------------------
# 12 - Directory Bruteforcer
# -----------------------

def dir_bruteforce():
    site = input("Website (ex: https://example.com): ")
    path = input("Wordlist Path: ")

    try:
        with open(path) as f:
            words = [w.strip() for w in f]
    except:
        print("Could not open wordlist")
        pause()
        return

    print("\nScanning...\n")

    for word in words:
        url = f"{site}/{word}"

        try:
            r = requests.get(url, timeout=3)

            if r.status_code == 200:
                print("Found:", url)

        except:
            pass

    pause()


# -----------------------
# 14 - Fast Port Scanner
# -----------------------

def port_scan():
    target = input("Target IP: ")

    ports = range(1,1025)

    print("\nScanning ports...\n")

    for port in ports:

        try:
            s = socket.socket()
            s.settimeout(0.5)

            if s.connect_ex((target,port)) == 0:
                print("Open Port:", port)

            s.close()

        except:
            pass

    pause()


# -----------------------
# 15 - Email Breach Checker
# -----------------------

def breach_check():
    email = input("Email: ")

    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

        r = requests.get(url)

        if r.status_code == 200:
            print("\n⚠ Email found in breaches\n")

            for breach in r.json():
                print(breach["Name"])

        else:
            print("No breaches found")

    except:
        print("Check failed")

    pause()


# -----------------------
# 16 - Admin Panel Finder
# -----------------------

def admin_finder():

    site = input("Website (ex: https://example.com): ")

    admin_paths = [
        "admin",
        "admin/login",
        "administrator",
        "adminpanel",
        "login",
        "cpanel",
        "dashboard",
        "backend"
    ]

    print("\nSearching for admin panels...\n")

    for path in admin_paths:

        url = f"{site}/{path}"

        try:
            r = requests.get(url, timeout=3)

            if r.status_code == 200:
                print("Possible Admin Page:", url)

        except:
            pass

    pause()
# -----------------------
# Existing tools
# -----------------------

def user_scanner():
    email = input("Email: ")
    run_command(f"user-scanner -e --allow-loud {email}")
    pause()


def nmap():
    ip = input("Target: ")
    run_command(f"nmap -sV {ip}")
    pause()


def nslookup():
    site = input("Site: ")
    run_command(f"nslookup {site}")
    pause()


def command():
    while True:
        cmd = input("Cub@Cub-Inspiron-2350:#~ ")

        if cmd.lower() == "exit":
            return

        run_command(cmd)


# -----------------------
# NEW TOOL 1
# Subdomain Scanner
# -----------------------

def subdomain_scanner():
    domain = input("Domain: ")
    wordlist = ["www","mail","ftp","api","dev","test","beta","admin"]

    print("\nSearching...\n")

    for sub in wordlist:
        url = f"http://{sub}.{domain}"
        try:
            requests.get(url, timeout=3)
            print("Found:", url)
        except:
            pass

    pause()


# -----------------------
# NEW TOOL 2
# Banner Grabber
# -----------------------

def banner_grabber():
    host = input("Host: ")
    port = int(input("Port: "))

    try:
        s = socket.socket()
        s.settimeout(3)
        s.connect((host, port))

        banner = s.recv(1024)
        print("Banner:", banner.decode(errors="ignore"))

        s.close()

    except:
        print("Could not grab banner")

    pause()


# -----------------------
# NEW TOOL 3
# DNS Recon
# -----------------------

def dns_recon():
    domain = input("Domain: ")

    record_types = ["A","MX","NS","TXT"]

    for record in record_types:
        print(f"\n{record} Records:")
        run_command(f"nslookup -type={record} {domain}")

    pause()


# -----------------------
# NEW TOOL 4
# Website Tech Detector
# -----------------------

def tech_detector():
    site = input("Website URL: ")

    try:
        r = requests.get(site, timeout=5)

        headers = r.headers

        print("\nDetected Technologies:\n")

        if "Server" in headers:
            print("Server:", headers["Server"])

        if "X-Powered-By" in headers:
            print("Powered By:", headers["X-Powered-By"])

        if "cloudflare" in r.text.lower():
            print("Possible Cloudflare Protection")

        if "wp-content" in r.text.lower():
            print("WordPress Detected")

    except:
        print("Detection failed")

    pause()


# -----------------------
# NEW TOOL 5
# Hash Cracker
# -----------------------

def hash_cracker():
    hash_value = input("Hash: ")
    path = input("Wordlist: ")

    try:
        with open(path) as f:
            for word in f:
                word = word.strip()

                if hashlib.md5(word.encode()).hexdigest() == hash_value:
                    print("Cracked (MD5):", word)
                    pause()
                    return

                if hashlib.sha1(word.encode()).hexdigest() == hash_value:
                    print("Cracked (SHA1):", word)
                    pause()
                    return

    except:
        print("Could not open wordlist")

    print("Hash not cracked")
    pause()


# -----------------------
# GEOLOCATOR
# -----------------------

def geolocator():
    ip = input("IP: ")

    try:
        print("Looking up...")
        result = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = result.json()

        if data["status"] == "success":
            print("\n--- GEOLOCATION RESULT ---")
            print("IP Address :", data["query"])
            print("Country    :", data["country"])
            print("Region     :", data["regionName"])
            print("City       :", data["city"])
            print("ISP        :", data["isp"])
        else:
            print("Lookup failed.")

    except:
        print("Lookup failed.")

    pause()


# -----------------------
# WHOIS
# -----------------------

def do_whois():
    domain_name = input("Whois: ").strip()

    try:
        domain_info = whois.whois(domain_name)

        print("\n=== Domain Information ===")
        print("Domain:", domain_info.domain_name)
        print("Registrar:", domain_info.registrar)
        print("Creation:", domain_info.creation_date)
        print("Expiration:", domain_info.expiration_date)
        print("Name Servers:", domain_info.name_servers)

    except Exception as e:
        print("Error:", e)

    pause()


# -----------------------
# SSH (UNCHANGED)
# -----------------------

def ssh_connect(ip_address, username, password):
    global found
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(ip_address, username=username, password=password)
        with lock:
            if found is None:
                found = password
                print(f"\nConnection successful with password: {password}")
    except paramiko.AuthenticationException:
        pass
    except Exception as e:
        print(f"Error: {e}")


def attempt_login(ip_address, username, password_list):
    threads = []
    for password in password_list:
        thread = threading.Thread(target=ssh_connect, args=(ip_address, username, password))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if found is None:
        print("All Passwords Failed.")

    pause()


# -----------------------
# MENU
# -----------------------

def render_menu():
    while True:

        clear()

        print(logo)
        print("")
        print("==========================================================")
        print("| [1] Whois Lookup | [7] Command Prompt | [13] SSH       |")
        print("| [2] Geolocator   | [8] Banner Grabber | [14] PortScan  |")
        print("| [3] Nslookup     | [9] DNS Recon      | [15] BreachChk |")
        print("| [4] Nmap         | [10] Tech Detect   | [16] AdminFind |")
        print("| [5] UserScanner  | [11] Hash Cracker  | [17]           |")
        print("| [6] SubdomainScan| [12] Dir Bruteforce| [18] Exit      |")
        print("==========================================================")
        print("")

        choice = input("Option: ").strip()

        if choice == "1":
            do_whois()

        elif choice == "2":
            geolocator()

        elif choice == "3":
            nslookup()

        elif choice == "4":
            nmap()

        elif choice == "5":
            user_scanner()

        elif choice == "6":
            subdomain_scanner()

        elif choice == "7":
            command()

        elif choice == "8":
            banner_grabber()

        elif choice == "9":
            dns_recon()

        elif choice == "10":
            tech_detector()

        elif choice == "11":
            hash_cracker()

        elif choice == "13":

            ip_address = input("IP: ")
            username = input("Username: ")

            path = input("Path to Passlist: ")

            try:
                with open(path) as f:
                    passwords = [line.strip() for line in f]
            except:
                print("Could not read password list.")
                pause()
                continue

            attempt_login(ip_address, username, passwords)
        elif choice == "12":
            dir_bruteforce()

        elif choice == "14":
            port_scan()

        elif choice == "15":
            breach_check()

        elif choice == "16":
            admin_finder()
        elif choice == "17":
                        
            if choice == "18":
                break

        else:
            print("Invalid option.")
            pause()


render_menu()
