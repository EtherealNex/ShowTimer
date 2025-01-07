from app.models.timer import *
from app.ui import *

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


    """ How To Call
         
        Example Call.  
        6:35 - call quarter
        6:50 - five
        6:55 - begginers

        The timer represents how long till next call.
        Run the next call as soon as call happens.
        
    """

    