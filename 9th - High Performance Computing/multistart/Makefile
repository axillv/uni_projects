CC=gcc
MPICC ?= mpicc
CFLAGS=-Wall -O3
# CFLAGS+=-DDEBUG
LDLIBS=-lm
OMPFLAGS=-fopenmp

all: multistart_mds_seq multistart_mds_omp multistart_mds_omp_task multistart_mds_mpi

multistart_mds_seq: multistart_mds_seq.c torczon.c Makefile
	$(CC) $(CFLAGS) -o multistart_mds_seq multistart_mds_seq.c torczon.c $(LDLIBS)

multistart_mds_omp: multistart_mds_omp.c torczon.c Makefile
	$(CC) $(CFLAGS) $(OMPFLAGS) -o multistart_mds_omp multistart_mds_omp.c torczon.c $(LDLIBS)

multistart_mds_omp_task: multistart_mds_omp_task.c torczon.c Makefile
	$(CC) $(CFLAGS) $(OMPFLAGS) -DOMPTASK -o multistart_mds_omp_task multistart_mds_omp_task.c torczon.c $(LDLIBS)

multistart_mds_mpi: multistart_mds_mpi.c torczon.c Makefile
	$(MPICC) $(CFLAGS) -o multistart_mds_mpi multistart_mds_mpi.c torczon.c $(LDLIBS)

clean:
	rm -f multistart_mds_seq multistart_mds_omp multistart_mds_omp_task multistart_mds_mpi
