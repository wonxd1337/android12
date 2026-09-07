import subprocess
import time
import re
import math

def run_root(cmd):
    try:
        res = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ""

def get_screen_size():
    try:
        out = run_root("dumpsys window displays | grep 'cur='")
        match = re.search(r'cur=(\d+)x(\d+)', out)
        if match: 
            return int(match.group(1)), int(match.group(2))
        
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

def get_dynamic_offset():
    try:
        out = run_root("wm density")
        match = re.findall(r'\d+', out)
        dpi = int(match[-1]) if match else 240
    except:
        dpi = 240
    return int(50 * (dpi / 160))

def get_grid_layout(item_index, total_items):
    if total_items <= 0:
        return 0, 0, 0, 0
    cols = math.ceil(math.sqrt(total_items))
    rows = math.ceil(total_items / cols)
    if cols > 2 and (cols - 1) * rows >= total_items:
        cols -= 1
        
    SCREEN_W, SCREEN_H = get_screen_size()
    TOP_OFFSET = get_dynamic_offset() 
    available_h = SCREEN_H - TOP_OFFSET
    
    win_w = SCREEN_W // cols
    win_h = available_h // rows
    
    col = item_index % cols
    row = item_index // cols 
    
    left = col * win_w
    top = (row * win_h) + TOP_OFFSET
    right = left + win_w
    bottom = top + win_h
    
    return left, top, right, bottom

def get_task_id(pkg):
    lines = run_root("dumpsys activity activities").splitlines()
    for i, line in enumerate(lines):
        if pkg in line:
            for j in range(max(0, i-6), min(len(lines), i+6)):
                m = re.search(r'taskId=(\d+)', lines[j])
                if m:
                    return int(m.group(1))
    return None

def launch_smart_grid(pkg, uri, index=0, total=1):
    print("Silakan keluar ke Home Screen... Tools akan berjalan dalam 10 detik.")
    for i in range(10, 0, -1):
        print(f"Mulai dalam {i} detik...", end="\r", flush=True)
        time.sleep(1)
    print("\nMenghitung posisi grid cerdas...")

    # 1. Hitung koordinat menggunakan logika grid cerdas
    left, top, right, bottom = get_grid_layout(index, total)
    print(f"-> Target Grid Posisi [{index} dari {total}]: L={left}, T={top}, R={right}, B={bottom}")

    # 2. Buka aplikasi langsung dengan parameter --windowingMode 5 dan URI private server
    print(f"-> Membuka {pkg} ke mode Freeform...")
    run_root(f'am start --windowingMode 5 -a android.intent.action.VIEW -d "{uri}" {pkg}')

    # 3. Beri jeda agar sistem mengalokasikan task window
    time.sleep(2.0)

    # 4. Ambil Task ID, resize sesuai grid, lalu switch ke foreground / focus
    task_id = get_task_id(pkg)
    if task_id:
        print(f"-> Task ID ditemukan ({task_id}), menerapkan ukuran grid & memindahkan ke foreground...")
        run_root(f"am task resize {task_id} {left} {top} {right} {bottom}")
        run_root(f"am task switch {task_id}")
        print("Berhasil! Jendela aplikasi masuk ke posisi grid layar dan aktif sepenuhnya.")
    else:
        print("[!] Gagal mendeteksi Task ID aplikasi.")

if __name__ == "__main__":
    pkg = "com.roblox.client"
    uri = "https://www.roblox.com/share?code=a219beb20055cb42b51dc9c8281d116d&type=Server"
    
    launch_smart_grid(pkg, uri, index=0, total=1)
