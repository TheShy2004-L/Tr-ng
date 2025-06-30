from time import sleep

from controllers.thread import ThreadController

a = ThreadController()
a.start_scanning()
sleep(2)

a.stop_scanning()
sleep(2)

a.start_scanning()
