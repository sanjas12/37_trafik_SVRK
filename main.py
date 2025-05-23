import pyshark
import pandas as pd
from pathlib import Path
from datetime import datetime
from config import FILTER, OUTPUT_CSV
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("log.log")]
)
logger = logging.getLogger(__name__)

# Константы
PCAP_DIR = Path("data_in")
SUPPORTED_EXTENSIONS = ('.pcap', '.pcapng')
CSV_COLUMNS = ['timestamp', 'payload', 'file']

def check_pcap_directory() -> bool:
    """Проверяет существование и валидность директории с PCAP файлами."""
    if not PCAP_DIR.exists():
        logger.warning(f"Directory {PCAP_DIR} not found. Creating new one.")
        PCAP_DIR.mkdir(parents=True, exist_ok=True)
        return False
    
    if not PCAP_DIR.is_dir():
        logger.error(f"{PCAP_DIR} exists but is not a directory!")
        return False
    
    if not any(PCAP_DIR.iterdir()):
        logger.info(f"Directory {PCAP_DIR} exists but is empty.")
        return False
    
    logger.info(f"Directory {PCAP_DIR} found and contains files")
    return True

def process_packet(packet, pcap_filename: str) -> dict:
    """Обрабатывает отдельный пакет и возвращает словарь с данными."""
    try:
        # Проверяем наличие payload (полезной нагрузки)
        if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'payload'):
            payload = packet.tcp.payload.strip()
            if not payload:  # Если payload пустой
                return None
        else:
            return None  # Нет payload - пропускаем пакет

        packet_data = {
            "timestamp": packet.sniff_time,
            "payload": payload,
            "file": pcap_filename,
        }
        return packet_data

    except AttributeError as e:
        logger.warning(f"Packet processing error: {e}")
        return None

def save_to_csv(data: list, output_file: str) -> bool:
    """Сохраняет данные в CSV, пропуская пустые строки."""
    if not data:
        logger.warning("No data to save.")
        return False
    
    try:
        df = pd.DataFrame(data)
        
        # Убеждаемся, что все нужные колонки существуют
        for col in CSV_COLUMNS:
            if col not in df.columns:
                df[col] = None  # Добавляем отсутствующие колонки
        
        # Выбираем только нужные колонки
        df = df[CSV_COLUMNS]
        
        # Удаляем строки, где payload пустой
        df_cleaned = df[df['payload'].notna() & (df['payload'] != '')]
        
        if df_cleaned.empty:
            logger.warning("No valid data to save after cleaning.")
            return False
        
        # Сохраняем в CSV
        df_cleaned.to_csv(output_file, index=False, sep=';')
        logger.info(f"Data successfully saved to {output_file}")
        return True
    
    except Exception as e:
        logger.error(f"Error saving to CSV: {e}")
        return False

def main():
    """Основная функция обработки PCAP файлов."""
    if not check_pcap_directory():
        return

    pcap_files = [
        f for ext in SUPPORTED_EXTENSIONS 
        for f in PCAP_DIR.glob(f"*{ext}")
    ]

    logger.info(f"Found {len(pcap_files)} traffic files")

    results = []
    start_time = datetime.now()

    for pcap_file in pcap_files:
        logger.info(f"Processing file: {pcap_file.name}")
        
        try:
            with pyshark.FileCapture(str(pcap_file), display_filter=FILTER) as capture:
                for packet in capture:
                    processed = process_packet(packet, pcap_file.name)
                    if processed:
                        results.append(processed)
        except Exception as e:
            logger.error(f"Error processing file {pcap_file.name}: {e}")

    # Сохраняем результаты
    save_to_csv(results, OUTPUT_CSV)
    logger.info(f"Total processing time: {datetime.now() - start_time}")

if __name__ == "__main__":
    main()