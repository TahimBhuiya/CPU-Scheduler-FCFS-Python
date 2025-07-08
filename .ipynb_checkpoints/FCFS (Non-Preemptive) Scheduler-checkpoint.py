from collections import deque

# Define Process class to store process data
class Process:
    def __init__(self, pid, burst_times, io_times):
        self.pid = pid
        self.burst_times = burst_times  # List of CPU bursts
        self.io_times = io_times        # List of I/O times
        self.current_burst = 0          # Track current CPU burst index
        self.waiting_time = 0           # Total waiting time
        self.turnaround_time = 0        # Total turnaround time
        self.response_time = -1         # First response time
        self.last_end_time = 0          # Last time the process was in CPU or I/O    
        
    def is_completed(self):
        """
        Check if the process has completed all its CPU bursts.
        Returns True if all CPU bursts have been executed, otherwise False.
        """
        return self.current_burst >= len(self.burst_times)

# Display the current simulation status, including running process, ready queue, and I/O list
def display_status(current_time, running_process, ready_queue, io_list):
    print(f"\nCurrent Execution Time: {current_time}")  # Show current time in the simulation

    # Display the currently running process, if any
    if running_process:
        print(f"Running Process: P{running_process.pid}")
    else:
        print("Running Process: None")

    # Show the contents of the ready queue: process ID and its current CPU burst time
    print("Ready Queue:", [(p.pid, p.burst_times[p.current_burst]) for p in ready_queue])

    # Show the processes in I/O: process ID and remaining I/O time (completion time - current time)
    print("Processes in I/O:", [(p.pid, t - current_time) for p, t in io_list])



# Simulate FCFS (First-Come, First-Served) CPU Scheduling with I/O handling
def fcfs_scheduling(processes):
    current_time = 0                      # Simulation clock
    ready_queue = deque(processes)       # Queue of processes ready to execute (in order of arrival)
    io_list = []                         # List of processes currently performing I/O: (process, io_completion_time)
    completed_processes = []            # List to store completed processes
    cpu_busy_time = 0                    # Total time the CPU was actively executing a process

    # Continue simulation as long as there are processes in the ready queue or in I/O
    while ready_queue or io_list:

        # Check for I/O completions at the current time
        # Move completed I/O processes back to the ready queue
        io_completed = [(p, t) for (p, t) in io_list if t <= current_time]
        for p, t in io_completed:
            ready_queue.append(p)           # Process is now ready for its next CPU burst
            io_list.remove((p, t))          # Remove from I/O list
            p.last_end_time = t             # Update process's last end time to I/O completion time

       
        # Display the current status
        running_process = ready_queue[0] if ready_queue else None
        display_status(current_time, running_process, ready_queue, io_list)

        if ready_queue:
            # Dequeue the first process from the ready queue
            process = ready_queue.popleft()

            # If it's the first time the process is getting the CPU
            if process.response_time == -1:
                process.response_time = current_time

            # Calculate waiting time since last end time
            waiting_since_last = current_time - process.last_end_time
            if waiting_since_last > 0:
                process.waiting_time += waiting_since_last

            # Execute the current CPU burst
            burst_time = process.burst_times[process.current_burst]
            current_time += burst_time
            cpu_busy_time += burst_time  # CPU is busy during this time

            # Move to next burst
            process.current_burst += 1

            if process.current_burst < len(process.burst_times):
                # Schedule I/O
                io_time = process.io_times[process.current_burst - 1]
                io_completion_time = current_time + io_time
                io_list.append((process, io_completion_time))
            else:
                # Process is complete
                process.turnaround_time = current_time  
                completed_processes.append(process)
                print(f"Process P{process.pid} has completed its total execution.")

        else:
            # If no process is ready, advance time to the next I/O completion
            if io_list:
                next_io_completion = min(io_list, key=lambda x: x[1])[1]
                # Idle time is the gap between current_time and next_io_completion
                idle_time = next_io_completion - current_time
                current_time = next_io_completion
            else:
                break  # No processes left

    # Calculate CPU Utilization
    total_time = current_time
    cpu_utilization = (cpu_busy_time / total_time) * 100 if total_time > 0 else 0

    return completed_processes, cpu_utilization, total_time


p1 = Process(1, [5, 3, 5, 4, 6, 4, 3, 4], [27, 31, 43, 18, 22, 26, 24])
p2 = Process(2, [4, 5, 7, 12, 9, 4, 9, 7, 8], [48, 44, 42, 37, 76, 41, 31, 43])
p3 = Process(3, [8, 12, 18, 14, 4, 15, 14, 5, 6], [33, 41, 65, 21, 61, 18, 26, 31])
p4 = Process(4, [3, 4, 5, 3, 4, 5, 6, 5, 3], [35, 41, 45, 51, 61, 54, 82, 77])
p5 = Process(5, [16, 17, 5, 16, 7, 13, 11, 6, 3, 4], [24, 21, 36, 26, 31, 28, 21, 13, 11])
p6 = Process(6, [11, 4, 5, 6, 7, 9, 12, 15, 8], [22, 8, 10, 12, 14, 18, 24, 30])
p7 = Process(7, [14, 17, 11, 15, 4, 7, 16, 10], [46, 41, 42, 21, 32, 19, 33])
p8 = Process(8, [4, 5, 6, 14, 16, 6], [14, 33, 51, 73, 87])

processes = [p1, p2, p3, p4, p5, p6, p7, p8] 


completed_processes, cpu_utilization, total_time = fcfs_scheduling(processes)

# Calculate averages
total_waiting_time = sum(p.waiting_time for p in completed_processes)
total_turnaround_time = sum(p.turnaround_time for p in completed_processes)
total_response_time = sum(p.response_time for p in completed_processes)
num_processes = len(completed_processes)

average_waiting_time = total_waiting_time / num_processes
average_turnaround_time = total_turnaround_time / num_processes
average_response_time = total_response_time / num_processes

# Display final results
print("\nResults at the end of the simulation:")
print(f"Total time needed to complete all processes: {total_time}")
print(f"CPU Utilization: {cpu_utilization:.2f}%")
print(f"\n{'Process':<12}{'Tw':<10}{'Ttr':<12}{'Tr':<10}")
for process in completed_processes:
    print(f"P{process.pid:<10}{process.waiting_time:<10}{process.turnaround_time:<12}{process.response_time:<10}")



# Display averages
print(f"\n{'Average':<12}{average_waiting_time:<10.2f}{average_turnaround_time:<12.2f}{average_response_time:<10.2f}")











