import subprocess
import time
import re

def run_root(cmd):
    try:
        res = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""

def get_screen_size():
    try:
        out_wm = run_root("wm size")
        for line in out_wm.splitlines():
            if "Override size:" in line or "Physical size:" in line:
                size_str = line.split(":")[1].strip()
                if "x" in size_str:
                    w, h = size_str.split("x")
                    return int(w), int(h)
    except Exception:
        pass
    return 1280, 720

def get_task_id(pkg):
    lines = run_root("dumpsys activity activities").splitlines()
    for i, line in enumerate(lines):
        if pkg in line:
            for j in range(max(0, i-6), min(len(lines), i+6)):
                m = re.search(r'taskId=(\d+)', lines[j])
                if m:
                    return int(m.group(1))
    return None

def launch_and_grid(pkg, uri):
    screen_w, screen_h = get_screen_size()
    
    # 1. Buka aplikasi langsung dalam mode format bebas (Freeform)
    run_root(f'am start --windowingMode 5 -a android.intent.action.VIEW -d "{uri}" {pkg}')
    
    # 2. Beri jeda agar sistem membuat task window
    time.sleep(2.0)
    
    # 3. Tangkap Task ID lalu atur ukuran & posisinya agar pas di layar (tidak off-screen)
    task_id = get_task_id(pkg)
    if task_id:
        # Contoh ukuran grid setengah layar (sesuaikan koordinat left, top, right, bottom)
        left, top, right, bottom = 0, 100, screen_w // 2, screen_h
        run_root(f"am task resize {task_id} {left} {top} {right} {bottom}")
        print(f"Berhasil meluncurkan {pkg} (Task ID: {task_id}) ke dalam grid on-screen.")
    else:
        print("Gagal mendeteksi Task ID aplikasi.")

if __name__ == "__main__":
    pkg = "com.roblox.client"
    uri = "https://www.roblox.com/share?code=a219beb20055cb42b51dc9c8281d116d&type=Server"
    
    print("Bersiap dalam 5 detik. Silakan posisikan ke Home Screen...")
    time.sleep(5)
    
    launch_and_grid(pkg, uri)
