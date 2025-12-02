import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mpv import MPV

MUSIC_DIR = os.path.expanduser("~/Music/YTMusic")

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, player):
        self.player = player

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".mp3"):
            print(f"Nuevo archivo detectado: {event.src_path}")
            self.player.command('loadfile', event.src_path, 'append')

def main():
    player = MPV(ytdl=True, input_default_bindings=True, input_vo_keyboard=True)
    files = [os.path.join(MUSIC_DIR, f) for f in os.listdir(MUSIC_DIR) if f.endswith(".mp3")]
    if files:
        player.playlist_clear()
        for f in files:
            player.command('loadfile', f, 'append')
        player.playlist_pos = 0
    else:
        print("No hay archivos para reproducir todavía.")

    event_handler = NewFileHandler(player)
    observer = Observer()
    observer.schedule(event_handler, MUSIC_DIR, recursive=False)
    observer.start()

    print("Reproduciendo MPV, monitoreando carpeta para nuevas canciones...")
    try:
        player.wait_until_playback_starts()
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
