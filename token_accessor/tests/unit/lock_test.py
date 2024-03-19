import threading

from token_accessor.lock import ThreadLock


def test_acquire():
    lock = ThreadLock()
    assert lock.acquire() is True


def test_release():
    lock = ThreadLock()
    lock.acquire()
    lock.release()
    assert lock._ThreadLock__thread_lock.locked() is False


def test_thread_lock():
    lock = ThreadLock()
    results = []

    def task1():
        acquired = lock.acquire()
        results.append(acquired)
        lock.release()

    def task2():
        acquired = lock.acquire()
        results.append(acquired)
        lock.release()

    thread1 = threading.Thread(target=task1)
    thread2 = threading.Thread(target=task2)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert results == [True, True]
