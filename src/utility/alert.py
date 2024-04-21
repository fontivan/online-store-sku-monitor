# MIT License
#
# Copyright (c) 2020 fontivan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
TODO: Add header
"""

import threading
import time
import pyttsx3

class Alert:
    """
    TODO: Add header
    """
    engine = None
    logger = None
    config = None

    # A lock must be used because the voice engine can only say one message at a time
    voice_alert_queue_lock = None
    voice_alert_queue = []
    voice_alert_thread = None

    def __init__(self, logger, config):
        self.logger = logger
        self.config = config

        if self.config['voice_alerts']:
            try:
                self.engine = pyttsx3.init()
                msg = "Voice alerts are enabled"
                self.logger.info(f"[[ alert ]] :: {msg}")
                self.voice_alert_queue_lock = threading.Lock()
                self.send_voice_msg_to_queue(msg)
                self.voice_alert_thread = threading.Thread(
                    target=self.process_voice_queue
                )
                self.voice_alert_thread.start()
            except OSError as e:
                self.logger.warn(f"Voice alerts unavailable due to exception: \'{e}\'")
    def send_alert(self, item, vendor_name):
        """
        TODO: Add header
        """
        msg = f"Item in stock \'{item['name']}\'"
        self.logger.critical(f"[[ {vendor_name} ]] :: {msg} at \'{item['url']}")
        if self.config['voice_alerts'] and self.engine is not None:
            self.send_voice_msg_to_queue(f"{msg} at {vendor_name}")

    def send_voice_msg_to_queue(self, msg):
        """
        TODO: Add header
        """
        # Replace _ca with ". c a" so the output sounds better
        msg = msg.replace("_ca", " . c a")
        # Replace _com with ". com" so the output sounds better
        msg = msg.replace("_com", ". com")

        # Acquire lock and add message to the queue
        with self.voice_alert_queue_lock:
            self.voice_alert_queue.append(msg)

    def process_voice_queue(self):
        """
        TODO: Add header
        """
        try:
            while True:
                # Acquire lock and check for a message
                with self.voice_alert_queue_lock:
                    if len(self.voice_alert_queue) > 0:
                        msg = self.voice_alert_queue.pop(0)
                        self.engine.say(msg)
                        self.engine.runAndWait()
                time.sleep(1)
        except KeyboardInterrupt:
            return
