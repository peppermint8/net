class Player():
    
    px = (0,0)
    top_left_px = (0,0)
    bottom_right_px = (1,1)
    screen_px = (0,0)
    
    
    
    color = (0,0,0)

    velocity = 40
    vx = 0 # velocity x
    vy = 0 # velocity y
    xd = 0
    yd = 0
    
    def __init__(self, px, top_left_px, bottom_right_px):
        self.px = px
        self.top_left_px = top_left_px
        self.bottom_right_px = bottom_right_px
        self.screen_px = (self.bottom_right_px[0] // 2, self.bottom_right_px[1] // 2)
    

    
    def __del__(self):
        pass
        #print("deleted player")




    def movement(self, px):
        """calculate speed based on (x,y) of mouse in window"""
        # xd = -1 .. 1
        # yd = -1 .. 1
        self.screen_px = px

        self.xd = 2*px[0] / self.bottom_right_px[0] - 1
        self.yd = 2*px[1] / self.bottom_right_px[1] - 1
        
        self.vx = int(self.velocity * self.xd)
        self.vy = int(self.velocity * self.yd)
        #print("v = {},{} -- d = {},{}".format(self.vx, self.vy, self.xd, self.yd))

    def move(self):
        """update player px"""

        
        x0 = self.px[0]
        y0 = self.px[1]

        x = self.px[0]
        x += self.vx
        x = max(self.top_left_px[0], x)
        x = min(self.bottom_right_px[0], x)

        y = self.px[1]
        y += self.vy
        y = max(self.top_left_px[1], y)
        y = min(self.bottom_right_px[1], y)

        self.px = (x, y)

    def netmove(self, x, y):
        if x > 0 and y > 0:
            self.px = (x,y)
        
