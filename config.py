# config.py

IP = "192.168.16.1"
PORT = 15002
FILTER = f'(ip.addr == {IP}) && (tcp.srcport == {PORT})' # Фильтр для анализа трафика

# Другие настройки (пример)
INPUT_FOLDER = "pcaps"       # Папка с .pcap файлами
OUTPUT_CSV = "filtered_traffic.csv"  # Выходной CSV-файл