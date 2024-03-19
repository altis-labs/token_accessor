from gevent.lock import BoundedSemaphore

THREAD_LOCK_TYPE = "thread"


class ThreadLock:
    def __init__(self):
        self.__thread_lock = BoundedSemaphore(1)

    def acquire(self) -> bool:
        return self.__thread_lock.acquire()

    def release(self) -> None:
        self.__thread_lock.release()
