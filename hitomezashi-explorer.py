#!/usr/bin/env python
import wx,random,itertools

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
   

class ExplorerGrid(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.SetBackgroundColour(wx.WHITE)

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
        self.x_string=""
        self.y_string=""
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
        self.x_string=self.x_bitcode_field.GetValue()
        self.x_bitcode_field.Bind(wx.EVT_TEXT, self.evt_changed_bitstrings)
        y_bitstring_entries.Add(
            wx.StaticText(self,label="Horizontal-stitch bitcode: "),
            flag=wx.RIGHT,
            border=8)
        self.y_bitcode_field = wx.TextCtrl(self,validator=BitStringValidator(),value=randomword(5))
        x_bitstring_entries.Add(self.x_bitcode_field,flag=wx.RIGHT | wx.EXPAND, border=10)
        self.y_bitcode_field.Bind(wx.EVT_TEXT, self.evt_changed_bitstrings)
        self.y_string=self.y_bitcode_field.GetValue()
        y_bitstring_entries.Add(self.y_bitcode_field,flag=wx.RIGHT | wx.EXPAND, border=10, proportion=1)
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

  

        self.grid_display=ExplorerGrid(self)
        self.grid_display.SetBackgroundColour('white')
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

        self.bg_color_sizer = wx.BoxSizer(wx.HORIZONTAL)
  
        self.list_bgstyle = wx.ComboBox(self,value="None", choices=["None","Two colors","Enclave coloring"],style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.list_bgstyle.Bind(wx.EVT_COMBOBOX,self.evt_changed_colormode)
        self.bg_color_sizer.Add(
            wx.StaticText(self,label="Fill-color style: "),
            flag=wx.RIGHT|wx.TOP|wx.BOTTOM,
            border=8)
        self.bg_color_sizer.Add(self.list_bgstyle)

        self.bg_twocolor=[
            wx.ColourPickerCtrl(self,colour=wx.Colour("WHITE")),
            wx.ColourPickerCtrl(self,colour=wx.Colour("RED"))]
        for i in [0,1]:
            self.bg_color_sizer.Add(self.bg_twocolor[i])
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
            self.bg_color_sizer.Add(self.bg_enclavecolor[i])
            print(self.bg_enclavecolor[i].GetSize())
            self.bg_enclavecolor[i].Bind(wx.EVT_COLOURPICKER_CHANGED,self.evt_refresh)
            self.bg_enclavecolor[i].Hide()


        self.main_layout.Add(self.bg_color_sizer)
  
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
            self.x_string=self.x_bitcode_field.GetValue()
            self.y_string=self.y_bitcode_field.GetValue()

            self.enclave_colors=None
            self.two_colors=None
            if(len(self.x_string)>1 and len(self.y_string)>1):
                self.rebuild_colortables()
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
        self.rebuild_colortables()
        self.grid_display.Refresh()


    def rebuild_colortables(self):
        self.two_colors=[[0]*(len(self.y_string)-1) for i in range(len(self.x_string)-1)]
        for x in range(len(self.x_string)-1):
            for y in range(len(self.y_string)-1):
                crossings=0
                for i in range(x+1):
                    crossings+=(self.x_string[i]=="0")
                for i in range(1,y+1):
                    crossings+=(1-(self.y_string[i]=="0")-x-y)%2
                self.two_colors[x][y]=crossings % 2

        # Only rebuild enclave colors if we have to (it can be very
        # computationally intensive)
        if (self.list_bgstyle.GetSelection()==2) and self.enclave_colors is None:
            INFINITY=len(self.x_string)*len(self.y_string);

            # Initialize all distances from border to "infinity"
            self.enclave_colors=[[INFINITY]*(len(self.y_string)-1) for i in range(len(self.x_string)-1)]

            def borderDistWrapper(x,y):
                if(x<0 or x>=len(self.x_string)-1):
                    return INFINITY
                if(y<0 or y>=len(self.y_string)-1):
                    return INFINITY
                return self.enclave_colors[x][y]

            # Seed the open edges with zeroes and ones
            curColor=0
            for i in range(len(self.x_string)-2):
                if (i%2 != int(self.y_string[0])):
                    self.enclave_colors[i][0]=curColor
                if False:
                    if (int(self.x_string[i+1])==0):
                        curColor = 1-curColor
            for i in range(len(self.y_string)-2):
                if (i%2 != int(self.x_string[len(self.x_string)-1])):
                    self.enclave_colors[len(self.x_string)-2][i]=curColor
                if False:
                    if (int(self.y_string[i+1])==len(self.x_string)%2):
                        curColor = 1-curColor
            for i in range(len(self.x_string)-2,0,-1):
                if (i%2 != int(self.y_string[len(self.y_string)-1])):
                    self.enclave_colors[i][len(self.y_string)-2]=curColor
                if False:
                    if (int(self.x_string[i])==len(self.y_string)%2):
                        curColor = 1-curColor
            for i in range(len(self.y_string)-2,0,-1):
                if (i%2 != int(self.x_string[0])):
                    self.enclave_colors[0][i]=curColor
                if False:
                    if (int(self.y_string[i])==0):
                        curColor = 1-curColor

            # This is definitely not even remotely the most efficient way to
            # do it, but it works.
            changesMade=True
            while(changesMade):
                changesMade=False
                for x in range(0,len(self.x_string)-1):
                    for y in range(0,len(self.y_string)-1):
                        probe=min(
                            borderDistWrapper(x,y+1)+1-((int(self.y_string[y+1])-x)%2),
                            borderDistWrapper(x+1,y)+1-((int(self.x_string[x+1])-y)%2),
                            borderDistWrapper(x,y-1)+1-((int(self.y_string[y])-x)%2),
                            borderDistWrapper(x-1,y)+1-((int(self.x_string[x])-y)%2)
                        )
                        if probe<self.enclave_colors[x][y]:
                            changesMade=True
                            self.enclave_colors[x][y]=probe
  
    def resize_grid(self):
        size=self.grid_display.GetSize()
        self.grid_sizer.SetRatio(((float) (len(self.x_string)-1))/(len(self.y_string)-1))
        self.main_layout.Layout()
  
    def evt_repaint_grid(self,event):
        dc = wx.PaintDC(self.grid_display)
        (xMax,yMax)=dc.GetSize()
        xMax=xMax-2*GRID_BORDER-1
        yMax=yMax-2*GRID_BORDER-1
        if(len(self.x_string)<2 or len(self.y_string)<2):
            return


        # Color in all squares using two-color mode
        dc.SetPen(wx.NullPen)
        if(self.list_bgstyle.GetSelection()==1):
            brushes=[wx.Brush(self.bg_twocolor[i].GetColour()) for i in [0,1]]
            for x in range(len(self.x_string)-1):
                for y in range(len(self.y_string)-1):
                    dc.SetBrush(brushes[self.two_colors[x][y]])
                    dc.DrawRectangle(int(GRID_BORDER+xMax*x/(len(self.x_string)-1))-1,int(GRID_BORDER+yMax*y/(len(self.y_string)-1))-1,int(xMax/(len(self.x_string)-1))+2,int(yMax/(len(self.y_string)-1))+2)

        # Color in all squares using enclave mode
        elif(self.list_bgstyle.GetSelection()==2):
            brushes=[wx.Brush(self.bg_enclavecolor[i].GetColour()) for i in range(9)]
            for x in range(len(self.x_string)-1):
                for y in range(len(self.y_string)-1):
                    dc.SetBrush(brushes[self.enclave_colors[x][y] % 10])
                    dc.DrawRectangle(int(GRID_BORDER+xMax*x/(len(self.x_string)-1))-1,int(GRID_BORDER+yMax*y/(len(self.y_string)-1))-1,int(xMax/(len(self.x_string)-1))+2,int(yMax/(len(self.y_string)-1))+2)
              
        # Draw gridlines
        dc.SetBrush(wx.NullBrush)
        if(self.cb_grid_display.GetValue()):
            dc.SetPen(wx.Pen(self.grid_color.GetColour()))
            for i in range(len(self.x_string)):
                dc.DrawLine(GRID_BORDER+int(xMax*i/(len(self.x_string)-1)),GRID_BORDER,GRID_BORDER+int(xMax*i/(len(self.x_string)-1)),GRID_BORDER+yMax)
            for i in range(len(self.y_string)):
                dc.DrawLine(GRID_BORDER,GRID_BORDER+int(yMax*i/(len(self.y_string)-1)),GRID_BORDER+xMax,GRID_BORDER+int(yMax*i/(len(self.y_string)-1)))

        # Draw stitches
        dc.SetPen(wx.Pen(self.stitchcolor.GetColour(),width=self.stitchweight.GetValue()))
        for i in range(len(self.x_string)):
            dashon=(self.x_string[i]=="0")
            for j in range(len(self.y_string)-1):
                if dashon:
                    dc.DrawLine(GRID_BORDER+int(xMax*i/(len(self.x_string)-1)),GRID_BORDER+int(yMax*j/(len(self.y_string)-1)),GRID_BORDER+int(xMax*i/(len(self.x_string)-1)),GRID_BORDER+int(yMax*(j+1)/(len(self.y_string)-1)))
                dashon=not dashon
        for i in range(len(self.y_string)):
            dashon=(self.y_string[i]=="0")
            for j in range(len(self.x_string)-1):
                if dashon:
                    dc.DrawLine(GRID_BORDER+int(xMax*j/(len(self.x_string)-1)),GRID_BORDER+int(yMax*i/(len(self.y_string)-1)),GRID_BORDER+int(xMax*(j+1)/(len(self.x_string)-1)),GRID_BORDER+int(yMax*i/(len(self.y_string)-1)))
                dashon=not dashon

  
if __name__ == '__main__':
    app = wx.App()
    frame = ExplorerFrame()
    app.MainLoop()
