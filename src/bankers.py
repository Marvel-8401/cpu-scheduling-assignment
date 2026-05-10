"""
============================================================
  OS Assignment: CPU Scheduling & Deadlock Avoidance
  File: bankers.py — Banker's Algorithm
============================================================

Overview:
  The Banker's Algorithm determines whether a system is in a
  SAFE STATE by checking if there exists at least one safe
  sequence in which all processes can complete without
  causing a deadlock.

Key Data Structures:
  n          : number of processes
  m          : number of resource types
  Available  : [m]        — currently available units of each resource
  Max        : [n][m]     — max demand of each process
  Allocation : [n][m]     — currently allocated resources
  Need       : [n][m]     — remaining need = Max - Allocation

Safety Algorithm (used internally):
  1. Work  = Available
     Finish = [False] * n
  2. Find index i such that Finish[i] == False AND Need[i] <= Work
  3. If found: Work += Allocation[i]; Finish[i] = True; go to 2
  4. If all Finish[i] == True → SAFE; else → UNSAFE

Resource-Request Algorithm:
  For a request Request_i from process P_i:
  1. If Request_i > Need_i      → error
  2. If Request_i > Available   → P_i must wait
  3. Pretend to allocate and check safety:
       Available  -= Request_i
       Allocation[i] += Request_i
       Need[i]    -= Request_i
     If SAFE → grant; else → roll back and deny
============================================================
"""


def is_safe(available, allocation, need, n, m):
    """
    Run the safety algorithm.

    Returns
    -------
    (is_safe : bool, safe_sequence : list of int)
    """
    work   = available[:]
    finish = [False] * n
    safe_seq = []

    while len(safe_seq) < n:
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                # Process i can proceed: "release" its allocation
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_seq.append(i)
                found = True
                break   # restart scan from the beginning
        if not found:
            break  # no eligible process found → unsafe

    all_finished = all(finish)
    return all_finished, safe_seq


def bankers_algorithm():
    """
    Interactive Banker's Algorithm demonstration.
    Reads system state from stdin, checks safety, then
    optionally processes a resource request.
    """
    print("--- Banker's Algorithm ---\n")

    # ── Input system state ─────────────────────────────────
    n = int(input("Enter number of processes              : "))
    m = int(input("Enter number of resource types         : "))

    print(f"\nEnter Available resources ({m} values, space-separated):")
    available = list(map(int, input().split()))

    print(f"\nEnter Max matrix ({n} rows × {m} cols):")
    max_matrix = []
    for i in range(n):
        row = list(map(int, input(f"  P{i} Max   : ").split()))
        max_matrix.append(row)

    print(f"\nEnter Allocation matrix ({n} rows × {m} cols):")
    allocation = []
    for i in range(n):
        row = list(map(int, input(f"  P{i} Alloc : ").split()))
        allocation.append(row)

    # ── Compute Need matrix ────────────────────────────────
    need = [
        [max_matrix[i][j] - allocation[i][j] for j in range(m)]
        for i in range(n)
    ]

    # ── Display matrices ───────────────────────────────────
    header = "  " + "  ".join(f"R{j}" for j in range(m))
    print(f"\n{'─'*50}")
    print("  Allocation Matrix          Need Matrix")
    print(f"{'─'*50}")
    for i in range(n):
        alloc_str = "  ".join(f"{allocation[i][j]:<3}" for j in range(m))
        need_str  = "  ".join(f"{need[i][j]:<3}"       for j in range(m))
        print(f"  P{i}  [ {alloc_str}]         [ {need_str}]")
    print(f"\n  Available : {available}")
    print(f"{'─'*50}\n")

    # ── Check current system safety ────────────────────────
    safe, seq = is_safe(available[:], [row[:] for row in allocation],
                        [row[:] for row in need], n, m)

    if safe:
        seq_str = " → ".join(f"P{i}" for i in seq)
        print(f"  ✅ System is in a SAFE STATE.")
        print(f"  Safe Sequence : {seq_str}\n")
    else:
        print("  ❌ System is in an UNSAFE STATE (deadlock risk).\n")

    # ── Optional: process a resource request ───────────────
    ans = input("Do you want to simulate a resource request? (yes/no): ").strip().lower()
    if ans not in ("yes", "y"):
        return

    pid = int(input(f"Enter requesting process index (0 to {n-1}): "))
    print(f"Enter request vector for P{pid} ({m} values):")
    request = list(map(int, input().split()))

    print(f"\n--- Processing Request from P{pid}: {request} ---")

    # Validation 1: request must not exceed process need
    if any(request[j] > need[pid][j] for j in range(m)):
        print("  ❌ Request exceeds maximum need. Error — process misbehaving.")
        return

    # Validation 2: request must not exceed available resources
    if any(request[j] > available[j] for j in range(m)):
        print("  ⏳ Insufficient resources — P{pid} must wait.")
        return

    # Pretend to allocate
    avail_copy  = available[:]
    alloc_copy  = [row[:] for row in allocation]
    need_copy   = [row[:] for row in need]

    for j in range(m):
        avail_copy[j]       -= request[j]
        alloc_copy[pid][j]  += request[j]
        need_copy[pid][j]   -= request[j]

    safe2, seq2 = is_safe(avail_copy, alloc_copy, need_copy, n, m)

    if safe2:
        seq_str = " → ".join(f"P{i}" for i in seq2)
        print(f"  ✅ Request GRANTED — system remains in a safe state.")
        print(f"  New Safe Sequence : {seq_str}")
    else:
        print("  ❌ Request DENIED — granting it would lead to an unsafe state.")
        print("  Resources rolled back. P{pid} must wait.")


# ── Quick self-test (hard-coded example from textbook) ─────
if __name__ == "__main__":
    # Classic 5-process, 3-resource example
    # Processes: P0–P4   Resources: A, B, C
    n, m = 5, 3
    available  = [3, 3, 2]
    max_m      = [
        [7, 5, 3],   # P0
        [3, 2, 2],   # P1
        [9, 0, 2],   # P2
        [2, 2, 2],   # P3
        [4, 3, 3],   # P4
    ]
    alloc = [
        [0, 1, 0],   # P0
        [2, 0, 0],   # P1
        [3, 0, 2],   # P2
        [2, 1, 1],   # P3
        [0, 0, 2],   # P4
    ]
    need = [
        [max_m[i][j] - alloc[i][j] for j in range(m)]
        for i in range(n)
    ]

    safe, seq = is_safe(available, alloc, need, n, m)
    print("Textbook example:")
    print(f"  Safe: {safe}")
    print(f"  Sequence: {' → '.join(f'P{i}' for i in seq)}")
