
from Base import Base
class Node(Base):

    # constructor, including node number and coordinates
    def __init__(self, nodeNr, x, y):

        # we inherit from the Base class! -> call Base's constructor
        Base.__init__(self)

        try:
            self._nodeNr  = int(nodeNr)
            self._x        = [float(x), float(y)]

        except Exception as e:
            self.appendLog(e.message)
            raise Exception("***Node Data error: object id id: %d" %self._id)

    def logData(self):
        self.appendLog("Node %d: x = %10.4f, y = %10.4f"\
                            %(self._nodeNr, self._x[0], self._x[1]))




