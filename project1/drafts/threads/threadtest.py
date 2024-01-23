from threading import Thread, Lock
from time import sleep

class Shared:
    def __init__(self):
        self.__test = 0
        self.__lock = Lock()

    def inc(self):
        with self.__lock:
            self.__test += 1
    
    def read(self):
        with self.__lock:
            return self.__test

st: Shared = Shared()

def inc(st):
    for i in range(0, 5000000):
        st.inc()

t1 = Thread(target=inc, args=(st,))
t1.start()

t2 = Thread(target=inc, args=(st,))
t2.start()

t3 = Thread(target=inc, args=(st,))
t3.start()

t4 = Thread(target=inc, args=(st,))
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()

print(st.read())

