import logging

# https://docs.python.org/2/library/logging.html#logrecord-attributes
logging.basicConfig(filename="debug.log", level=logging.DEBUG, format="%(levelname)s %(message)s")

logging.debug("hello world")
logging.debug("good bye")
