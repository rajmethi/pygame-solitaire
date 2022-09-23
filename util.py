import pygame, time

#module level scope
pygame.init()
font = pygame.font.SysFont("Arial", 12)

class Button():
    #3 states:
    IDLE = 0
    CLICKED = 1
    HOVERED_OVER = 2

    def __init__(self, surface, x, y, w, h, color, on_click, text=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.surface = surface
        self.button_rect = pygame.Rect(x, y, w, h)
        if color is None:
            color = "Red"
        normal_color = pygame.Color(color)
        lighter_color = (min(normal_color.r + 50, 255),
                         min(normal_color.g + 50, 255),
                         min(normal_color.b + 50, 255))
        darker_color = (max(normal_color.r - 50, 0),
                        max(normal_color.g - 50, 0),
                        max(normal_color.b - 50, 0))
        self.colors = [color, darker_color, lighter_color]
        self.on_click = on_click
        self.state = self.IDLE
        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, self.colors[self.state], self.button_rect)
        button_description = font.render(self.text, True, "Black")
        self.surface.blit(button_description,(self.x + self.w / 2 -button_description.get_width(), self.y + self.h / 2 -button_description.get_height()))




    #event handler - function that does something when some event occurs
    def handle_mouse_motion(self, event):
        if self.button_rect.collidepoint(event.pos):
            if self.state != self.CLICKED:
                self.state = self.HOVERED_OVER
        else:
            self.state = self.IDLE #allows us to move off the button
            #without firing the event
        self.draw() #update color


    def handle_mouse_down(self, event):
        if self.state == self.HOVERED_OVER:
            self.state = self.CLICKED
            self.draw()

    #optional parameter - by default, number_of_objects is 1
    def handle_mouse_up(self, event):
        if self.state == self.CLICKED:
            self.state = self.HOVERED_OVER
            if self.on_click is not None:
                self.on_click() #fires the event
            self.draw()

    def handle_key_press(self, event):
        pass


#inheritance - when one class shares many characteristics or functions
#with another class, we can inherit the functionality/characteristics
#from one to the other
class RadioButton(Button):
#RadioButton class inherits from the Button class
#RadioButton - child/sub class
#Button - parent/super class
    def __init__(self, surface, x, y, radius, text_string):
        self.toggled = False
        self.text_string = text_string
        super().__init__(surface, x, y, radius*2, radius*2, None, None)
        self.on_click = self.toggle

    def toggle(self):
        self.toggled = not self.toggled


    #overriding a method - change the behavior of an inherited method
    def draw(self):
        #outer circle
        pygame.draw.circle(self.surface, "White", self.button_rect.center, self.button_rect.w/2)
        #inner circle
        if self.toggled:
            pygame.draw.circle(self.surface, "Black", self.button_rect.center, self.button_rect.w/4)
        button_description = font.render(self.text_string, True, "White")
        self.surface.blit(button_description, self.button_rect.topright)


class Slider():
    IDLE = 0
    CLICKED = 1

    def __init__(self, surface, x, y, w, h, min_value=0, max_value=1, slider_value=0.5, precision=2):
        self.surface = surface
        self.bound_rect = pygame.Rect(x, y, w, h)
        if min_value >= max_value: #if the user defines an invalid value for max or min
            min_value = 0
            max_value = 1
        self.min_value = min_value
        self.max_value = max_value
        if slider_value < min_value: #initial can't be too small
            slider_value = min_value
        elif slider_value > max_value: #can't be too large
            slider_value = max_value
        self.slider_value = round(slider_value, precision)
        self.precision = precision
        #slider_x - x coordinate within self.bound_rect
        self.slider_x = x + (self.slider_value - self.min_value)/(self.max_value - self.min_value)*w
        self.state = self.IDLE
        self.slider_w = 10
        self.draw()

    def handle_mouse_down(self, event):
        if self.bound_rect.collidepoint(event.pos):
            self.state = self.CLICKED

    def handle_mouse_up(self, event):
        self.state = self.IDLE

    def handle_mouse_motion(self, event):
        #only move the slide if it was clicked on
        if self.state == self.CLICKED:
            #set slider_x to the mouse x position
            if event.pos[0] < self.bound_rect.x: #left bound
                self.slider_x = self.bound_rect.x
            elif event.pos[0] > self.bound_rect.right: #right bound
                self.slider_x = self.bound_rect.right
            else:
                self.slider_x = event.pos[0] #just the x coordinate of the mouse
            self.slider_value = (self.slider_x - self.bound_rect.x)*(self.max_value-
                            self.min_value)/self.bound_rect.w + self.min_value
            self.slider_value = round(self.slider_value, self.precision)

            self.draw()

    def draw(self):
        background_rect = self.bound_rect.inflate(self.slider_w, 0)
        #draw background rect (color = white)
        pygame.draw.rect(self.surface, "white", background_rect)
        #draw line through the middle of the rectangle horizontally (color = blue)
        pygame.draw.line(self.surface, "blue", self.bound_rect.midleft, self.bound_rect.midright)
        #draw a smaller rectangle representing the slider (color = red)
        slider_rect = pygame.Rect(self.slider_x-self.slider_w/2, self.bound_rect.centery-self.bound_rect.h//2,
                                  self.slider_w, self.bound_rect.h)
        pygame.draw.rect(self.surface, "red", slider_rect)
        #render font
        value_text = font.render(str(self.slider_value), True, "Black")
        self.surface.blit(value_text, (self.bound_rect.centerx - value_text.get_width()/2,
                                       self.bound_rect.centery - value_text.get_height() + 2))

class EntryBox():
    IDLE = 0
    CLICKED = 1
    HOVERED_OVER = 2
    def __init__(self, surface, x, y, w, h, color, text_color, font, label_text, label_loc):
        self.state = self.IDLE
        self.screen = surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.box = pygame.Rect(x,y,w,h)
        self.color = color
        self.text_color = text_color
        self.label_text = label_text #label of entry box
        self.label_loc = label_loc #location of label- above or below box
        self.font = pygame.font.SysFont(font, 25)
        self.user_text = '' #live text update
        self.final_input = '' #final text string after RETURN key

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.box)
        label_render = font.render(self.label_text,True, 'white')
        if self.label_loc == 'above':
            self.screen.blit(label_render,(self.x, self.y-label_render.get_height())) #label of box location
        else:
            self.screen.blit(label_render, (self.x, self.y+ self.w))
        pygame.draw.line(self.screen, 'black', (self.x+1,self.y+1), (self.x+1,self.y+self.w-1)) #cursor
        user_text_render = font.render(self.user_text,True,'black')
        self.screen.blit(user_text_render, (self.x+2, self.y+2))

    def reset_values(self):
        self.user_text = ''
        self.final_input = ''

    def handle_mouse_down(self, event):
        if self.state == self.HOVERED_OVER:
            self.state = self.CLICKED
            self.draw()

    def handle_mouse_up(self, event):
        if not self.box.collidepoint(event.pos):
            self.state = self.IDLE



    def handle_mouse_motion(self, event):
        if self.box.collidepoint(event.pos):
            if self.state != self.CLICKED:
                self.state = self.HOVERED_OVER

    def handle_key_press(self, event):
        if self.state == self.CLICKED:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.final_input = self.user_text
                else:
                    self.user_text += event.unicode
