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


def calculate_moments(sample, n_moments):
    moments = np.zeros((n_moments, sample.shape[1]))
    aggregate = sample.copy()
    for i in xrange(n_moments):
        moments[i] = aggregate.mean(axis=0)
        aggregate *= sample
    return moments


def evaluate_by_moments(moments, threshold):
    ratios = moments.max(axis=1) / moments.min(axis=1)
    result = ratios.max()
    print ratios
    return result < threshold


def visualize(sample):
    pass


def evaluate(distribution_method):
    sample, elapsed = simulate(10, 100000, distribution_method)
    print '{} seconds'.format(elapsed)
    moments = calculate_moments(sample, 4)
    fair = evaluate_by_moments(moments, 1.1)
    if fair:
        print 'pass'
    else:
        print 'fail'


def beta_sample(j, current_amount, num_people):
    c = 1.5
    x = np.random.beta(c, c*(j-1))
    return current_amount * x


def order_sample(j, current_amount, num_people):
    x = np.random.rand(j-1).min()
    return current_amount * x


if __name__ == '__main__':
    evaluate(beta_sample)
    evaluate(order_sample)
