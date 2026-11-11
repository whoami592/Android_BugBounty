#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ADB SMS & Call Tool
Coded by: Cyber Security Engineer Mr. Sabaz Ali Khan

Sends SMS and places/ends phone calls on YOUR OWN Android device over ADB.
Requirements:
  * Python 3.8+
  * Android platform-tools (adb) installed and in PATH
  * USB debugging enabled on the phone and this computer authorized
Use only on devices you own or have explicit permission to control.
"""

import shlex
import shutil
import subprocess
import sys
from urllib.parse import quote

BANNER = r"""
⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣷⣷⣶⣶⣷⣷⣷⣶⣶⣶⣶⣶⣶⣶⣶⣦⣄⠻⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣬⠻⣿⣿⡿⣿⡿⠿⠛⣻⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡈⠶⠖⠛⣋⣉⣉⣭⣤⣤⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠋⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠘⣛⣉⣭⣥⣴⣶⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡿⠁⢲⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠔⠒⠈⣉⡉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣉⣉⣩⣥⣤⣤⠆⣰⣿⣿⣿⣿⣿⣿⣿⣿⣋⣤⣤⣶⢾⣿⣿⣦⣄⠀⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⡆⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡟⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⢈⣈⡀⠙⠛⠷⢦⡀⠀⡹⠋⠛⢻⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⠟⠛⢿⠇⢻⣿⣿⣿⣿⣿⣿⣿⡿⠛⠀⠀⠠⠖⠛⠋⠛⠳⠀⠀⠀⠙⠆⠀⡾⠀⠀⠻⠿⢿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡟⠀⣴⣄⡀⢾⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⣀⣤⡙⠂⠀⠀⡄⠀⠀⠀⠀⣴⣾⣧⠀⠀⠀⠀⠀⠀⠃⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡇⠀⣾⣿⣿⣦⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⣀⠀⠐⠃⠀⢀⣠⣼⣿⣿⣿⠀⠀⠀⠀⠀⢤⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⡇⠘⠋⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠅⣠⣼⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀⠀⠀⠀⡾⠿⠿⠿⠿⠿⠟⠿⠿⡿⡿⡿
⣿⣿⡀⣀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢹⣦⣤⣤⣦⡄⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣧⣼⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⡀⠀⠹⣿⠇⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻⢃⣾⡿⠿⢿⣿⣿⣿⠙⠻⣿⠟⢻⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠈⠓⡄⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠘⠏⠀⢀⣀⣙⡛⠋⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣭⠀⠀⠀⢀⣠⣆⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢩⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⠁⠀⠇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠹⠿⠿⠛⠋⠉⠉⠁⠀⠈⠙⠋⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢸⠀⠀⢤⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡁⢠⣤⣤⣄⣤⣤⣤⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣬⡾⠓⠀⣸⣿⣿⣿⣿⣿⡟⢿⣿⣿⣿⣿⣿⡏⢀⠄⣸⣿⣿⣿⣿⣿⠟⠉⠉⠉⠉⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⡯⠐⣡⣾⣿⣿⣿⣿⣿⣿⠻⣎⠻⣿⣿⣿⣿⣇⢘⣠⣹⣿⣿⣿⣿⣧⣀⡀⣀⣀⠀⢀⠀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢁⣼⣿⣿⣿⣿⣿⣿⣿⣿⣧⡙⢷⣽⣿⣮⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡟⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⢻⣿⣿⣮⣻⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠙⠙⠃⢰⣌⠣⡀⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⡟⠈⠙⠛⠿⠿⠿⠋⠀⠀⠀⠀⠀⢀⣄⣹⣇⠱⠘⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠟⢻⣿⠀⡆⢸⡇⢿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀
"""

CREDIT = "Coded by: Cyber Security Engineer Mr. Sabaz Ali Khan"


# ----------------------------------------------------------------- helpers
def show_banner():
    print(BANNER)
    print("=" * 60)
    print("   ADB SMS & CALL TOOL")
    print(f"   {CREDIT}")
    print("=" * 60)


def adb_available():
    return shutil.which("adb") is not None


def run_adb(args, serial=None, timeout=30):
    """Run an adb command and return (returncode, combined output)."""
    cmd = ["adb"]
    if serial:
        cmd += ["-s", serial]
    cmd += args
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 1, "adb command timed out"
    except FileNotFoundError:
        return 1, "adb not found in PATH"


def adb_shell(command, serial=None):
    return run_adb(["shell", command], serial)


def get_devices():
    code, out = run_adb(["devices"])
    devices = []
    for line in out.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2:
            devices.append((parts[0], parts[1]))
    return devices


def pick_device():
    """Return the serial of a ready device, or None."""
    devices = get_devices()
    ready = [s for s, st in devices if st == "device"]
    for s, st in devices:
        if st == "unauthorized":
            print(f"[!] {s} is unauthorized - accept the USB debugging prompt on the phone.")
        elif st == "offline":
            print(f"[!] {s} is offline - reconnect the cable / restart adb.")
    if not ready:
        print("[-] No authorized device found.")
        return None
    if len(ready) == 1:
        print(f"[+] Using device: {ready[0]}")
        return ready[0]
    print("Multiple devices found:")
    for i, s in enumerate(ready, 1):
        print(f"  {i}. {s}")
    while True:
        c = input("Select device number: ").strip()
        if c.isdigit() and 1 <= int(c) <= len(ready):
            return ready[int(c) - 1]
        print("Invalid choice.")


def android_version(serial):
    _, out = adb_shell("getprop ro.build.version.release", serial)
    try:
        return int(out.split(".")[0])
    except ValueError:
        return 0


def valid_number(num):
    n = num.replace(" ", "").replace("-", "")
    body = n[1:] if n.startswith("+") else n
    return body.isdigit() and 3 <= len(body) <= 15


# ----------------------------------------------------------------- SMS
def send_sms_service(serial, number, text):
    """Send directly through the isms service (no UI). Parameters differ
    between Android versions, so this may fail on some devices."""
    ver = android_version(serial)
    num = shlex.quote(number)
    msg = shlex.quote(text)
    if ver >= 12:
        cmd = (f"service call isms 5 i32 0 s16 com.android.mms.service "
               f"s16 null s16 {num} s16 null s16 {msg} s16 null s16 null "
               f"i32 0 i64 0")
    elif ver >= 11:
        cmd = (f"service call isms 5 i32 0 s16 com.android.mms.service "
               f"s16 null s16 {num} s16 null s16 {msg} s16 null s16 null "
               f"i32 0 i64 0")
    else:
        cmd = (f"service call isms 7 i32 0 s16 com.android.mms.service "
               f"s16 {num} s16 null s16 {msg} s16 null s16 null")
    code, out = adb_shell(cmd, serial)
    ok = code == 0 and "Exception" not in out and "Error" not in out
    return ok, out


def send_sms_ui(serial, number, text):
    """Open the default messaging app with the text prefilled and press Send."""
    cmd = (f"am start -a android.intent.action.SENDTO -d sms:{quote(number)} "
           f"--es sms_body {shlex.quote(text)} --ez exit_on_sent true")
    code, out = adb_shell(cmd, serial)
    if code != 0 or "Error" in out:
        return False, out
    import time
    time.sleep(2)
    # Move focus to the send button and press it (works on most apps)
    adb_shell("input keyevent 22", serial)
    adb_shell("input keyevent 66", serial)
    return True, "Send key pressed (verify on the phone screen)."


def sms_menu(serial):
    number = input("Phone number (e.g. +923001234567): ").strip()
    if not valid_number(number):
        print("[-] Invalid phone number.")
        return
    text = input("Message: ")
    if not text:
        print("[-] Message is empty.")
        return
    print("Method:  1) Direct (service call)   2) Via messaging app UI")
    m = input("Choose [1/2, default 1]: ").strip() or "1"
    if m == "2":
        ok, out = send_sms_ui(serial, number, text)
    else:
        ok, out = send_sms_service(serial, number, text)
        if not ok:
            print("[!] Direct method failed, trying UI method...")
            ok, out = send_sms_ui(serial, number, text)
    print("[+] SMS request sent." if ok else "[-] SMS failed.")
    if out:
        print(out)


# ----------------------------------------------------------------- CALLS
def make_call(serial, number):
    dial = number.replace(" ", "").replace("-", "").replace("#", "%23")
    code, out = adb_shell(
        f"am start -a android.intent.action.CALL -d tel:{shlex.quote(dial)}", serial)
    return code == 0 and "Error" not in out, out


def end_call(serial):
    code, out = adb_shell("input keyevent KEYCODE_ENDCALL", serial)
    return code == 0, out


def answer_call(serial):
    code, out = adb_shell("input keyevent KEYCODE_CALL", serial)
    return code == 0, out


def call_state(serial):
    _, out = adb_shell("dumpsys telephony.registry | grep mCallState", serial)
    states = {"0": "IDLE", "1": "RINGING", "2": "OFFHOOK (in call)"}
    for line in out.splitlines():
        if "mCallState=" in line:
            return states.get(line.split("mCallState=")[1].strip()[:1], line.strip())
    return "unknown"


def call_menu(serial):
    number = input("Phone number to call: ").strip()
    if not valid_number(number.replace("#", "").replace("*", "") or "x"):
        print("[-] Invalid phone number.")
        return
    ok, out = make_call(serial, number)
    print("[+] Call started." if ok else "[-] Call failed.")
    if out:
        print(out)


# ----------------------------------------------------------------- main
def menu():
    print("""
  [1] List connected devices
  [2] Send SMS
  [3] Make a call
  [4] End current call
  [5] Answer incoming call
  [6] Show call state
  [0] Exit
""")


def main():
    show_banner()
    if not adb_available():
        print("[-] 'adb' not found. Install Android platform-tools and add it to PATH.")
        sys.exit(1)
    run_adb(["start-server"])
    serial = pick_device()

    while True:
        menu()
        choice = input("Select option: ").strip()
        if choice == "0":
            print(f"Goodbye!  - {CREDIT}")
            break
        if choice == "1":
            devs = get_devices()
            if not devs:
                print("[-] No devices.")
            for s, st in devs:
                print(f"  {s}\t{st}")
            continue
        if choice in {"2", "3", "4", "5", "6"}:
            if not serial:
                serial = pick_device()
                if not serial:
                    continue
            if choice == "2":
                sms_menu(serial)
            elif choice == "3":
                call_menu(serial)
            elif choice == "4":
                print("[+] Call ended." if end_call(serial)[0] else "[-] Failed.")
            elif choice == "5":
                print("[+] Answered." if answer_call(serial)[0] else "[-] Failed.")
            elif choice == "6":
                print("Call state:", call_state(serial))
        else:
            print("[-] Invalid option.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nExiting. {CREDIT}")
