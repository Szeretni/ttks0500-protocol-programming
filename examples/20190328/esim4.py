import threading
import time
import logging

total = 0
lock = threading.Lock()

'''
def with_lock():
    # with: don't need to acquire and release
    with lock:
'''

logging.basicConfig(level=logging.DEBUG,format="(%(threadName)s %(message)s)")
def increase_sum(sum):
    lock.acquire()
    logging.debug("lock acquired")
    global total
    try:
        total += sum
    finally:
        print total
        lock.release()
        logging.debug("lock released")

def main():
    for x in range(10):
        own_thread = threading.Thread(target=increase_sum, args=(5,))
        own_thread.start()
        time.sleep(1)

main()
