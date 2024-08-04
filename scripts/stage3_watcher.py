import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from stage3 import validate_hypothesis_across_experiments  # Import function from stage3.py
from utils.utils_funcs import load_config


class Stage3Handler(FileSystemEventHandler):
    """
        Validate the hypothesis across all the processed experiments
    """
    def __init__(self, config):
        self.config = config

    def on_created(self, event):
        if not event.is_directory:
            print("Detected new file for Stage 3, recalculating hypothesis accuracy.")
            # Call the function from stage3.py directly
            validate_hypothesis_across_experiments()


if __name__ == "__main__":
    config = load_config()
    path = config['paths']['final_output']
    event_handler = Stage3Handler(config)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
