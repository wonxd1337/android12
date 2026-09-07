import subprocess
import re

def run_root(cmd):
    try:
        res = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception as e:
        return str(e)

def get_all_roblox_packages():
    out = run_root("pm list packages | grep 'com.roblox'")
    if out:
        return [line.replace("package:", "").strip() for line in out.splitlines() if line.strip()]
    return []

def test_android12_grid_auto():
    print("--- DIAGNOSTIK WINDOW ANDROID 12 (AUTO DETECT) ---")
    
    # 1. Cek Resolusi Layar & Density
    size = run_root("wm size")
    density = run_root("wm density")
    print(f"[1] Layar: {size} | {density}\n")
    
    # Deteksi otomatis package com.roblox
    packages = get_all_roblox_packages()
    if not packages:
        print("[2] Tidak ditemukan package dengan prefix 'com.roblox'.")
        return
    
    print(f"[2] Ditemukan {len(packages)} package: {packages}\n")
    
    for i, pkg in enumerate(packages, 1):
        print(f"--- [Pemeriksaan {i}] {pkg} ---")
        
        # Cek apakah aplikasi berjalan
        pid = run_root(f"pidof {pkg}")
        if not pid:
            print(f"    Status: Tidak berjalan (Offline)\n")
            continue
        print(f"    Status: Aktif dengan PID: {pid}")
        
        # Cek Task ID untuk Android 12 Freeform/Split
        activities_dump = run_root(f"dumpsys activity activities | grep -i {pkg}")
        print(f"    Status Activity:\n    {activities_dump[:250]}...")
        
        # Cek Window Focus terkait package
        focus = run_root(f"dumpsys window windows | grep -i {pkg}")
        print(f"    Window Match:\n    {focus[:250] if focus else 'Tidak ada window aktif'}\n")
    
    print("--- SELESAI ---")

if __name__ == "__main__":
    test_android12_grid_auto()
