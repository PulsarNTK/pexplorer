import pyglet, os


class explorer():
    def __init__(self, width, height):
        print("init")
        self.window = pyglet.window.Window(width = width, height = height, resizable=True, style = pyglet.window.Window.WINDOW_STYLE_TOOL )
        self.width=width
        self.height=height
        
        self.path = "D:/Music/Youtube eski/"
        self.lsdir = os.listdir(self.path)
        self.scrl = 0
        
        
        @self.window.event
        def on_draw():
            self.window.clear()
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2i', (0, 0,
                    self.width, 0,
                    self.width, 64,
                    0, 64)),
            ('c3B', (64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64, 64))
            )
            
            pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
            ('v2i', (0, 64,
                    self.width, 64,
                    self.width, self.height,
                    0, self.height)),
            ('c3B', (16, 40, 16, 40, 16, 16, 16, 16, 48, 16, 16, 48))
            )
            
            
            pyglet.text.Label("__Name__",
                            font_name='monofur',
                            font_size=11,
                            x=240, y=self.height - (12),
                            anchor_x='center', anchor_y='center').draw()
            
            self.exp_len = (self.height-64)//24-1+self.scrl
            for idx, i in enumerate(self.lsdir[self.scrl:self.exp_len]):
                pyglet.text.Label(str(i),
                                font_name='monofur',
                                font_size=11,
                                x=240, y=self.height - (idx*24+24+12),
                                anchor_x='center', anchor_y='center').draw()
                pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                ('v2i', (0, (self.height - ((idx+1)*24)),
                        self.width, (self.height - ((idx+1)*24)))),
                ('c3B', (255, 255, 255, 255, 255, 255))
                )



        @self.window.event
        def on_key_press(e, r):
            print("k")
        
        @self.window.event
        def on_resize(width, height):
            self.width = width
            self.height = height
        
        @self.window.event
        def on_mouse_scroll(x, y, sx, sy):
            self.scrl -= int(sy)
    

exp = explorer(1024,720)

pyglet.app.run()