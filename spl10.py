su -c '
# 1. Matikan dulu aplikasi agar bersih dari cache sisa
am force-stop com.roblox.client

# 2. Buka awal dalam mode window (freeform / mode 5)
am start --windowingMode 5 com.roblox.client

echo "Aplikasi dibuka di mode window, menunggu inisialisasi..."

# 3. Tunggu 4 detik agar engine game sempat merender surface di awal
sleep 4

# 4. Tangkap taskId secara otomatis dari sistem
TASK_ID=$(dumpsys activity activities | grep -i "com.roblox.client" | grep -o "taskId=[0-9]*" | tail -n 1 | cut -d= -f2)

if [ ! -z "$TASK_ID" ]; then
    echo "Task ID $TASK_ID ditemukan! Mengubah ukuran ke fullscreen..."
    
    # 5. Ubah ukuran task tersebut menjadi menutupi seluruh layar (Fullscreen)
    # (Ganti 720 1280 dengan resolusi lebar & tinggi layar Anda)
    am task resize "$TASK_ID" 0 0 720 1280
    
    echo "Berhasil di-resize!"
else
    echo "Gagal mendeteksi taskId."
fi
'
