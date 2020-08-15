import random
import numpy
import scipy
from scipy.stats import bernoulli

time_count = 100000
arm_count = 100
alpha = 1
beta = 1

#to be a list of bernoulli districutions, which model newly repleased books
arms = [] 

#to be the list of parameters for the bernoulli distributions
ctrs_true = []

for i in range(arm_count):
    # set a random ctr less than 10%
    ctr_true = random.random()/10
    ctrs_true.append(ctr_true)
    
results = [[0]*2 for i in range(arm_count)]

hit = 0

for i in range(time_count):
    if i % 100 == 0:
        print("completed:"+str(i)+"/"+str(time_count))
    ctrs_sampled = []
    for j in range(arm_count):
        ctrs_sampled.append(numpy.random.beta(alpha + results[j][1], beta + results[j][0]))
    arm_to_pull = numpy.argmax(ctrs_sampled)
    outcome = bernoulli.rvs(ctrs_true[arm_to_pull])
    if outcome == 0:
        results[arm_to_pull][0] += 1
    else:
        hit += 1
        results[arm_to_pull][1] += 1

print("outcome ctr:" + str(hit/time_count))
print("true ctrs:"+ str(ctrs_true))