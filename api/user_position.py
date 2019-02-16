from bean import  Position
from threading import Lock

TARGET_LOCK = Lock()
BM_LOCK = Lock()

bm_position = Position()
target_position = Position()


def set_target_position(position):
    TARGET_LOCK.acquire()
    global target_position
    target_position = position
    TARGET_LOCK.release()


def get_target_position():
    TARGET_LOCK.acquire()
    position = target_position.copy()
    TARGET_LOCK.release()
    return position


def set_bm_position(position):
    TARGET_LOCK.acquire()
    global bm_position
    bm_position = position
    TARGET_LOCK.release()


def get_bm_position():
    TARGET_LOCK.acquire()
    position = bm_position.copy()
    TARGET_LOCK.release()
    return position
