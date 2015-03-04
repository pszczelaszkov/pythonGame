import curses
import math

def priority(node):
        return node.priority

class Node(object):

        def __init__(self):
                self.objects = []
                self.screen = None
                self.parent = None
                self.position = [0,0]
                self.direction = 0
                self.priority = 0
                self.addList = []
                self.removeList = []

        def addObject(self,object):
                object.screen = self.screen
                object.parent = self
                self.addList.append(object)


        def removeObject(self,object):
                self.removeList.append(object)

        def update(self):

                for object in reversed(self.addList):
                        self.objects.append(object)
                        self.addList.remove(object)

                for object in reversed(self.removeList):
                        self.objects.remove(object)
                        self.removeList.remove(object)

                self.objects = sorted(self.objects,key=priority)

                for object in self.objects:
                        object.update()

        def getObjectFromPosition(position):
                for object in self.objects:
                        if (int(self.position[0]) == int(object.position[0])) and (int(self.position[1]) == int(object.position[1])):
                                return object

                return None

        def getWorldPosition(self,finalPosition,DepthLimitNode = None):
                finalPosition[0] += self.position[0]
                finalPosition[1] += self.position[1]
                if self.parent != DepthLimitNode:
                        self.parent.getWorldPosition(finalPosition)

        def rotate(self,angle):
                radians = (angle * math.pi)/180
                self.direction += angle
                for object in self.objects:
                        y = object.position[0]
                        x = object.position[1]

                        object.position[0] = x * math.sin(radians) + y * math.cos(radians)
                        object.position[1] = x * math.cos(radians) - y * math.sin(radians)


class WorldObject(Node):

        def __init__(self):
                Node.__init__(self)
                self.speed = 0
                self.pattern = ""
                self.colorPair = 0
                self.modifiers = []

        def update(self):
                Node.update(self)

                for modifier in self.modifiers:
                        modifier.update()

                if(self.parent != None):
                        worldPosition = [0,0]
                        self.getWorldPosition(worldPosition)
                        self.screen.addstr(int(worldPosition[0]),int(worldPosition[1]),self.pattern,curses.color_pair(self.colorPair))
                        self.position[0] += math.sin((self.direction * math.pi)/180) * self.speed
                        self.position[1] += math.cos((self.direction * math.pi)/180) * self.speed

        def addModifier(self,modifier):
                modifier.modifiedObject = self
                self.modifiers.append(modifier)

class World(Node):

        def __init__(self):
                Node.__init__(self)
                cameraSize = []

        def updateWorld(self):
                self.screen.clear()
                self.update()
                self.screen.refresh()
