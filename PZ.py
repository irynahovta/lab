import socket
from contextlib import closing

def check_port(host, port, timeout=1):
    """
    Перевіряє, чи відкритий порт на вказаному хості.
    
    :param host: IP-адреса або ім'я хоста для перевірки.
    :param port: Номер порту для перевірки.
    :param timeout: Таймаут для з'єднання (за замовчуванням 1 секунда).
    :return: True, якщо порт відкритий, False інакше.
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        return result == 0

def scan_single_port(host, port):
    """
    Сканує один порт і виводить результат.
    
    :param host: IP-адреса або ім'я хоста для перевірки.
    :param port: Номер порту для перевірки.
    """
    if check_port(host, port):
        print(f"Порт {port} відкритий на {host}")
    else:
        print(f"Порт {port} закритий на {host}")

def scan_multiple_ports(host, ports):
    """
    Сканує список портів на вказаному хості.
    
    :param host: IP-адреса або ім'я хоста для перевірки.
    :param ports: Список портів для сканування.
    """
    print(f"Сканування портів {ports} на {host}...")
    for port in ports:
        status = "відкритий" if check_port(host, port) else "закритий"
        print(f"Порт {port} {status}")

def scan_port_range(host, start_port, end_port):
    """
    Сканує діапазон портів на вказаному хості.
    
    :param host: IP-адреса або ім'я хоста для перевірки.
    :param start_port: Початковий порт діапазону.
    :param end_port: Кінцевий порт діапазону.
    """
    print(f"Сканування портів від {start_port} до {end_port} на {host}...")
    for port in range(start_port, end_port + 1):
        if check_port(host, port, timeout=0.5):
            print(f"Порт {port} відкритий")

# Приклад використання
host = "127.0.0.1"

# Сканування одного порту
scan_single_port(host, 80)

# Сканування вибраних портів
scan_multiple_ports(host, [22, 80, 443])

# Сканування діапазону портів
scan_port_range(host, 1, 1024)
