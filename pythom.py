from random import randint

class Process:
    def __init__(self, pid, at, bt, wt=0):
        self.pid = pid # process number
        self.at = at # arrival time
        self.bt = bt # burst time
        self.wt = wt # waiting time
        self.rt = self.bt
        self.start = None
        self.end = None
        
    def __str__(self):
        return f'{self.pid},{self.at},{self.bt},{self.wt}'
    
    __repr__ = __str__

    def generator(self, num_of_processes, filename):
        file = open(filename, 'w')
        for i in range(0, num_of_processes):
            file.write(str(Process(i, randint(1,10), randint(1,10))) + '\n')
        file.close()
                
    def read(self, filename):
        data = []
        file = open(filename, 'r')
        for process in file:
            temp = process.split(',')
            data.append(Process(int(temp[0]), int(temp[1]), int(temp[2])))
        file.close()
        return data

class CPU:
    def __init__(self):
        self.processes = []
        self.done = []
        self.time = 0
    
    def take_data(self, filename):
        proc = Process(0,0,0)
        self.processes = proc.read(filename)
        self.processes.sort(key=lambda x: x.at)
    
    def simulation(self, filename, results, is_sjf=False):
        self.take_data(filename)
        self.queue = []
        self.is_sjf = is_sjf
        while True:
            for proc in self.processes:
                if proc.at == self.time:
                    self.processes.remove(proc)
                    self.queue.append(proc)
            
            if self.queue:
                self.algorithm()
                

            self.time += 1
            if self.time > 10000:
                break
        file = open(results, 'w')
        for proc in self.done:
            file.write(str(proc.at) + ',' +  str(proc.bt) + ',' +  str(proc.wt) + '\n' )
        file.close()

    def algorithm(self):
        if self.is_sjf:
            self.queue[1:] = sorted(self.queue[1:], key=lambda x: x.bt)
        if not self.queue[0].start:
            self.queue[0].start = self.time
        
        self.queue[0].rt -= 1
        
        if self.queue[0].rt == 0:
            self.queue[0].end = self.time + 1
            self.queue[0].wt = self.queue[0].end - self.queue[0].bt - self.queue[0].at
            self.done.append(self.queue[0])
            del self.queue[0]

proc = Process(1,2,3)
proc.generator(20,'generated.csv')
cpu = CPU()
cpu.simulation('generated.csv', 'sorted.csv')
# cpu1 = CPU()
# cpu1.simulation('abc.csv', 'dcs,csv', is_sjf=True)


# def generator(n, filename):
#     file = open(filename, 'w')
#     for i in range(0, n):
#         file.write(str(randint(1,10)) + '\n')
#     file.close()
            
# def read(filename):
#     data = []
#     file = open(filename, 'r')
#     for ref in file:
#         data.append(int(ref))
#     file.close()
#     return data

# class CPU_pages:
#     def __init__(self, size=4):
#         self.frame = []
#         self.size = size
#         self.rep = 0
    
#     def take_data(self, filename):
#         self.calls = read(filename)
        
#     def simulation(self, filename, results=None, is_lru=False):
#         self.take_data(filename)
#         self.is_lru = is_lru
#         for call in self.calls:
#             self.algorithm(call)
#         print(self.rep)
    
#     def algorithm(self, ref):
#         if ref not in self.frame:
#             self.frame.insert(0, ref)
#             self.rep += 1
#         if self.is_lru and ref in self.frame:
#             del self.frame[self.frame.index(ref)]
#             self.frame.insert(0, ref)
#         if len(self.frame) > self.size:
#             del self.frame[self.size]

# cpu = CPU_pages()

# generator(15,'abdsa.csv')
# cpu.simulation('abdsa.csv', 'asdasdasdsad.csv', is_lru=True)