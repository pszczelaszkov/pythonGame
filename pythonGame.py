"""
Main game module.
Contains game loop and init methods
"""
import gameEssentials
import gameModifiers
import curses
import time

def main(stdscr):
	"""Call to start game engine"""
        stdscr.nodelay(True)#disable delays while getch()
        curses.curs_set(0)#hide cursor
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_GREEN)

	#create main node (world)
        world = gameEssentials.World()
        world.screen = stdscr
        world.cameraSize = (stdscr.getmaxyx()[0] - 2,stdscr.getmaxyx()[1]-10)#not used now

        #creating player controlled tank
        player = gameEssentials.WorldObject()
        player.priority = 1
        player.position = [20,70]
        player.addModifier(gameModifiers.KeyboardControl(stdscr))

	#create separate node for trails
        trailHolder = gameEssentials.Node()
        trailHolder.priority = 0#priority 0 is highest

        world.addObject(player)
        world.addObject(trailHolder)
	#define tank with 4 tracks(strange but rotation messing everything cuz characters are higher than wider)
        for i in range(0,15):
                object = gameEssentials.WorldObject()
                object.colorPair = 0
                object.position = [-3,7-i]
                object.addModifier(gameModifiers.TracksModifier(["x"," "]  if i % 2 == 0 else [" ","x"],trailHolder))
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.colorPair = 0
                object.position = [3,7-i]
                object.addModifier(gameModifiers.TracksModifier(["x"," "] if i % 2 == 0 else [" ","x"],trailHolder))
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.pattern = "*"
                object.colorPair = 0
                object.position = [-2,7-i]
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.pattern = "*"
                object.colorPair = 0
                object.position = [2,7-i]
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.pattern = "*"
                object.colorPair = 0
                object.position = [-1,7-i]
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.pattern = "*"
                object.colorPair = 0
                object.position = [1,7-i]
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.pattern = "*"
                object.colorPair = 0
                object.position = [0,7-i]
                player.addObject(object)

        for i in range(5):
                object = gameEssentials.WorldObject()
                object.colorPair = 0
                object.position = [2-i,-8]
                object.addModifier(gameModifiers.TracksModifier(["x"," "] if i % 2 == 0 else [" ","x"],trailHolder,gameModifiers.TYPE_VERTICAL))
                player.addObject(object)

                object = gameEssentials.WorldObject()
                object.colorPair = 0
                object.position = [2-i,8]
                object.addModifier(gameModifiers.TracksModifier(["x"," "] if i % 2 == 0 else [" ","x"],trailHolder,gameModifiers.TYPE_VERTICAL))
                player.addObject(object)
	#tank defined
        while True:#Game Loop
                world.updateWorld()
                time.sleep(.1)#hardcoded 100ms sleep time (we dont need precision in ASCII game)giving 10FPS
                #clearing key buffer after sleeping
                key = stdscr.getch()
                lastKey = -1
                while key != -1:
                        key = stdscr.getch()
                        if key != -1:
                                lastKey = key

                curses.ungetch(lastKey)#pass last key to catch it in next pass

if __name__ == "__main__":
        curses.wrapper(main)#helps debugging and auto initialize curses
