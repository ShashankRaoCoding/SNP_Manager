from snp_manager import * 
import tkinter as tk 
import tkinter as tk 
import pyperclip 


def main(paths,data,logarithmic,xaxisattr,yaxisattr): 

    selected_option1 = yaxisattr.get()
    selected_option2 = xaxisattr.get()
    logarithmic = logarithmic.get() 
    logarithmic = eval(logarithmic) 
    pyperclip.copy(generatefilename(paths)) 
    data.plot(selected_option2,selected_option1,selected_option2,selected_option1,logarithmic,generatefilename(paths),True,False) 

paths = select_files() 
filedict= parsepaths(paths) 
data = filegroup(filedict) 
root = tk.Tk()
root.title("PLOT UI ")
logarithmic = tk.StringVar(root)
logarithmic.set("Logarithmic? ")  # Set the default value
logarithmic_options = ["True","False"] 
dropdown = tk.OptionMenu(root, logarithmic, *logarithmic_options)
dropdown.pack(pady=20) 
dropdown.pack(pady=20) 
yaxisattr = tk.StringVar(root)
yaxisattr.set("y axis attribute ")  # Set the default value
xaxisattr = tk.StringVar(root)
xaxisattr.set("x axis attribute ")  # Set the default value
axisattr_options = data.atts 
dropdown = tk.OptionMenu(root, yaxisattr, *axisattr_options)
dropdown.pack(pady=20)
dropdown = tk.OptionMenu(root, xaxisattr, *axisattr_options)
dropdown.pack(pady=20)
button = tk.Button(root, text="Create ", command=lambda: main(paths,data,logarithmic,xaxisattr,yaxisattr))
button.pack(pady=20)
root.mainloop() 






