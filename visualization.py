import matplotlib.pyplot as plt

def visualize_results(results):
    algorithms = list(results.keys())
    avg_turnaround_time = [results[alg][0] for alg in algorithms]
    avg_waiting_time = [results[alg][1] for alg in algorithms]
    avg_response_time = [results[alg][2] for alg in algorithms]

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.bar(algorithms, avg_turnaround_time, color='blue')
    plt.title('Average Turnaround Time')
    plt.xlabel('Algorithms')
    plt.ylabel('Time')

    plt.subplot(1, 3, 2)
    plt.bar(algorithms, avg_waiting_time, color='green')
    plt.title('Average Waiting Time')
    plt.xlabel('Algorithms')
    plt.ylabel('Time')

    plt.subplot(1, 3, 3)
    plt.bar(algorithms, avg_response_time, color='red')
    plt.title('Average Response Time')
    plt.xlabel('Algorithms')
    plt.ylabel('Time')

    plt.tight_layout()
    plt.show()
