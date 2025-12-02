import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mpv import MPV

MUSIC_DIR = os.path.expanduser("~/Music/YTMusic")
MPV_SOCKET_PATH = "/tmp/mpvsocket"  # Puedes cambiar o eliminar si no usas IPC

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, player):
        self.player = player

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp3"):
            print(f"Nuevo archivo detectado: {event.src_path}")
            # Añadir a mpv en modo append
            self.player.command('loadfile', event.src_path, 'append')

def main():
    # Crear la instancia de mpv
    player = MPV(socket=MPV_SOCKET_PATH)
    # Iniciar la reproducción con archivos existentes
    files = [os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR) if f.endswith('.mp3')]
    if files:
        player.playlist_clear()
        for f in files:
            player.command('loadfile', f, 'append')
        player.playlist_pos = 0
    else:
        print("No hay archivos en la carpeta inicialmente.")

    # Iniciar monitoreo
    event_handler = NewFileHandler(player)
    observer = Observer()
    observer.schedule(event_handler, MUSIC_DIR, recursive=False)
    observer.start()

    print("Reproduciendo y monitoreando carpeta para nuevas canciones...")
    try:
        # Sleep o espera indefinida
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Cerrando...")
    finally:
        observer.stop()
        observer.join()
        player.terminate()

if __name__ == "__main__":
    main()
