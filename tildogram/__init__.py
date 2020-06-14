import logging
from . import tildes

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

topics = tildes.get_topics()
print(topics)
