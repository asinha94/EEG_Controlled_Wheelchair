import pygame, sys
from numpy import *
from pygame.locals import *
import scipy
from mindwave_mobile.pyeeg import bin_power
from mindwave_mobile.mindwave import MindwaveBluetooth
from time import sleep
from bluetooth.btcommon import BluetoothError
pygame.init()

fpsClock= pygame.time.Clock()

window = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Mindwave Viewer")


p = MindwaveBluetooth("A0:E6:F8:F7:B9:58")
sleep(1)

blackColor = pygame.Color(0,0,0)
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
deltaColor = pygame.Color(100,0,0)
thetaColor = pygame.Color(0,0,255)
alphaColor = pygame.Color(255,0,0)
betaColor = pygame.Color(0,255,00)
gammaColor = pygame.Color(0,255,255)

background_img = pygame.image.load("viewer_background.png")

font = pygame.font.Font("freesansbold.ttf",20)
raw_eeg = True
spectra = []
iteration = 0

meditation_img = font.render("Meditation", False, redColor)
attention_img = font.render("Attention", False, redColor)

record_baseline = False

while True:
    sleep(1)
    try:
        p.update()
    except BluetoothError:
        sleep(3)
        continue
    
    window.blit(background_img,(0,0))
    if p.connected:
        iteration+=1
        
        flen = 50
            
        if len(p.parser.raw_values)>=500:
            spectrum, relative_spectrum = bin_power(p.parser.raw_values[-p.parser.buffer_len:], range(flen),512)
            spectra.append(array(relative_spectrum))
            if len(spectra)>30:
                spectra.pop(0)
                
            spectrum = mean(array(spectra),axis=0)
            for i in range (flen-1):
                value = float(spectrum[i]*1000) 
                if i<3:
                    color = deltaColor
                elif i<8:
                    color = thetaColor
                elif i<13:
                    color = alphaColor
                elif i<30:
                    color = betaColor
                else:
                    color = gammaColor
                pygame.draw.rect(window, color, (25+i*10,400-value, 5,value))
        else:
            pass
        pygame.draw.circle(window,redColor, (800,200),p.get_attention_value()/2)
        pygame.draw.circle(window,greenColor, (800,200),60/2,1)
        pygame.draw.circle(window,greenColor, (800,200),100/2,1)
        window.blit(attention_img, (760,260))
        pygame.draw.circle(window,redColor, (700,200),p.get_meditation_value()/2)
        pygame.draw.circle(window,greenColor, (700,200),60/2,1)
        pygame.draw.circle(window,greenColor, (700,200),100/2,1)
        
        window.blit(meditation_img, (600,260))
        if len(p.parser.current_vector)>7:
            m = max(p.parser.current_vector)
            for i in range(7):
                value = p.parser.current_vector[i] *100.0/m
                pygame.draw.rect(window, redColor, (600+i*30,450-value, 6,value))

        if raw_eeg:
            lv = 0
            for i,value in enumerate(p.parser.raw_values[-1000:]):
                v = value/ 255.0/ 5
                pygame.draw.line(window, redColor, (i+25,500-lv),(i+25, 500-v))
                lv = v
    else:
        img = font.render("Mindwave Headset is not sending data... Press F5 to autoconnect or F6 to disconnect.", False, redColor)
        window.blit(img,(100,100))
    
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN:
            if event.key== K_F5:
                p.write("\xc2")
            elif event.key== K_F6:
                p.write("\xc1")
            elif event.key==K_ESCAPE:
                pygame.quit()
                sys.exit()

    pygame.display.update()
    fpsClock.tick(30)
