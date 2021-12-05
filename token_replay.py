class Node(object):
    def __init__(self,label,type,pairNodes = [], isStart = False, isEnd = False):
        self.label = label
        self.node_type = type # t -> Transaction | s -> State
        self.transcTo = pairNodes
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
        n_start = Node('start','t',isStart=True)
        n_a = Node('a','s')
        n_b = Node('b','s')
        n_c = Node('c','s')
        n_d = Node('d','s')
        n_e = Node('e','s')
        n_f = Node('f','s')
        n_g = Node('g','s')
        n_h = Node('h','s')
        n_p1 = Node('p1','t')
        n_p2 = Node('p2','t')
        n_p3 = Node('p3','t')
        n_p4 = Node('p4','t')
        n_p5 = Node('p4','t')
        n_end = Node('end','t',isEnd=True)
        n_start.transcTo = [n_a]
        n_a.transcTo = [n_p1,n_p2]
        n_p1.transcTo = [n_b,n_c]
        n_b.transcTo = [n_p3]
        n_c.transcTo = [n_p3]
        n_p2.transcTo = [n_d]
        n_d.transcTo = [n_p4]
        n_p3.transcTo = [n_e]
        n_e.transcTo = [n_p5]
        n_p4.transcTo = [n_e]
        n_p5.transcTo = [n_g,n_h,n_f]
        n_f.transcTo = [n_p1,n_p2]
        n_g.transcTo = [n_end]
        n_h.transcTo = [n_end]

        return n_start

    def consumeActivity(self, activ):
        self.c += activ.tokens
        self.p += len(activ.transcTo)
        explored = []
        for process in activ.transcTo:

            if process.isEnd:
                self.reachEnd = True
            
            explored += process.transcTo
            
            for n in process.transcTo:
                n.tokens += 1 
        
        return explored

    def checkTrace(self, trace):
        root = self.build()
        self.p += 1
        exploredActivities = root.transcTo

        for n in exploredActivities:
            n.tokens += 1

        while len(trace) != 0:
            n = trace.pop(0)
            for activ in exploredActivities:
                if n == activ.label: 
                    exploredActivities += self.consumeActivity(activ)
                    break
        
        if self.reachEnd:
            self.c += 1

        print([self.p,self.c,self.m,self.r])
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







