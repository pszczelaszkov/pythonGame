import gameEssentials
import gameModifiers
import curses
import time

def main(stdscr):

        stdscr.nodelay(True)
        curses.curs_set(0)#hide cursor
        curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_GREEN)

        world = gameEssentials.World()
        world.screen = stdscr
        world.cameraSize = (stdscr.getmaxyx()[0] - 2,stdscr.getmaxyx()[1]-10)

        #creating tank
        player = gameEssentials.WorldObject()
        player.speed = 0
        player.priority = 1
        player.direction = 90
        player.position = [20,70]
        player.addModifier(gameModifiers.KeyboardControl(stdscr))

        trailHolder = gameEssentials.Node()
        trailHolder.priority = 0

        world.addObject(player)
        world.addObject(trailHolder)
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

        while True:
                world.updateWorld()
                time.sleep(.1)
                #clearing key buffer after sleeping
                key = stdscr.getch()
                lastKey = -1
                while key != -1:
                        key = stdscr.getch()
                        if key != -1:
                                lastKey = key

                curses.ungetch(lastKey)

if __name__ == "__main__":
        curses.wrapper(main)
