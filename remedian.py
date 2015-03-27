import random
from  collections import defaultdict
class Remedian:
    def __init__(self, base, ntile=50):
        self.ntile = ntile
        self.base = base
        self.exponent = 1
        self.storage = []
        self.positions = []
        self.storage.append([])
        self.positions.append(0)


    @staticmethod
    def partition(vector, left, right, pivotIndex):
        pivotValue = vector[pivotIndex]
        vector[pivotIndex], vector[right] = vector[right], vector[pivotIndex]  # Move pivot to end
        storeIndex = left
        for i in range(left, right):
            if vector[i] < pivotValue:
                vector[storeIndex], vector[i] = vector[i], vector[storeIndex]
                storeIndex += 1
        vector[right], vector[storeIndex] = vector[storeIndex], vector[right]  # Move pivot to its final place
        return storeIndex

    @staticmethod
    def _select(vector, left, right, k):
        while True:
            pivotIndex = random.randint(left, right)     # select pivotIndex between left and right
            pivotNewIndex = Remedian.partition(vector, left, right, pivotIndex)
            pivotDist = pivotNewIndex - left
            if pivotDist == k:
                return vector[pivotNewIndex]
            elif k < pivotDist:
                right = pivotNewIndex - 1
            else:
                k -= pivotDist + 1
                left = pivotNewIndex + 1

    @staticmethod
    def quickselect(vector, k, left=None, right=None):
        if left is None:
            left = 0
        lv1 = len(vector) - 1
        if right is None:
            right = lv1
        return Remedian._select(vector, left, right, k)

    def next_element(self, element, level=0):
        if level >= self.exponent:
            self.exponent += 1
            self.positions.append(0)
            self.storage.append([])
        if len(self.storage[level]) <= self.positions[level]:
            self.storage[level].append(element)
        else:
            self.storage[level][self.positions[level]] = element
        if self.positions[level] < (self.base - 1):
            self.positions[level] += 1
        else:
            self.positions[level] = 0
            if level == 0:
                self.next_element(Remedian.quickselect(self.storage[level], (len(self.storage[level]) * self.ntile)/100), level + 1)
            else:
                self.next_element(Remedian.quickselect(self.storage[level], len(self.storage[level])/2), level + 1)

    def result(self):
        weighted_total = 0
        total_weight = 0
        weight = 1
        for a in self.storage:
            for v in a:
                total_weight += weight
                weighted_total += v*weight
            weight *= self.base
        return weighted_total/total_weight

if __name__ == '__main__':
    ntile = 50
    set_size = 20000
    base = 101
    print "ntile of %d for a set size of %d using base %d" % (ntile, set_size, base)
    r = Remedian(base, ntile)

    for num in range(1,20000):
        r.next_element(num)

    print "sequential result: %d" % r.result()
    top = set_size
    bottom = 1
    r = Remedian(base, ntile)

    while(True):
        for i in range(base/2 + 1):
            r.next_element(top)
            top -= 1
            if top < bottom:
                break
        if top < bottom:
            break
        for i in range(base/2):
            r.next_element(bottom)
            bottom += 1
            if top < bottom:
                break
        if top < bottom:
            break

    print "worst case result: %d" % r.result()

    print "10 random permutations:"

    for i in range(10):
        r = Remedian(base, ntile)
        a = range(set_size)
        while len(a) > 0:
            r.next_element(a.pop(random.randint(0, len(a) - 1)))
        print r.result()


    print "distribution of 1000 random permutations:"
    result_counts = defaultdict(int)

    for i in range(1000):
        r = Remedian(base, ntile)
        a = range(set_size)
        while len(a) > 0:
            r.next_element(a.pop(random.randint(0, len(a) - 1)))
        result_counts[r.result()] += 1

    for key, value in sorted(result_counts.iteritems()):
        print "%d: %d" % (key,value)
