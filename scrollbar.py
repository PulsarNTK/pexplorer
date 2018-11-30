
class scrollbar():
    def __init__(self, x, y, w, h, full_h):
        self.x = x
        self.y = y
        self.w = w-6
        self.h = h
        self.full_h = full_h
        self.rate = full_h / h
        self.scroll_height = h / self.rate
        self.set_pos(0)
    
    def set_pos(self, pos):
        self.pos = pos
        self.rated_pos = self.pos/self.rate
        
        self.scroll_out_s_x = self.w
        self.scroll_out_s_y = self.y
        self.scroll_out_s_x2 = self.w
        self.scroll_out_s_y2 = self.rated_pos + self.y
        
        self.scroll_in_x = self.w
        self.scroll_in_y = self.rated_pos + self.y
        self.scroll_in_x2 = self.w
        self.scroll_in_y2 = self.rated_pos + self.scroll_height + self.y
        
        self.scroll_out_e_x = self.w
        self.scroll_out_e_y = self.rated_pos + self.scroll_height + self.y
        self.scroll_out_e_x2 = self.w
        self.scroll_out_e_y2 = self.h + self.y
    