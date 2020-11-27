from math import e
from tkinter import *
from time import sleep


class Window:
    def __init__(self, title, w, h):
        # Initilize the window
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f'{w}x{h}')
        # Create the equations table
        self.eq = Equations()
        self.create_equation_table()
        # Creates the dropdown menu
        self.create_dropdown()
        self.last_chosen = "Equations"

    def create_dropdown(self):  # Creates the equation choice menu
        equations = ['Add', 'Subtract', 'Multiply', 'Divide']
        self.drop_down = StringVar(self.root)
        self.drop_down.set("Equations")
        items = OptionMenu(self.root, self.drop_down, *equations)
        items.place(x=10, y=10)

    def create_equation_table(self):
        self.equations = {'Add': self.eq.add,
                          'Subtract': self.eq.sub,
                          'Multiply': self.eq.mult,
                          'Divide': self.eq.div}

    def current_equation(self):
        # Get the equation entered
        return self.drop_down.get()

    def new_equation_chosen(self):
        if self.current_equation() != self.last_chosen:
            self.last_chosen = self.current_equation()
            return True
        else:
            return False

    def check(self):
        if self.new_equation_chosen():
            try:
                self.reset()
            except AttributeError:
                pass
            self.set_input_widgets()
        self.root.after(500, self.check)

    def set_input_widgets(self):
        self.last_chosen = self.current_equation()
        lab1 = Label(self.root, text="Val A:")
        lab2 = Label(self.root, text="Val B:")
        lab1.place(x=10, y=80)
        lab2.place(x=10, y=110)
        box1 = Entry(self.root, width=6)
        box2 = Entry(self.root, width=6)
        box1.place(x=45, y=80)
        box2.place(x=45, y=110)
        calc_button = Button(self.root, text="Calculate",
                             command=lambda: self.calc_button_cmd(box1, box2))
        calc_button.place(x=120, y=150)
        self.temp_widgets = [box1, box2, lab1, lab2, calc_button]

    def calc_button_cmd(self, box1, box2):
        global result_text # this is made global so the result label can be stored after the function stops executing
        try:
            val1 = float(box1.get())
            val2 = float(box2.get())
        except ValueError:
            # Warning thing here
            pass
        else:
            current_equation = self.current_equation()
            try:
                res = self.equations[current_equation](val1, val2)
            except ZeroDivisionError:
                pass  # Different warning thing here
            else:
                # Check if result can be printed as an int rather than a float
                check = int(res)
                if res == check:
                    res = check
                    
                try: # checks if the result label is in the temp; deletes old label before new label is created
                    if result_text in self.temp_widgets:
                        result_text.destroy()
                except NameError:
                    # exception if result text dosen't exist yet 
                    pass

                result_text = Label(self.root, text=f"Result -> {res}")
                result_text.place(x=15, y=180)
                reset_button = Button(
                    self.root, text="Done", command=self.reset)
                reset_button.place(x=15, y=210)
                self.temp_widgets.extend([result_text, reset_button])

    def reset(self):
        for w in self.temp_widgets:
            w.destroy()

    def run(self):
        self.root.after(500, self.check)
        self.root.mainloop()


class Equations:
    def add(self, val1, val2):
        return val1 + val2

    def sub(self, val1, val2):
        return val1 - val2

    def mult(self, val1, val2):
        return val1 * val2

    def div(self, val1, val2):
        return round(val1 / val2, 12)


window = Window("Math thing", 300, 300)
window.run()
