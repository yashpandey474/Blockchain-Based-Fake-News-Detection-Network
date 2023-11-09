import queue

shared_queue = queue.Queue()

def get_shared_variable():
    try:
        return shared_queue.get_nowait()
    
    except queue.Empty:
        return None

def set_shared_variable(value):
    shared_queue.put(value)
