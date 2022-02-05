import Tkinter


class GUI:

    CONSTANTS = 0

    def __init__ (self):
        top = Tkinter.Tk ()
        top.configure(background='white')
        for r in range(3):
            for c in range(4):
                Tkinter.Label(top, text='R%s/C%s'%(r,c),
                    borderwidth=1 ).grid(row=r,column=c)

        top.mainloop ()


gui = GUI()