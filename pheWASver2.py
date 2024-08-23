# imports 
from tqdm import tqdm 
from snp_manager import * 
import pandas 
import pygame 
import os 
import math 
import pyperclip 
from math import log10 

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

    def click(self,text2): 
        text = str(f"{self.rsid}, {self.phenotype}") 
        pyperclip.copy(text) 
        if text == text2: 
            self.websearch() if self.websearched == False else None 
        return text 

# functions 


def display_text(text, font_name, font_size, color, position,display):

    # Set up font
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color) 
    display.blit(text_surface, position) 

def update_squares(x,y,square,squares): 
    for square_instance in squares: 
        square_instance.x += x 
        square_instance.y += y 
        square_instance.rect = pygame.Rect(square_instance.x,square_instance.y,square,square) 

def generate_squares(data_dict,square,weight,x,y,squares): 
    ywithoffset = y 
    xwithoffset = x 
    for rsid in tqdm(data_dict): 
        pheWAS_colour_dict[rsid] = {} 
        for phenotype in data_dict[rsid]: 
            data = data_dict[rsid][phenotype] 
            beta = data[0] if data[0] != "" else 0 
            beta = float(beta) 
            mlogpvalue = data[2] if 0 < float(data[2] ) else 1 
            effect = min([max([0,math.floor(255-abs(weight*float(beta)))]) ,255]) 
            # opacity = min([max([0,80*abs(log10(float(mlogpvalue) ) ) ]),255]) 
            opacity = min([max([0,150*abs((float(mlogpvalue) ) ) ]),255]) 

            if 0 < beta: 
                colour = (effect,effect,255,opacity) 
            else: 
                colour = (255, effect,effect,opacity) 
            pheWAS_colour_dict[rsid][phenotype] = Square(colour,xwithoffset,ywithoffset,square,rsid,phenotype,squares) 
            xwithoffset += square 
        xwithoffset = x 
        ywithoffset += square 
    return pheWAS_colour_dict 

def handle_events(pygame,data_dict,square,weight,pheWAS_colour_dict,movement,x,y,original_pos,squares,text): 
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
                    text = square_instance.click(text) 

        elif event.type == pygame.MOUSEWHEEL: 
            clear(display=display,type=0) 
            update(display=display) 
            yvalue = event.y 
            absoluteyvalue=abs(yvalue) 
            sign = yvalue//absoluteyvalue 
            for scroll in range(0,absoluteyvalue): 
                square += sign 
            pheWAS_colour_dict = generate_squares(data_dict=data_dict,square=square,weight=weight,x=x,y=y,squares=squares) 
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            if movement == False and event.button == 1: 
                original_pos = pygame.mouse.get_pos() 
                movement = True 
            elif event.button == 3: 
                mouse_pos = pygame.mouse.get_pos() 
                for square_instance in squares: 
                    if square_instance.rect.collidepoint(mouse_pos): 
                        text = square_instance.click(text) 

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
                pheWAS_colour_dict = generate_squares(data_dict=data_dict,square=square,weight=weight,x=x,y=y,squares=squares) 

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

def getmlogpvalbyphenotypewithrsid(phenotype,rsid,data_dict): 
    try: 
        return data_dict[rsid][phenotype] 
    except: 
        return 0 

def update(display): 
    pygame.display.flip() 
    return display 

pygame.init() 

# initializing drawings 
x = 0 
y = 0 
square = 1 
weight = 25 
pheWAS_colour_dict = {} 
original_pos = 0 
squares = [] 

data_dict = eval(open(select_files()[0],"r").readlines()[0]) 


pheWAS_colour_dict = generate_squares(data_dict=data_dict,square=square,weight=weight,x=x,y=y,squares=squares) 

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

pheWAS_colour_dict, square, weight, movement, x, y, original_pos, text = handle_events(pygame=pygame,data_dict=data_dict,square=square,weight=weight,pheWAS_colour_dict=pheWAS_colour_dict,movement=movement,x=x,y=y,original_pos=original_pos,squares=squares,text=text) 
display = clear(display,1) 
display = draw(display,pheWAS_colour_dict) 
display = update(display) 
clock = tick_clock(clock) 
pygame.image.save(display,"pheWAS Heatmap.bmp") 

while (drawing): 
    pheWAS_colour_dict, square, weight, movement, x, y, original_pos, text = handle_events(pygame=pygame,data_dict=data_dict,square=square,weight=weight,pheWAS_colour_dict=pheWAS_colour_dict,movement=movement,x=x,y=y,original_pos=original_pos,squares=squares,text=text) 
    display = clear(display,1) 
    display = draw(display,pheWAS_colour_dict) 
    display_text(text, 'Arial', 48, (0, 0, 0), (0, 0),display=display) 

    display = update(display) 
    clock = tick_clock(clock) 
