from Node import Node
from Element import Element
from Profile import Profile
from math import sin, radians, cos

class Combined_section(Profile):

    def __init__(self, h_T, b_T, s_T,                                                   # T_Section.
                 h_I, b_I, s_I, t_I,                                                    # I_Section.
                 D, t_D,                                                                # Pipe_Section.
                 length, load, E,                                                       # Values needed for deflection.
                 num_n=20 ):                                                            # Num of nodes in pipe sections. Default is 20
        # initialize the parent class's constructor
        name = "Combined Section"
        Profile.__init__(self, name)

        # Initializing the parameters of the model.
        try:
            # The values for the T_Section.
            self._h_T = float(h_T)                                                      # height of the T_section
            self._b_T = float(b_T)                                                      # length of the T_section flange.
            self._s_T = float(s_T)  # length                                            # Thickness of the T_section.

            # The values for the I_Section.
            self._h_I = float(h_I)                                                      # height of the I_section.
            self._b_I = float(b_I)                                                      # length of the I_section flange.
            self._s_I = float(s_I)                                                      # Thickness of the I_section web.
            self._t_I = float(t_I)                                                      # Thickness of the I_section flange.

            # The Values for the Pipe section.
            self._D = float(D)                                                          # Outer diameter of the Pipe section.
            self._t_D = float(t_D)                                                      # Thickness of the pipe section.
            self._num_n = int(num_n)                                                    # Number of nodes in the Pipe section. Default is 20 nodes.

            # The values needed for calculating the deflection of the beam.
            self._length = float(length)                                                # Length of the beam.
            self._load = float(load)                                                    # Load on the beam.
            self._E = float(E)                                                          # Young's modulus.

        except ValueError:
            print("Please check the input values.")
        # Helping values for the coordinates.
        self._y1 = self._t_I / 2
        self._x1 = self._b_I / 2
        self._y2 = self._h_I - (self._t_I / 2)
        self._x2 = self._b_T / 2
        self._y3 = self._h_T + self._h_I - (self._s_T / 2)
        self._r = self._D / 2 - self._t_D / 2
        # Checking the validity of the parameters
        if self._h_T <= 0:
            raise Exception("> Invalid height of T section : %f" % self._h_T)
        elif self._b_T <= 0:
            raise Exception("> Invalid length of the T section Flange: %f" % self._b_T)
        elif self._s_T <= 0:
            raise Exception("> Invalid length of the T section Flange: %f" % self._s_T)
        elif self._h_I <= 0:
            raise Exception("> Invalid height of I section : %f" % self._h_I)
        elif self._b_I <= 0:
            raise Exception("> Invalid length of the I section Flange: %f" % self._b_I)
        elif self._s_I <= 0:
            raise Exception("> Invalid length of the I section Flange: %f" % self._s_I)
        elif self._t_I <= 0:
            raise Exception("> Invalid length of the I section Flange: %f" % self._t_I)
        elif self._D <= 0:
            raise Exception("> Invalid Diameter for the pipe section: %f" % self._s_I)
        elif self._t_D <= 0:
            raise Exception("> Invalid thickness for the pipe section: %f" % self._t_I)

        # creating nodes and elements.
        nodes = [Node(1, 0, self._y1),
                 Node(2, self._x1, self._y1),
                 Node(3, - self._x1, self._y1),
                 Node(4, 0, self._y2),
                 Node(5, self._x1, self._y2),
                 Node(6, - self._x1, self._y2),
                 Node(7, 0, self._y3),
                 Node(8, self._x2, self._y3),
                 Node(9, - self._x2, self._y3),
                 Node(10, self._r, self._y3),
                 Node(11, - self._r, self._y3)]

        # Creating nodes for the pipe section on the right-hand side.
        Phi = 0  # angle
        angle_increment = 360 / self._num_n

        for i in range(11, self._num_n + 11):
            nodes += [Node(i + 1, self._r + self._r * (sin(radians(Phi))),
                           self._y3 - self._r + self._r * cos(radians(Phi)))]
            Phi += angle_increment

        # Creating nodes for the pipe section on the left-hand side.
        Phi = 0  # angle

        for i in range(self._num_n + 11, self._num_n + 11 + self._num_n):
            nodes += [Node(i + 1, - self._r + self._r * (sin(radians(Phi))),
                           self._y3 - self._r + self._r * cos(radians(Phi)))]
            Phi += angle_increment

        # Generating elements using nodes and thicknesses.
        el = [Element(1, nodes[0], nodes[1], self._t_I),
              Element(2, nodes[0], nodes[2], self._t_I),
              Element(3, nodes[0], nodes[3], self._s_I),
              Element(4, nodes[3], nodes[4], self._t_I),
              Element(5, nodes[3], nodes[5], self._t_I),
              Element(6, nodes[3], nodes[6], self._s_T),
              Element(7, nodes[6], nodes[7], self._s_T),
              Element(8, nodes[6], nodes[8], self._s_T)]

        # Generating Elements for the right pipe section:
        for i in range(8, self._num_n + 8):
            if i == (self._num_n + 8) - 1:
                el += [Element(i + 1, nodes[i+3], nodes[9], self._t_D)]
            else:
                el += [Element(i + 1, nodes[i+3], nodes[i + 4], self._t_D)]

        # Generating Elements for the left pipe section:
        for x in range(self._num_n + 8,  self._num_n + 8 + self._num_n):
            if x == (self._num_n + 8 + self._num_n) - 1:
                el += [Element(x + 1, nodes[x + 3], nodes[10], self._t_D)]
            else:
                el += [Element(x + 1, nodes[x + 3], nodes[x + 4], self._t_D)]

        for e in el:
            self.addElement(e)
        self.computeProfileProps()

    def Calculate_deflection(self):
        uniform_load = self._load * (1 / self._length)
        # Maximum value of deflection is at the Free end, where x = L.
        deflection = - ((self._length * 1000) ** 4 * uniform_load)/(8 * self._E * (10 ** 3) * self._ic[0])
        return self.appendLog(f" Maximum Deflection in mm is {deflection}")
