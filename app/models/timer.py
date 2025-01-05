import time, threading

class formatter:
    def format_centi(self, seconds):
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centi = int((seconds * 100) % 100)

        return f"{hours:02}:{mins:02}:{secs:02}:{centi:02}"
    
    def format_secs(self, seconds):
        sign = "-" if seconds < 0 else ""
        seconds = abs(seconds)
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)

        return f"{sign}{hours:02}:{mins:02}:{secs:02}"
    
    def delta_time(self, time1, time2):
        start_seconds = time.mktime(time1)
        end_seconds = time.mktime(time2)
        elapsed_time = end_seconds - start_seconds

        return self.format_secs(elapsed_time)

class Stopwatch(formatter):
    def __init__(self):
        self._running = False
        self._elapsed_time = 0
        self._start_time = None

        self.recordStart = None
        self.recordStop = None

    def start(self):
        if not self._running:
            self.recordStart = time.localtime()
            self._running = True
            self._start_time = time.time()

            self._update_thread = threading.Thread(target=self._update, daemon=True)
            self._update_thread.start()
    
    def _update(self):
        while self._running:
            current_time = time.time()
            elapsed = (current_time - self._start_time)
            self._elapsed_time += elapsed
            self._start_time = current_time
            time.sleep(0.01)

    def stop(self):
        if self._running:
            self.recordStop = time.localtime()
            self._running = False
            self._elapsed_time += (time.time() - self._start_time)
            self._start_time = None

    def reset(self):
        self._running = False
        self._elapsed_time = 0
        self._start_time = 0

        self.recordStart = None
        self.recordStart = None

    def get_running(self):
        return self._running

    def get_time(self):
        return self.format_centi(self._elapsed_time)
    
    def StartEndLocal(self):
        try:
            return [time.strftime("%H:%M:%S", self.recordStart), time.strftime("%H:%M:%S", self.recordStop)]
        except TypeError:
            return None

class Timer(formatter):
    def __init__(self, duration = 300, no_overflow = True):
        self._running = False
        self._duration = duration
        self._remaining_time = self._duration
        self._start_time = None

        self.no_overflow = no_overflow

        self.recordStart = None
        self.recordEnd = None

    def start(self):
        if not self._running:
            self._running = True
            self._start_time = time.time()
            self._update_thread = threading.Thread(target=self._update, daemon=True)
            self._update_thread.start()
            self.recordStart = time.localtime()

    def _update(self):
        while self._running:
            current_time = time.time()
            elapsed = (current_time - self._start_time)
            self._remaining_time -= elapsed
            self._start_time = current_time
            if self.no_overflow and (self._remaining_time <= 0): # If the timer dose not allow overflows
                self._remaining_time = 0
                self.stop()
                return "Timer End"

            time.sleep(0.01)

    def stop(self):
        if self._running:
            self._running = False
            self._remaining_time -= (time.time() - self._start_time)
            self._start_time = None
            self.recordEnd = time.localtime()
    
    def reset(self):
        self._running = False
        self._remaining_time = self._duration
        self._start_time = None

        self.recordStart = None
        self.recordEnd = None

    def get_time(self):
        return self.format_secs(self._remaining_time)
    
    def get_running(self):
        return self._running
    
    def StartEndLocal(self):
        try:
            return [time.strftime("%H:%M:%S", self.recordStart), time.strftime("%H:%M:%S", self.recordEnd)]
        except TypeError:
            return None
    
class LocalTime(formatter):
    def __init__(self):
        self._running = False
        self._current_time = None

    def start(self):
        if not self._running:
            self._running = True
            self._update_thread = threading.Thread(target=self._update, daemon=True)
            self._update_thread.start()

    def _update(self):
        while self._running:
            self._current_time = time.localtime()
            time.sleep(1)
    
    def stop(self):
        self._running = False
    
    def get_time(self):
        return time.strftime("%H:%M:%S", self._current_time) if self._current_time else None

