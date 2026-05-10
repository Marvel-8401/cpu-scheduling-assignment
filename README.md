# OS Assignment — CPU Scheduling & Deadlock Avoidance

## Overview

This project implements four CPU scheduling algorithms and the Banker's Algorithm for deadlock avoidance, fulfilling the requirements of the Operating Systems programming assignment.

---

## Project Structure

```
cpu-scheduling-assignment/
│
├── README.md
├── src/
│   ├── main.py          ← Entry point (runs all algorithms interactively)
│   ├── fcfs.py          ← First Come First Served
│   ├── sjf.py           ← Non-Preemptive Shortest Job First
│   ├── srtf.py          ← Shortest Remaining Time First (Preemptive SJF)
│   ├── round_robin.py   ← Round Robin (Time Quantum = 2)
│   └── bankers.py       ← Banker's Algorithm for deadlock avoidance
│
├── input/
│   └── sample_input.txt ← Example input used in testing
│
└── output/
    └── sample_output.txt ← Expected output with Gantt charts & metrics
```

---

## How to Run

### Prerequisites
- Python 3.7 or later (no external libraries required)

### Run all algorithms together
```bash
cd src
python3 main.py
```

### Run individual modules
```bash
python3 fcfs.py
python3 sjf.py
python3 srtf.py
python3 round_robin.py
python3 bankers.py
```

### Input Format
```
<number of processes>
<PID> <Arrival Time> <Burst Time>
...
```

**Example (`input/sample_input.txt`):**
```
4
P1 0 7
P2 2 4
P3 4 1
P4 5 4
```

---

## Algorithms Implemented

### 1. FCFS — First Come First Served (`fcfs.py`)
- **Type:** Non-Preemptive
- **Policy:** Processes execute in order of arrival. If two processes arrive at the same time, the lower PID goes first.
- **Idle CPU:** If the CPU is free before the next process arrives, time is advanced.
- **Complexity:** O(n log n) for sorting + O(n) for scheduling

### 2. SJF — Non-Preemptive Shortest Job First (`sjf.py`)
- **Type:** Non-Preemptive
- **Policy:** At each scheduling point, the arrived process with the shortest burst time is chosen. Once started, it runs to completion.
- **Tie-breaking:** Shorter AT, then lexicographic PID.
- **Note:** Optimal for minimizing average waiting time among non-preemptive algorithms.

### 3. SRTF — Shortest Remaining Time First (`srtf.py`)
- **Type:** Preemptive (Preemptive SJF)
- **Policy:** At every time unit, the process with the shortest *remaining* burst time runs. A newly arriving process preempts the current one if it has a shorter remaining time.
- **Complexity:** O(n²) in the worst case (unit-step simulation)
- **Note:** Optimal for minimizing average waiting time overall.

### 4. Round Robin (`round_robin.py`)
- **Type:** Preemptive
- **Time Quantum:** 2 (configurable via `quantum` parameter)
- **Policy:** Processes rotate through the CPU in FIFO order, each receiving at most `quantum` units per turn. Preempted processes go to the back of the ready queue.
- **Newly arrived processes** are enqueued before the preempted process when they arrive at the same moment as preemption.

---

## Performance Metrics

| Metric | Formula |
|--------|---------|
| Completion Time (CT) | Time the process finishes execution |
| Turnaround Time (TAT) | CT − Arrival Time (AT) |
| Waiting Time (WT) | TAT − Burst Time (BT) |
| Average TAT | Sum of all TAT ÷ number of processes |
| Average WT | Sum of all WT ÷ number of processes |

### Sample Results (from `sample_input.txt`)

| Algorithm  | Avg TAT | Avg WT |
|------------|---------|--------|
| FCFS       | 8.75    | 4.75   |
| SJF (NP)   | 8.00    | 4.00   |
| SRTF       | **7.00**| **3.00** |
| Round Robin| 9.00    | 5.00   |

SRTF achieves the lowest average waiting and turnaround times, at the cost of context switching overhead.

---

## Banker's Algorithm (`bankers.py`)

### Purpose
Determines whether the system is in a **safe state** and safely processes resource requests to avoid deadlock.

### Key Structures

| Structure    | Size   | Description |
|--------------|--------|-------------|
| `available`  | [m]    | Currently available units of each resource type |
| `max_matrix` | [n][m] | Maximum demand of each process |
| `allocation` | [n][m] | Resources currently allocated to each process |
| `need`       | [n][m] | Remaining need = Max − Allocation |

### Safety Algorithm
1. Set `Work = Available`, `Finish[i] = False` for all i
2. Find an unfinished process i such that `Need[i] ≤ Work`
3. If found: `Work += Allocation[i]`, `Finish[i] = True`, repeat
4. If all `Finish[i] == True` → **SAFE STATE** with a valid sequence

### Resource Request Algorithm
1. If `Request > Need[i]` → error (exceeds declared maximum)
2. If `Request > Available` → process must wait
3. Tentatively allocate and run safety check
   - If safe → **grant** the request
   - If unsafe → **roll back** and deny

### Banker's Algorithm Input Format (interactive)
```
Enter number of processes              : 5
Enter number of resource types         : 3
Enter Available resources (3 values)   : 3 3 2
Enter Max matrix (5 rows × 3 cols):
  P0 Max   : 7 5 3
  P1 Max   : 3 2 2
  ...
Enter Allocation matrix (5 rows × 3 cols):
  P0 Alloc : 0 1 0
  ...
```

---

## Code Quality Notes

- **Modular design:** Each algorithm lives in its own file with a single well-named function.
- **Deep copies:** Input data is never mutated; `copy.deepcopy()` is used throughout.
- **Idle CPU handling:** All schedulers correctly advance time when no process is ready.
- **Comments:** Every function has a docstring explaining its algorithm, parameters, and return value.
- **Self-tests:** Each file can be run standalone (`python3 fcfs.py`) with a built-in sample.

---

## Author
OS Assignment Submission — CPU Scheduling & Deadlock Avoidance
# cpu-scheduling-assignment
