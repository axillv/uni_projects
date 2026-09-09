Random Search for L1 Logistic Regression

Setup
- Python 3, `numpy`, `scikit-learn`; `mpi4py` for MPI modes.
- Optional: `conda create -n rs_env python`; `pip install numpy scikit-learn mpi4py`.

Modes (`rs.py --mode`)
- `serial`
- `threads` (ThreadPoolExecutor)
- `processes` (ProcessPoolExecutor)
- `mpi_futures` (mpi4py.futures)
- `mpi_manual` (explicit master/worker)

Run examples
- Serial, 100 trials: `python rs.py --mode serial --n_trials 100 --out results.csv`
- Threads, 8 workers: `python rs.py --mode threads --workers 8 --n_trials 200 --out results.csv`
- Processes, 4 workers: `python rs.py --mode processes --workers 4 --n_trials 200 --out results.csv`
- MPI futures, 4 ranks: `mpirun -np 4 python rs.py --mode mpi_futures --n_trials 200 --out results.csv`
- MPI manual, 4 ranks: `mpirun -np 4 python rs.py --mode mpi_manual --n_trials 200 --out results.csv`

Benchmarking
- Batch sweep: `./run_all_benchmarks.sh` (configure CONCURRENCY_LIST, MODE_LIST, DATASET_SEED, etc.)
- MPI helper/wrapper: `./run_mpi.sh` (env: MODE, WORKERS, MPI_PROCS, N_TRIALS, OUT_PREFIX)
- Results written to `benchmarks_summary.csv` and logs/.

Notes
- Dataset is built once and reused by workers when possible.
- Trials are independent; RNG seeded per trial for reproducible comparisons.
