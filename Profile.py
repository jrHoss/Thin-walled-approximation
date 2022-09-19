# -*- en/coding: UTF-8/ -*-

from Base import Base
from Element import Element
from math import *


class Profile(Base):

    # constructor
    def __init__(self, name):
        Base.__init__(self)

        #input data
        self._name = name               # profile name
        self._e = []                    # element list (initialize as empty list)
        # profile properties

        self._a = 0                     # profile area
        self._s = [0, 0]                # static moment
        self._iu = [0, 0, 0]            # 2nd moment of area
        self._cg = [0, 0]               # center of gravity
        self._ic = [0, 0, 0]            # 2nd moment of area w.r.t CG coordinate
        self._ip = [0, 0]               # 2nd moment of area tensor's principal value
        self._ang = 0                   # angle between current x-axis abd  1st principal axis

    def addElement(self, e):
        if not isinstance(e, Element):
            raise Exception("***Error : can only pass Element object")
        self._e.append(e)


    def logData(self):
        self.appendLog("---Begin Profile Output")
        self.appendLog("---Profile Name: " + self._name)
        self.appendLog("Area.................:           A: %10.3f" %self._a)
        self.appendLog("Static moment........:      Sx,Sy.: %10.3f,%10.3f" \
                        %tuple(self._s)) #%(self._s[0],self._s[1]))
        self.appendLog("2nd moment of Area...: Ixx,Iyy,Ixy: %10.3f,%10.3f,%10.3f"\
                        %tuple(self._iu))  #%(self._iu[0],self._iu[1],self._iu[2]))
        self.appendLog("Center of Gravity....:       Cx,Cy: %10.3f,%10.3f" \
                       %tuple(self._cg))   #%(self._cg[0],self._cg[1]))
        self.appendLog("Shifed SMOA in CG CS : Ixx,Iyy,Ixy: %10.3f,%10.3f,%10.3f" \
                       % tuple(self._ic))
        self.appendLog("SMOA principal value.:    Ieta,Ixi: %10.3f,%10.3f" \
                       % tuple(self._ip))
        self.appendLog("rotation angle.......:      pistar: %10.3f°" \
                       %self._ang)

        for elem in self._e: elem.logData()
        self.appendLog("---End Profile Output")


    def computeProfileProps(self):
        if len(self._e) < 1:
            raise Exception("***Error: No element found in profile")

        # part 1 : compute accumulated/ integral properties
        for e in self._e:
            self._a += e.getA()
            # accumulate area

            for i in range(2):
                self._s[i] += e.getS(i)
                # accumulate static moment

            for i in range(3):
                self._iu[i] += e.getI(i)
                # accumulate moment of inertia (these are in user coordinate system)

        # Part 2: derived global profile properties
        self._cg[0] = self._s[1] / self._a
        self._cg[1] = self._s[0] / self._a

        # shift s.m.o.a. to CG coordinate system using thr parallel axis theorem
        self._ic[0] = self._iu[0] - self._cg[1]**2 * self._a
        self._ic[1] = self._iu[1] - self._cg[0] ** 2 * self._a
        self._ic[2] = self._iu[2] + self._cg[0]*self._cg[1] * self._a

        # principal axis transformation / principal value (eigenvalues) of the profile's
        # s.m.o.a. tensor
        Ixx = self._ic[0]
        Iyy = self._ic[1]
        Ixy = self._ic[2]
        self._ip[0] = (Ixx + Iyy + sqrt(4 * Ixy ** 2 + (Ixx - Iyy)**2)) / 2
        self._ip[1] = (Ixx + Iyy + sqrt(4 * Ixy ** 2 + (Ixx - Iyy)**2)) / 2
        # use atan2() to avoid div. by 0 if the profile is symmetric (Ixx = Iyy)
        self._ang   = -atan2(2*Ixy, Iyy-Ixx)/2
        self._ang  *= 180/pi
    # view the profile shape
    def view(self):
        try:
            import pylab
            self.appendLog("Profile.view(): pylab imported!")
        except:
            self.appendLog("***Warning: profile.view(): pylab not found")
            return

        # for each element in the profile.
        for e in self._e:
            x1 = e._n[0]._x[0]
            x2 = e._n[1]._x[0]
            y1 = e._n[0]._x[1]
            y2 = e._n[1]._x[1]
            pylab.plot([x1, x2], [y1, y2], 'b')
            pylab.plot([x1, x2], [y1, y2], 'pr')

        pylab.axis('equal')
        pylab.title(self._name)
        pylab.grid('on')
        pylab.show()