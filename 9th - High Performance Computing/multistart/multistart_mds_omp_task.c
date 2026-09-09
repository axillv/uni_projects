#define _XOPEN_SOURCE 700
#define _DEFAULT_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <sys/time.h>
#include <unistd.h>

#define MAXVARS (250) /* max # of variables	     */
#define RNG_BASE_SEED (0x12345UL)
#define EPSMIN (1E-6) /* ending value of stepsize  */

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

int main(int argc, char *argv[])
{
	/* problem parameters */
	int nvars = 4;						   /* number of variables (problem dimension) */
	int ntrials = 64;					   /* number of trials */
	double lower[MAXVARS], upper[MAXVARS]; /* lower and upper bounds */

	/* mds parameters */
	double eps = EPSMIN;
	int maxfevals = 10000;
	int maxiter = 10000;
	double mu = 1.0;
	double theta = 0.25;
	double delta = 0.25;

	double startpt[MAXVARS], endpt[MAXVARS]; /* initial and final point of mds */
	double fx;								 /* function value at the final point of mds */
	int nt, nf;								 /* number of iterations and function evaluations used by mds */

	/* information about the best point found by multistart */
	TrialResult best;
	best.fx = 1e10;
	best.trial = -1;
	best.nt = -1;
	best.nf = -1;

	/* local variables */
	int trial, i;
	double t0, t1;

	/* initialization of lower and upper bounds of search space */
	for (i = 0; i < MAXVARS; i++)
		lower[i] = -2.0; /* lower bound: -2.0 */
	for (i = 0; i < MAXVARS; i++)
		upper[i] = +2.0; /* upper bound: +2.0 */

	t0 = get_wtime();

#pragma omp parallel
	{
#pragma omp single nowait // single thread creates tasks
		{
			for (trial = 0; trial < ntrials; trial++)
			{

/* here trial is assigned as a firstprivate because each task needs its own copy */
#pragma omp task firstprivate(trial) private(i, startpt, endpt, fx, nt, nf) shared(lower, upper, best)
				{
					RNGState rng;
					rng_init(&rng, trial);
					/* starting guess for rosenbrock test function, search space in [-2, 2) */
					for (i = 0; i < nvars; i++)
					{
						startpt[i] = lower[i] + (upper[i] - lower[i]) * rng_next(&rng);
					}

					int term = -1;
					mds(startpt, endpt, nvars, &fx, eps, maxfevals, maxiter, mu, theta, delta,
						&nt, &nf, lower, upper, &term);

#if DEBUG
					printf("\n\n\nMDS %d USED %d ITERATIONS AND %d FUNCTION CALLS, AND RETURNED\n", trial, nt, nf);
					for (i = 0; i < nvars; i++)
						printf("x[%3d] = %15.7le \n", i, endpt[i]);

					printf("f(x) = %15.7le\n", fx);
#endif

					/* build current trial result and update thread-private best via reduction */
					TrialResult cur;
					cur.fx = fx;
					cur.trial = trial;
					cur.nt = nt;
					cur.nf = nf;
					for (i = 0; i < nvars; i++)
						cur.pt[i] = endpt[i];
#pragma omp critical
					{
						if (cur.fx < best.fx)
							best = cur;
					}
				}
			}
		}
	}
	t1 = get_wtime();

	printf("\n\nFINAL RESULTS:\n");
	printf("Elapsed time = %.3lf s\n", t1 - t0);
	printf("Total number of trials = %d\n", ntrials);
	printf("Total number of function evaluations = %ld\n", funevals);
	printf("Best result at trial %d used %d iterations, %d function calls and returned\n", best.trial, best.nt, best.nf);
	for (i = 0; i < nvars; i++)
	{
		printf("x[%3d] = %15.7le \n", i, best.pt[i]);
	}
	printf("f(x) = %15.7le\n", best.fx);

	return 0;
}
