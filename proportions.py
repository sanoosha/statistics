from scipy.stats import norm, t
import scipy.stats.distributions as dist
import argparse
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import confint_proportions_2indep, test_proportions_2indep

def confidence_interval_diff_proportions(c1, n1, c2, n2, confidence_interval):

    '''
    If compare is diff, then the confidence interval 
    is for diff = p1 - p2. If compare is ratio, 
    then the confidence interval is for the risk ratio 
    defined by ratio = p1 / p2. If compare is odds-ratio, 
    then the confidence interval is for the 
    odds-ratio defined by or = p1 / (1 - p1) / (p2 / (1 - p2).
    '''

    low_interval, upp_interval = confint_proportions_2indep(c1, n1, c2, n2, method=None, compare='diff', alpha=1-confidence_interval)

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


def sample_size_single_proportion(confidence_interval, margin_error, p=0.5, tails=2):

    z_critical = -norm.ppf((1-confidence_interval)/tails)
    print('z-score :', "{:.3f}".format(z_critical))
    ss = (z_critical/margin_error)**2*(1-p)*p

    return ss


def two_proportions_hypothesis_test(c1, n1, c2, n2, confidence_interval, tails=2):

    p_pooled = (c1 + c2)/(n1 +n2)
    std_error = np.sqrt(p_pooled*(1-p_pooled)*(1/n1 + 1/n2))
    z = ((c1/n1 - c2/n2) - 0)/std_error

    print('z-score two proportion hypothesis test :', "{:.3f}".format(z))
    pval = norm.cdf(z)*tails

    return pval


def one_proportion_hypothesis_test(c1, n1, p0, tails=2):

    std_error = np.sqrt(p0*(1-p0)/n1)
    z = (c1/n1 - p0)/std_error

    print('z-score :', "{:.3f}".format(z))
    pval = norm.cdf(z)

    return pval


def two_proportions_confidence_interval(c1, n1, c2, n2, confidence_interval, tails=2):

    z_critical = -norm.ppf((1-confidence_interval)/tails)
    # print('z-score two proportion confidence interval :', "{:.3f}".format(z_critical))
    std_error = np.sqrt(((c1/n1)*(1-(c1/n1))/n1) + ((c2/n2)*(1-(c2/n2))/n2))
    # print('standard error two proportion confidence interval :', "{:.3f}".format(std_error))

    low_interval = (c1/n1)-(c2/n2) - z_critical*std_error
    upp_interval = (c1/n1)-(c2/n2) + z_critical*std_error

    return low_interval, upp_interval

def one_proportions_confidence_interval(c1, n1, confidence_interval, tails=2):

    z_critical = -norm.ppf((1-confidence_interval)/tails)
    print('z-score :', "{:.3f}".format(z_critical))

    std_error = np.sqrt((c1/n1)*(1-(c1/n1))/n1)

    low_interval = (c1/n1) - z_critical*std_error
    upp_interval = (c1/n1) + z_critical*std_error

    return low_interval, upp_interval


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c1', '--count1', help='Enter number of successes of group 1.')
    parser.add_argument('-n1', '--samples1', help='Enter number of samples from group 1.')
    parser.add_argument('-c2', '--count2', help='Enter number of success of group 2.')
    parser.add_argument('-n2', '--samples2', help='Enter number of samples from group 2.')
    parser.add_argument('-ci', '--confidence_interval', help='Enter confidence interval.')
    args = parser.parse_args()

    ## group 1 values
    count1 = float(args.count1)
    samples1 = float(args.samples1)

    ## group 2 values
    count2 = float(args.count2)
    samples2 = float(args.samples2)

    ## alpha level
    alpha = 1 - float(args.confidence_interval)

    ## Run statistic functions
    samples_statistic = (count1/samples1) - (count2/samples2)
    print('Sample Statistic :')
    print("{:.3f}".format(samples_statistic))

    # ## confidence intervals
    # low_interval, upp_interval = confidence_interval_diff_proportions(c1=6, n1=24, c2=14, n2=24, confidence_interval=0.83)
    # print('Range of interval :')
    # print("{:.3f}".format(low_interval)," - " , "{:.3f}".format(upp_interval))
    # print('Length of confidence interval :', "{:.3f}".format(abs(upp_interval-low_interval)))
    
    # low_interval, upp_interval = two_proportions_confidence_interval(c1=6, n1=24, c2=14, n2=24, confidence_interval=0.83, tails=2)
    # print('Range of interval :')
    # print("{:.3f}".format(low_interval)," - " , "{:.3f}".format(upp_interval))
    # print('Length of confidence interval :', "{:.3f}".format(abs(upp_interval-low_interval)))

    ## hypothesis tests
    # pval = two_proportions_hypothesis_test(c1=6, n1=24, c2=14, n2=24, confidence_interval=0.38, tails=2)
    statistic, pval = hypothesis_test_diff_proportions(count1, samples1, count2, samples2)

    print('Two-tailed Hypothesis Test Statistic :', "{:.3f}".format(statistic))
    print('Two-tailed Hypothesis Test p-value :', "{:.3f}".format(pval))

    # ## sample size
    # sample_size = sample_size_single_proportion(confidence_interval=0.90, margin_error=0.06, p=0.25)
    # print('Sample size for estimating single proportion :', "{:.2f}".format(sample_size))

