
Multistart MDS (Rosenbrock)

Modes
- Sequential: multistart_mds_seq
- OpenMP parallel for: multistart_mds_omp
- OpenMP tasks: multistart_mds_omp_task
- MPI: multistart_mds_mpi

Build
- Sequential/OpenMP: `make multistart_mds_seq multistart_mds_omp multistart_mds_omp_task`
- MPI: `make multistart_mds_mpi` (requires mpicc)

Run examples
- Sequential: `./multistart_mds_seq`
- OpenMP (8 threads): `OMP_NUM_THREADS=8 ./multistart_mds_omp`
- OpenMP tasks (8 threads): `OMP_NUM_THREADS=8 ./multistart_mds_omp_task`
- MPI (4 ranks): `mpirun -np 4 ./multistart_mds_mpi`

Benchmarking
- Batch sweep: `./run_all_benchmarks.sh` (env: CONCURRENCY_LIST, MODE_LIST, MPIEXEC)
- Per-run wrapper: `./run_multistart.sh -m {seq|omp|omp_task|mpi} -c <concurrency>`
- Results saved to `benchmarks_summary.csv` and logs/.

Notes
- Objective `f()` sleeps 100µs to mimic expensive evaluation.
- RNG seed per trial = BASE_SEED + trial for reproducible comparisons across modes.
