import logging
import sys
import can

LOGGER = logging.getLogger(__name__)


class CanBus:
    def __init__(self, interface, sender):
        self.interface = interface
        self.sender = int(str(sender), 16)

    def __enter__(self):
        try:
            self.bus = can.interface.Bus(
                channel=self.interface,
                bustype='socketcan',
                bitrate=20000
            )

            return self
        except OSError:
            LOGGER.error('Can not connect to interface "%s".', self.interface)
            sys.exit(1)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.notifier.stop()
        self.bus.shutdown()

    def print_message(self, msg: can.Message) -> None:
        print(msg)

    def send(self, data):
        msg = can.Message(
            arbitration_id=self.sender,
            data=data,
            is_extended_id=False
        )
        self.bus.send(msg)

    def notifier(self, listener):
        self.notifier = can.Notifier(self.bus, [listener])
