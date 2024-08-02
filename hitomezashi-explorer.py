#!/usr/bin/env python
import wx,random,itertools

#import PIL,drawsvg

GRID_BORDER=10

def str_complement(x):
    new=""
    for i in range(len(x)):
        if x[i]=='0':
            new += '1'
        else:
            new += '0'
    return new

def str_reverse(x):
    return x[::-1]

def pellword(n):
    olderWord=""
    oldWord="0"
    while(n>1):
        word=str_complement(oldWord) + str_reverse(str_complement(olderWord)) + oldWord
        olderWord=oldWord
        oldWord=word
        n=n-1
    return (oldWord + str_reverse(oldWord))

def randomword(n):
    string=""
    for i in range(n):
        string += random.choice(['0','1'])
    return string

def thuemorse(n):
    oldWord="0"
    while(n>0):
        word=oldWord + str_complement(oldWord)
        oldWord=word
        n=n-1
    return word

import itertools,sys

def cycler(start_items):
	return itertools.cycle(start_items).__next__


def kolakoski(start_items=(1, 2), length=20):
    def _kolakoski_gen(start_items):
        s, k = [], 0
        c = cycler(start_items)
        while True:
            c_next = c()
            s.append(c_next)
            sk = s[k]
            yield sk
            if sk > 1:
                s += [c_next] * (sk - 1)
            k += 1

    def _run_len_encoding(truncated_series):
        return [len(list(group)) for grouper, group in itertools.groupby(truncated_series)][:-1]

    def is_series_eq_its_rle(series):
        rle = _run_len_encoding(series)
        return (series[:len(rle)] == rle) if rle else not series

    return list(itertools.islice(_kolakoski_gen(start_items), length))

class HitomezashiDrawing:
    def __init__(self):
        pass
    def set_gridcolor(self,color):
        pass
    def set_gridweight(self,weight):
        pass
    def set_stitchcolor(self,color):
        pass
    def set_stitchweight(self,weight):
        pass
    def set_fillcolor(self,number,color):
        pass
    def draw_grid(self):
        pass
    def draw_polyline(self,points):
        pass
    def draw_loop(self,points):
        pass
    def fill_square(self,color,x,y):
        pass
    def fill_polygon(self,color,points):
        pass
    def draw_all(self,
                 grid_pen=None,
                 stitch_pen=None,
                 colors=None,
                 polylines=[],
                 cycles=[],
                 fills=[]):
        if grid_pen is not None:
            self.set_gridcolor(grid_pen.GetColour())
            self.set_gridweight(grid_pen.GetWidth())
        self.set_stitchcolor(stitch_pen.GetColour())
        self.set_stitchweight(stitch_pen.GetWidth())
        if(colors is not None):
            for i in range(len(colors)):
                self.set_fillcolor(i,colors[i].GetColour())

        if(colors is not None):
            for x in range(len(fills)):
                for y in range(len(fills[x])):
                    self.fill_square(fills[x][y],x,y)
            
        if grid_pen is not None:
            self.draw_grid()
        for points in polylines:
            self.draw_polyline(points)
        for points in cycles:
            self.draw_loop(points)

class TikzDrawing(HitomezashiDrawing):
    def __init__(self,filehandle,xsize,ysize):
        self.filehandle=filehandle
        self.xsize=xsize
        self.ysize=ysize
        self.gridweight=None
        self.stitchweight=None

    def set_gridcolor(self,color):
        self.filehandle.write('\\definecolor{{HZgridlines}}{{RGB}}{{{},{},{}}}\n'.format(color.GetRed(),color.GetBlue(),color.GetGreen()))
        
    def set_gridweight(self,weight):
        self.gridweight=weight
        
    def set_stitchcolor(self,color):
        self.filehandle.write('\\definecolor{{HZstitches}}{{RGB}}{{{},{},{}}}\n'.format(color.GetRed(),color.GetBlue(),color.GetGreen()))

    def set_stitchweight(self,weight):
        self.gridweight=weight
        
    def set_fillcolor(self,number,color):
        self.filehandle.write('\\definecolor{{HZfill{}}}{{RGB}}{{{},{},{}}}\n'.format(number,color.GetRed(),color.GetBlue(),color.GetGreen()))

    def draw_grid(self):
        if(self.gridweight is None):
            self.filehandle.write('\\draw[very thin,HZgridlines] ')
        else:
            self.filehandle.write('\\draw[line width={:0.2f}pt,HZgridlines] '.format(0.2*self.gridweight))
        self.filehandle.write('(-0.5,0.5) grid ({},-{});\n'.format(self.xsize-0.5,self.ysize-0.5))

    def __draw_polyline_basic(self,points):        
        if(self.stitchweight is None):
            self.filehandle.write('\\draw[very thick,HZstitches] ')
        else:
            self.filehandle.write('\\draw[line width={:0.2f}pt,HZstitches] '.format(0.2*self.stitchweight))
        self.filehandle.write("--".join(["({},{})".format(coord[0],-coord[1]) for coord in points]))

    def draw_polyline(self,points):
        self.__draw_polyline_basic(points)
        self.filehandle.write(';\n')
        
    def draw_loop(self,points):
        self.__draw_polyline_basic(points)
        self.filehandle.write('--cycle;\n')

    def fill_square(self,color,x,y):
        self.filehandle.write('\\fill[color=HZfill{}] ({},-{}) rectangle ++(1,-1);\n'.format(color,x,y))
    def fill_polygon(self,color,points):
        self.filehandle.write('\\fill[color=HZfill{}] ')
        self.filehandle.write("--".join(["({},{})".format(coord[0],-coord[1]) for coord in points]))
        self.filehandle.write('--cycle;\n')

class WXDrawing(HitomezashiDrawing):
    def __init__(self,canvas,xsize,ysize):
        self.dc = wx.PaintDC(canvas)
        self.canvassize=self.dc.GetSize()
        self.xsize=xsize
        self.ysize=ysize
        self.gridpen=wx.NullPen
        self.stitchpen=wx.Pen(colour=wx.Colour("BLACK"),width=3)
        self.fillcolors={}

    def resize(self,x,y):
        self.xsize=x
        self.ysize=y
        
    def __scale_x(self,xvalue):
        return int((xvalue+0.5)*(self.canvassize.x)/self.xsize)

    def __scale_y(self,yvalue):
        return int((yvalue+0.5)*(self.canvassize.y)/self.ysize)

    def __xlength(self):
        return int(self.canvassize.x/self.xsize)

    def __ylength(self):
        return int(self.canvassize.y/self.ysize)
    
    def __scale_point(self,point):
        return [self.__scale_x(point[0]),self.__scale_y(point[1])]

    def __scale_line(self,line):
        return [self.__scale_x(line[0]),self.__scale_y(line[1]),
                self.__scale_x(line[2]),self.__scale_y(line[3])]
    
    def set_gridcolor(self,color):
        self.gridpen.SetColour(color)
        
    def set_gridweight(self,weight):
        self.gridpen.SetWidth(weight)
        
    def set_stitchcolor(self,color):
        self.stitchpen.SetColour(color)

    def set_stitchweight(self,weight):
        self.stitchpen.SetWidth(weight)
        
    def set_fillcolor(self,number,color):
        self.fillcolors[number]=color

    def draw_grid(self):
        self.dc.SetBrush(wx.NullBrush)
        self.dc.SetPen(self.gridpen)
        lineList=[self.__scale_line([-0.5,i,self.xsize-0.5,i]) for i in range(self.ysize)] + [self.__scale_line([i,-0.5,i,self.xsize-0.5]) for i in range(self.xsize)]
        self.dc.DrawLineList(lineList)

    def draw_polyline(self,points):
        self.dc.SetBrush(wx.NullBrush)
        self.dc.SetPen(self.stitchpen)
        self.dc.DrawLines([self.__scale_point(point) for point in points])

    def draw_loop(self,points):
        self.dc.SetBrush(wx.Brush(wx.Colour("WHITE"),wx.BRUSHSTYLE_TRANSPARENT))
        self.dc.SetPen(self.stitchpen)
        self.dc.DrawPolygon([self.__scale_point(point) for point in points])


    def fill_square(self,color,x,y):
        self.dc.SetPen(wx.NullPen)
        self.dc.SetBrush(wx.Brush(self.fillcolors[color]))
        self.dc.DrawRectangle(self.__scale_x(x),self.__scale_y(y),self.__xlength(),self.__ylength())

    def fill_polygon(self,color,points):
        self.dc.SetPen(wx.NullPen)
        self.dc.SetBrush(wx.Brush(self.fillcolors[color]))
        self.dc.DrawPolygon([self.__scale_point(point) for point in points])
    
class HitomezashiEngine:
    def __init__(self,xstring="",ystring=""):
        self.set_strings(xstring,ystring)
        self.rebuild_structures()

    def set_strings(self,xstring=None,ystring=None):
        if xstring is not None:
            self.x_bits=[int(i) for i in xstring]
        if ystring is not None:
            self.y_bits=[int(i) for i in ystring]

    def rebuild_structures(self):
        self.polylines=[]
        self.cycles=[]
        self.regions=[]

        # From each point in the grid, propogate until the initial
        # point is reached or an edge is crossed.
        visited=[[False]*(len(self.y_bits)) for i in range(len(self.x_bits))]
        for i in range(len(self.x_bits)):
            for j in range(len(self.y_bits)):
                if visited[i][j]:
                    continue
                current_polyline=[]
                laststep_horiz=True
                curx=i
                cury=j
                while ((curx>=0) and (cury>=0) and
                       (curx<len(self.x_bits)) and (cury<len(self.y_bits))):
                    visited[curx][cury]=True
                    current_polyline.append((curx,cury))
                    if laststep_horiz:
                        cury=cury+(1 if self.x_bits[curx]==cury % 2 else -1)
                    else:
                        curx=curx+(1 if self.y_bits[cury]==curx % 2 else -1)
                    laststep_horiz=not laststep_horiz
                    if (curx==i) and (cury==j):
                        break
                if (curx != i) or (cury != j):
                    curx=i
                    cury=j
                    laststep_horiz=False
                    while ((curx>=0) and (cury>=0) and
                           (curx<len(self.x_bits)) and
                           (cury<len(self.y_bits))):
                        if (curx != i) or (cury != j):
                            visited[curx][cury]=True
                            current_polyline.insert(0,(curx,cury))
                        if laststep_horiz:
                            cury=cury+(1 if self.x_bits[curx]==cury % 2 else -1)
                        else:
                            curx=curx+(1 if self.y_bits[cury]==curx % 2 else -1)
                        laststep_horiz=not laststep_horiz
                    if len(current_polyline)>1:
                        self.polylines.append(current_polyline)
                else:
                    self.cycles.append(current_polyline)
        # To have a sensible order for filling in regions, the cycles
        # should appear from longest to shortest.
        self.cycles.sort(key=len,reverse=True)

        # Produce coloration rules for each individual cell
        self.two_colors=[]
        startcolor=0
        for x in range(len(self.x_bits)-1):
            startcolor = (startcolor+self.x_bits[x]+1) % 2
            current_row=[startcolor]
            current_color=startcolor
            for y in range(1,len(self.y_bits)-1):
                current_color=(current_color + self.y_bits[y]+x-1) % 2
                current_row.append(current_color)
            self.two_colors.append(current_row)

        # Much faster, now that I use cycle raycasting!
        self.enclave_colors=[[0]*(len(self.y_bits)-1) for i in range(len(self.x_bits)-1)]
        for cycle in self.cycles:
            leftpoint=min([x[0] for x in cycle])
            rightpoint=max([x[0] for x in cycle])
            toppoint=min([x[1] for x in cycle])
            bottompoint=max([x[1] for x in cycle])
            for x in range(leftpoint,rightpoint):
                enclosure=0
                for y in range(toppoint,bottompoint):
                    for i in range(len(cycle)):
                        if ((cycle[i]==(x,y) and cycle[i-1]==(x+1,y)) or
                            (cycle[i]==(x+1,y) and cycle[i-1]==(x,y))):
                            enclosure=(enclosure+1) % 2
                    self.enclave_colors[x][y] = self.enclave_colors[x][y]+enclosure

        # Finally, building the map of "regions". Work in progress!
        touchCount={}

        def touchCell(x,y):
            s=str([x,y])
            if s in touchCount:
                touchCount[s]=touchCount[s]+1
            else:
                touchCount[s]=1

        def onBorder(x,y):
            return ((x==0) or (y==0) or
                    (x==len(self.x_bits)-1) or
                    (y==len(self.y_bits)-1))
                
        def nextBorderCell(x,y):
            if (y==0) and (x<len(self.x_bits)-1):
                return [x+1,0]
            if (y<len(self.y_bits)-1) and (x==len(self.x_bits)-1):
                return [x,y+1]
            if (y==len(self.y_bits)-1) and (x>0):
                return [x-1,y]
            if (x==0):
                return [x,y-1]

        for i in range(len(self.x_bits)):
            touchCell(i,0)
            curX=i
            curY=0
            newRegion=[[i,0]]
            
            

class HitomezashiCanvas(wx.Panel):
    def __init__(self,parent,engine):
        wx.Panel.__init__(self,parent)
        self.SetBackgroundColour(wx.WHITE)
        self.engine=engine
        self.size=None

    def scale_x(self,xvalue):
        return int((xvalue+0.5)*(self.size.x)/(len(self.engine.x_bits)))

    def scale_y(self,yvalue):
        return int((yvalue+0.5)*(self.size.y)/(len(self.engine.y_bits)))
        


class BitStringValidator(wx.Validator):
    def __init__(self):
        super().__init__()

    def Clone(self):
        return BitStringValidator()

    def Validate(self,win):
         textCtrl = self.GetWindow()
         text = textCtrl.GetValue()

         if len(text)<2:
             textCtrl.SetBackgroundColour("pink")
             return False
         else:
             for i in text:
                 if (i!="0" and i!="1"):
                     textCtrl.SetBackgroundColour("pink")
                     return False
             textCtrl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
             return True

    def TransferToWindow(self):
         return True

    def TransferFromWindow(self):
         return True
   

class PresetDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title = "Presets")
        mainlayout = wx.BoxSizer(wx.VERTICAL)
        preset_row = wx.BoxSizer(wx.HORIZONTAL)
        self.preset_combos = [None,None]
        self.preset_spinners = [None,None]
        for i in range(2):
            self.preset_combos[i]=wx.ComboBox(self,value="Don't change", choices=["Don't change","Fibonacci-Pell snowflake","Thue-Morse sequence","Kolakoski sequence","Random"],style=wx.CB_DROPDOWN|wx.CB_READONLY)
            preset_row.Add(self.preset_combos[i],proportion=2)
            self.preset_spinners[i]=wx.SpinCtrl(self,value="0")
            preset_row.Add(self.preset_spinners[i],proportion=1)
        mainlayout.Add(preset_row)
        mainlayout.Add(self.CreateButtonSizer(flags = wx.OK | wx.CANCEL),0,wx.ALL|wx.EXPAND)
        self.SetSizer(mainlayout)
        self.Fit()

class ExplorerFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Hitomezashi Explorer",size=wx.Size(600,600))
        self.enclave_colors=None
        self.two_colors=None
  
        self.main_layout = wx.BoxSizer(wx.VERTICAL)

        bitstring_entries = wx.BoxSizer(wx.HORIZONTAL)

        x_bitstring_entries = wx.BoxSizer(wx.VERTICAL)
        y_bitstring_entries = wx.BoxSizer(wx.VERTICAL)
        x_bitstring_entries.Add(
            wx.StaticText(self,label="Vertical-stitch bitcode: "),
            flag=wx.RIGHT,
            border=8)
        self.x_bitcode_field = wx.TextCtrl(self,validator=BitStringValidator(),value=randomword(5))
        self.x_bitcode_field.Bind(wx.EVT_TEXT, self.evt_changed_bitstrings)
        y_bitstring_entries.Add(
            wx.StaticText(self,label="Horizontal-stitch bitcode: "),
            flag=wx.RIGHT,
            border=8)
        self.y_bitcode_field = wx.TextCtrl(self,validator=BitStringValidator(),value=randomword(5))
        
        x_bitstring_entries.Add(self.x_bitcode_field,flag=wx.RIGHT | wx.EXPAND, border=10)
        self.y_bitcode_field.Bind(wx.EVT_TEXT, self.evt_changed_bitstrings)
        y_bitstring_entries.Add(self.y_bitcode_field,flag=wx.RIGHT | wx.EXPAND, border=10, proportion=1)

        self.engine=HitomezashiEngine(self.x_bitcode_field.GetValue(),self.y_bitcode_field.GetValue())
        x_bitstring_buttons = wx.BoxSizer(wx.HORIZONTAL)
        x_bitstring_dualize = wx.Button(self,label="Dualize")
        x_bitstring_reverse = wx.Button(self,label="Reverse")
        y_bitstring_buttons = wx.BoxSizer(wx.HORIZONTAL)
        y_bitstring_dualize = wx.Button(self,label="Dualize")
        y_bitstring_reverse = wx.Button(self,label="Reverse")
        x_bitstring_dualize.Bind(wx.EVT_BUTTON,self.evt_dualize_x)
        x_bitstring_reverse.Bind(wx.EVT_BUTTON,self.evt_reverse_x)
        y_bitstring_dualize.Bind(wx.EVT_BUTTON,self.evt_dualize_y)
        y_bitstring_reverse.Bind(wx.EVT_BUTTON,self.evt_reverse_y)
        x_bitstring_buttons.Add(x_bitstring_dualize,flag=wx.ALL|wx.EXPAND)
        x_bitstring_buttons.Add(x_bitstring_reverse,flag=wx.ALL|wx.EXPAND)
        y_bitstring_buttons.Add(y_bitstring_dualize,flag=wx.ALL|wx.EXPAND)
        y_bitstring_buttons.Add(y_bitstring_reverse,flag=wx.ALL|wx.EXPAND)
        x_bitstring_entries.Add(x_bitstring_buttons)
        y_bitstring_entries.Add(y_bitstring_buttons)
        bitstring_entries.Add(x_bitstring_entries,proportion=1,flag=wx.ALL|wx.EXPAND)
  
        bitstring_entries.Add(y_bitstring_entries,proportion=1,flag=wx.ALL|wx.EXPAND)

        bitcode_presets_button=wx.Button(self,label="Presets...")
        bitcode_presets_button.Bind(wx.EVT_BUTTON,self.evt_select_presets)
        self.main_layout.Add(bitstring_entries,
                            flag=wx.ALL|wx.EXPAND)
        self.main_layout.Add(bitcode_presets_button,flag=wx.EXPAND)

        self.grid_display=HitomezashiCanvas(self,self.engine)
        self.grid_display.Bind(wx.EVT_PAINT,self.evt_repaint_grid)
        self.grid_sizer=self.main_layout.Add(self.grid_display,5,wx.SHAPED|wx.ALL,border=10)

        stitchcolorline=wx.BoxSizer(wx.HORIZONTAL)
        stitchcolorline.Add(
            wx.StaticText(self,label="Stitch style: "),
            flag=wx.RIGHT,
            border=8)
        self.stitchcolor=wx.ColourPickerCtrl(self)
        self.stitchcolor.Bind(wx.EVT_COLOURPICKER_CHANGED,self.evt_refresh)
        stitchcolorline.Add(self.stitchcolor)
        self.stitchweight=wx.SpinCtrl(self,value="3m",min=1)
        self.stitchweight.Bind(wx.EVT_SPINCTRL,self.evt_refresh)
        stitchcolorline.Add(self.stitchweight)
        self.main_layout.Add(stitchcolorline)
  
        gridrow=wx.BoxSizer(wx.HORIZONTAL)
        self.cb_grid_display = wx.CheckBox(self,label="Display grid lines")
        self.cb_grid_display.SetValue(True)
        self.cb_grid_display.Bind(wx.EVT_CHECKBOX,self.evt_refresh)
        self.cb_grid_display.Bind(wx.EVT_CHECKBOX,self.evt_gridcontrols)
        gridrow.Add(self.cb_grid_display,flag=wx.RIGHT|wx.TOP|wx.BOTTOM,border=8)
        self.grid_color = wx.ColourPickerCtrl(self,colour=wx.Colour("LIGHT GREY"))
        self.grid_color.Bind(wx.EVT_COLOURPICKER_CHANGED,self.evt_refresh)
        gridrow.Add(self.grid_color)
        self.main_layout.Add(gridrow)

        bg_color_sizer = wx.BoxSizer(wx.HORIZONTAL)
  
        self.list_bgstyle = wx.ComboBox(self,value="None", choices=["None","Two colors","Enclave coloring"],style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.list_bgstyle.Bind(wx.EVT_COMBOBOX,self.evt_changed_colormode)
        bg_color_sizer.Add(
            wx.StaticText(self,label="Fill-color style: "),
            flag=wx.RIGHT|wx.TOP|wx.BOTTOM,
            border=8)
        bg_color_sizer.Add(self.list_bgstyle)

        self.bg_twocolor=[
            wx.ColourPickerCtrl(self,colour=wx.Colour("WHITE")),
            wx.ColourPickerCtrl(self,colour=wx.Colour("RED"))]
        for i in [0,1]:
            bg_color_sizer.Add(self.bg_twocolor[i])
            self.bg_twocolor[i].Bind(wx.EVT_COLOURPICKER_CHANGED,self.evt_refresh)
            self.bg_twocolor[i].Hide()
        self.bg_enclavecolor=[
            wx.ColourPickerCtrl(self,colour=wx.Colour("WHITE"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("PINK"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("RED"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("ORANGE"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("YELLOW"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("GREEN"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("CYAN"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("BLUE"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("PURPLE"),size=(34,34)),
            wx.ColourPickerCtrl(self,colour=wx.Colour("BLACK"),size=(34,34)),
        ]
        for i in range(10):
            bg_color_sizer.Add(self.bg_enclavecolor[i])
            self.bg_enclavecolor[i].Bind(wx.EVT_COLOURPICKER_CHANGED,self.evt_refresh)
            self.bg_enclavecolor[i].Hide()


        self.main_layout.Add(bg_color_sizer)
        
        export_button = wx.Button(self,label="Export...")
        export_button.Bind(wx.EVT_BUTTON,self.evt_export)
        self.main_layout.Add(export_button)
  
        self.SetSizer(self.main_layout)
        self.Show()
        self.grid_display.Refresh()

    def evt_dualize_x(self,event):
        if self.x_bitcode_field.Validate():
            self.x_bitcode_field.SetValue(str_complement(self.x_bitcode_field.GetValue()))

    def evt_reverse_x(self,event):
        if self.x_bitcode_field.Validate():
            self.x_bitcode_field.SetValue(str_reverse(self.x_bitcode_field.GetValue()))

    def evt_dualize_y(self,event):
        if self.y_bitcode_field.Validate():
            self.y_bitcode_field.SetValue(str_complement(self.y_bitcode_field.GetValue()))
     
    def evt_reverse_y(self,event):
        if self.y_bitcode_field.Validate():
            self.y_bitcode_field.SetValue(str_reverse(self.y_bitcode_field.GetValue()))

    def evt_export(self,event):
        try:
            import PIL
        except ImportError:
            PIL = None
        try:
            import drawsvg
        except ImportError:
            drawsvg = None
        wildcards=["TikZ code (*.tex)|*.tex"]
        if drawsvg is None:
            print("Install drawsvg module for export to SVG")
        else:
            wildcards.insert(0,"SVG files (*.svg)|*.svg")
        if PIL is None:
            print("Install PIL module for export to graphics files")
        else:
            wildcards.insert(0,"Image files|*.bmp;*.gif;*.jpg;*.png")
        with wx.FileDialog(self, "Export to file...",
                           wildcard="|".join(wildcards),
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal()==wx.ID_CANCEL:
                return
            if(wildcards[fileDialog.GetFilterIndex()]=="TikZ code (*.tex)|*.tex"):
                # TikZ source
                with open(fileDialog.GetPath(),"w") as f:
                    tikzBuilder=TikzDrawing(f,len(self.engine.x_bits),len(self.engine.y_bits))
                    grid_pen=wx.Pen(self.grid_color.GetColour()) if self.cb_grid_display.GetValue() else None;
                    if(self.list_bgstyle.GetSelection()==1):
                        colors=self.bg_twocolor
                        fills=self.engine.two_colors
                    elif(self.list_bgstyle.GetSelection()==2):
                        colors=self.bg_enclavecolor
                        fills=self.engine.enclave_colors
                    else:
                        colors=None
                        fills=[]
                    tikzBuilder.draw_all(
                        grid_pen=grid_pen,
                        stitch_pen=wx.Pen(self.stitchcolor.GetColour(),width=self.stitchweight.GetValue()),
                        colors=colors,
                        polylines=self.engine.polylines,
                        cycles=self.engine.cycles,
                        fills=fills);
            elif(wildcards[fileDialog.GetFilterIndex()]=="Image files|*.bmp;*.gif;*.jpg;*.png"):
                pass
        
    def evt_gridcontrols(self,event):
        if(self.cb_grid_display.GetValue()):
            self.grid_color.Show()
            self.Layout()
        else:
            self.grid_color.Hide()
  
    def evt_select_presets(self,event):
        dialog=PresetDialog(self)
        if(dialog.ShowModal()==wx.ID_OK):
            xchoice=dialog.preset_combos[0].GetValue()
            ychoice=dialog.preset_combos[1].GetValue()
            if xchoice=="Fibonacci-Pell snowflake":
                self.x_bitcode_field.SetValue(pellword(dialog.preset_spinners[0].GetValue()))
            elif xchoice=="Thue-Morse sequence":
                self.x_bitcode_field.SetValue(thuemorse(dialog.preset_spinners[0].GetValue()))
            elif xchoice=="Kolakoski sequence":
                kolakoski_string=""
                for i in kolakoski(length=dialog.preset_spinners[0].GetValue()):
                    kolakoski_string += str(i-1)
                self.x_bitcode_field.SetValue(kolakoski_string)
            elif xchoice=="Random":
                self.x_bitcode_field.SetValue(randomword(dialog.preset_spinners[0].GetValue()))

            if ychoice=="Fibonacci-Pell snowflake":
                self.y_bitcode_field.SetValue(pellword(dialog.preset_spinners[1].GetValue()))
            elif ychoice=="Thue-Morse sequence":
                self.y_bitcode_field.SetValue(thuemorse(dialog.preset_spinners[1].GetValue()))
            elif ychoice=="Kolakoski sequence":
                kolakoski_string=""
                for i in kolakoski(length=dialog.preset_spinners[0].GetValue()):
                    kolakoski_string += str(i-1)
                self.y_bitcode_field.SetValue(kolakoski_string)
            elif ychoice=="Random":
                self.y_bitcode_field.SetValue(randomword(dialog.preset_spinners[1].GetValue()))

    def evt_refresh(self,event):
        self.grid_display.Refresh()

    def evt_changed_bitstrings(self,event):
        if(self.x_bitcode_field.Validate() and self.y_bitcode_field.Validate()):
            self.engine.set_strings(self.x_bitcode_field.GetValue(),self.y_bitcode_field.GetValue())
            self.engine.rebuild_structures()
            self.resize_grid()
            self.grid_display.Refresh()

    def evt_changed_colormode(self,event):
        if(self.list_bgstyle.GetSelection()==1):
            for i in [0,1]:
                self.bg_twocolor[i].Show()
        else:
            for i in [0,1]:
                self.bg_twocolor[i].Hide()
        if(self.list_bgstyle.GetSelection()==2):
            for i in range(10):
                self.bg_enclavecolor[i].Show()
        else:
            for i in range(10):
                self.bg_enclavecolor[i].Hide()
        self.Layout()
        self.grid_display.Refresh()

    def resize_grid(self):
        size=self.grid_display.GetSize()
        self.grid_sizer.SetRatio(((float) (len(self.engine.x_bits)-1))/(len(self.engine.y_bits)-1))
        self.main_layout.Layout()
  
    def evt_repaint_grid(self,event):
        gridBuilder=WXDrawing(self.grid_display,len(self.engine.x_bits),len(self.engine.y_bits))
        grid_pen=wx.Pen(self.grid_color.GetColour()) if self.cb_grid_display.GetValue() else None;
        if(self.list_bgstyle.GetSelection()==1):
            colors=self.bg_twocolor
            fills=self.engine.two_colors
        elif(self.list_bgstyle.GetSelection()==2):
            colors=self.bg_enclavecolor
            fills=self.engine.enclave_colors
        else:
            colors=None
            fills=[]
        gridBuilder.draw_all(
            grid_pen=grid_pen,
            stitch_pen=wx.Pen(self.stitchcolor.GetColour(),width=self.stitchweight.GetValue()),
            colors=colors,
            polylines=self.engine.polylines,
            cycles=self.engine.cycles,
            fills=fills);
  
if __name__ == '__main__':
    app = wx.App()
    frame = ExplorerFrame()
    app.MainLoop()
