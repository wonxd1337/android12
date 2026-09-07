import subprocess
import time
import re

package_name = "com.roblox.clienw"

# 1. Bersihkan proses lama
subprocess.run(["su", "-c", f"am force-stop {package_name}"])
time.sleep(1)

# 2. Buka aplikasi dalam mode freeform (windowingMode 5)
subprocess.run(["su", "-c", f"am start --windowingMode 5 -f 0x18000000 {package_name}"])
print("Membuka aplikasi di mode window...")

# 3. Tunggu hingga proses inisialisasi awal selesai
time.sleep(4)

# 4. Ambil data dumpsys secara utuh untuk di-parsing menggunakan Python
result = subprocess.run(
    ["su", "-c", "dumpsys activity activities"],
    capture_output=True,
    text=True
)
output = result.stdout

# 5. Cari taskId yang spesifik terikat dengan package Roblox menggunakan logika blok
task_id = None
blocks = output.split("Task{")
for block in blocks:
    if package_name in block:
        match = re.search(r"taskId=(\d+)", block)
        if match:
            task_id = match.group(1)

# 6. Eksekusi resize jika taskId berhasil ditemukan
if task_id:
    print(f"Task ID berhasil dideteksi: {task_id}")
    # Sesuaikan koordinat (left, top, right, bottom) di bawah ini sesuai ukuran yang diinginkan
    subprocess.run(["su", "-c", f"am task resize {task_id} 50 50 723 414"])
    print("Perintah resize telah dikirim ke sistem.")
else:
    print("Gagal menemukan Task ID. Pastikan aplikasi terbuka dengan benar.")
