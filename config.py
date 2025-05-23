# config.py
# Фильтр для анализа трафика
IP = "192.168.16.1"
PORT = 15002
FILTER = f'(ip.addr == {IP}) && (tcp.srcport == {PORT})'

# Другие настройки (пример)
INPUT_FOLDER = "pcaps"       # Папка с .pcap файлами
OUTPUT_CSV = "traffic.csv"  # Выходной CSV-файл