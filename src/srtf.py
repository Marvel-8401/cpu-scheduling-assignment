"""
============================================================
  OS Assignment: CPU Scheduling & Deadlock Avoidance
  File: srtf.py — Shortest Remaining Time First (Preemptive SJF)
============================================================

Algorithm:
  At every unit of time the scheduler checks all arrived
  processes and runs the one with the shortest *remaining*
  burst time.  If a newly arrived process has a shorter
  remaining time than the currently running process, it
  preempts the CPU immediately.

  Ties in remaining time are broken by arrival time then PID.

Metrics:
  CT  = Completion Time  (time the process finishes)
  TAT = Turnaround Time  = CT - AT
  WT  = Waiting Time     = TAT - BT
============================================================
"""

import copy


def srtf(processes):
    """
    Shortest Remaining Time First (Preemptive SJF) scheduling.

    Parameters
    ----------
    processes : list of dict
        Each dict has keys: 'pid' (str), 'at' (int), 'bt' (int)

    Returns
    -------
    list of dict
        Original fields plus 'ct', 'tat', 'wt' for each process.
    """
    procs = copy.deepcopy(processes)

    # Track remaining burst time for each process
    remaining_bt = {p['pid']: p['bt'] for p in procs}
    proc_map     = {p['pid']: p        for p in procs}

    total_burst  = sum(p['bt'] for p in procs)
    current_time = 0
    completed    = 0
    results      = {}      # pid -> completion time

    while completed < len(procs):
        # Gather all processes that have arrived and still have work
        available = [
            p for p in procs
            if p['at'] <= current_time and remaining_bt[p['pid']] > 0
        ]

        if not available:
            # CPU idle — jump to next arrival
            future = [p for p in procs if remaining_bt[p['pid']] > 0]
            current_time = min(p['at'] for p in future)
            continue

        # Pick process with shortest remaining time; break ties by AT, PID
        chosen = min(available,
                     key=lambda p: (remaining_bt[p['pid']], p['at'], p['pid']))

        # Execute for 1 time unit
        remaining_bt[chosen['pid']] -= 1
        current_time += 1

        # Check if process is now complete
        if remaining_bt[chosen['pid']] == 0:
            results[chosen['pid']] = current_time
            completed += 1

    # Build output list with full metrics
    output = []
    for p in procs:
        pid = p['pid']
        ct  = results[pid]
        tat = ct - p['at']
        wt  = tat - p['bt']
        output.append({
            'pid': pid,
            'at' : p['at'],
            'bt' : p['bt'],
            'ct' : ct,
            'tat': tat,
            'wt' : wt,
        })

    return sorted(output, key=lambda p: p['pid'])


# ── Quick self-test ────────────────────────────────────────
if __name__ == "__main__":
    sample = [
        {"pid": "P1", "at": 0, "bt": 7},
        {"pid": "P2", "at": 2, "bt": 4},
        {"pid": "P3", "at": 4, "bt": 1},
        {"pid": "P4", "at": 5, "bt": 4},
    ]
    results = srtf(sample)
    print(f"{'PID':<6} {'AT':<5} {'BT':<5} {'CT':<5} {'TAT':<6} {'WT':<5}")
    for p in results:
        print(f"{p['pid']:<6} {p['at']:<5} {p['bt']:<5} {p['ct']:<5} {p['tat']:<6} {p['wt']:<5}")
    total_tat = sum(p['tat'] for p in results)
    total_wt  = sum(p['wt']  for p in results)
    n = len(results)
    print(f"\nAvg TAT = {total_tat/n:.2f}   Avg WT = {total_wt/n:.2f}")
