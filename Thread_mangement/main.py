import time
import random
from customer import Customer
from scheduling_algorithms import simulate_sjf, simulate_srtf, simulate_rr
from metrics import calculate_metrics
from visualization import visualize_results

def reset_customers(customers):
    for customer in customers:
        customer.start_time = None
        customer.end_time = None

def main():
    customers = [Customer(i, time.time()) for i in range(5)]
    
    while True:
        print("Choose a scheduling algorithm:")
        print("1. Shortest Job First (SJF)")
        print("2. Shortest Remaining Time First (SRTF)")
        print("3. Round Robin (RR)")
        choice = input("Enter your choice (1/2/3): ")

        reset_customers(customers)
        
        results = {}
        
        if choice == '1':
            simulate_sjf(customers)
            sjf_results = calculate_metrics(customers)
            results["SJF"] = sjf_results
            print(f"SJF Metrics: {sjf_results}")
        elif choice == '2':
            simulate_srtf(customers)
            srtf_results = calculate_metrics(customers)
            results["SRTF"] = srtf_results
            print(f"SRTF Metrics: {srtf_results}")
        elif choice == '3':
            quantum = int(input("Enter the quantum time: "))
            simulate_rr(customers, quantum)
            rr_results = calculate_metrics(customers)
            results["RR"] = rr_results
            print(f"RR Metrics: {rr_results}")
        else:
            print("Invalid choice. Please try again.")
            continue

        visualize_results(results)

        again = input("Do you want to choose another algorithm? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    main()
