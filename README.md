# 🌐 Legion DNS Manager

![Platform](https://img.shields.io/badge/Platform-Windows-0078d7?logo=windows&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&style=flat-square)
![PyQt5](https://img.shields.io/badge/UI-PyQt5-green?logo=qt&style=flat-square)
![License](https://img.shields.io/badge/License-MIT-orange?style=flat-square)

**Legion DNS Manager** is a lightweight, modern GUI application for Windows that allows you to easily switch between custom IPv4 DNS servers. Say goodbye to digging through Windows Network Adapter settings—change, reset, or flush your DNS with a single click.

## ✨ Features

* **Modern UI:** A beautiful, dark-themed interface built with PyQt5.
* **Profile Management:** Add, save, and delete custom DNS profiles (e.g., Google, Cloudflare, OpenDNS).
* **One-Click Apply:** Quickly apply your chosen DNS profile to all active physical network adapters.
* **Auto-Reset:** Revert back to automatic DNS (DHCP) instantly.
* **Flush Cache:** Built-in utility to silently flush the Windows DNS cache (`ipconfig /flushdns`).
* **Persistent Data:** Your DNS profiles are safely saved locally in your `%APPDATA%` folder.
* **Smart Elevation:** Automatically prompts for Windows Administrator privileges only when applying network changes.

## 📸 Screenshot
<img width="452" height="632" alt="image" src="https://github.com/user-attachments/assets/93ab8ebb-03f0-43eb-b0da-b7f02294982b" />


## 🚀 Installation & Setup

### Prerequisites
* Windows OS (Required for PowerShell network commands)
* [Python 3.10+](https://www.python.org/downloads/)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/seniorherton/LegionDNS.git](https://github.com/seniorherton/LegionDNS.git)
   cd LegionDNS
