"""This module contains essential tools for creating game(Core of Game Engine)"""
import curses
import math

def priority(node):
	"""Return Node draw priority"""
        return node.priority

class Node(object):
	"""
	Node can hold other Nodes as children
	Note:
	Position: is in parent scope not world.
	Priority: 0 is highest,so Node with priority 1 will be updated after Node with priority 0.
	"""
        def __init__(self):
                self.objects = []
                self.screen = None
                self.parent = None
                self.position = [0,0]
                self.direction = 0
                self.priority = 0
		#queues for objects
                self.addList = []#objects will be added in next update
                self.removeList = []#objects will be removed after next update

        def addObject(self,object):
		"""Adds Object to this Node ,claiming ownership over this object by setting parent field
		Note: Object will be added in next update"""
                object.screen = self.screen
                object.parent = self
                self.addList.append(object)


        def removeObject(self,object):
                """Removes Object from this Node
                Note: Object will be removed in next update"""
                self.removeList.append(object)

        def update(self):
		"""Updates Node by adding/removing objects and calling children update method"""
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
                """Returning child located in specified local coordinates"""
                for object in self.objects:
                        if (int(self.position[0]) == int(object.position[0])) and (int(self.position[1]) == int(object.position[1])):
                                return object

                return None

        def getWorldPosition(self,finalPosition,DepthLimitNode = None):
		"""Recursively change passed position,depth can be limited by setting end object reference as second parameter"""
                finalPosition[0] += self.position[0]
                finalPosition[1] += self.position[1]
                if self.parent != DepthLimitNode:
                        self.parent.getWorldPosition(finalPosition)

        def rotate(self,angle):
		"""Rotates this Node and children by specified angle"""
                radians = (angle * math.pi)/180
                self.direction += angle
                for object in self.objects:
                        y = object.position[0]
                        x = object.position[1]

                        object.position[0] = x * math.sin(radians) + y * math.cos(radians)
                        object.position[1] = x * math.cos(radians) - y * math.sin(radians)


class WorldObject(Node):
	"""WorldObject is extension of Node.
	World objects are moveable and drawable,and can be modified by various modifiers"""
        def __init__(self):
                Node.__init__(self)
                self.speed = 0
                self.pattern = ""
                self.colorPair = 0
                self.modifiers = []

        def update(self):
		"""Update Position(based on speed and direction) and update modifiers"""
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
		"""Assign passed modifier to this object"""
                modifier.modifiedObject = self
                self.modifiers.append(modifier)

class World(Node):
	"""World is extension of Node ,should be root object."""
        def __init__(self):
                Node.__init__(self)
                cameraSize = []#not used now

        def updateWorld(self):
        	"""Clears screen and start recursive updating of his children"""
	        self.screen.clear()
                self.update()
                self.screen.refresh()
