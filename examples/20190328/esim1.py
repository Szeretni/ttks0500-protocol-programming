import threading
import time
import Queue

def thread2(q1):
    for x in range(5):
#        print "thread2"
        q1.put("thread2")
        time.sleep(1)


def thread1(q1):
    for x in range(5):
#        print "the thread is just looping nums: %d" % x
#        print "thread1"
        q1.put("thread1")
        time.sleep(1)

def main():
    q1 = Queue.Queue()
    t1 = threading.Thread(target=thread1,args=(q1,))
    t2 = threading.Thread(target=thread2,args=(q1,))
    t1.start()
    t2.start()

    for x in range(10):
        msg = q1.get()
        print msg

main()
