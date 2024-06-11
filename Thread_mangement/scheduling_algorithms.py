import random
import time

def simulate_fcfs(customers):
    for customer in customers:
        service_time = random.randint(1, 5)
        if customer.start_time is None:
            customer.start_time = time.time()
        time.sleep(service_time)
        customer.end_time = time.time()
        print(f"Customer {customer.id} serviced for {service_time} seconds")

def simulate_sjf(customers):
    customers = sorted(customers, key=lambda x: random.randint(1, 5))
    for customer in customers:
        service_time = random.randint(1, 5)
        if customer.start_time is None:
            customer.start_time = time.time()
        time.sleep(service_time)
        customer.end_time = time.time()
        print(f"Customer {customer.id} serviced for {service_time} seconds")

def simulate_srtf(customers):
    remaining_customers = customers[:]
    while remaining_customers:
        remaining_customers.sort(key=lambda x: random.randint(1, 5))
        current_customer = remaining_customers.pop(0)
        service_time = random.randint(1, 5)
        if current_customer.start_time is None:
            current_customer.start_time = time.time()
        time.sleep(service_time)
        current_customer.end_time = time.time()
        print(f"Customer {current_customer.id} serviced for {service_time} seconds")

def simulate_rr(customers, quantum):
    queue = customers[:]
    while queue:
        current_customer = queue.pop(0)
        if current_customer.start_time is None:
            current_customer.start_time = time.time()
        service_time = min(quantum, random.randint(1, 5))
        time.sleep(service_time)
        if service_time < quantum:
            current_customer.end_time = time.time()
            print(f"Customer {current_customer.id} finished with service time {service_time} seconds")
        else:
            queue.append(current_customer)
            print(f"Customer {current_customer.id} quantum expired; remaining time {random.randint(1, 5) - quantum}")
