import subprocess
import time

def run_root(cmd):
    try:
        res = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""

pkg = "com.roblox.client"
uri = "https://www.roblox.com/share?code=a219beb20055cb42b51dc9c8281d116d&type=Server"

print("Silakan keluar ke Home Screen... Tools akan berjalan dalam 10 detik.")
for i in range(10, 0, -1):
    print(f"Mulai dalam {i} detik...", end="\r", flush=True)
    time.sleep(1)
print("\nMenjalankan perintah...")

# Perintah inti untuk membuka aplikasi langsung ke format bebas dengan private server
run_root(f'am start --windowingMode 5 -a android.intent.action.VIEW -d "{uri}" {pkg}')
