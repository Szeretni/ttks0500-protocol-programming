import Queue

# FIFO
print "FIFO"

q1 = Queue.Queue()

for x in range(5):
    q1.put(x)

while not q1.empty():
    print q1.get()

# -------------------------------------

# LIFO
print "LIFO"

q2 = Queue.LifoQueue()

for x in range (5):
    q2.put(x)

while not q2.empty():
    print q2.get()

#PRIO
print "PRIO"

q3 = Queue.PriorityQueue()

q3.put(1,"prio 1")
q3.put(5,"prio 5")
q3.put(2,"prio 2")

while not q3.empty():
    print q3.get()
