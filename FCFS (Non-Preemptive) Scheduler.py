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

       
        # Display the current simulation status (time, running process, queues)
        running_process = ready_queue[0] if ready_queue else None
        display_status(current_time, running_process, ready_queue, io_list)

        if ready_queue:
            # Fetch the next process to run from the front of the ready queue (FCFS)
            process = ready_queue.popleft()

            # If the process is getting the CPU for the first time, record its response time
            if process.response_time == -1:
                process.response_time = current_time

            # Calculate how long the process has waited since it last finished CPU or I/O
            waiting_since_last = current_time - process.last_end_time
            if waiting_since_last > 0:
                process.waiting_time += waiting_since_last  # Add to total waiting time

            # Get the duration of the current CPU burst
            burst_time = process.burst_times[process.current_burst]

            # Simulate execution: advance the current time by the burst duration
            current_time += burst_time

            # Add the burst time to total CPU busy time (used to calculate CPU utilization later)
            cpu_busy_time += burst_time

            # Move to the next CPU burst (increment burst index)
            process.current_burst += 1

            if process.current_burst < len(process.burst_times):
                # If there are more CPU bursts left, schedule the next I/O operation

                # Get the corresponding I/O time (index is current_burst - 1 because I/O follows a completed CPU burst)
                io_time = process.io_times[process.current_burst - 1]

                # Compute the time at which this I/O will complete
                io_completion_time = current_time + io_time

                # Add the process to the I/O list with its completion time
                io_list.append((process, io_completion_time))
            else:
                # If all CPU bursts are completed, mark the process as finished

                # Turnaround time is the total time taken from arrival (assumed 0) to completion
                process.turnaround_time = current_time

                # Add the process to the list of completed processes
                completed_processes.append(process)

                # Log completion
                print(f"Process P{process.pid} has completed its total execution.")

        else:
            # If no process is in the ready queue, advance time to the next I/O completion

            if io_list:
                # Find the soonest I/O completion time among all processes in I/O
                next_io_completion = min(io_list, key=lambda x: x[1])[1]

                # Calculate idle time (gap between now and the next I/O completion)
                idle_time = next_io_completion - current_time

                # Move the simulation clock forward to that time
                current_time = next_io_completion
            else:
                # No processes left in the system (both ready queue and I/O list are empty)
                break


    # Calculate total time taken for the simulation (from start to when all processes are completed)
    total_time = current_time

    # Calculate CPU Utilization:
    # It's the percentage of time the CPU was actively executing processes (not idle)
    # Formula: (CPU Busy Time / Total Simulation Time) * 100
    cpu_utilization = (cpu_busy_time / total_time) * 100 if total_time > 0 else 0

    # Return the list of completed processes and final performance metrics
    return completed_processes, cpu_utilization, total_time
    

# Define 8 processes with varying CPU and I/O burst patterns
# Each process is initialized with:
# - A unique process ID (pid)
# - A list of CPU bursts (in order)
# - A list of I/O times (one less than the number of CPU bursts)

p1 = Process(1, [5, 3, 5, 4, 6, 4, 3, 4], [27, 31, 43, 18, 22, 26, 24])
p2 = Process(2, [4, 5, 7, 12, 9, 4, 9, 7, 8], [48, 44, 42, 37, 76, 41, 31, 43])
p3 = Process(3, [8, 12, 18, 14, 4, 15, 14, 5, 6], [33, 41, 65, 21, 61, 18, 26, 31])
p4 = Process(4, [3, 4, 5, 3, 4, 5, 6, 5, 3], [35, 41, 45, 51, 61, 54, 82, 77])
p5 = Process(5, [16, 17, 5, 16, 7, 13, 11, 6, 3, 4], [24, 21, 36, 26, 31, 28, 21, 13, 11])
p6 = Process(6, [11, 4, 5, 6, 7, 9, 12, 15, 8], [22, 8, 10, 12, 14, 18, 24, 30])
p7 = Process(7, [14, 17, 11, 15, 4, 7, 16, 10], [46, 41, 42, 21, 32, 19, 33])
p8 = Process(8, [4, 5, 6, 14, 16, 6], [14, 33, 51, 73, 87])

# Add all processes to a list for scheduling
processes = [p1, p2, p3, p4, p5, p6, p7, p8]

# Run the FCFS scheduling simulation with the provided process list
# This function returns:
# - A list of completed processes (with updated timing info)
# - CPU utilization percentage
# - Total time the simulation took to complete
completed_processes, cpu_utilization, total_time = fcfs_scheduling(processes)


# 📊 Calculate total and average performance metrics across all completed processes

# Sum of waiting times for all processes
total_waiting_time = sum(p.waiting_time for p in completed_processes)

# Sum of turnaround times for all processes
total_turnaround_time = sum(p.turnaround_time for p in completed_processes)

# Sum of response times for all processes
total_response_time = sum(p.response_time for p in completed_processes)

# Total number of completed processes (used to calculate averages)
num_processes = len(completed_processes)


# Calculate average performance metrics

# Average Waiting Time: total waiting time divided by number of processes
average_waiting_time = total_waiting_time / num_processes

# Average Turnaround Time: total turnaround time divided by number of processes
average_turnaround_time = total_turnaround_time / num_processes

# Average Response Time: total response time divided by number of processes
average_response_time = total_response_time / num_processes


# Display the final simulation summary
print("\nResults at the end of the simulation:")

# Print the total time taken to complete all processes
print(f"Total time needed to complete all processes: {total_time}")

# Print how much of that time the CPU was actively working
print(f"CPU Utilization: {cpu_utilization:.2f}%")

# Print the table header with aligned columns:
# Tw  = Waiting Time
# Ttr = Turnaround Time
# Tr  = Response Time
print(f"\n{'Process':<12}{'Tw':<10}{'Ttr':<12}{'Tr':<10}")

# Print performance metrics for each completed process
# Each row shows:
# - Process ID (pid)
# - Tw: Total Waiting Time
# - Ttr: Total Turnaround Time
# - Tr: Response Time (first time the process got the CPU)
for process in completed_processes:
    print(f"P{process.pid:<10}{process.waiting_time:<10}{process.turnaround_time:<12}{process.response_time:<10}")




# Display averages
print(f"\n{'Average':<12}{average_waiting_time:<10.2f}{average_turnaround_time:<12.2f}{average_response_time:<10.2f}")











