from scipy.stats import norm
import scipy.stats.distributions as dist
import argparse
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import confint_proportions_2indep, test_proportions_2indep

def confidence_interval_diff_proportions(c1, s1, c2, s2, a):

    '''
    If compare is diff, then the confidence interval 
    is for diff = p1 - p2. If compare is ratio, 
    then the confidence interval is for the risk ratio 
    defined by ratio = p1 / p2. If compare is odds-ratio, 
    then the confidence interval is for the 
    odds-ratio defined by or = p1 / (1 - p1) / (p2 / (1 - p2).
    '''

    low_interval, upp_interval = confint_proportions_2indep(c1, s1, c2, s2, method=None, compare='diff', alpha=a)

    return low_interval, upp_interval

def hypothesis_test_diff_proportions(c1, s1, c2, s2):

    '''
    Assume two-tail test; Will add 
    functionality for left or right tail 
    test.
    '''

    print(c1, s1, c2, s2)

    statistic, pval = test_proportions_2indep(c1, s1, c2, s2, compare='diff', alternative='two-sided', return_results=False)

    return statistic, pval

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c1', '--count1', help='Enter number of successes of group 1.')
    parser.add_argument('-s1', '--samples1', help='Enter number of samples from group 1.')
    parser.add_argument('-c2', '--count2', help='Enter number of success of group 2.')
    parser.add_argument('-s2', '--samples2', help='Enter number of samples from group 2.')
    parser.add_argument('-ci', '--confidence_interval', help='Enter confidence interval.')
    args = parser.parse_args()

    count1 = float(args.count1)
    samples1 = float(args.samples1)
    count2 = float(args.count2)
    samples2 = float(args.samples2)
    alpha = 1 - float(args.confidence_interval)

    samples_statistic = (count1/samples1) - (count2/samples2)
    low_interval, upp_interval = confidence_interval_diff_proportions(count1, samples1, count2, samples2, alpha)
    statistic, pval = hypothesis_test_diff_proportions(count1, samples1, count2, samples2)

    print('Sample Statistic :')
    print("{:.3f}".format(samples_statistic))

    print('Range of interval :')
    print("{:.3f}".format(low_interval)," - " , "{:.3f}".format(upp_interval))

    print('Two-tailed Hypothesis Test  Statistic :', "{:.3f}".format(statistic))
    print('Two-tailed Hypothesis Test  p-value :', "{:.3f}".format(pval))
    # test_pval = 2*dist.norm.cdf(-np.abs(statistic))
    # print(test_pval)