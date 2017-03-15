import matplotlib.pyplot as plt
from time import time
import numpy as np


def simulate(num_people, num_simulation, distribution_method):
    sample = np.zeros((num_simulation, num_people))
    elapsed = 0
    for i in xrange(num_simulation):
        current_amount = 1
        for j in xrange(num_people-1):
            start = time()
            delta = distribution_method(num_people-j, current_amount, num_people)
            elapsed += time() - start
            sample[i, j] = delta
            current_amount -= delta
        sample[i, num_people-1] = current_amount
    return sample, elapsed


def evaluate_by_moments(sample, params):
    n_moments = params.get('n_moments', 4)
    moments = np.zeros((n_moments, sample.shape[1]))
    aggregate = sample.copy()
    for i in xrange(n_moments):
        moments[i] = aggregate.mean(axis=0)
        aggregate *= sample

    epsilon = 0.0000001
    ratios = (moments.max(axis=1) + epsilon) / (moments.min(axis=1) + epsilon)
    print 'moment ratios =', ratios
    deviation = abs(ratios - 1).max()
    return deviation < params.get('threshold', 0.1)


def evaluate_by_variance(sample, params):
    var = sample.var(axis=0)
    print 'minimum variances =', var.min()
    return var.min() > params.get('min_var', 0.001)


def visualize(sample):
    n_col = sample.shape[1]
    f, axarr = plt.subplots(2, 2)
    axarr[0, 0].hist(sample[:, 0], bins=100, normed=1)
    axarr[0, 1].hist(sample[:, n_col/3], bins=100, normed=1)
    axarr[1, 0].hist(sample[:, 2 * n_col/3], bins=100, normed=1)
    axarr[1, 1].hist(sample[:, -1], bins=100, normed=1)
    plt.show()


def evaluate(distribution_method, vis=False):
    print '-' * 40
    print 'Evaluating', distribution_method.func_name
    sample, elapsed = simulate(4, 1000000, distribution_method)
    if vis:
        visualize(sample)
    print 'time elapsed:', elapsed
    m_params = {'n_moments': 4, 'threshold': 0.1}
    result = evaluate_by_moments(sample, m_params)
    if not result:
        print 'FAILED, moments does not match'
        return
    v_params = {'min_var': 0.001}
    result = evaluate_by_variance(sample, v_params)
    if not result:
        print 'FAILED, variance is too small'
        return
    if elapsed > 2:
        print 'FAILED, too slow'
        return
    print 'PASSED'


def sample_by_beta(j, current_amount, num_people):
    c = 2
    x = np.random.beta(c, c*(j-1))
    return current_amount * x


def sample_by_order_statistics(j, current_amount, num_people):
    x = sorted(np.random.rand(2*j-1))
    return current_amount * x[1]


def sample_by_gaussian(j, current_amount, num_people):
    x = max(np.random.normal(1.0/j, 0.1/j), 0)
    return current_amount * min(x, 1)


def sample_by_gaussian2(j, current_amount, num_people):
    x = max(np.random.normal(1.0/j, 0.5/j), 0)
    return current_amount * min(x, 1)


def sample_by_dirac(j, current_amount, num_people):
    return current_amount / float(j)


if __name__ == '__main__':
    evaluate(sample_by_beta, vis=True)
    # evaluate(sample_by_order_statistics)
    # evaluate(sample_by_gaussian)
    # evaluate(sample_by_gaussian2)
    # evaluate(sample_by_dirac)
