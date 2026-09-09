import argparse
import csv
import hashlib
import os
import threading
import time
from collections import deque
from datetime import datetime, timezone

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

try:
    from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
except Exception:
    ThreadPoolExecutor = ProcessPoolExecutor = as_completed = None

try:
    from mpi4py import MPI
    from mpi4py.futures import MPICommExecutor, MPIPoolExecutor

    mpi_available = True
except Exception:
    MPI = None
    MPIPoolExecutor = None
    mpi_available = False


_SHARED_DATA = None
_SHARED_DATA_SEED = None


def init_shared_data(dataset_seed=42):
    global _SHARED_DATA, _SHARED_DATA_SEED
    if _SHARED_DATA is None or _SHARED_DATA_SEED != dataset_seed:
        _SHARED_DATA = prepare_data(random_state=dataset_seed)
        _SHARED_DATA_SEED = dataset_seed
    return _SHARED_DATA


def _process_pool_init(dataset_seed):
    """Initializer for ProcessPoolExecutor workers to ensure local data exists."""
    init_shared_data(dataset_seed)


def get_shared_data():
    if _SHARED_DATA is None:
        raise RuntimeError(
            "Shared dataset not initialized; call init_shared_data first"
        )
    return _SHARED_DATA


# Shared dataset creation (loaded once)
def prepare_data(random_state=42):
    X, y = make_classification(
        n_samples=100000,
        n_features=200,
        n_informative=10,
        n_redundant=10,
        n_repeated=0,
        n_classes=2,
        n_clusters_per_class=2,
        class_sep=1.2,
        flip_y=0.08,
        weights=[0.5, 0.5],
        random_state=random_state,
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_ = scaler.fit_transform(X_train)
    X_val_ = scaler.transform(X_val)
    return X_train_, X_val_, y_train, y_val


# Task function (top-level so picklable)
def run_trial(i, seed_base, dataset_seed=None):
    if dataset_seed is not None or _SHARED_DATA is None:
        init_shared_data(dataset_seed if dataset_seed is not None else 42)
    X_train, X_val, y_train, y_val = get_shared_data()
    # Each trial uses a reproducible RNG based on seed_base + i
    rng = np.random.default_rng(seed_base + i)
    C = 10 ** rng.uniform(-5, -1)

    t0 = time.perf_counter()
    clf = LogisticRegression(
        C=C,
        penalty="elasticnet",
        l1_ratio=1.0,
        solver="saga",
        max_iter=3000,
        random_state=seed_base + i,
    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_val)
    acc = accuracy_score(y_val, y_pred)
    t1 = time.perf_counter()

    # small checksum of result for verification
    h = hashlib.sha1(f"{C:.12e}:{acc:.12e}".encode()).hexdigest()[:8]

    return {
        "task_id": i,
        "C": C,
        "acc": float(acc),
        "start": t0,
        "end": t1,
        "duration": t1 - t0,
        "result_hash": h,
    }


def write_csv_header(out_path):
    if not out_path:
        return None, None

    header = [
        "run_id",
        "mode",
        "task_id",
        "worker",
        "worker_type",
        "task_start_s",
        "task_end_s",
        "task_duration_s",
        "C",
        "acc",
        "result_hash",
    ]
    new_file = not os.path.exists(out_path)
    f = open(out_path, "a", newline="")
    writer = csv.DictWriter(f, fieldnames=header)
    if new_file:
        writer.writeheader()
    return f, writer


def serial_run(n_trials, seed_base, out_path=None, dataset_seed=42):
    init_shared_data(dataset_seed)
    run_id = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")
    f, writer = write_csv_header(out_path)
    start = time.perf_counter()
    results = []
    for i in range(n_trials):
        r = run_trial(i, seed_base, dataset_seed)
        if writer:
            r_row = {
                "run_id": run_id,
                "mode": "serial",
                "task_id": r["task_id"],
                "worker": os.getpid(),
                "worker_type": "process",
                "task_start_s": r["start"],
                "task_end_s": r["end"],
                "task_duration_s": r["duration"],
                "C": r["C"],
                "acc": r["acc"],
                "result_hash": r["result_hash"],
            }
            writer.writerow(r_row)
            f.flush()
        results.append(r)
    total = time.perf_counter() - start
    if f:
        f.close()
    best = max(results, key=lambda t: t["acc"])
    print(
        f"Serial completed in {total:.3f}s; best C={best['C']:.3e}, acc={best['acc']:.4f}"
    )
    return results


def concurrent_run(
    n_trials, seed_base, out_path=None, workers=1, use_processes=False, dataset_seed=42
):
    init_shared_data(dataset_seed)
    run_id = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")
    f, writer = write_csv_header(out_path)
    start = time.perf_counter()

    Executor = ProcessPoolExecutor if use_processes else ThreadPoolExecutor
    worker_type = "process" if use_processes else "thread"
    executor_kwargs = {}
    if use_processes:
        executor_kwargs = {
            "initializer": _process_pool_init,
            "initargs": (dataset_seed,),
        }

    # Submit one task per trial for dynamic load balancing
    with Executor(max_workers=workers, **executor_kwargs) as ex:
        futures = []
        for i in range(n_trials):
            futures.append(ex.submit(run_trial, i, seed_base, dataset_seed))

        results = []
        for fut in as_completed(futures):
            r = fut.result()
            worker_id = os.getpid() if use_processes else threading.get_ident()
            if writer:
                r_row = {
                    "run_id": run_id,
                    "mode": f"concurrent_{worker_type}",
                    "task_id": r["task_id"],
                    "worker": worker_id,
                    "worker_type": worker_type,
                    "task_start_s": r["start"],
                    "task_end_s": r["end"],
                    "task_duration_s": r["duration"],
                    "C": r["C"],
                    "acc": r["acc"],
                    "result_hash": r["result_hash"],
                }
                writer.writerow(r_row)
                f.flush()
            results.append(r)

    total = time.perf_counter() - start
    if f:
        f.close()
    best = max(results, key=lambda t: t["acc"])
    print(
        f"Concurrent ({worker_type}) completed in {total:.3f}s; best C={best['C']:.3e}, acc={best['acc']:.4f}"
    )
    return results


def mpi_futures_run(n_trials, seed_base, out_path=None, dataset_seed=42):
    if not mpi_available:
        raise RuntimeError("mpi4py is not available")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    init_shared_data(dataset_seed)
    run_id = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")

    f, writer = (None, None)
    if rank == 0:
        f, writer = write_csv_header(out_path)

    # Single-rank fallback: behave like serial but keep mode labeling.
    if size == 1:
        start = time.perf_counter()
        results = []
        for i in range(n_trials):
            r = run_trial(i, seed_base, dataset_seed)
            if writer:
                r_row = {
                    "run_id": run_id,
                    "mode": "mpi_futures",
                    "task_id": r["task_id"],
                    "worker": 0,
                    "worker_type": "mpi_single",
                    "task_start_s": r["start"],
                    "task_end_s": r["end"],
                    "task_duration_s": r["duration"],
                    "C": r["C"],
                    "acc": r["acc"],
                    "result_hash": r["result_hash"],
                }
                writer.writerow(r_row)
                f.flush()
            results.append(r)
        total = time.perf_counter() - start
        if f:
            f.close()
        best = max(results, key=lambda t: t["acc"])
        print(
            f"MPI futures (single rank) completed in {total:.3f}s; best C={best['C']:.3e}, acc={best['acc']:.4f}"
        )
        return results

    # Multi-rank path: root also executes tasks to avoid idle ranks.
    with MPICommExecutor(comm, root=0) as ex:
        if ex is None:
            # non-root ranks service executor tasks
            init_shared_data(dataset_seed)
            return []

        start = time.perf_counter()
        results = []

        # Distribute tasks: root handles a stride of tasks, workers handle the rest.
        root_tasks = [i for i in range(n_trials) if i % size == 0]
        worker_tasks = [i for i in range(n_trials) if i % size != 0]

        futures = [
            ex.submit(run_trial, i, seed_base, dataset_seed) for i in worker_tasks
        ]

        for i in root_tasks:
            r = run_trial(i, seed_base, dataset_seed)
            if writer:
                r_row = {
                    "run_id": run_id,
                    "mode": "mpi_futures",
                    "task_id": r["task_id"],
                    "worker": 0,
                    "worker_type": "mpi_root",
                    "task_start_s": r["start"],
                    "task_end_s": r["end"],
                    "task_duration_s": r["duration"],
                    "C": r["C"],
                    "acc": r["acc"],
                    "result_hash": r["result_hash"],
                }
                writer.writerow(r_row)
                f.flush()
            results.append(r)

        for fut in as_completed(futures):
            r = fut.result()
            if writer:
                r_row = {
                    "run_id": run_id,
                    "mode": "mpi_futures",
                    "task_id": r["task_id"],
                    "worker": "mpi_worker",
                    "worker_type": "mpi",
                    "task_start_s": r["start"],
                    "task_end_s": r["end"],
                    "task_duration_s": r["duration"],
                    "C": r["C"],
                    "acc": r["acc"],
                    "result_hash": r["result_hash"],
                }
                writer.writerow(r_row)
                f.flush()
            results.append(r)

        total = time.perf_counter() - start
        if f:
            f.close()
        best = max(results, key=lambda t: t["acc"])
        print(
            f"MPI futures completed in {total:.3f}s; best C={best['C']:.3e}, acc={best['acc']:.4f}"
        )
    return results


def mpi_manual_run(n_trials, seed_base, out_path=None, dataset_seed=42):
    """Explicit master/worker MPI implementation with root participation.

    The root rank distributes tasks to workers *and* executes a share of tasks
    locally to avoid an idle coordinator bottleneck. Communication uses a simple
    tagged protocol with small control messages only.
    """

    if not mpi_available or MPI is None:
        raise RuntimeError("mpi4py is not available")

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    TAG_TASK = 1
    TAG_RESULT = 2
    TAG_TERMINATE = 3

    # Ensure each rank has data ready before processing.
    init_shared_data(dataset_seed)

    # --- Single-rank fast path -------------------------------------------------
    if size == 1:
        start = time.perf_counter()
        run_id = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")
        f, writer = write_csv_header(out_path)
        results = []
        for i in range(n_trials):
            r = run_trial(i, seed_base, dataset_seed)
            if writer:
                writer.writerow(
                    {
                        "run_id": run_id,
                        "mode": "mpi_manual",
                        "task_id": r["task_id"],
                        "worker": 0,
                        "worker_type": "mpi_single",
                        "task_start_s": r["start"],
                        "task_end_s": r["end"],
                        "task_duration_s": r["duration"],
                        "C": r["C"],
                        "acc": r["acc"],
                        "result_hash": r["result_hash"],
                    }
                )
                f.flush()
            results.append(r)
        if f:
            f.close()
        total = time.perf_counter() - start
        best = max(results, key=lambda t: t["acc"]) if results else None
        print(
            f"MPI manual (single rank) completed in {total:.3f}s; best C={best['C']:.3e}, acc={best['acc']:.4f}"
            if best
            else "MPI manual (single rank) completed"
        )
        return results

    # --- Multi-rank master/worker path ----------------------------------------
    if rank == 0:
        run_id = datetime.now(timezone.utc).strftime("run_%Y%m%d_%H%M%S")
        f, writer = write_csv_header(out_path)
        start = time.perf_counter()

        task_queue = deque(range(n_trials))
        awaiting = set()
        results = []

        def record_result(r, worker_id, worker_type="mpi_worker"):
            if writer:
                writer.writerow(
                    {
                        "run_id": run_id,
                        "mode": "mpi_manual",
                        "task_id": r["task_id"],
                        "worker": worker_id,
                        "worker_type": worker_type,
                        "task_start_s": r["start"],
                        "task_end_s": r["end"],
                        "task_duration_s": r["duration"],
                        "C": r["C"],
                        "acc": r["acc"],
                        "result_hash": r["result_hash"],
                    }
                )
                f.flush()
            results.append(r)

        def dispatch_task(dest_rank, allow_terminate=True):
            """Send the next task to a worker and track outstanding replies."""
            if task_queue:
                payload = (task_queue.popleft(), seed_base, dataset_seed)
                comm.send(payload, dest=dest_rank, tag=TAG_TASK)
                awaiting.add(dest_rank)
                return True
            if allow_terminate:
                comm.send(None, dest=dest_rank, tag=TAG_TERMINATE)
                awaiting.add(dest_rank)
            return False

        def handle_message(status, msg):
            src = status.Get_source()
            tag = status.Get_tag()
            awaiting.discard(src)
            if tag == TAG_RESULT:
                r = msg
                record_result(r, worker_id=src, worker_type="mpi_worker")
                # Either send new work or a termination notice and await the ack.
                if task_queue:
                    dispatch_task(src)
                else:
                    comm.send(None, dest=src, tag=TAG_TERMINATE)
                    awaiting.add(src)

        # Handle the degenerate case early to avoid leaving workers hanging.
        if not task_queue:
            for worker in range(1, size):
                comm.send(None, dest=worker, tag=TAG_TERMINATE)
            # Collect acknowledgements so workers can exit cleanly.
            for _ in range(1, size):
                status = MPI.Status()
                comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            if f:
                f.close()
            print("MPI manual completed (no tasks to run)")
            return []

        # Prime workers with one task each (ranks 1..size-1)
        for worker in range(1, size):
            dispatch_task(worker, allow_terminate=True)

        # Root participates in computation while servicing incoming results.
        while task_queue or awaiting:
            # Drain any pending messages without blocking so we can reuse idle workers quickly.
            while comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG):
                status = MPI.Status()
                msg = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
                handle_message(status, msg)

            # Give root a task if available.
            if task_queue:
                task_id = task_queue.popleft()
                r = run_trial(task_id, seed_base, dataset_seed)
                record_result(r, worker_id=0, worker_type="mpi_root")
                # After finishing a root task, service any waiting messages immediately.
                while comm.Iprobe(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG):
                    status = MPI.Status()
                    msg = comm.recv(
                        source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status
                    )
                    handle_message(status, msg)
                continue

            # If no root work remains, block waiting for a worker result/termination.
            if awaiting:
                status = MPI.Status()
                msg = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
                handle_message(status, msg)

        if f:
            f.close()
        total = time.perf_counter() - start
        best = max(results, key=lambda t: t["acc"]) if results else None
        print(
            f"MPI manual completed in {total:.3f}s; best C={best['C']:.3e}, acc={best['acc']:.4f}"
            if best
            else "MPI manual completed"
        )
        return results

    # --- Worker ranks ----------------------------------------------------------
    while True:
        status = MPI.Status()
        msg = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()

        if tag == TAG_TERMINATE or msg is None:
            comm.send(None, dest=0, tag=TAG_TERMINATE)
            break

        task_id, seed_base_worker, dataset_seed_worker = msg
        r = run_trial(task_id, seed_base_worker, dataset_seed_worker)
        comm.send(r, dest=0, tag=TAG_RESULT)


def parse_args():
    p = argparse.ArgumentParser(description="Parallel Random Search (exercise)")
    p.add_argument(
        "--mode",
        choices=["serial", "threads", "processes", "mpi_futures", "mpi_manual"],
        default="serial",
    )
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--n_trials", type=int, default=32)
    p.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional task-level CSV log (disabled by default)",
    )
    p.add_argument("--seed_base", type=int, default=1000)
    p.add_argument("--dataset-seed", type=int, default=42)
    return p.parse_args()


def main():
    args = parse_args()
    mode = args.mode
    n = args.n_trials
    out = args.out
    workers = args.workers
    seed_base = args.seed_base
    dataset_seed = args.dataset_seed

    if mode == "serial":
        serial_run(n, seed_base, out, dataset_seed)
    elif mode == "threads":
        concurrent_run(
            n, seed_base, out, workers, use_processes=False, dataset_seed=dataset_seed
        )
    elif mode == "processes":
        concurrent_run(
            n, seed_base, out, workers, use_processes=True, dataset_seed=dataset_seed
        )
    elif mode == "mpi_futures":
        if not mpi_available:
            print("mpi4py not available; cannot run mpi_futures")
            return
        mpi_futures_run(n, seed_base, out, dataset_seed)
    elif mode == "mpi_manual":
        if not mpi_available:
            print("mpi4py not available; cannot run mpi_manual")
            return
        mpi_manual_run(n, seed_base, out, dataset_seed)


if __name__ == "__main__":
    main()
