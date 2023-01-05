import time
import logging

from .elster.elster import Elster
from .interface.can_bus import CanBus
from .datasinks.mysql import Mysql as Datastore
from .config import (
    CAN as CAN_CONFIG,
    DATA,
    DATABASE as DATABASE_CONFIG,
    LOG_LEVEL,
    CONSOLE_OUT,
    HTTP as HTTP_CONFIG
)

logging.basicConfig(level=LOG_LEVEL)


def main():
    elster = Elster(sender=CAN_CONFIG['sender'], items=DATA)

    with CanBus(**CAN_CONFIG) as can_bus:
        can_bus.notifier(elster.listener)

        for frame in elster.frames:
            can_bus.send(frame.message())
            time.sleep(0.01)

        # Wait for response
        timeout = 0
        while elster.is_done() is False:
            timeout += 1
            time.sleep(0.5)

            if timeout == 10:
                logging.error('TimeoutError: Not all data received.')
                break

    if DATABASE_CONFIG['database']:
        # Save result
        with Datastore(**DATABASE_CONFIG) as db:
            db.save(elster.values)

    if HTTP_CONFIG['url_template']:
        # Create HTTP requests for all values
        pass

    if CONSOLE_OUT:
        print(elster.values)

if __name__ == '__main__':
    main()
