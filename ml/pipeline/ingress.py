"""Bounded live-source ingress: retain one latest decoded frame."""
import threading
import time


class LatestFrameSource:
    def __init__(self, capture, timeout=5):
        self.capture, self.timeout = capture, timeout
        self.condition = threading.Condition()
        self.latest = None
        self.closed = False
        self.error = False
        self.started_at = time.monotonic()
        self.thread = threading.Thread(target=self._read, daemon=True)
        self.thread.start()

    def _read(self):
        index = -1
        try:
            while not self.closed:
                ok, frame = self.capture.read()
                received = time.monotonic()
                if not ok:
                    break
                index += 1
                with self.condition:
                    self.latest = (index, (received-self.started_at)*1000, received, frame)
                    self.condition.notify_all()
        except Exception:
            self.error = True
        finally:
            with self.condition:
                self.closed = True
                self.condition.notify_all()

    def read(self):
        with self.condition:
            ready = self.condition.wait_for(lambda: self.latest is not None or self.closed, self.timeout)
            if not ready:
                raise TimeoutError('live source stopped producing frames')
            value, self.latest = self.latest, None
            return value

    def close(self):
        self.closed = True
        self.capture.release()
        with self.condition:
            self.condition.notify_all()
        self.thread.join(timeout=1)
