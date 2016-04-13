from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import time


class MyHandler(LoggingEventHandler):
    def on_modified(self, event):
        print("Analysing")
        EmotiveInvestor.emotion_measure("$AAPL")
        EmotiveInvestor.emotion_measure("$GOOG")
        EmotiveInvestor.emotion_measure("$FB")

if __name__ == "__main__":
    path = 'C:/Users/MOYIN/Desktop/Dissertation/Development/WebSc/Tracker'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


