import copy
import gameEssentials
import curses

TYPE_VERTICAL = 0
TYPE_HORIZONTAL = 1

class Modifier(object):
        def __init__(self):
                self.modifiedObject = None

        def update(self):
                pass

class AutoDelete(Modifier):
        def __init__(self,ticks):
                self.ticksToDelete = ticks

        def update(self):
                self.ticksToDelete -= 1
                if self.ticksToDelete < 1:
                        self.modifiedObject.parent.removeObject(self.modifiedObject)

class KeyboardControl(Modifier):

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

        def __init__(self,patterns,trailsHolder,type = TYPE_HORIZONTAL):
                Modifier.__init__(self)
                self.lastPosition = [-1,-1]
                self.index = -1
                self.patterns = patterns
                self.trailsHolder = trailsHolder
                self.type = type

        def update(self):
                positionChanged = False
                if self.type == TYPE_HORIZONTAL:
                        if self.lastPosition[1] != self.modifiedObject.parent.position[1]:
                                positionChanged = True
                else:
                        if self.lastPosition[0] != self.modifiedObject.parent.position[0]:
                                positionChanged = True

                if positionChanged == True:
                        self.index += 1
                        if self.index == len(self.patterns):
                                self.index = 0

                        self.modifiedObject.pattern = self.patterns[self.index]

                        object = gameEssentials.WorldObject()
                        self.modifiedObject.getWorldPosition(object.position)
                        object.pattern = "#"
                        object.addModifier(AutoDelete(10))
                        self.trailsHolder.addObject(object)

                #update position
                self.lastPosition = copy.deepcopy(self.modifiedObject.parent.position)
