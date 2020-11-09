import time

from threading import Thread
from multiprocessing import Process

from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

def chrono(function):
    start = time.time()
    function()
    duration = time.time() - start
    print(f'{function.__name__} : {duration:.2f}s')

def calcul_long():
    n = 1E8
    while n > 0:
        n -= 1

def multithreading():
    thread = Thread(target=calcul_long)
    thread.start()
    thread.join()

def multiprocessing():
    process = Process(target=calcul_long)
    process.start()
    process.join()

def multithreading_futures():
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(calcul_long)

def multiprocessing_futures():
    with ProcessPoolExecutor(max_workers=4) as executor:
        executor.submit(calcul_long)

if __name__ == '__main__':
    chrono(multithreading)
    chrono(multiprocessing)
    chrono(multithreading_futures)
    chrono(multiprocessing_futures)
