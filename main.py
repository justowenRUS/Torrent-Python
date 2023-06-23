import os
import libtorrent as lt
import tkinter as tk

def update_progress():
    s = h.status()
    progress = s.progress * 100
    download_speed = s.download_rate / 1000000
    upload_speed = s.upload_rate / 1000000
    progress_label.config(text="Прогресс: %.2f%%" % progress)
    download_label.config(text="Скорость загрузки: %.1f MB/s" % download_speed)
    upload_label.config(text="Скорость раздачи: %.1f MB/s" % upload_speed)
    if not h.is_seed():
        root.after(1000, update_progress)
    else:
        status_label.config(text="Загрузка/раздача завершена")

# Получение пути к папке "save" в текущей директории
save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save")

# Создание сессии Bittorrent
ses = lt.session()

# Добавление торрент-файла в сессию
info = lt.torrent_info("torrent/only-up-2023.torrent")
h = ses.add_torrent({"ti": info, "save_path": save_directory})

# Запуск загрузки/раздачи торрента
ses.start_dht()

# Создание графического интерфейса
root = tk.Tk()
root.title("BitTorrent Client")

progress_label = tk.Label(root, text="Прогресс: 0.00%")
progress_label.pack()

download_label = tk.Label(root, text="Скорость загрузки: 0.0 MB/s")
download_label.pack()

upload_label = tk.Label(root, text="Скорость раздачи: 0.0 MB/s")
upload_label.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.after(1000, update_progress)
root.mainloop()