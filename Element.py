
from Base import Base
from Node import Node

class Element(Base):
    def __init__(self, no, n1, n2, t, viewlog=False):
        Base.__init__(self)

        if not isinstance(n1, Node):
            raise Exception("Error: invalid Node 1")
        if not isinstance(n2, Node):
            raise Exception("Error: invalid Node2")
        self._n = [n1, n2]
        self._viewlog = viewlog            # please change it to True to view the details for each element.
        try:
            self._no = int(no)
            self._t = float(t)
        except Exception as e:
            self.appendLog(e.message)
            raise Exception("***Element Data error: object id id: %d" %self._id)

    def logData(self):
        while self._viewlog:
            self.appendLog(">Element %d: t : %.3f, l: %.3f" %(self._no, self._t, self.getL()))
            self._n[0].logData()
            self._n[1].logData()
            self.appendLog("        A:  %10.3f" %self.getA())
            self.appendLog("       CG: (%10.3f,%10.3f)" % (self.getC(0),self.getC(1)))
            self.appendLog("Static moment: Sx,Sy: %10.3f,%10.3f" %(self.getS(0),self.getS(1)))
            self.appendLog("2nd moment of Area : Ixx,Iyy,Ixy: %10.3f,%10.3f%10.3f"\
                           %(self.getI(0), self.getI(1), self.getI(2)))
        # for n in self._n:
        #     n.logData()


    # def delt(self,i):
    #     return (self._n[1])
    def getL(self):
        return (((self._n[0]._x[0] - self._n[1]._x[0])**2
                +(self._n[0]._x[1] - self._n[1]._x[1])**2)**0.5)

    def getA(self):
        return (self.getL() * self._t)

    def getC(self, i):
        return ((self._n[0]._x[i] + self._n[1]._x[i])/2)

    def getS(self,i):
        #we need the other index here -> (i+1)%2
        return self.getC((i+1)%2) * self.getA()

    def getI(self,i):
        n1x = self._n[0]._x[0]
        n1y = self._n[0]._x[1]
        n2x = self._n[1]._x[0]
        n2y = self._n[1]._x[1]
        Cx  = self.getC(0)
        Cy = self.getC(1)
        A = self.getA()


        if i ==0 :
            return ((n2y - n1y) ** 2 / 12 + Cy ** 2) * A
        if i==1:
            return ((n2x - n1x) ** 2 / 12 + Cx ** 2) * A
        if i==2:
            return -((n2x - n1x)*(n2y - n1y)/12 + Cx*Cy) * A


