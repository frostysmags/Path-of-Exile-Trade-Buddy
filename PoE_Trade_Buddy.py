from dig import *
import time, keyboard

class DisplayPanel:
    def __init__(self, engine:Engine, title:str, coords:tuple[int, int], bounds_color=Color.white, text_color=Color.white, bounds_size=(200, 50)):
        self.engine = engine
        self.bounds_size = bounds_size
        self.title = Text(text=title, outline=True, coords=(coords[0] + self.bounds_size[0]/2, self.bounds_size[1]/2), center=True, color=text_color, scale=.8)
        self.coords = coords
        self.border_color = Color.auto
        self.bounds_color = bounds_color
        self.__bounds = (self.coords[0], self.coords[1], self.coords[0]+self.bounds_size[0], self.coords[1]+self.engine.get_display()[1])
    
    def Implement(self):
        self.title.coords = (self.coords[0] + self.bounds_size[0]/2, self.bounds_size[1]/2)
        mouse_pos = Engine.GetMouse()
        if mouse_pos[0] >= self.__bounds[0]+1 and mouse_pos[0] <= self.__bounds[2]-1 and mouse_pos[1] >= self.__bounds[1]+1 and mouse_pos[1] <= self.__bounds[3]-1:
            if self.engine.clicks["scroll_up"]:
                # self.x.coords = (self.x.coords[0], self.x.coords[1] + 20)
                pass
            if self.engine.clicks["scroll_down"]:
                # self.x.coords = (self.x.coords[0], self.x.coords[1] - 20)
                pass
        self.engine.MakeRect((self.coords[0], 0), size=self.bounds_size, color=self.border_color)
        self.engine.MakeRect((self.coords[0], self.engine.get_display()[1] - self.bounds_size[1]), size=self.bounds_size, color=self.border_color)
        self.engine.MakeRect((self.coords[0], self.coords[1]+self.bounds_size[1]), (self.bounds_size[0], self.engine.get_display()[1]-(self.bounds_size[1]*2)), color=self.bounds_color, border=True)
        self.engine.AddText(self.title)
        self.engine.MakeRect(coords=(self.coords[0] + self.bounds_size[0] - 15, self.coords[1] + 20), size=(15, 15), color=Color.white)

def check_move(engine, displays, init_set, init_pos, min_x, max_x):
    height_max = engine.get_display()[1] - displays[0].bounds_size[1]
    if Engine.GetMouse()[1] < height_max and engine.clicks["left_hold"]:
        if not init_set:
            return Engine.GetMouse(), True
        if displays[0].coords[0] <= min_x + 2 and displays[-1].coords[0]+displays[-1].bounds_size[0] >= max_x - 2:
            for display in displays:
                    display.coords = (display.coords[0] + (Engine.GetMouse()[0] - init_pos[0]), display.coords[1])
        else:
            if displays[0].coords[0] > min_x + 2:
                for display in displays:
                    display.coords = (display.coords[0] - 2, display.coords[1])
            if displays[-1].coords[0]+displays[-1].bounds_size[0] < max_x - 2:
                for display in displays:
                    display.coords = (display.coords[0] + 2, display.coords[1])
    if not displays[0].coords[0] <= min_x + 2:
        for display in displays:
            display.coords = (display.coords[0] - 2, display.coords[1])
    if not displays[-1].coords[0]+displays[-1].bounds_size[0] >= max_x - 2:
        for display in displays:
            display.coords = (display.coords[0] + 2, display.coords[1])

    

    if engine.clicks["left_release"]:
        return (0, 0), False
    else:
        return (0, 0), False

def main():
    bounds_size = (200, 50)
    engine = Engine(resolution=(800, 400), caption="PoE Trade Buddy", always_front=True)
    displays = [DisplayPanel(engine, item, coords=(10 + (i * (bounds_size[0] + 20)), 0)) for i, item in enumerate(["Currency", "Exotic Currency","Essence", "Blight", "Legion", "Scarabs", "Delirium", "Delve", "Incursion"])]
    #------------------------------------ CHECK IF MOUSE DOWN + MOVE
    init_set = False
    init_pos = (0, 0)
    min_max_x = (10, engine.get_display()[0]-10)
    #------------------------------------
    while True:
        engine.Manage()
        [display.Implement() for display in displays]
        init_pos, init_set = check_move(engine, displays, init_set, init_pos, min_max_x[0], min_max_x[1])
        engine.Update()
        if engine.quit:
            break

if __name__ == "__main__":
    main()