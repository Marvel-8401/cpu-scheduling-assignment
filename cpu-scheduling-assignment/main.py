"""
============================================================
  OS Assignment: CPU Scheduling & Deadlock Avoidance
  File: main.py — Entry Point
============================================================
"""

from fcfs import fcfs
from sjf import sjf_non_preemptive
from srtf import srtf
from round_robin import round_robin
from bankers import bankers_algorithm


def input_processes():
    """
    Read process data from the user.
    Returns a list of dicts: [{pid, at, bt}, ...]
    """
    n = int(input("Enter number of processes: "))
    processes = []
    print("Enter Process ID, Arrival Time (AT), Burst Time (BT) for each process:")
    for _ in range(n):
        line = input().split()
        pid = line[0]
        at  = int(line[1])
        bt  = int(line[2])
        processes.append({"pid": pid, "at": at, "bt": bt})
    return processes


def print_metrics(label, results):
    """
    Pretty-print scheduling results and averages.
    results: list of dicts with keys pid, at, bt, ct, tat, wt
    """
    print(f"\n{'='*55}")
    print(f"  {label}")
    print(f"{'='*55}")
    print(f"{'PID':<6} {'AT':<5} {'BT':<5} {'CT':<5} {'TAT':<6} {'WT':<5}")
    print(f"{'-'*55}")
    total_tat = total_wt = 0
    for p in results:
        print(f"{p['pid']:<6} {p['at']:<5} {p['bt']:<5} {p['ct']:<5} {p['tat']:<6} {p['wt']:<5}")
        total_tat += p['tat']
        total_wt  += p['wt']
    n = len(results)
    print(f"{'-'*55}")
    print(f"  Average Turnaround Time : {total_tat/n:.2f}")
    print(f"  Average Waiting Time    : {total_wt/n:.2f}")
    print(f"{'='*55}\n")


def main():
    print("\n=== CPU Scheduling Simulator ===\n")
    processes = input_processes()

    # ── Scheduling Algorithms ──────────────────────────────
    print_metrics("FCFS  (First Come First Served)",
                  fcfs(processes))

    print_metrics("SJF   (Non-Preemptive Shortest Job First)",
                  sjf_non_preemptive(processes))

    print_metrics("SRTF  (Shortest Remaining Time First)",
                  srtf(processes))

    print_metrics("Round Robin  (Time Quantum = 2)",
                  round_robin(processes, quantum=2))

    # ── Banker's Algorithm ─────────────────────────────────
    print("\n=== Banker's Algorithm — Deadlock Avoidance ===\n")
    bankers_algorithm()


if __name__ == "__main__":
    main()
