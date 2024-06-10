def calculate_metrics(customers):
    total_turnaround_time = 0
    total_waiting_time = 0
    total_response_time = 0

    for customer in customers:
        turnaround_time = customer.end_time - customer.arrival_time
        waiting_time = turnaround_time - (customer.end_time - customer.start_time)
        response_time = customer.start_time - customer.arrival_time

        total_turnaround_time += turnaround_time
        total_waiting_time += waiting_time
        total_response_time += response_time

    n = len(customers)
    avg_turnaround_time = total_turnaround_time / n
    avg_waiting_time = total_waiting_time / n
    avg_response_time = total_response_time / n

    return avg_turnaround_time, avg_waiting_time, avg_response_time
