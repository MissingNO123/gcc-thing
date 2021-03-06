print("please wait...")
import sys, time
from TPPFLUSH.tppflush import *
import pygame
from enum import IntEnum

done=False

#edit this to True to print the bytes that are sent.
print_bytes=False

buttonMappings = {
                0: HIDButtons.A,
                1: HIDButtons.B,
                2: HIDButtons.X,
                3: HIDButtons.Y,
                4: HIDButtons.SELECT, #Z
                5: HIDButtons.R,
                6: HIDButtons.L,
                7: HIDButtons.START,
                8: HIDButtons.DPADUP,
                9: HIDButtons.DPADDOWN,
                10: HIDButtons.DPADLEFT,
                11: HIDButtons.DPADRIGHT
        }

class KBDButtons(IntEnum):
        C_UP = pygame.K_w
        C_DOWN = pygame.K_s
        C_LEFT = pygame.K_a
        C_RIGHT = pygame.K_d

        DPADUP = pygame.K_UP
        DPADDOWN = pygame.K_DOWN
        DPADLEFT = pygame.K_LEFT
        DPADRIGHT = pygame.K_RIGHT

        A = pygame.K_j
        B = pygame.K_k
        X = pygame.K_u
        Y = pygame.K_i
        L = pygame.K_h
        R = pygame.K_l
        START = pygame.K_RETURN
        SELECT = pygame.K_BACKSPACE
        ZL = pygame.K_y
        ZR = pygame.K_o

        HOME = pygame.K_HOME
        POWER = pygame.K_END

def handle_unmapped_button(event):
        #todo: Add a graphical warning of some kind, or allow users to rebind
        print("[Warning] Joystick {} button {} is not mapped to any button.".format(event.joy,event.button))

if len(sys.argv) < 2:
	server = input("3DS IP >").strip()
else:
        server = sys.argv[1]
        
server=LumaInputServer(server)

#time.sleep(3)
#server.hid_press(HIDButtons.X) #to show it works
#server.send(print_bytes)

pygame.init()
screen = pygame.display.set_mode((320, 240))
#screen.fill((0,0,0))
TCImg="images/home.jpg"
try:
        img=pygame.image.load(TCImg)
except pygame.error:
        print("Could not find touch screen file, using default black screen")
        screen.fill((0,0,0))
else:
        screen.blit(img,(0,0))
        pygame.display.flip()
pygame.display.set_caption('touchscreen')
pygame.display.update()

pygame.joystick.init()

joystick_count = pygame.joystick.get_count()
print("Number of joysticks: {}".format(joystick_count) )
for i in range(joystick_count):
        print("")
        joystick = pygame.joystick.Joystick(i)
        print("initting joystick {}".format(i))
        joystick.init()
        name = joystick.get_name()
        print(" Joystick name: {}".format(name))
        axes = joystick.get_numaxes()
        print(" Number of axes: {}".format(axes))
        buttons = joystick.get_numbuttons()
        print(" Number of buttons: {}".format(buttons))
        hats = joystick.get_numhats()
        print(" Number of hats: {}".format(hats))

print("ready!")
while done==False:
        for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done=True

                #Touchscreen input
                if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        server.touch(pos[0], pos[1])
                        #print("THSC: ",pos[0],",",pos[1])
                        server.send(print_bytes)
                elif event.type == pygame.MOUSEBUTTONUP:
                        server.clear_touch()
                        server.send(print_bytes)

                #Keyboard Mappings
                elif event.type == pygame.KEYDOWN:
                        if event.key == KBDButtons.C_UP:
                                server.circle_pad_set(CPAD_Commands.CPADUP)
                                #print("C_UP")
                        if event.key == KBDButtons.C_LEFT:
                                server.circle_pad_set(CPAD_Commands.CPADLEFT)
                                #print("C_LEFT")
                        if event.key == KBDButtons.C_DOWN:
                                server.circle_pad_set(CPAD_Commands.CPADDOWN)
                                #print("C_DOWN")
                        if event.key == KBDButtons.C_RIGHT:
                                server.circle_pad_set(CPAD_Commands.CPADRIGHT)
                                #print("C_RIGHT")
                              
                        for button in KBDButtons:
                            if event.key == button:
                                if hasattr(HIDButtons, button.name): #KBDButtons.B -> HIDButtons.B
                                        server.press(HIDButtons[button.name])
                                        #print(button.name)

                        if event.key == KBDButtons.ZL: #ZL
                                server.n3ds_zlzr_press(N3DS_Buttons.ZL)
                                #print("ZL")
                        if event.key == KBDButtons.ZR: #ZR
                                server.n3ds_zlzr_press(N3DS_Buttons.ZR)
                                #print("ZR")
                        if event.key == KBDButtons.HOME: #Home
                                server.special_press(Special_Buttons.HOME)
                                #print("HOME")
                        if event.key == KBDButtons.POWER: #Power
                                server.special_press(Special_Buttons.POWER)
                                #print("POWER")
                                
                        if event.key == pygame.K_ESCAPE:
                                server.clear_everything()
                                done = True
                        server.send(print_bytes)
                        
                elif event.type == pygame.KEYUP:
                        if event.key == KBDButtons.C_UP:
                                server.circle_pad_coords[1] = 0
                        if event.key == KBDButtons.C_LEFT:
                                server.circle_pad_coords[0] = 0
                        if event.key == KBDButtons.C_DOWN:
                                server.circle_pad_coords[1] = 0
                        if event.key == KBDButtons.C_RIGHT:
                                server.circle_pad_coords[0] = 0
                        
                        for button in KBDButtons:
                            if event.key == button:
                                if hasattr(HIDButtons, button.name): #KBDButtons.B -> HIDButtons.B
                                        server.unpress(HIDButtons[button.name])

                        if event.key == KBDButtons.ZL: #Zl
                                server.n3ds_zlzr_unpress(N3DS_Buttons.ZL)
                        if event.key == KBDButtons.ZR: #Zr
                                server.n3ds_zlzr_unpress(N3DS_Buttons.ZR)
                        if event.key == KBDButtons.HOME: #Home
                                server.special_unpress(Special_Buttons.HOME)
                        if event.key == KBDButtons.POWER: #Power
                                server.special_unpress(Special_Buttons.POWER)

                        server.send(print_bytes)

                # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
                if event.type == pygame.JOYBUTTONDOWN:
                        print("Joystick {} button {} pressed.".format(event.joy,event.button))
                        if event.button in buttonMappings:
                                server.press(buttonMappings[event.button])
                                server.send(print_bytes)
                        else:
                                handle_unmapped_button(event)
                if event.type == pygame.JOYBUTTONUP:
                        print("Joystick {} button {} released.".format(event.joy,event.button))
                        if event.button in buttonMappings:
                                server.unpress(buttonMappings[event.button])
                                server.send(print_bytes)
                        else:
                                handle_unmapped_button(event)
                if event.type == pygame.JOYAXISMOTION:
                        #if event.axis in range(2,3): print("Joystick {} axis {} moved to {}.".format(event.joy,event.axis, event.value))
                        if event.axis == 0: server.circle_pad_coords[0] = int(32767*event.value) #ls x
                        if event.axis == 1: server.circle_pad_coords[1] = int(-32767*event.value) #ls y
                        if event.axis == 2: #l trig
                                if event.value >= 0: server.press(HIDButtons.L) #Zero is a half-press on GC Controller
                                else: server.unpress(HIDButtons.L)
                        if event.axis == 3: #r trig
                                if event.value >= 0: server.press(HIDButtons.R)
                                else: server.unpress(HIDButtons.R)
                        if event.axis == 4: server.cstick_coords[1] = int(-32767*event.value)  #rs y
                        if event.axis == 5: server.cstick_coords[0] = int(32767*event.value) #rs x
                        server.send(print_bytes)
                        
                #server.send(print_bytes) #GCC Axes - 0:LStickX 1:LStickY 4:CStickY 5:CStickX 2:LTrig 3:RTrig
print("clearing everything...")
server.clear_everything()
for i in range(1,50):
        server.send(print_bytes)
pygame.quit()
        
        

