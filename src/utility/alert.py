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

import os
import simpleaudio

class Alert:
    """
    Class for handling alerts for item availability, including voice alerts if enabled.
    """

    logger = None
    config = None
    alert_audio_file_path = os.path.join(os.path.dirname(__file__), "resources", "alert.wav")

    def __init__(self, logger, config):
        """
        Initializes the Alert object with the specified logger and configuration.

        Args:
            logger: The logger object for logging messages.
            config: Configuration settings for the alert system.
        """
        self.logger = logger
        self.config = config

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
        if self.config['audio_alerts']:
            self.make_sound()

    def make_sound(self):
        """
        Play the alert audio file.
        """
        try:
            wave_obj = simpleaudio.WaveObject.from_wave_file(self.alert_audio_file_path)
            play_obj = wave_obj.play()
            play_obj.wait_done()
        except Exception as e:
            raise e
