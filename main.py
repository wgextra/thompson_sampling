import random
import numpy
import scipy
from scipy.stats import bernoulli

class Results:
    class Result:
        def __init__(self):
            self.success = 0
            self.failure = 0

    def __init__(self,arm_count):
        self._results = [self.Result() for i in range(arm_count)]
    
    def record_success(self,arm_index):
        self._results[arm_index].success += 1

    def record_failure(self,arm_index):
        self._results[arm_index].failure += 1

    def get_success_count(self,arm_index):
        return self._results[arm_index].success

    def get_failure_count(self,arm_index):
        return self._results[arm_index].failure


if __name__ == "__main__":
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
        
    results = Results(arm_count)

    hit = 0

    for i in range(time_count):
        if i % 10000 == 0:
            print("completed:"+str(i)+"/"+str(time_count))
        ctrs_sampled = []
        for j in range(arm_count):
            ctrs_sampled.append(numpy.random.beta(alpha + results.get_success_count(j), beta + results.get_failure_count(j)))
        arm_to_pull = numpy.argmax(ctrs_sampled)
        outcome = bernoulli.rvs(ctrs_true[arm_to_pull])
        if outcome == 0:
            results.record_failure(arm_to_pull)
        else:
            hit += 1
            results.record_success(arm_to_pull)

    print("outcome ctr:" + str(hit/time_count))
    print("true ctrs:"+ str(ctrs_true))
    print("true ctrs mean:"+ str(sum(ctrs_true)/arm_count))

