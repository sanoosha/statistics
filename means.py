from scipy.stats import norm, t
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


def sample_size_single_mean(confidence_interval, margin_error, std_dev, tails=2):

    z_critical = -norm.ppf((1-confidence_interval)/tails)
    print('z-score :', "{:.3f}".format(z_critical))
    ss = (z_critical*std_dev/margin_error)**2

    return ss


if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument('-m1', '--mean1', help='Enter mean of group 1.')
    # parser.add_argument('-m2', '--mean2', help='Enter mean of group 2.')
    # parser.add_argument('-ci', '--confidence_interval', help='Enter confidence interval.')
    # args = parser.parse_args()

    # ## group 1 values
    # mean1 = float(args.mean1)

    # ## group 2 values
    # mean2 = float(args.mean2)

    # ## alpha level
    # alpha = 1 - float(args.confidence_interval)

    # ## Run statistic functions
    # samples_statistic = mean1 - mean2
    # low_interval, upp_interval = confidence_interval_diff_proportions(mean1, mean2, alpha)
    # statistic, pval = hypothesis_test_diff_proportions(mean1, mean2)
    sample_size = sample_size_single_mean(confidence_interval=0.90, margin_error=3.5, std_dev=13.3)

    # print('Sample Statistic :')
    # print("{:.3f}".format(samples_statistic))

    # print('Range of interval :')
    # print("{:.3f}".format(low_interval)," - " , "{:.3f}".format(upp_interval))

    # print('Two-tailed Hypothesis Test Statistic :', "{:.3f}".format(statistic))
    # print('Two-tailed Hypothesis Test p-value :', "{:.3f}".format(pval))

    print('Sample size for estimating single mean :', "{:.2f}".format(sample_size))
