import pandas as pd
import numpy as np

url = 'https://raw.githubusercontent.com/AilingLiu/Udacity_AB_testing/master/data.csv'

df = pd.read_csv(url, index_col='uuid', usecols=['uuid', 'multiple_session_conducted', 'test_group'])
print(df.head(10))

"""
Toy data:
         multiple_session_conducted test_group
uuid
1002313                       False       test
1003270                       False    control
1003726                        True    control
1003911                       False       test
1005340                       False       test
1006034                       False    control
1007483                       False       test
1007614                       False    control
1008319                       False    control
1008548                        True    control
"""

# compare proportions of success between control and experiment group based on binomial distribution

# create count table
def create_count_table(df, group_col='test_group', event_col='event_col', success_label=True):
  count_tab = pd.crosstab(df[event_col], df[group_col], margins=True, margins_name='Total').loc[[success_label, 'Total'], :]
  print('Count Table: ')
  print('*'*40)
  print(count_tab)
  return count_tab

def get_event_counts(count_table, control_name='control', exp_name='test'):
  x_cont, x_exp = count_table.loc[count_table.index[0], control_name], count_table.loc[count_table.index[0], exp_name]
  N_cont, N_exp = count_table.loc[count_table.index[1], control_name], count_table.loc[count_table.index[1], exp_name]
  return x_cont, x_exp, N_cont, N_exp

def get_ab_proportion(x_cont, x_exp, N_cont, N_exp):
  con_prop = round(x_cont/N_cont, 3)
  exp_prop = round(x_exp/N_exp, 3)
  print('Estimated proportion in Experiment Group: {}\nEstimated proportion in Control Group: {}'.format(exp_prop, con_prop))
  return con_prop, exp_prop

def get_prop_diff(cont_bprop, exp_prop):
  estimated_diff = round(exp_prop - cont_bprop, 5)
  print('The change due to the experiment is: {}%'.format(estimated_diff*100))
  return estimated_diff

def get_poopled_prob(x_cont, x_exp, N_cont, N_exp):
  return round((x_cont + x_exp) / (N_cont + N_exp), 5)

def get_pooled_stderr(pool_prob, n_cont, n_exp):
  pool_stderr = np.round(np.sqrt(pool_prob*(1-pool_prob)*(1/n_cont + 1/n_exp)), 5)
  print('Pooled Standard Error(Uncertainty): {}'.format(pool_stderr))
  return pool_stderr

def calculate_margin_error(sig_level=0.05, stderr=0.005):
  import scipy.stats as st
  me = round(st.norm.ppf(1-sig_level/2)*stderr, 5)
  print('Calculated Margin Error: {} at {} significance level'.format(me, sig_level))
  return me

def get_confi_interval(cal_mean, margin, sig_level=0.05):
  conf_level = 1-sig_level
  lower_bound = round(cal_mean - margin, 3)
  upper_bound = round(cal_mean + margin, 3)
  print('True value falls into following interval at {}% confidence: [{}, {}]'.format(conf_level*100,lower_bound, upper_bound))
  print('This means that if you run the experiment again for another 10,000 trials, \
  you might get successful event for about {} to {} times.'.format(lower_bound*10000, upper_bound*10000))
  return lower_bound, upper_bound

def evaluate_result(cal_d, margin_error, prac_sig=0.02):
  if cal_d < -margin_error or cal_d > margin_error:
    print('The change is statistically significant.')

    if cal_d -margin_error >= prac_sig:
      print('The change is practically significant.')
    else:
      print('But the change fails practical significance expectation.')
  else:
    print('Fail to reject null hypothesis. The change is not statistically significant.')

def compare_two_group_proportion(df, group_col='test_group', event_col='event_col', \
                                 success_label=True, control_name='control', exp_name='test', sig_level=0.05, prac_sig=0.02):

  count_tab = create_count_table(df, group_col=group_col, event_col=event_col, success_label=success_label)
  print('Result:')
  print('*'*40)
  xcont, xexp, ncont, nexp = get_event_counts(count_tab, control_name=control_name, exp_name=exp_name)
  ap, bp = get_ab_proportion(xcont, xexp, ncont, nexp)
  d = get_prop_diff(ap, bp)
  p = get_poopled_prob(xcont, xexp, ncont, nexp)
  stdr = get_pooled_stderr(p, ncont, nexp)
  m = calculate_margin_error(sig_level=sig_level, stderr=stdr)
  lb, ub = get_confi_interval(d, m, sig_level=sig_level)
  evaluate_result(cal_d=d, margin_error=m, prac_sig=prac_sig)


compare_two_group_proportion(df, event_col='multiple_session_conducted')

""" You will see below result:

Estimated proportion in Experiment Group: 0.121
Estimated proportion in Control Group: 0.115
The change due to the experiment is: 0.6%
Pooled Standard Error(Uncertainty): 0.00762
Calculated Margin Error: 0.01493 at 0.05 significance level
True value falls into following interval at 95.0% confidence: [-0.009, 0.021]
This means that if you run the experiment again for another 10,000 trials,   you might get successful event for about -90.0 to 210.0 times.
Fail to reject null hypothesis. The change is not statistically significant.
"""
