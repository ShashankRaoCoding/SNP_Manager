# imports 
from tqdm import tqdm 
from snp_manager import * 
import pandas 
import pygame 
import os 
import math 
import pyperclip 

# classes 

class Square(snp): 
    def __init__(self,colour,x,y,square,rsid,phenotype,squares) -> None: 
        super().__init__(rsid) 

        squares.append(self) 
        self.x = x 
        self.y = y 
        self.colour = colour 
        self.rsid = rsid 
        self.phenotype = phenotype 
        self.rect = pygame.Rect(x,y,square,square) 
        self.websearched = False 
        pass 

    def click(self,type): 
        text = str(f"{self.rsid}, {self.phenotype}") 
        pyperclip.copy(text) 
        if type == 1: 
            self.websearch() if self.websearched == False else None 
        return text 

# functions 


def update_squares(x,y,square,squares): 
    for square_instance in squares: 
        square_instance.x += x 
        square_instance.y += y 
        square_instance.rect = pygame.Rect(square_instance.x,square_instance.y,square,square) 



def display_text(text, font_name, font_size, color, position,display):

    # Set up font
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color) 
    display.blit(text_surface, position) 


def generate_squares(mlogpvalue_dict,square,weight,x,y,squares): 
    ywithoffset = y 
    xwithoffset = x 
    for rsid in tqdm(mlogpvalue_dict): 
        pheWAS_colour_dict[rsid] = {} 
        for phenotype in mlogpvalue_dict[rsid]: 
            colour= max([0,math.floor(255-weight*float(mlogpvalue_dict[rsid][phenotype]))]) 
            pheWAS_colour_dict[rsid][phenotype] = Square((255,colour,colour),xwithoffset,ywithoffset,square,rsid,phenotype,squares) 
            xwithoffset += square 
        xwithoffset = x 
        ywithoffset += square 
    return pheWAS_colour_dict 

def handle_events(pygame,mlogpvalue_dict,square,weight,pheWAS_colour_dict,movement,x,y,original_pos,squares,text): 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit() 
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            pygame.quit() 
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w: 
            # pygame.quit() 
            
            # elif event.button == 6: 
            mouse_pos = pygame.mouse.get_pos() 
            for square_instance in squares: 
                if square_instance.rect.collidepoint(mouse_pos): 
                    text = square_instance.click(1) 

        elif event.type == pygame.MOUSEWHEEL: 
            clear(display=display,type=0) 
            update(display=display) 
            yvalue = event.y 
            absoluteyvalue=abs(yvalue) 
            sign = yvalue//absoluteyvalue 
            for scroll in range(0,absoluteyvalue): 
                square += sign 
            pheWAS_colour_dict = generate_squares(mlogpvalue_dict=mlogpvalue_dict,square=square,weight=weight,x=x,y=y,squares=squares) 
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if movement == False and event.button == 1: 
                original_pos = pygame.mouse.get_pos() 
                movement = True 
            elif event.button == 3: 
                mouse_pos = pygame.mouse.get_pos() 
                for square_instance in squares: 
                    if square_instance.rect.collidepoint(mouse_pos): 
                        text = square_instance.click(0) 

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
            if movement == True: 
                new_pos = pygame.mouse.get_pos() 
                xoffset = -original_pos[0]+new_pos[0] 
                yoffset = -original_pos[1]+new_pos[1] 
                x += xoffset 
                y += yoffset 
                clear(display=display,type=0) 
                update(display=display) 
                # update_squares(x=xoffset,y=yoffset,square=square,squares=squares) 
                pheWAS_colour_dict = generate_squares(mlogpvalue_dict=mlogpvalue_dict,square=square,weight=weight,x=x,y=y,squares=squares) 

                original_pos = 0 
                movement = False 
    return pheWAS_colour_dict, square, weight, movement, x, y, original_pos, text 

def clear(display,type): 
    display.fill((255*type,255*type,type*255)) 
    return display 

def draw(display,pheWAS_colour_dict): 
    for rsid in pheWAS_colour_dict: 
        for phenotype in pheWAS_colour_dict[rsid]: 
            square_instance = pheWAS_colour_dict[rsid][phenotype] 
            # print(display,pheWAS_colour_dict[rsid][phenotype][0],pheWAS_colour_dict[rsid][phenotype][1]) 
            pygame.draw.rect(display,square_instance.colour,square_instance.rect) 
    return display 

def getmlogpvalbyphenotypewithrsid(phenotype,rsid,mlogpvalue_dict): 
    try: 
        return mlogpvalue_dict[rsid][phenotype] 
    except: 
        return 0 

def update(display): 
    pygame.display.flip() 
    return display 

# file initializations 
phenotypes = open("pheWAS/phenotypes.txt","r").readlines()[0].split("\t") 
rsids = open("pheWAS/rsids.txt","r").readlines()[0].split("\t") 

# dictionary creation 
for i in rsids: 
    if i == "": 
        rsids.remove(i) 
for i in phenotypes: 
    if i == "": 
        phenotypes.remove(i) 

mlogpvalue_dict = {} 

for rsid in tqdm(rsids): 
    mlogpvalue_dict[rsid] = {} 
    for phenotype in phenotypes: 
        mlogpvalue_dict[rsid][phenotype] = 0 
        
for rsid in tqdm(rsids): 
    with open(f"TSVs/Web/{rsid}.tsv") as file: 
        lines = file.readlines() 
        for line in lines[1:]: 
            lineparts = line.split("\t") 
            if lineparts[4] == "": 
                lineparts[4] = 0 
            mlogpvalue_dict[rsid][lineparts[1]]=lineparts[4] # {rsid: {phenotype: mlogpvalue}} 

pygame.init() 

# initializing drawings 
x = 0 
y = 0 
square = 1 
weight = 25 
pheWAS_colour_dict = {} 
original_pos = 0 
squares = [] 


pheWAS_colour_dict = generate_squares(mlogpvalue_dict=mlogpvalue_dict,square=square,weight=weight,x=x,y=y,squares=squares) 

def tick_clock(clock): 
    clock.tick(60) 
    return clock 


# pygame initializations 

display = pygame.display.set_mode((0,0),pygame.RESIZABLE) 
clock = pygame.time.Clock() 


# drawing 

drawing = True 
movement = False 
text = "" 

pheWAS_colour_dict, square, weight, movement, x, y, original_pos, text = handle_events(pygame=pygame,mlogpvalue_dict=mlogpvalue_dict,square=square,weight=weight,pheWAS_colour_dict=pheWAS_colour_dict,movement=movement,x=x,y=y,original_pos=original_pos,squares=squares,text=text) 
display = clear(display,1) 
display = draw(display,pheWAS_colour_dict) 
display = update(display) 
clock = tick_clock(clock) 
pygame.image.save(display,"pheWAS Heatmap.bmp") 

while (drawing): 
    pheWAS_colour_dict, square, weight, movement, x, y, original_pos, text = handle_events(pygame=pygame,mlogpvalue_dict=mlogpvalue_dict,square=square,weight=weight,pheWAS_colour_dict=pheWAS_colour_dict,movement=movement,x=x,y=y,original_pos=original_pos,squares=squares,text=text) 
    display = clear(display,1) 
    display = draw(display,pheWAS_colour_dict) 
    display_text(text, 'Arial', 48, (0, 0, 0), (0, 0),display=display) 

    display = update(display) 
    clock = tick_clock(clock) 
