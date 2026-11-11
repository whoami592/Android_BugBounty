# 🛡️ Android BugBounty — ADB SMS & Call Tool

> A lightweight, menu-driven Python tool to send SMS and control phone calls on **your own Android device** over ADB.

**Coded by: Cyber Security Engineer Mr. Sabaz Ali Khan**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Dependencies](https://img.shields.io/badge/Dependencies-stdlib%20only-brightgreen)
![Use](https://img.shields.io/badge/Use-Own%20devices%20only-orange)

---

## 📖 Overview

**Android BugBounty – ADB SMS & Call Tool** (`adb_sms_call_tool.py`) talks to an Android phone through the Android Debug Bridge (ADB). It is useful for Android testing, QA, telephony debugging and device automation in a lab or on your personal phone.

The tool uses only the Python standard library — no `pip install` needed.

## ✨ Features

| Feature | Description |
|---|---|
| 📱 Device detection | Lists connected devices, detects `unauthorized` / `offline` states, supports multiple devices |
| ✉️ Send SMS | Direct method (`service call isms`) with automatic fallback to the messaging-app UI method |
| 📞 Make a call | Starts a call using the `CALL` intent (supports `*` and `#` codes) |
| ❌ End call | Ends the current call (`KEYCODE_ENDCALL`) |
| ✅ Answer call | Answers an incoming call (`KEYCODE_CALL`) |
| 📊 Call state | Shows `IDLE`, `RINGING` or `OFFHOOK (in call)` via `dumpsys telephony.registry` |
| 🔒 Safe input handling | Phone-number validation and `shlex` quoting of all shell arguments |

## 🧰 Requirements

- Python **3.8+**
- Android **platform-tools** (`adb`) installed and available in your `PATH`
- An Android phone with:
  - **Developer options** enabled
  - **USB debugging** turned on
  - This computer **authorized** (accept the RSA prompt on the phone)
- A SIM card and an active network for SMS/calls to actually go through

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/android-bugbounty.git
cd android-bugbounty
```

Verify ADB sees your phone:

```bash
adb devices
```

You should see your device listed with the status `device`.

## 🚀 Usage

```bash
python3 adb_sms_call_tool.py
```

On Windows:

```bat
python adb_sms_call_tool.py
```

### Menu

```
  [1] List connected devices
  [2] Send SMS
  [3] Make a call
  [4] End current call
  [5] Answer incoming call
  [6] Show call state
  [0] Exit
```

### Example: sending an SMS

```
Select option: 2
Phone number (e.g. +923001234567): +923001234567
Message: Hello from ADB
Method:  1) Direct (service call)   2) Via messaging app UI
Choose [1/2, default 1]: 1
[+] SMS request sent.
```

### Example: making a call

```
Select option: 3
Phone number to call: +923001234567
[+] Call started.
```

## 🔍 How It Works

1. **Device selection** – runs `adb devices` and picks a ready device (asks you if more than one is connected).
2. **SMS (direct)** – calls the `isms` system service through `adb shell service call`. Parameters differ between Android versions, so the tool checks `ro.build.version.release` first.
3. **SMS (UI fallback)** – opens the default messaging app with the text prefilled (`SENDTO` intent) and simulates the Send key press.
4. **Calls** – uses `am start -a android.intent.action.CALL` and `input keyevent` to place, answer and end calls.

## ⚠️ Known Limitations

- The **direct SMS method** relies on internal service transaction codes that change between Android versions and OEM builds. It may fail on some devices; the tool then falls back to the UI method automatically.
- The **UI method** depends on the default messaging app's layout, so always verify on the phone screen.
- Some phones block the `CALL` intent or SMS sending from the shell on newer Android versions or when the device is locked.
- Result messages show that the **request was sent**, not that the SMS was delivered.

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `'adb' not found` | Install platform-tools and add it to your `PATH` |
| Device shows `unauthorized` | Unlock the phone and accept the USB debugging prompt |
| Device shows `offline` | Reconnect the cable, then run `adb kill-server && adb start-server` |
| No device found | Enable USB debugging, try another cable/port, set USB mode to *File transfer* |
| SMS not sent | Switch to method **2** (UI) and make sure the phone is unlocked and has a SIM |

## ⚖️ Legal Disclaimer

This tool is intended **only for devices you own or have explicit written permission to control**, such as personal phones, test devices and authorized security-research labs.

Sending messages or placing calls from a device without the owner's consent may be illegal. The author is **not responsible** for any misuse or damage caused by this software. By using it, you accept full responsibility for your actions.

## 🤝 Contributing

Pull requests and issues are welcome — especially for adding working SMS parameters for more Android versions.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Open a Pull Request

## 📜 License

Released under the **MIT License**. Add a `LICENSE` file to your repository to apply it.

---

<p align="center">
  <b>Coded by: Cyber Security Engineer Mr. Sabaz Ali Khan</b><br>
  <i>Android BugBounty — test responsibly.</i>
</p>
