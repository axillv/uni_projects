#define _XOPEN_SOURCE 700
#define _DEFAULT_SOURCE

#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

#define MAXVARS (250) /* max # of variables */
#define RNG_BASE_SEED (0x12345UL)
#define EPSMIN (1E-6) /* ending value of stepsize */

/* prototype of local optimization routine, code available in torczon.c */
extern void mds(double *startpoint, double *endpoint, int n, double *val, double eps, int maxfevals, int maxiter,
                double mu, double theta, double delta, int *ni, int *nf, double *xl, double *xr, int *term);
typedef struct
{
    struct drand48_data state;
} RNGState;

static inline void rng_init(RNGState *rng, int trial)
{
    long seed = (long)RNG_BASE_SEED + (long)trial;
    srand48_r(seed, &rng->state);
}

static inline double rng_next(RNGState *rng)
{
    double value;
    drand48_r(&rng->state, &value);
    return value;
}

/* global variables */
unsigned long funevals = 0;

/* Rosenbrock classic parabolic valley ("banana") function */
double f(double *x, int n)
{
    double fv;
    int i;

    funevals++;
    fv = 0.0;
    for (i = 0; i < n - 1; i++) /* rosenbrock */
        fv = fv + 100.0 * pow((x[i + 1] - x[i] * x[i]), 2) + pow((x[i] - 1.0), 2);

    usleep(100); /* do not remove, introduces some artificial work */

    return fv;
}

double get_wtime(void)
{
    struct timeval t;

    gettimeofday(&t, NULL);

    return (double)t.tv_sec + (double)t.tv_usec * 1.0e-6;
}

/* struct for keeping trial results*/
typedef struct
{
    double fx;
    int trial, nt, nf;
    double pt[MAXVARS];
} TrialResult;

#define MPI_CHECK(call)                                                        \
    do                                                                         \
    {                                                                          \
        int _rc = (call);                                                      \
        if (_rc != MPI_SUCCESS)                                                \
        {                                                                      \
            char _msg[MPI_MAX_ERROR_STRING];                                   \
            int _len = 0;                                                      \
            MPI_Error_string(_rc, _msg, &_len);                                \
            fprintf(stderr, "MPI error %d at %s:%d: %s\n", _rc, __FILE__,      \
                    __LINE__, _msg);                                           \
            MPI_Abort(MPI_COMM_WORLD, _rc);                                    \
        }                                                                      \
    } while (0)

static void trial_result_init(TrialResult *result)
{
    result->fx = 1e10;
    result->trial = -1;
    result->nt = -1;
    result->nf = -1;
    for (int i = 0; i < MAXVARS; i++)
        result->pt[i] = 0.0;
}

static void trial_result_reduce(void *in, void *inout, int *len, MPI_Datatype *type)
{
    TrialResult *src = (TrialResult *)in;
    TrialResult *dest = (TrialResult *)inout;
    for (int idx = 0; idx < *len; idx++)
    {
        if (src[idx].fx < dest[idx].fx)
            memcpy(&dest[idx], &src[idx], sizeof(TrialResult));
    }
}

int main(int argc, char *argv[])
{
    MPI_CHECK(MPI_Init(&argc, &argv));

    int rank, size;
    MPI_CHECK(MPI_Comm_rank(MPI_COMM_WORLD, &rank));
    MPI_CHECK(MPI_Comm_size(MPI_COMM_WORLD, &size));

    /* problem parameters */
    int nvars = 4;                         /* number of variables (problem dimension) */
    int ntrials = 64;                      /* number of trials */  
    double lower[MAXVARS], upper[MAXVARS]; /* lower and upper bounds */

    /* mds parameters */
    double eps = EPSMIN;
    int maxfevals = 10000;
    int maxiter = 10000;
    double mu = 1.0;
    double theta = 0.25;
    double delta = 0.25;

    /* information about the best point found by multistart */
    double startpt[MAXVARS], endpt[MAXVARS]; /* initial and final point of mds */
    double fx;                               /* function value at the final point of mds */ 
    int nt, nf;                             /* number of iterations and function evaluations used by mds */

    TrialResult best;
    trial_result_init(&best);

    int trial, i;

    for (i = 0; i < MAXVARS; i++)
        lower[i] = -2.0;
    for (i = 0; i < MAXVARS; i++)
        upper[i] = +2.0;

    double t0 = get_wtime();
    for (trial = rank; trial < ntrials; trial += size)
    {
        RNGState rng;
        rng_init(&rng, trial);

        for (i = 0; i < nvars; i++)
            startpt[i] = lower[i] + (upper[i] - lower[i]) * rng_next(&rng);

        int term = -1;
        mds(startpt, endpt, nvars, &fx, eps, maxfevals, maxiter, mu, theta, delta,
            &nt, &nf, lower, upper, &term);

        if (fx < best.fx)
        {
            best.fx = fx;
            best.trial = trial;
            best.nt = nt;
            best.nf = nf;
            for (i = 0; i < nvars; i++)
                best.pt[i] = endpt[i];
        }
    }

    MPI_Datatype mpi_trial_result;
    int blocklengths[5] = {1, 1, 1, 1, MAXVARS};
    MPI_Datatype types[5] = {MPI_DOUBLE, MPI_INT, MPI_INT, MPI_INT, MPI_DOUBLE};
    MPI_Aint displacements[5];
    TrialResult reference;
    trial_result_init(&reference);
    MPI_Aint base_address;
    MPI_Get_address(&reference, &base_address);
    MPI_Get_address(&reference.fx, &displacements[0]);
    MPI_Get_address(&reference.trial, &displacements[1]);
    MPI_Get_address(&reference.nt, &displacements[2]);
    MPI_Get_address(&reference.nf, &displacements[3]);
    MPI_Get_address(&reference.pt[0], &displacements[4]);
    for (int entry = 0; entry < 5; entry++)
        displacements[entry] -= base_address;
    MPI_CHECK(MPI_Type_create_struct(5, blocklengths, displacements, types, &mpi_trial_result));
    MPI_CHECK(MPI_Type_commit(&mpi_trial_result));

    MPI_Op trial_result_best_op;
    MPI_CHECK(MPI_Op_create(trial_result_reduce, 1, &trial_result_best_op));

    TrialResult global_best;
    trial_result_init(&global_best);

    MPI_CHECK(MPI_Reduce(&best, &global_best, 1, mpi_trial_result, trial_result_best_op, 0, MPI_COMM_WORLD));

    unsigned long total_funevals = 0;
    MPI_CHECK(MPI_Reduce(&funevals, &total_funevals, 1, MPI_UNSIGNED_LONG, MPI_SUM, 0, MPI_COMM_WORLD));

    if (rank == 0)
    {
        double t1 = get_wtime();
        printf("\n\nFINAL RESULTS:\n");
        printf("Elapsed time = %.3lf s\n", t1 - t0);
        printf("MPI ranks = %d\n", size);
        printf("Total number of trials = %d\n", ntrials);
        printf("Total number of function evaluations = %lu\n", total_funevals);
        printf("Best result at trial %d used %d iterations, %d function calls and returned\n",
               global_best.trial, global_best.nt, global_best.nf);
        for (i = 0; i < nvars; i++)
            printf("x[%3d] = %15.7le \n", i, global_best.pt[i]);
        printf("f(x) = %15.7le\n", global_best.fx);
    }

    MPI_CHECK(MPI_Op_free(&trial_result_best_op));
    MPI_CHECK(MPI_Type_free(&mpi_trial_result));
    MPI_CHECK(MPI_Finalize());

    return 0;
}
