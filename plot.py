from Libraries.snp_manager import * 
import matplotlib.pyplot as plt 
import tkinter as tk 
import tkinter as tk 
import pyperclip 
import os 

# (xattr: Any, yattr: Any, xlabel: Any, ylabel: Any, logarithmic: type[bool] = bool, title: type[str] = str, show: type[bool] = bool, save: str = "") -> None


def main(paths,data,logarithmic,xaxisattr,yaxisattr): 

    selected_option1 = xaxisattr.get()
    selected_option2 = yaxisattr.get()
    logarithmic = logarithmic.get() 
    logarithmic = eval(logarithmic) 
    pyperclip.copy(generatefilename(paths)) 
    # create_scatter_plot([data.snps],f'{generatefilename(paths)}',selected_option2,selected_option1,selected_option2,selected_option1,True,False, logarithmic) 
    data.plot(selected_option2,selected_option1,selected_option2,selected_option1,logarithmic,generatefilename(paths),True,False) 
    print("Writing... ") 
    import os

    current_path = os.getcwd()
    print(f'Current Working Directory: {current_path}') 

    output = open(f"{current_path}/{generatefilename(paths)}.txt","w") 
    output.write("rsID\tP\n") 
    for variant in getcommonsnps(data): 
        rsid = getattr(variant,"rsid") 
        pval = getattr(variant,selected_option2) 
        output.write(f"{rsid}\t{pval}\n") 
    output.close() 
    print("Done!! ") 

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
xaxisattr = tk.StringVar(root)
xaxisattr.set("y axis attribute ")  # Set the default value
yaxisattr = tk.StringVar(root)
yaxisattr.set("x axis attribute ")  # Set the default value
# options = ["P-value", "P", "pval"] 
axisattr_options = data.atts 
dropdown = tk.OptionMenu(root, xaxisattr, *axisattr_options)
dropdown.pack(pady=20)
dropdown = tk.OptionMenu(root, yaxisattr, *axisattr_options)
dropdown.pack(pady=20)
button = tk.Button(root, text="Create ", command=lambda: main(paths,data,logarithmic,xaxisattr,yaxisattr))
button.pack(pady=20)
root.mainloop() 






