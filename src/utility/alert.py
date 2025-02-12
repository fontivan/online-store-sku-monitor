# MIT License
#
# Copyright (c) 2020-2024 fontivan
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
This module contains the Alert class, which handles alerts for item
availability, including voice alerts if enabled.
"""

import threading
import time
import pyttsx3

class Alert:
    """
    Class for handling alerts for item availability, including voice alerts if enabled.
    """

    engine = None
    logger = None
    config = None

    # A lock must be used because the voice engine can only say one message at a time
    voice_alert_queue_lock = None
    voice_alert_queue = []
    voice_alert_thread = None

    def __init__(self, logger, config):
        """
        Initializes the Alert object with the specified logger and configuration.

        Args:
            logger: The logger object for logging messages.
            config: Configuration settings for the alert system.
        """
        self.logger = logger
        self.config = config

        if self.config['voice_alerts']:
            try:
                self.engine = pyttsx3.init()
                voices = self.engine.getProperty('voices')
                self.engine.setProperty('voice', voices[1].id)
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

    def send_alert(self, item, vendor_name, location):
        """
        Sends an alert for the availability of an item.

        Args:
            item: The item for which the alert is generated.
            vendor_name: The name of the vendor.
            location: The name of the location with the item.
        """
        msg = f"Item in stock \'{item['name']}\'"
        self.logger.critical(f"[[ {vendor_name} ]] :: {msg} at \'{item['url']}\' at \'{location}\'")
        if self.config['voice_alerts'] and self.engine is not None:
            self.send_voice_msg_to_queue(f"{msg} at {vendor_name} at {location}")

    def send_voice_msg_to_queue(self, msg):
        """
        Adds a voice message to the queue for processing.

        Args:
            msg: The message to be added to the queue.
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
        Processes the voice alert queue, speaking messages using the TTS engine.
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
        except KeyboardInterrupt as e:
            raise KeyboardInterrupt from e
