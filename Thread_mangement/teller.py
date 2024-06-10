import threading
import time
import random

class Teller(threading.Thread):
    def __init__(self, id, service_queue):
        threading.Thread.__init__(self)
        self.id = id
        self.service_queue = service_queue

    def run(self):
        while True:
            customer = self.service_queue.get()
            if customer is None:
                break
            print(f"Customer {customer.id} is in Teller {self.id}")
            customer.start_time = time.time()
            service_time = random.randint(1, 5)  # random service time between 1 and 5 seconds
            time.sleep(service_time)
            customer.end_time = time.time()
            print(f"Customer {customer.id} leaves Teller {self.id}")
            self.service_queue.task_done()
