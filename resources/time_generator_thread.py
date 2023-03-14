import threading
import random
import datetime
import time


class TimeGenerator:
    def __init__(self):
        self.current_time = datetime.datetime(2022, 3, 3)

    def run(self):
        while True:
            # Increment time by a random number of seconds
            increment = random.randint(2400, 12000)
            self.current_time += datetime.timedelta(seconds=increment)
            time.sleep(1)


class DataGenerator:
    def __init__(self, time_generator):
        self.time_generator = time_generator

    def run(self):
        while True:
            print(f"Current time: {self.time_generator.current_time}")
            time.sleep(5)


class App:
    def __init__(self):
        self.time_generator = TimeGenerator()
        self.data_generator = DataGenerator(self.time_generator)

    def run(self):
        # Start time generator thread
        time_thread = threading.Thread(target=self.time_generator.run)
        time_thread.daemon = True
        time_thread.start()

        # Start data generator thread
        data_thread = threading.Thread(target=self.data_generator.run)
        data_thread.daemon = True
        data_thread.start()

        # Wait for threads to complete (which they won't in this case)
        time_thread.join()
        data_thread.join()

app = App()
app.run()