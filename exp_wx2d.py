import wx, os, time, win32api, win32con, win32ui, win32gui
from win32com.shell import shell, shellcon
from PIL import Image, ImageTk
from wx import glcanvas
from wx import html2

class scrollbar():
    def __init__(self, x, y, w, h, full_h, panel):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.full_h = full_h
        self.rate = full_h / h
        self.scroll_height = h / self.rate
        self.set_pos(0)
        self.dc = wx.WindowDC(panel)
    
    def set_pos(self, pos):
        self.pos = pos
        self.rated_pos = self.pos*self.rate
        
        self.scroll_out_s_x = self.x
        self.scroll_out_s_y = 0
        self.scroll_out_s_h = self.x
        self.scroll_out_s_h2 = self.pos
        
        self.scroll_in_x = self.x
        self.scroll_in_y = self.pos
        self.scroll_in_h = self.x
        self.scroll_in_h2 = self.pos+self.scroll_height
        
        self.scroll_out_e_x = self.x
        self.scroll_out_e_y = self.pos+self.scroll_height
        self.scroll_out_e_h = self.x
        self.scroll_out_e_h2 = self.h
    
    def draw(self):
        self.dc.SetPen(wx.Pen('#222222',self.w/2))
        self.dc.DrawLine(self.scroll_out_s_x,
            self.scroll_out_s_y,
            self.scroll_out_s_h,
            self.scroll_out_s_h2)
        
        self.dc.DrawLine(self.scroll_out_e_x,
            self.scroll_out_e_y,
            self.scroll_out_e_h,
            self.scroll_out_e_h2)
        
        self.dc.SetPen(wx.Pen('#444444',self.w/2))
        self.dc.DrawLine(self.scroll_in_x,
            self.scroll_in_y,
            self.scroll_in_h,
            self.scroll_in_h2)
        
        
        
    

class Example(wx.Frame):

    def __init__(self, parent, witdh, height):
        self.witdh = witdh
        self.height = height
        self.epx_w = self.witdh
        self.exp_h = self.height-64-39
        self.exp_y = 64+39
        self.exp_x = 0
        super(Example, self).__init__(parent, size=(self.witdh, self.height))
        self.font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, 'monofur')
        self.InitUI()

    def InitUI(self):
        self.Centre()
        self.Show(True)
        self.path_hist_b = []
        self.path_hist_f = []
        self.files_path = []
        self.scrl = 0
        self.exp_len = (self.height - 64 - 39) // 24
        self.Bind(wx.EVT_SIZE, self.sizer)
        self.Bind(wx.EVT_KEY_DOWN, self.keyb)
        
        self.pnl_nav = wx.Window(self,pos = (0,0), size = (self.witdh,64))
        self.pnl_nav.Bind(wx.EVT_LEFT_UP, self.nav_l_up)
        self.pnl_nav.SetBackgroundColour(wx.Colour(32,32,32))
        self.pnl_nav.Refresh()
        self.pnl_exp = wx.Window(self,pos = (0,64), size = (self.witdh,self.height-64))
        self.pnl_exp.Bind(wx.EVT_LEFT_DCLICK, self.dclick)
        self.pnl_exp.Bind(wx.EVT_MOUSEWHEEL, self.on_scroll)
        self.pnl_exp.Bind(wx.EVT_LEFT_DOWN, self.exp_l_down)
        self.pnl_exp.SetBackgroundColour(wx.Colour(48,48,48))
        self.adress_bar = wx.TextCtrl(self.pnl_nav, pos=(150,21), size=(800,18))
        
        self.dc = wx.WindowDC(self.pnl_exp)
        self.dc.SetFont(self.font)
        self.dc.SetTextForeground('#ffffff')
        self.dc.SetPen(wx.Pen('#bbbbbb'))
        self.dc.SetBackground(wx.Brush(wx.Colour(48,48,48)))
        self.frwbmp = wx.Bitmap()
        self.bcwbmp = wx.Bitmap()
        self.upbmp = wx.Bitmap()
        self.frwbmp.LoadFile("forward.png")
        self.bcwbmp.LoadFile("backward.png")
        self.upbmp.LoadFile("up.png")
        self.dcn = wx.WindowDC(self.pnl_nav)
        self.dcn.DrawBitmap(self.bcwbmp,8,4)
        self.dcn.DrawBitmap(self.frwbmp,56,4)
        self.dcn.DrawBitmap(self.upbmp,96,4)
        self.dcn.SetPen(wx.Pen('#88888',0))
        self.dcn.DrawLine(0,40,self.witdh,40)
        self.nav_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL, False, 'monofur')
        self.dcn.SetFont(self.nav_font)
        self.dcn.SetTextForeground('#aaaaaa')
        self.dcn.DrawText("Name", 36, 44)
        self.dcn.DrawText("Date", 330, 44)
        
        
        self.path = "C:/" 
        self.listcons()
        
    def listcons(self):
        
        self.dc.Clear()
        self.adress_bar.Clear()
        self.adress_bar.AppendText(self.path)
        try:
            self.lsdir = os.listdir(self.path)
        except PermissionError as error:
            self.adress_bar.Clear()
            self.adress_bar.AppendText(self.path)
            self.err_font = wx.Font(64, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,wx.FONTWEIGHT_NORMAL, False, 'monofur')
            self.dc.SetFont(self.err_font)
            self.dc.DrawText(error.strerror, 24, 0)
            self.dc.SetFont(self.font)
            return
        self.files_path.clear()
        self.exts = {}
        self.icos = {}
        
        
        for idx, i in enumerate(self.lsdir):
            f, fext = os.path.splitext(i)
            self.exts[fext] = self.path + i
            self.files_path.append(self.path + i + "/")
        for r, z in self.exts.items():
            self.icos[r] = wx.Icon()
            ret, ico = shell.SHGetFileInfo(z, 0, 0x000001000 | 0x000000100 | 0x00001 | 0x000000010)
            self.icos[r].CreateFromHICON(shell.SHGetFileInfo(z, 0, 0x000001000 | 0x000000100 | 0x00001 | 0x000000010)[1][0])
        self.icos[""] = wx.Icon()
        self.icos[""].CreateFromHICON(shell.SHGetFileInfo("D:/Source/Python/explorer/fold.ico", 0, 0x000001000 | 0x000000100 | 0x00001 | 0x000000010)[1][0])
        self.scroll = scrollbar(self.epx_w-20, self.exp_y, 20, self.exp_h, len(self.lsdir)*24, self.pnl_exp)
        self.draw_list()
        
    def draw_list(self):
        self.dc.Clear()
        self.dc.SetPen(wx.Pen('#bbbbbb'))
        self.scrl = int(self.scroll.pos/(24/self.scroll.rate))
        print(self.scrl)
        for idx, i in enumerate(self.lsdir[self.scrl:self.scrl + self.exp_len]):
            y = idx*24
            tl = 30 - len(i)
            date = os.path.getmtime(self.path + i)
            if tl > 0:
                text = i + tl*" "
            else:
                text = i[:27] + "..."
            self.dc.DrawText(text + " " + time.ctime(os.path.getmtime(self.path + i))[8:], 36, y+5)
            self.dc.DrawLine(0,y,self.witdh,y)
            f, fext = os.path.splitext(i)
            self.dc.DrawIcon(self.icos[fext],10,y+3)
        self.scroll.draw()
    
    
    def keyb(self, e):
        print(e.GetKeyCode())
    
    def dclick(self, e):
        x, y = e.GetPosition()
        selected_file = (y // 24) + self.scrl
        if os.path.isdir(self.files_path[selected_file]):
            self.path_hist_b.append(self.path)
            self.scrl = 0
            self.path = self.files_path[selected_file]
            self.listcons()
        else:
            os.system('"' + self.files_path[selected_file][:-1] + '"')
        
    def on_scroll(self, e):
        sc = e.GetWheelRotation()
        if sc > 0:
            if self.scrl <= len(self.lsdir) - self.exp_len and self.scrl >= 0:
                if self.scrl != 0:
                    self.scroll.set_pos(self.scroll.pos - 24//self.scroll.rate)
                    
                self.draw_list()
        else:
            if self.scrl <= len(self.lsdir) - self.exp_len and self.scrl >= 0:
                if self.scrl != len(self.lsdir) - self.exp_len:
                    self.scroll.set_pos(self.scroll.pos + 24//self.scroll.rate)
                self.draw_list()
        print(self.scrl)
    
    def nav_l_up(self, e):
        x, y = e.GetPosition()
        if 48 > x > 0:
            if self.path_hist_b != []:
                self.path_hist_f.append(self.path)
                self.path = self.path_hist_b.pop()
                self.listcons()
        elif 96 > x > 48:
            if self.path_hist_f != []:
                self.path_hist_b.append(self.path)
                self.path = self.path_hist_f.pop()
                self.listcons()
        elif 144 > x > 96:
            self.path = self.path[:self.path.rfind("/",0,-1)+1]
            self.listcons()
    
    def sizer(self, e):
        witdh, height = e.GetSize()
        lenght = (height - 64 - 39) // 24
        if self.exp_len < lenght:
            if self.scrl + lenght >= len(self.lsdir) and self.scrl != 0:
                self.scrl -= lenght - self.exp_len
                if self.scrl < 0:
                    self.scrl = 0
        self.witdh = witdh
        self.height = height
        self.exp_len = lenght
        self.epx_w = self.witdh
        self.exp_h = self.height-64-39
        self.exp_y = 64+39
        self.exp_x = 0
        self.pnl_exp.SetSize(wx.DefaultCoord, wx.DefaultCoord, witdh, height - 64 - 39)
        self.pnl_nav.SetSize(wx.DefaultCoord, wx.DefaultCoord, witdh, wx.DefaultCoord)
        self.scroll = scrollbar(self.epx_w-20, self.exp_y, 20, self.exp_h, len(self.lsdir)*24, self.pnl_exp)
        self.draw_list()
    
    def exp_l_down(self, e):
        x, y = e.GetPosition()
        if x >= (self.witdh - 36):
            self.scrl_y = y
            if self.scroll.scroll_in_y < y < self.scroll.scroll_in_h2:
                 self.scrl_y -= self.scroll.pos
            self.pnl_exp.Bind(wx.EVT_MOTION, self.scroll_move)
    
    def scroll_move(self, e):
        x, y = e.GetPosition()
        if e.Dragging() and e.LeftIsDown():
            self.scroll.set_pos(y - self.scrl_y)
            test_scrl =  int(self.scroll.rated_pos/24)
            if (self.scroll.pos + self.scroll.scroll_height) < self.scroll.h  and self.scroll.pos > 0:
                self.draw_list()
        else:
            self.pnl_exp.Bind(wx.EVT_MOTION, None)
    
    
    
    
    
    '''
        def OnLeftDown(self, e):
            pass
            # x, y = self.ClientToScreen(e.GetPosition())
            # ox, oy = self.GetPosition()
            # dx = x - ox
            # dy = y - oy
            # self.delta = ((dx, dy))

        def OnMouseMove(self, e):

            if e.Dragging() and e.LeftIsDown():

                self.SetCursor(wx.Cursor(wx.CURSOR_HAND))

                x, y = self.ClientToScreen(e.GetPosition())
                fp = (x - self.delta[0], y - self.delta[1])
                self.Move(fp)

        def OnLeftUp(self, e):

            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        def OnRightDown(self, e):

            self.Close()
    '''


def main():
    app = wx.App()
    ex = Example(None,1024,720)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()