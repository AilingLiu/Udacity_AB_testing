This file is used to guide AB testing on binomial distribution with two groups: control and experiment.


Terminologies:
* $x_{cont}$: number of success in control group
* $x_{exp}$: number of success in experiment group
* $N_{cont}$: total number of trials in control group
* $N_{exp}$: total number of trials in experiment group
* $\hat{p}_{cont}$: expected probability of control group
* $\hat{p}_{exp}$: expected probability of experiment group
* $\hat{d}$: estimated probability differences between control and experiment group
* $SE_{pool}$: pooled standard error
* $\hat{p}_{pool}$: pool estimated probability

Steps:

0. Choose statistical significance level $\alpha$ and practical significance level $\beta$. Get the critical value Z according to $1-\alpha$

1. Construct Null hypothesis

$$\hat{d}=0$$
where $\hat{d}\sim N(0, SE_{pool})$.

2. Construct 2x2 table as below:

|   |Control   | Experiment   |
|---|---|---|
|Num. of Success   | $x_{cont}$   |$x_{exp}$   |
|Total Number of Trials| $N_{cont}$  |$N_{exp}$   |

3. Calculate expected probability of success of each group:

$\hat{p}_{cont}=\dfrac{x_{cont}}{N_{cont}}$

$\hat{p}_{exp}=\dfrac{x_{exp}}{N_{exp}}$

4. Calculate $\hat{d}$:

$\hat{d}=\hat{p}_{exp}-\hat{p}_{cont}$

5. Calculate pooled probability:

$\hat{p}_{pool} = \dfrac{x_{cont}+x_{exp}}{N_{cont}+N_{exp}}$

6. Calculate pooled standard error:

$\sqrt{\hat{p}_{pool}(1-\hat{p}_{pool})\times(\dfrac{1}{N_{cont}}+\dfrac{1}{N_{exp}})}$

7. Calculate $m=Z*SE_{pool}$

*****Evaluate statistical significance******

if $m < \alpha_{0.05}$, reject $H_{0}$;

Else, fail to reject $H_{0}$

*****Evaluate Practical significance*****

8. Calculate confidence interval for $\hat{d}$

[$\hat{d}-m$, $\hat{d}+m$]

Differences between control and experiment group lower bound: $\hat{d}-m$

Differences between control and experiment group upper bound: $\hat{d}+m$

if lower bound value is smaller than the practical significance $\beta$, we will not proceed new change that has been adapted on experiment group to system simply because it fail our expectation to be worthy.
