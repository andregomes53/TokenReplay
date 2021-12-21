class Node(object):
    def __init__(self,label,pairNodes = []):
        self.label = label
        self.transcTo = pairNodes

class ActivityNode(Node):
    def __init__(self, label, pairNodes=[], father=[]):
        super().__init__(label, pairNodes=pairNodes)
        self.father = father

class ProcessNode(Node):
    def __init__(self, label, pairNodes=[], isStart=False, isEnd=False):
        super().__init__(label, pairNodes=pairNodes)
        self.isStart = isStart
        self.isEnd = isEnd
        self.tokens = 0

class Model(object):

    def __init__(self):
        self.p = 0
        self.c = 0
        self.m = 0
        self.r = 0
        self.build()

    def build(self):
        n_start = ProcessNode('start', isStart=True)
        n_end = ProcessNode('end', isEnd=True)
        n_p1 = ProcessNode('p1')
        n_p2 = ProcessNode('p2')
        n_p3 = ProcessNode('p3')
        n_p4 = ProcessNode('p4')
        n_p5 = ProcessNode('p4')
        n_a = ActivityNode('a', pairNodes=[n_p1,n_p2], father=[n_start])
        n_b = ActivityNode('b', pairNodes=[n_p3], father=[n_p1])
        n_c = ActivityNode('c', pairNodes=[n_p3], father=[n_p1])
        n_d = ActivityNode('d', pairNodes=[n_p4], father=[n_p2])
        n_e = ActivityNode('e', pairNodes=[n_p5], father=[n_p3,n_p4])
        n_f = ActivityNode('f', pairNodes=[n_p1,n_p2], father=[n_p5])
        n_g = ActivityNode('g', pairNodes=[n_end], father=[n_p5])
        n_h = ActivityNode('h', pairNodes=[n_end], father=[n_p5])
        n_start.transcTo = [n_a]
        n_p1.transcTo = [n_b,n_c]
        n_p2.transcTo = [n_d]
        n_p3.transcTo = [n_e]
        n_p4.transcTo = [n_e]
        n_p5.transcTo = [n_g,n_h,n_f]

        n_start.tokens = 1 #Root process should start with a token

        return n_start

    def consumeActivity(self, activ):
        for f in activ.father: # Consume the tokens from parent processes
            f.tokens -= 1
            self.c += 1
        
        explored = []
        
        for c in activ.transcTo: # Produce a token for all child processes
            if c.isEnd:
                self.reachEnd = True
            explored += c.transcTo
            c.tokens += 1
            self.p += 1
        
        return explored

    def checkTrace(self, trace):
        root = self.build()

        exploredActivities = root.transcTo
        
        while len(trace) != 0:
            n = trace.pop(0)

            for activ in exploredActivities:
                if n == activ.label:
                    found = True
                    exploredActivities += self.consumeActivity(activ)
                    break

            if not found:
                self.m += 1
                #self.seekNext()
            
            found = False 

        if self.reachEnd:
            self.c += 1

        print([self.p,self.c,self.m,self.r])

        if self.m == self.r == 0:
            print('trace succeeded')
        else:
            print('the trace has failed in conformance check')

        return self.getFitness()

    def getFitness(self):
        missing_term = .5 * (1-self.m/self.c)
        remaining_tern = .5 * (1-self.r/self.p)
        fitness = missing_term + remaining_tern
        return fitness

def main():
    trace = ['a','c','d','e','h']
    model = Model()
    print(model.checkTrace(trace))

main()