# 🧮 FCFS CPU Scheduling Simulation in Python  
**By Tahim Bhuiya**

This project implements a **First-Come, First-Served (FCFS) CPU Scheduling Algorithm** with support for **I/O bursts** in Python. It simulates the execution of processes with alternating CPU and I/O bursts, and computes performance metrics like **waiting time**, **turnaround time**, **response time**, and **CPU utilization**.

---

## 📜 Overview

This simulation models how an operating system schedules processes using the **FCFS non-preemptive algorithm**, where:

- Each process has a list of CPU bursts and I/O times  
- Processes execute their bursts in order  
- I/O-bound processes are temporarily removed from the ready queue  
- Time is advanced to simulate actual scheduling with idle gaps when needed  
- Metrics are tracked for all processes

---

## ▶️ Usage

Run the Python file directly:

```bash
python FCFS (Non-Preemptive) Scheduler.py
```

Then observe the simulation output in the terminal, including:

- Real-time status updates (e.g. which process is running or in I/O)  
- Completion logs for each process  
- A table with waiting, turnaround, and response times  
- CPU utilization and average performance metrics

---

## 🧠 Code Description

| Component                  | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| `Process` class           | Stores burst times, I/O times, and performance metrics per process       |
| `fcfs_scheduling()`       | Core simulation function for FCFS with I/O handling                      |
| `display_status()`        | Prints real-time status of CPU, ready queue, and I/O queue               |
| `is_completed()`          | Checks if a process has finished all its CPU bursts                      |
| Metrics Calculation       | Computes average waiting, turnaround, and response time + CPU utilization|

---

## 🔧 Key Concepts

| Concept           | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| CPU Burst         | Duration for which a process needs the CPU                                  |
| I/O Time          | Time for which a process performs I/O between CPU bursts                    |
| Ready Queue       | Queue of processes waiting for the CPU (FCFS order)                         |
| I/O List          | List of processes currently doing I/O and their completion times            |
| Response Time     | Time from arrival to first CPU allocation                                   |
| Waiting Time      | Time spent waiting in the ready queue                                       |
| Turnaround Time   | Total time from arrival to process completion                               |
| CPU Utilization   | % of time the CPU was actively processing (not idle)                        |

---


## 📈 Example Output

```
Current Execution Time: 93
Running Process: P1
Ready Queue: [(3, 8), (4, 3), (6, 11), (5, 16), (7, 14), (8, 4)]
Processes in I/O: [(2, 24)]

Process P1 has completed its total execution.

Results at the end of the simulation:
Total time needed to complete all processes: 980
CPU Utilization: 81.24%

Process     Tw        Ttr         Tr        
P1          63        198         0         
P2          112       312         12        
...

Average     84.75     256.50      15.38
```

---