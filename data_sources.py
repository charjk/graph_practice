import time, threading, random, math

class DataSource():

    def __init__(self):
        pass


class SWTimedSource(DataSource):

    def __init__(self, period, init_state):
        super(SWTimedSource, self).__init__()

        self.period = period
        self.running = False
        self.cbLock = threading.Lock()
        with self.cbLock:
            self.callback = None

        self.stateLock = threading.Lock()
        with self.stateLock:
            self.state = init_state
            self.time = 0.0
            self.newData = True


    def step():
        self.time = self.time + self.period
        self.newData = True

    def connect(self, cb):
        with self.cbLock:
            self.callback = cb


    def __main_loop(self):
        while self.running:
            time.sleep(self.period)
            with self.stateLock:
                self.step()        
                t = float(self.time)
                d = float(self.state)

            with self.cbLock:
                threading.Thread(target=self.callback, args=(t,d)).start()


    def start(self):
        if self.running == False:
            self.mainLoop = threading.Thread(target=self.__main_loop)
            self.running = True
            self.mainLoop.start()


    def stop(self):
        if self.running == True:
            self.running = False
            self.mainLoop.join()


    def readData(self):
        with self.stateLock:
            s = float(self.state)
            t = float(self.time)
            n = float(self.newData)
            self.newData = False

        return s, t, n


class RandomWalk(SWTimedSource):

    def __init__(self, period=1.0, init_state=0.0, 
                 sigma=1.0, rseed=None):

        super(RandomWalk, self).__init__(period, init_state)

        self.sigma = sigma
        random.seed(rseed)


    def step(self):
        self.time = self.time + self.period
        self.state = self.state + random.gauss(0.0, self.sigma)
        self.newData = True


class Sinusoid(SWTimedSource):

    def __init__(self, period=1.0, init_state=1.0, 
                 amp=1.0, offset = 0.0, freq=0.1, phase=0.0):

        super(Sinusoid, self).__init__(period, init_state)

        self.amplitude = amp
        self.offset = offset
        self.freq = freq
        self.phase = phase


    def step(self):
        self.time = self.time + self.period
        self.state = self.amplitude*math.cos(2.0*math.pi*self.freq*self.time + self.phase) + self.offset


class FileSource(DataSource):

    def __init__(self):
        super(FileSource, self).__init__()


def printCB(t, d):
    print(str(t) + ", " + str(d))

