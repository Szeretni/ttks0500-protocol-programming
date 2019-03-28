import threading
import time

def service1():
    print threading.currentThread().getName(), "starting"
    time.sleep(1)
    print threading.currentThread().getName(), "stopping"

def main():
    t1 = threading.Timer(2,service1)
    t2 = threading.Thread(name="own thread",target=service1)

    t1.start()
    t2.start()

main()
