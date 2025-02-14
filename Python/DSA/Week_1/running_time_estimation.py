import time

def measure_runtime(n):
    cnt = 0
    start_time = time.time()

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                cnt += 1

    end_time = time.time()
    return end_time - start_time

n_values = [50, 100, 200]
execution_times = {n: measure_runtime(n) for n in n_values}

estimated_time_2000 = execution_times[200] * (2000 / 200) ** 3

print("Measured Execution Times:")
for n, time_taken in execution_times.items():
    print(f"n = {n}: {time_taken:.6f} seconds")

print(
    f"\nEstimated Execution Time for n = 2000: {estimated_time_2000:.2f} seconds (~{estimated_time_2000 / 60:.2f} minutes)")