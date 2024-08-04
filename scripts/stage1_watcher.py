import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from stage1 import extract_relevant_data
from utils.utils_funcs import load_config


class Stage1Handler(FileSystemEventHandler):
    """
        Generate a raw data file using the experiment ID
    """
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            experiment_id = os.path.basename(event.src_path).split('.')[0]
            print(f"Detected new file for Stage 1: {experiment_id}")
            extract_relevant_data(experiment_id)


if __name__ == "__main__":
    config = load_config()
    path = config['paths']['raw_experiment_data']
    event_handler = Stage1Handler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
