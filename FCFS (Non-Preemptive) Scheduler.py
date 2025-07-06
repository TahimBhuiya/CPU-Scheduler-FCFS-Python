from collections import deque

# Define Process class to store process data
class Process:
    def __init__(self, pid, burst_times, io_times):
        self.pid = pid
        self.burst_times = burst_times  
        self.io_times = io_times       
        self.current_burst = 0          
        self.waiting_time = 0          
        self.turnaround_time = 0        
        self.response_time = -1         
        self.last_end_time = 0         
        
    def is_completed(self):
        return self.current_burst >= len(self.burst_times)

# Display simulation status
def display_status(current_time, running_process, ready_queue, io_list):
    print(f"\nCurrent Execution Time: {current_time}")
    if running_process:
        print(f"Running Process: P{running_process.pid}")
    else:
        print("Running Process: None")
    print("Ready Queue:", [(p.pid, p.burst_times[p.current_burst]) for p in ready_queue])
    print("Processes in I/O:", [(p.pid, t - current_time) for p, t in io_list])


# Simulate FCFS (First-Come, First-Served) Scheduling
def fcfs_scheduling(processes):
    current_time = 0
    ready_queue = deque(processes)  
    io_list = []                   
    completed_processes = []
    cpu_busy_time = 0   
    
    while ready_queue or io_list:
        # Check for I/O completions
        io_completed = [ (p, t) for (p, t) in io_list if t <= current_time ]
        for p, t in io_completed:
            ready_queue.append(p)
            io_list.remove((p, t))
            p.last_end_time = t  # Update last end time to I/O completion time

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






