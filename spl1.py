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

def get_all_roblox_packages():
    out = run_root("pm list packages | grep 'com.roblox'")
    if out:
        return [line.replace("package:", "").strip() for line in out.splitlines() if line.strip()]
    return []

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
    return 1280, 720 # Fallback

def get_running_packages():
    installed = get_all_roblox_packages()
    running_info = []
    for pkg in installed:
        pid = run_root(f"pidof {pkg}")
        if pid:
            running_info.append(pkg)
    return running_info

def get_task_id(pkg):
    # Mengambil Task ID dari dumpsys activity untuk manipulasi window Android 12
    lines = run_root("dumpsys activity activities").splitlines()
    for i, line in enumerate(lines):
        if pkg in line:
            for j in range(max(0, i-6), min(len(lines), i+6)):
                m = re.search(r'taskId=(\d+)', lines[j])
                if m:
                    return int(m.group(1))
    return None

def resize_task_android12(task_id, l, t, r, b):
    # Perintah resize task bawaan Android 12 via am task
    run_root(f"am task resize {task_id} {l} {t} {r} {b}")

def test_auto_split_grid():
    print("=== TEST AUTO SPLIT & GRID ANDROID 12 ===")
    screen_w, screen_h = get_screen_size()
    print(f"Resolusi Layar: {screen_w}x{screen_h}\n")
    print("Menunggu game dengan prefix 'com.roblox' berjalan...")

    last_state = []

    while True:
        try:
            running_pkgs = get_running_packages()
            
            # Jika ada perubahan status aplikasi yang berjalan
            if running_pkgs != last_state:
                print(f"\n[{time.strftime('%H:%M:%S')}] Deteksi perubahan game aktif: {running_pkgs}")
                last_state = running_pkgs.copy()
                
                if running_pkgs:
                    total = len(running_pkgs)
                    cols = math.ceil(math.sqrt(total))
                    rows = math.ceil(total / cols)
                    
                    win_w = screen_w // cols
                    win_h = screen_h // rows
                    
                    for index, pkg in enumerate(running_pkgs):
                        col = index % cols
                        row = index // cols
                        left = col * win_w
                        top = row * win_h
                        right = left + win_w
                        bottom = top + win_h
                        
                        print(f"  -> Memproses {pkg} ke Grid [{col},{row}] -> Box({left}, {top}, {right}, {bottom})")
                        
                        # Cari Task ID Android 12
                        task_id = get_task_id(pkg)
                        if task_id:
                            print(f"     Task ID ditemukan ({task_id}), menerapkan resize...")
                            resize_task_android12(task_id, left, top, right, bottom)
                        else:
                            print(f"     Task ID tidak ditemukan untuk {pkg}, pastikan aplikasi berada di foreground.")
                else:
                    print("  -> Tidak ada game com.roblox yang sedang berjalan.")
            
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nTest dihentikan.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    test_auto_split_grid()
