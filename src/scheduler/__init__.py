import os
import sys

sys.path.insert(0, os.getcwd())

from src.scheduler.message_queue import MessageQueue

# Instantiate Message Queue and create a queue
MQ = MessageQueue()
queue = MQ.create_queue()
