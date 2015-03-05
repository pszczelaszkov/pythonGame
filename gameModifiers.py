"""This module contains modifiers that can be used to modify WorldObject"""
import copy
import gameEssentials
import curses

TYPE_VERTICAL = 0
TYPE_HORIZONTAL = 1

class Modifier(object):
	"""Modifier Class is Abstract"""
        def __init__(self):
                self.modifiedObject = None

        def update(self):
                pass

class AutoDelete(Modifier):
	"""Delete modifiedObject when passed in constructor ticks hits 0"""
        def __init__(self,ticks):
                self.ticksToDelete = ticks

        def update(self):
                self.ticksToDelete -= 1
                if self.ticksToDelete < 1:
                        self.modifiedObject.parent.removeObject(self.modifiedObject)

class KeyboardControl(Modifier):
	"""Reads pressed key's and changes modifiedObject behaviour"""
        def __init__(self,screen):
                self.screen = screen

        def update(self):
                key = self.screen.getch()

                if key == 119: #w
                        self.modifiedObject.direction = 270
                        self.modifiedObject.speed = 1
                if key == 115: #s
                        self.modifiedObject.direction = 90
                        self.modifiedObject.speed = 1
                if key == 97: #a
                        self.modifiedObject.direction = 180
                        self.modifiedObject.speed = 1
                if key == 100: #d
                        self.modifiedObject.direction = 0
                        self.modifiedObject.speed = 1
                if key == -1:  #None
                        self.modifiedObject.speed = 0


class TracksModifier(Modifier):
	"""Modify object by changing his pattern and dropping trails making it looks like moving track."""
        def __init__(self,patterns,trailsHolder,type = TYPE_HORIZONTAL):
                Modifier.__init__(self)
                self.lastPosition = [-1,-1]
                self.index = -1
                self.patterns = patterns
                self.trailsHolder = trailsHolder
                self.type = type

        def update(self):
                positionChanged = False#assume object is standing still
                if self.type == TYPE_HORIZONTAL:#in horizontal type check X axis
                        if self.lastPosition[1] != self.modifiedObject.parent.position[1]:
                                positionChanged = True
                else:#in vertical type check Y axis
                        if self.lastPosition[0] != self.modifiedObject.parent.position[0]:
                                positionChanged = True

                if positionChanged == True:
			#change pattern to next in patterns list
                        self.index += 1
                        if self.index == len(self.patterns):
                                self.index = 0

                        self.modifiedObject.pattern = self.patterns[self.index]
			#leave trails in specified trailHolder node
                        object = gameEssentials.WorldObject()
                        self.modifiedObject.getWorldPosition(object.position)
                        object.pattern = "#"
                        object.addModifier(AutoDelete(10))#disappear after 10 tick(~1s)
                        self.trailsHolder.addObject(object)

                #update position
                self.lastPosition = copy.deepcopy(self.modifiedObject.parent.position)
