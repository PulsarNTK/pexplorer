import pygame
import os
import time
import win32ui
import win32gui
import win32con
import win32api
from icon_save import get_icon_save
from scrollbar import scrollbar

class exp():
    def __init__(self, w, h):
        pygame.init()
        pygame.display.set_caption('PulExp')
        self.flags_d = pygame.RESIZABLE
        self.display = pygame.display.set_mode((w, h), self.flags_d)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Monofur', 16)
        self.err_font = pygame.font.SysFont('Consolas', 48)
        self.nav_img = []
        self.nav_img.append(pygame.image.load("backward.png"))
        self.nav_img.append(pygame.image.load("forward.png"))
        self.nav_img.append(pygame.image.load("up.png"))
        self.scroll_mouse = False
        self.is_run = True
        
        self.nav_x = 0
        self.nav_y = 0
        self.nav_w = w
        self.nav_h = 64
        self.exp_x = 0
        self.exp_y = 64
        self.exp_w = w
        self.exp_h = h-64
        self.exp_len = self.exp_h / 24
        self.exp_b_history = []
        self.exp_f_history = []
        
        self.evt_QUIT = []
        self.evt_MOUSEBUTTONDOWN = []
        self.evt_MOUSEMOTION = []
        self.evt_VIDEORESIZE = []
        
        self.icons = {}
        for i in os.listdir("ico"):
            f, ext = os.path.splitext(i)
            if f != "" and ext != "" and f != "." and ext != ".":
                self.icons["." + f] = pygame.image.load("ico/" + i)
        self.icons["folder"] = pygame.image.load("folder" + ".bmp")
        self.m_llf = time.time()
        self.path = "C:/"
        self.list_cons("C:/")
        self.draw()
        self.default_evts()
        self.loop()
        
    def loop(self):
        while self.is_run:
            self.clock.tick(60)
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    for func in self.evt_QUIT:
                        func(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for func in self.evt_MOUSEBUTTONDOWN:
                        func(event)
                if event.type == pygame.MOUSEMOTION:
                    for func in self.evt_MOUSEMOTION:
                        func(event)
                if event.type == pygame.VIDEORESIZE:
                    for func in self.evt_VIDEORESIZE:
                        func(event)
    
    def list_cons(self, path, navcontrol=False):
        oldpath = self.path
        if self.lisdir(path):
            self.exp_b_history.append(oldpath)
            if not navcontrol:
                if self.exp_f_history != []:
                    self.exp_f_history = []
            if len(self.lsdir) > self.exp_len:
                self.scrol = scrollbar(self.exp_x, self.exp_y, self.exp_w, self.exp_h, 24*(len(self.lsdir)+1))
            for i in self.lsdir:
                f, ext = os.path.splitext(i)
                if f != "" and ext != "" and f != "." and ext != ".":
                    if not os.path.isdir(i):
                        if ext not in self.icons and not os.path.isdir(self.path + i):
                            self.icons[ext] = pygame.image.load(get_icon_save(self.path + i))
            self.draw()
    
    def draw(self):
        self.display.fill((32,32,32))
        self.nav()
        for idx, i in enumerate(self.lsdir[self.scrl:int(self.exp_len+self.scrl)+1]):
            f ,ext =os.path.splitext(i)
            if f != "" and ext != "" and f != "." and ext != "." and not os.path.isdir(self.path + i):
                self.display.blit(self.icons[ext],(self.exp_x+12,idx*24+self.exp_y+4))
            else:
                self.display.blit(self.icons["folder"],(self.exp_x+12,idx*24+self.exp_y+4))
            
            date = self.font.render(time.ctime(os.path.getmtime(self.path + i))[8:], False, (128, 128, 128))
            self.display.blit(date,(self.exp_x+320,idx*24+self.exp_y+2))
            
            if len(i)-30 > 0:
                i = i[:27] + "..."
            name = self.font.render(i, False, (128, 128, 128))
            self.display.blit(name,(self.exp_x+48,idx*24+self.exp_y+2))
            pygame.draw.line(self.display, (64,64,64), [self.exp_x, (idx+1)*24+self.exp_y], [self.exp_w, (idx+1)*24+self.exp_y], 1)
            
            if len(self.lsdir) > self.exp_len:
                pygame.draw.line(self.display, (64,64,64), (self.scrol.scroll_out_s_x, self.scrol.scroll_out_s_y), (self.scrol.scroll_out_s_x2, self.scrol.scroll_out_s_y2), 9)
                pygame.draw.line(self.display, (128,128,128), (self.scrol.scroll_in_x, self.scrol.scroll_in_y), (self.scrol.scroll_in_x2, self.scrol.scroll_in_y2), 9)
                pygame.draw.line(self.display, (64,64,64), (self.scrol.scroll_out_e_x, self.scrol.scroll_out_e_y), (self.scrol.scroll_out_e_x2, self.scrol.scroll_out_e_y2), 9)
            
        pygame.display.update()
    
    def nav(self):
        self.display.blit(self.nav_img[0],(self.nav_x+12,self.nav_y+12))
        self.display.blit(self.nav_img[1],(self.nav_x+64,self.nav_y+12))
        self.display.blit(self.nav_img[2],(self.nav_x+100,self.nav_y+8))
        
        pygame.draw.line(self.display, (92,92,92), [self.nav_x, self.nav_h-2], [self.nav_w, self.nav_h-2], 2)
        self.spltpath = self.path.split("/", )
        self.spltpath.pop()
        self.spltpath_coord = []
        self.nav_bar_pathlist = []
        lenght = 0
        for idx, pth in enumerate(self.spltpath):
            nav_bar_path = ""
            for z in self.spltpath[:idx+1]:
                nav_bar_path +=  z + "/"
            self.nav_bar_pathlist.append(nav_bar_path)
            
            lenghtold = lenght
            lenght += len(pth)*8.3
            space = idx*14
            height = 18
            margin_top = 40
            margin_left = 150
            padding_top = 1
            padding_left = 5
            padding_right = 6
            self.display.blit(self.font.render(pth, False, (128, 128, 128)),(self.nav_x+margin_left+lenghtold+space,self.nav_y+margin_top))
            self.spltpath_coord.append(((self.nav_x+margin_left+lenghtold-padding_left+space, self.nav_y+margin_top-padding_top),(self.nav_x+margin_left+lenght+padding_right+space,self.nav_y+margin_top+height)))
            pygame.draw.line(self.display, (92,92,92), (self.nav_x+margin_left+lenghtold-padding_left+space,self.nav_y+margin_top-padding_top), (self.nav_x+margin_left+lenght+padding_right+space,self.nav_y+margin_top-padding_top), 1)
            pygame.draw.line(self.display, (92,92,92), (self.nav_x+margin_left+lenghtold-padding_left+space,self.nav_y+margin_top+height), (self.nav_x+margin_left+lenght+padding_right+space,self.nav_y+margin_top+height), 1)
            pygame.draw.line(self.display, (92,92,92), (self.nav_x+margin_left+lenghtold-padding_left+space,self.nav_y+margin_top-padding_top), (self.nav_x+margin_left+lenghtold-padding_left+space,self.nav_y+margin_top+height), 1)
            pygame.draw.line(self.display, (92,92,92), (self.nav_x+margin_left+lenght+padding_right+space,self.nav_y+margin_top-padding_top), (self.nav_x+margin_left+lenght+padding_right+space,self.nav_y+margin_top+height), 1)
    
    def lisdir(self, path):
        try:
            if os.path.isdir(path):
                self.lsdir = os.listdir(path)
            else:
                os.system('"' + path[:-1] + '"')
                return False
        except PermissionError as err:
            self.err_msg(err.strerror)
            return False
        else:
            self.path = path
            self.scrl = 0
            return True
    
    def nav_backward(self):
        if self.exp_b_history != []:
            self.exp_f_history.append(self.path)
            self.list_cons(self.exp_b_history.pop(), True)
    
    def nav_forward(self):
        if self.exp_f_history != []:
            self.exp_b_history.append(self.path)    
            self.list_cons(self.exp_f_history.pop(), True)
    
    def nav_up(self):
        pth = self.path[:self.path.rfind("/",0,-1)+1]
        if not len(pth) < 3:
            self.list_cons(pth)
    
    def err_msg(self, msg):
        self.display.fill((32,32,32))
        self.nav()
        self.display.blit(self.err_font.render(msg, False, (128, 128, 128)),(self.exp_x+48,self.exp_y+48))
        pygame.display.update()
    
    def tooltip(self, x, y, list_b, list_t,):
        pygame.draw.rect(self.display, (92,92,92), pygame.Rect(x, y, 400, 400))
        
        for idx, t in enumerate(list_b):
            self.display.blit(self.font.render(t, False, (128, 128, 128)),(x+20,y+(idx*24)))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("click")
        print(x,y)
    
    def loop_nav(self,event,*func):
        while self.is_run:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    if self.nav_y < y < self.nav_h + self.nav_y:
                            if x < 54:
                                self.nav_backward()
                            elif x < 100:
                                self.nav_forward()
                            elif x < 140:
                                self.nav_up()
                            else:
                                if self.spltpath_coord[0][0][0] < x < self.spltpath_coord[-1][1][0] and self.spltpath_coord[0][0][1] < y < self.spltpath_coord[-1][1][1]:
                                    for idx, coord in enumerate(self.spltpath_coord):
                                        if coord[0][0] < x < coord[1][0] and coord[0][1] < y < coord[1][1]:
                                            self.list_cons(self.nav_bar_pathlist[idx])
                    if event.button == 3:
                        x,y = event.pos
                        if self.spltpath_coord[0][0][0] < x < self.spltpath_coord[-1][1][0] and self.spltpath_coord[0][0][1] < y < self.spltpath_coord[-1][1][1]:
                                for idx, coord in enumerate(self.spltpath_coord):
                                    if coord[0][0] < x < coord[1][0] and coord[0][1] < y < coord[1][1]:
                                        self.list_cons(self.nav_bar_pathlist[idx])
                    else:
                        if event.button == 4:
                            if self.scrl > 0:
                                self.scrl -= 2
                                self.scrol.set_pos(self.scrl*24)
                                self.draw()
                        elif event.button == 5:
                            if self.scrl < (len(self.lsdir)-self.exp_len):
                                self.scrl += 2
                                self.scrol.set_pos(self.scrl*24)
                                self.draw()
                        
                        
                elif event.type == pygame.MOUSEMOTION and self.scroll_mouse:
                    if pygame.mouse.get_pressed()[0] == 1:
                        x,y = event.rel
                        if (self.scrol.rated_pos + (y*self.scrol.rate) + self.scrol.scroll_height) <= self.scrol.h  and (self.scrol.pos + (y*self.scrol.rate)) >= 0:
                            self.scrol.set_pos(self.scrol.pos + (y*self.scrol.rate))
                            self.scrl = int(self.scrol.pos / 24)
                        self.draw()
                    else:
                        self.scroll_mouse = False
                        
                        
                elif event.type == pygame.VIDEORESIZE:
                    self.display = pygame.display.set_mode((event.w, event.h), self.flags_d)
                    w = event.w
                    h = event.h
                    self.nav_x = 0
                    self.nav_y = 0
                    self.nav_w = w
                    self.nav_h = 64
                    self.exp_x = 0
                    self.exp_y = 64
                    self.exp_w = w
                    self.exp_h = h-64
                    self.exp_len = self.exp_h / 24
                    self.list_cons(self.path)
                    self.draw()
    
    def default_evts(self):
        self.evt_QUIT = [self.evt_quit]
        self.evt_MOUSEBUTTONDOWN = [self.evt_select_exp]
        self.evt_MOUSEMOTION = [self.evt_scroll_exp]
        self.evt_VIDEORESIZE = [self.evt_resize]
    
    # <----/ event /---->
    
    def evt_select_exp(self, event):
        if event.button == 1:
            x,y = event.pos
            if y > self.exp_y:
                if x > self.exp_w - 30:
                    self.scroll_mouse = True
                else:
                    if (self.m_llf+0.8) > time.time():
                        self.m_llf = 0
                        selelected = self.path + self.lsdir[((y-self.exp_y)//24)+self.scrl] + "/"
                        self.list_cons(selelected)
                    else:
                        self.m_llf = time.time()
            elif self.nav_y < y < self.nav_h + self.nav_y:
                if x < 54:
                    self.nav_backward()
                elif x < 100:
                    self.nav_forward()
                elif x < 140:
                    self.nav_up()
                else:
                    if self.spltpath_coord[0][0][0] < x < self.spltpath_coord[-1][1][0] and self.spltpath_coord[0][0][1] < y < self.spltpath_coord[-1][1][1]:
                        for idx, coord in enumerate(self.spltpath_coord):
                            if coord[0][0] < x < coord[1][0] and coord[0][1] < y < coord[1][1]:
                                self.list_cons(self.nav_bar_pathlist[idx])
        elif event.button == 2:
            x,y = event.pos
            self.tooltip(x,y,("bottom 1", "bottom 2"), ("top 1", "top 2"))
        if event.button == 3:
            x,y = event.pos
            if self.spltpath_coord[0][0][0] < x < self.spltpath_coord[-1][1][0] and self.spltpath_coord[0][0][1] < y < self.spltpath_coord[-1][1][1]:
                    for idx, coord in enumerate(self.spltpath_coord):
                        if coord[0][0] < x < coord[1][0] and coord[0][1] < y < coord[1][1]:
                            self.list_cons(self.nav_bar_pathlist[idx])
        else:
            if event.button == 4:
                if self.scrl > 0:
                    self.scrl -= 2
                    self.scrol.set_pos(self.scrl*24)
                    self.draw()
            elif event.button == 5:
                if self.scrl < (len(self.lsdir)-self.exp_len):
                    self.scrl += 2
                    self.scrol.set_pos(self.scrl*24)
                    self.draw()
    
    def evt_resize(self, event):
        self.display = pygame.display.set_mode((event.w, event.h), self.flags_d)
        w = event.w
        h = event.h
        self.nav_x = 0
        self.nav_y = 0
        self.nav_w = w
        self.nav_h = 64
        self.exp_x = 0
        self.exp_y = 64
        self.exp_w = w
        self.exp_h = h-64
        self.exp_len = self.exp_h / 24
        self.list_cons(self.path)
        self.draw()
    
    def evt_scroll_exp(self, event):
        if self.scroll_mouse:
            if pygame.mouse.get_pressed()[0] == 1:
                x,y = event.rel
                if (self.scrol.rated_pos + (y*self.scrol.rate) + self.scrol.scroll_height) <= self.scrol.h  and (self.scrol.pos + (y*self.scrol.rate)) >= 0:
                    self.scrol.set_pos(self.scrol.pos + (y*self.scrol.rate))
                    self.scrl = int(self.scrol.pos / 24)
                self.draw()
            else:
                self.scroll_mouse = False
    
    def evt_quit(self, event):
        self.is_run = False

test = exp(1024, 720)
quit()
