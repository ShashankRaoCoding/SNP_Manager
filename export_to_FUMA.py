from snp_manager import * 
import tkinter as tk 
import os 
from tkinter.messagebox import showinfo

def main(paths,data,pvalue_column_name,beta_column_name,standard_error_column_name,effect_allele_column_name,non_effect_allele_column_name,odds_ratio_column_name): 
    pval = pvalue_column_name.get()
    beta = beta_column_name.get()
    SE = standard_error_column_name.get()
    effect = effect_allele_column_name.get()
    ref = non_effect_allele_column_name.get()
    OR = odds_ratio_column_name.get()
    current_path = os.getcwd()
    
    default = { 
        pval:"Pvalue column name ", 
        beta:"Beta column name ", 
        SE:"Standard Error column name ", 
        effect:"Effect Allele column name ", 
        ref:"Non Effect Allele column name ", 
        OR:"Odds Ratio column name ", 
    } 
    attrs = [] 
    attributes_all = [pval,beta,SE,effect,ref,OR] 
    for attr in attributes_all: 
        if attr != default[attr]: 
            attrs.append(attr) 

    output = open(f"{current_path}/{generatefilename(paths)}_for_FUMA.txt","w") 
    output.write("rsID") 
    for attr in attrs: 
        output.write(f"\t{attr}") 
    output.write("\n") 

    for variant in getcommonsnps(data): 
        rsid = getattr(variant,"rsid") 
        output.write(f"{rsid}") 
        for attr in attrs: 
            output.write(f"\t{getattr(variant,attr)}") 
        output.write("\n") 
    output.close() 
    showinfo("Success!!", f"Exported to {current_path}\{generatefilename(paths=paths)}_for_FUMA.txt") 

paths = select_files() 
filedict= parsepaths(paths) 
data = filegroup(filedict) 

root = tk.Tk() 
root.title("Export to FUMA UI ") 

pvalue_column_name = tk.StringVar(root) 
pvalue_column_name.set("Pvalue column name ") 
beta_column_name = tk.StringVar(root) 
beta_column_name.set("Beta column name ") 
standard_error_column_name = tk.StringVar(root) 
standard_error_column_name.set("Standard Error column name ")  
effect_allele_column_name = tk.StringVar(root) 
effect_allele_column_name.set("Effect Allele column name ") 
non_effect_allele_column_name = tk.StringVar(root) 
non_effect_allele_column_name.set("Non Effect Allele column name ") 
odds_ratio_column_name = tk.StringVar(root) 
odds_ratio_column_name.set("Odds Ratio column name ") 

dropdown = tk.OptionMenu(root, pvalue_column_name,*data.atts) 
dropdown.pack(pady=2)
dropdown = tk.OptionMenu(root, beta_column_name,*data.atts) 
dropdown.pack(pady=2)
dropdown = tk.OptionMenu(root, standard_error_column_name,*data.atts) 
dropdown.pack(pady=2)
dropdown = tk.OptionMenu(root, effect_allele_column_name,*data.atts) 
dropdown.pack(pady=2)
dropdown = tk.OptionMenu(root, non_effect_allele_column_name,*data.atts) 
dropdown.pack(pady=2)
dropdown = tk.OptionMenu(root, odds_ratio_column_name,*data.atts) 
dropdown.pack(pady=2)

button = tk.Button(root, text="Export ", command=lambda: main(paths,data,pvalue_column_name,beta_column_name,standard_error_column_name,effect_allele_column_name,non_effect_allele_column_name,odds_ratio_column_name))
button.pack(pady=2)
root.mainloop() 






