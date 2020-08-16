import random
import numpy
import scipy
from scipy.stats import bernoulli

class Arm:
    def __init__(self,ctr):
        self.success = 0
        self.failure = 0
        self.ctr = ctr
        
    def add_success(self):
        self.success += 1

    def add_failure(self):
        self.failure += 1

    def get_success_count(self):
        return self.success

    def get_failure_count(self):
        return self.failure

class Arms:
    def __init__(self,ctrs_true):
        self.arms = [Arm(ctr) for ctr in ctrs_true]
        self.total_success = 0
    
    def _sample_from_beta(self,success_count,failure_count):
        #prior distribution is uniform: a = b = 1
        alpha = 1 + success_count
        beta = 1 + failure_count
        return numpy.random.beta(alpha, beta)

    def choose_arm_to_pull(self):
        ctrs_sampled = []
        for arm_index in range(len(self.arms)):
            success_count = self.arms[arm_index].get_success_count()
            failure_count = self.arms[arm_index].get_failure_count()
            ctrs_sampled.append(self._sample_from_beta(success_count,failure_count))
        return numpy.argmax(ctrs_sampled)

    def pull_and_record_outcome(self,chosen_arm_index):
        p = self.arms[chosen_arm_index].ctr
        outcome = bernoulli.rvs(p)
        if outcome == 0: #failure
            self.arms[chosen_arm_index].add_failure()
        else: #success
            self.total_success+=1
            self.arms[chosen_arm_index].add_success()


if __name__ == "__main__":
    #number of trials
    time_count = 100000
    
    #to be the list of parameters for the bernoulli distributions
    ctrs_true = []

    for i in range(100):
        # set a random ctr less than 10%
        ctr_true = random.random()/10
        ctrs_true.append(ctr_true)
    arms = Arms(ctrs_true)
    
    for i in range(time_count):
        if i % 10000 == 0:
            print("completed:"+str(i)+"/"+str(time_count))
        ctrs_sampled = []
        arm_to_pull = arms.choose_arm_to_pull()
        arms.pull_and_record_outcome(arm_to_pull)

    print("outcome ctr:" + str(arms.total_success/time_count))
    print("true ctrs:"+ str(ctrs_true))
    print("true ctrs mean:"+ str(sum(ctrs_true)/len(arms.arms)))