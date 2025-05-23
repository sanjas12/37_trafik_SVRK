import pyshark
import pandas as pd
from pathlib import Path
from config import FILTER

# Фильтр Wireshark
filter_str = FILTER

# Папка с .pcap/.pcapng файлами
pcap_dir = Path("data_in")

def check_pcap_directory():
    # Проверяем существование папки
    if not pcap_dir.exists():
        print(f"⚠️ Папка {pcap_dir} не найдена. Создаём новую.")
        pcap_dir.mkdir(parents=True, exist_ok=True)
        return False
    
    # Проверяем, что это действительно папка
    if not pcap_dir.is_dir():
        print(f"❌ {pcap_dir} существует, но это не папка!")
        return False
    
    # Проверяем, что папка не пустая
    if not any(pcap_dir.iterdir()):
        print(f"ℹ️ Папка {pcap_dir} существует, но пуста.")
        return False
    
    print(f"✓ Папка {pcap_dir} найдена и содержит файлы")
    return True

check_pcap_directory()

# Список всех файлов .pcap/.pcapng
pcap_files = list(pcap_dir.glob("*.pcap")) + list(pcap_dir.glob("*.pcapng"))

print(f"Найдено {len(pcap_files)} файлов c трафиком")

results = []

for pcap_file in pcap_files:
    print(f"Обработка файла: {pcap_file.name}")
    
    # Чтение файла с фильтром
    capture = pyshark.FileCapture(str(pcap_file), display_filter=filter_str)
    
    for packet in capture:
        try:
            # Извлекаем нужные данные (пример)
            src_ip = packet.ip.src
            dst_ip = packet.ip.dst
            src_port = packet.tcp.srcport
            dst_port = packet.tcp.dstport
            payload = packet.tcp.payload if hasattr(packet.tcp, 'payload') else ""

            results.append({
                # "source_ip": src_ip,
                # "dest_ip": dst_ip,
                # "source_port": src_port,
                # "dest_port": dst_port,
                "payload": payload,
                "timestamp": packet.sniff_time,
                # "file": pcap_file.name,
            })
        except AttributeError as e:
            print(f"Ошибка в пакете: {e}")
    
    capture.close()

# Сохраняем в CSV
df = pd.DataFrame(results)
df.to_csv("filtered_traffic.csv", index=False, sep=';')
print("Готово! Результат сохранён в filtered_traffic.csv")