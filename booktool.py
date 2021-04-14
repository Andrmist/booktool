#!/usr/bin/env python
import wx
from pages import parse_word, parse_line
import math

class MyFrame(wx.Frame):
    """ We simply derive a new class of Frame. """

    def __init__(self, parent, title):
        # Logical variables

        self.pages = []
        self.current_page = 0

        wx.Frame.__init__(self, parent, title=title, size=(600, 500))
        dw, dh = wx.DisplaySize()
        self.SetPosition((dw // 2 - 300, dh // 2 - 250))
        # self.SetFont()

        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(12)
        panel.SetFont(font)

        input_box = wx.BoxSizer(wx.VERTICAL)
        info = wx.StaticText(panel, label="Paste your text here:")
        self.input = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.input.Bind(wx.EVT_TEXT, self.on_input)

        input_box.Add(info, flag=wx.RIGHT)
        input_box.Add(self.input, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND)

        output_box = wx.BoxSizer(wx.VERTICAL)
        navigation_box = wx.BoxSizer(wx.HORIZONTAL)

        self.output = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)

        nav_left = wx.Button(panel, wx.ID_ANY, "<--")
        nav_right = wx.Button(panel, wx.ID_ANY, "-->")

        nav_left.Bind(wx.EVT_BUTTON, self.left)
        nav_right.Bind(wx.EVT_BUTTON, self.right)

        navigation_box.Add(nav_left, proportion=1, flag=wx.LEFT)
        navigation_box.Add(nav_right, proportion=1, flag=wx.LEFT)

        output_box.Add(navigation_box, flag=wx.LEFT | wx.RIGHT | wx.EXPAND)
        output_box.Add(self.output, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM | wx.EXPAND)

        hbox.Add(input_box, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)
        hbox.Add(output_box, wx.ID_ANY, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(hbox)
        self.Show(True)

    def on_input(self, e):
        a = self.input.GetValue()
        # print(['{}: {}'.format(i, parse_word(i)) for i in a.split()])
        b = []
        while True:
            # print(a)
            if len(a) == 0:
                break
            # print(parse_line(a)[0])
            # print(repr(" ".join(parse_line(a)[0])))  # , ":", parse_line(a)[2])
            b.append(" ".join(parse_line(a)[0]))
            a = " ".join(parse_line(a)[1])
        self.pages.clear()
        l = 0
        for i in range(1, (math.floor(len(b) / 14)) + 1):
            self.pages.append([b[k] for k in range(l, i * 14)])
            l = i * 14

        print(math.floor(len(b) / 14))
        # print()
        self.pages.append([b[k] for k in range(l, len(b))])
        print(self.pages)

        # print([b[k] for k in range(l, len(b) - len(b) // 14)])
        self.output.ChangeValue("\n".join(self.pages[self.current_page]))

    def left(self, e):
        if self.current_page < len(self.pages) and self.current_page - 1 >= 0:
            self.current_page -= 1
            self.output.ChangeValue("\n".join(self.pages[self.current_page]))
        else:
            difference = [abs(self.current_page - 0), abs(self.current_page - len(self.pages))]
            self.current_page = 0
            self.output.ChangeValue("\n".join(self.pages[self.current_page]))

    def right(self, e):
        if self.current_page < len(self.pages) and self.current_page + 1 <= len(self.pages) - 1:
            self.current_page += 1
            self.output.ChangeValue("\n".join(self.pages[self.current_page]))
        else:
            difference = [abs(self.current_page - 0), abs(self.current_page - len(self.pages))]
            self.current_page = len(self.pages) - 1
            self.output.ChangeValue("\n".join(self.pages[self.current_page]))


app = wx.App(False)
frame = MyFrame(None, 'Book Tool')
app.MainLoop()
