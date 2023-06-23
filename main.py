import os
import libtorrent as lt
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

h_list = []  # Список объектов torrent_handle для каждого торрент-файла
ses = None  # Объект session
is_paused = False  # Флаг для отслеживания состояния паузы

def update_progress():
    for h, progress_label, download_label, upload_label, status_label in h_list:
        s = h.status()
        progress = s.progress * 100
        download_speed = s.download_rate / 1000000
        upload_speed = s.upload_rate / 1000000
        progress_label.config(text="Прогресс: %.2f%%" % progress)
        download_label.config(text="Скорость загрузки: %.1f MB/s" % download_speed)
        upload_label.config(text="Скорость раздачи: %.1f MB/s" % upload_speed)
        if not h.is_seed():
            if not is_paused:
                root.after(1000, update_progress)
        else:
            status_label.config(text="Загрузка/раздача завершена")

def select_torrent_file():
    file_path = filedialog.askopenfilename(filetypes=[("Torrent Files", "*.torrent")])
    if file_path:
        load_torrent_file(file_path)

def load_torrent_file(file_path):
    global h_list, ses, is_paused

    # Создание сессии Bittorrent, если она не была создана
    if not ses:
        ses = lt.session()
        ses.listen_on(6881, 6891)  # Прослушивание портов для входящих соединений
        ses.start_dht()  # Запуск DHT
        ses.add_dht_router("router.bittorrent.com", 6881)  # Добавление DHT роутера

    # Добавление торрент-файла в сессию
    info = lt.torrent_info(file_path)
    save_directory = os.path.join(os.path.dirname(os.path.abspath(file_path)), info.name())
    h = ses.add_torrent({"ti": info, "save_path": save_directory})
    h_list.append((h, None, None, None, None))  # Добавление новой записи в список h_list

    # Создание и настройка элементов интерфейса для нового торрент-файла
    create_torrent_widgets(h, info)

    # Если торрент был на паузе, продолжаем его загрузку/раздачу
    if is_paused:
        h.resume()
        is_paused = False

    # Запуск обновления прогресса
    root.after(1000, update_progress)

def create_torrent_widgets(h, info):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=info.name())

    progress_label = tk.Label(frame, text="Прогресс: 0.00%")
    progress_label.pack()

    download_label = tk.Label(frame, text="Скорость загрузки: 0.0 MB/s")
    download_label.pack()

    upload_label = tk.Label(frame, text="Скорость раздачи: 0.0 MB/s")
    upload_label.pack()

    pause_button = tk.Button(frame, text="Пауза", command=lambda: toggle_pause(h))
    pause_button.pack()

    status_label = tk.Label(frame, text="")
    status_label.pack()

    # Обновление соответствующей записи в h_list с новыми элементами интерфейса
    for i, (handle, _, _, _, _) in enumerate(h_list):
        if handle == h:
            h_list[i] = (handle, progress_label, download_label, upload_label, status_label)
            break

def toggle_pause(handle):
    global is_paused
    for h, _, _, _, _ in h_list:
        if h == handle:
            if h.is_valid() and not h.is_seed():
                if is_paused:
                    h.resume()
                    is_paused = False
                else:
                    h.pause()
                    is_paused = True
            break

# Создание графического интерфейса
root = tk.Tk()
root.title("CRACKSTATUS Launcher")

# Создание вкладок
notebook = ttk.Notebook(root)
notebook.pack()

# Создание основной вкладки
main_frame = ttk.Frame(notebook)
notebook.add(main_frame, text="Главная")

select_button = tk.Button(main_frame, text="Выбрать торрент-файл", command=select_torrent_file)
select_button.pack()

root.mainloop()