import random, pygame, os, util

hearts = {}
clubs = {}
diamonds = {}
spades = {}
allcards = [hearts, clubs, diamonds, spades]

class Card:
    IDLE = 0
    HOVERED_OVER = 1
    CLICKED = 2
    def __init__(self,num, suit, image_path, back_image_path, hidden,width=98,length=152):
        self.x = None
        self.y = None
        self.initial_x = None
        self.initial_y = None
        self.width = width
        self.length = length
        #self.box = pygame.Rect(self.x, self.y, self.width, self.length)
        self.num = num
        self.suit = suit
        self.tuple = (num, suit)
        self.hidden = hidden
        self.image_path = image_path
        self.back_image_path = back_image_path
        self.state = self.IDLE
        self.hitbox = [self.x, self.y, self.width, self.length /4.5]
        self.image = self.update()

    def update(self):
        self.hitbox[0] = self.x
        self.hitbox[1] = self.y
        if not self.hidden:
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (98.28, 152.88))
            return self.image
            #return self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.image = pygame.image.load(self.back_image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (98.28, 152.88))
            return self.image

            #return self.image.get_rect(topleft=(self.x,self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def index_card(self, card):
        if card == self.tuple:
            return self
        else:
            return None




class Solitaire:
    IDLE = 0
    HOVERED_OVER = 1
    CLICKED = 2
    def __init__(self, screen):
        self.nums = ['ace','2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        self.spades = {}
        self.hearts = {}
        self.diamonds = {}
        self.clubs = {}
        self.allcards = [self.spades, self.hearts, self.clubs, self.diamonds]
        self.suits = ["hearts", "diamonds","clubs","spades"]
        self.allcards_dict = self.deckmaker()[0]
        self.allcards_tuples = self.deckmaker()[1]
        self.card_obj_list = self.add_card_obj()
        self.randomized = self.randomizer()
        self.foundations = [[],[],[],[]]
        self.tableau = self.tableaumaker()
        self.hand = self.handmaker()
        self.waste = []
        self.color_valid = {'hearts': 0, 'diamonds': 0, 'spades': 1, 'clubs': 1}
        self.tableau_coordinates = self.tab_locations()
        self.foundation_coordinates = self.foundation_locations()
        self.hand_state = self.IDLE
        self.hand_coordinate = (54, 100, 98, 152)
        self.waste_coordinate = (54,400,98,152)
        self.selected_tab = None
        self.moving_cards = None
        self.screen = screen


    def deckmaker(self):
        for index, suit in enumerate(self.allcards):
            suitstring = self.suits[index]
            for num in self.nums:
                suit[num] = suitstring
        allcards_tuples = []
        for suit in self.suits:
            for num in self.nums:
                allcards_tuples.append((num, suit))
        return allcards, allcards_tuples
    def add_card_obj(self):
        card_obj_list = []
        for index,card in enumerate(self.allcards_tuples):
            num = card[0]
            suit = card[1]
            if num == "king" or num == 'jack' or num == 'queen':
                face_img = "/Users/rajmethi/Downloads/PNG-cards-1.3/" + num + "_of_" + suit + "2.png"
            else:
                face_img = "/Users/rajmethi/Downloads/PNG-cards-1.3/" + num + "_of_" + suit + ".png"
            back_img = "/Users/rajmethi/Downloads/PNG-cards-1.3/09a58d561b2a7b92bd506c83414ef1ab.png"
            hidden = True
            tab_index = None
            card_obj = Card(card[0], card[1], face_img,back_img, hidden)

            card_obj_list.append(card_obj)
        return card_obj_list

    def randomizer(self):
        rand = self.card_obj_list.copy()
        random.shuffle(rand)
        return rand


    def tableaumaker(self):
        tableau = []
        y = 0
        for i in range(1,8):
            pile = []
            while len(pile) < i:
                pile.append(self.randomized[y])
                y+=1
            tableau.append(pile)
        return tableau

    def handmaker(self):
        hand = self.randomized.copy()

        for pile in self.tableau:
            for card in pile:
                if card in hand:
                    hand.remove(card)
        return hand
    def divisions(self,screen):
        pygame.draw.rect(screen, "white",(200,0,5,800))
        pygame.draw.rect(screen, "white", (1245, 0, 5, 800))
        for i in range(4):
            pygame.draw.rect(screen, 'white', (1300,15 + 200*i,98,152),2)

        #top to bottom: heart, diamond,club, spade
        #heart, 15
        pygame.draw.polygon(screen, 'white', ((1328,95),(1364,95),(1346,120)))
        pygame.draw.circle(screen, 'white', (1337,87),13)
        pygame.draw.circle(screen, 'white', (1355, 87), 13)
        #diamond, 215
        pygame.draw.polygon(screen, 'white', ((1346,255),(1327,291), (1346,327) , (1365,291)))
        #club, 415
        pygame.draw.polygon(screen, 'white', ((1340,525), (1352,525), (1346, 495)))
        pygame.draw.circle(screen, 'white', (1332,497),14)
        pygame.draw.circle(screen, 'white', (1360, 497), 14)
        pygame.draw.circle(screen, 'white', (1346, 474), 14)
        pygame.draw.polygon(screen, 'white', ((1332,497),(1360, 497) , (1346, 474)))
        #spade, 615
        pygame.draw.polygon(screen, 'white', ((1335, 723), (1357, 723), (1346, 697)))
        pygame.draw.circle(screen, 'white', (1332, 694), 14)
        pygame.draw.circle(screen, 'white', (1360, 694), 14)
        pygame.draw.polygon(screen, 'white', ((1322, 684), (1370, 684), (1346, 659)))
        pygame.draw.polygon(screen, 'white', ((1360, 694), (1332, 694), (1346, 660)))

        pygame.draw.rect(screen, 'white', (54,100,98,152),2)
    def foundation_locations(self):
        locs = []
        for i in range(4):
            locs.append(pygame.Rect(1300,15 + 200*i,98,152))
        return locs

    def tab_locations(self):
        #134.28 = equal dist?
        tab_x_y = []
        pile_xs = []
        for i in range(1,8):
            pile_xs.append(122+138*i)
        '''
        for i in range(20):
            for index,pile in enumerate(pile_xs):
                tab_x_y[index].append((pile,i*30))
        '''
        for index, pile in enumerate(pile_xs):
            curr_pile = []
            for i in range(20):
                curr_pile.append((pile, i*30))
            tab_x_y.append(curr_pile)
        return tab_x_y

    def card_location_update(self):
        for card in self.card_obj_list:
            if card in self.waste:

                card.x = self.waste_coordinate[0]
                card.y = self.waste_coordinate[1]
                card.hitbox[0] = self.waste_coordinate[0]
                card.hitbox[1] = self.waste_coordinate[1]
            elif card in self.hand:
                card.x = self.hand_coordinate[0]
                card.y = self.hand_coordinate[1]
                card.hitbox[0] = self.hand_coordinate[0]
                card.hitbox[1] = self.hand_coordinate[1]
            else:
                card_in_found = False
                for index,pile in enumerate(self.foundations):
                    if card in pile:

                        card.x = self.foundation_coordinates[index][0]
                        card.y = self.foundation_coordinates[index][1]
                        card.hitbox[0] = self.foundation_coordinates[index][0]
                        card.hitbox[1] = self.foundation_coordinates[index][1]
                        card_in_found = True
                if not card_in_found:
                    for i in range(len(self.tableau)):
                        for y in range(len(self.tableau[i])):
                            if card == self.tableau[i][y]:

                                card.x = self.tableau_coordinates[i][y][0]
                                card.y = self.tableau_coordinates[i][y][1]
                                card.hitbox[0] = self.tableau_coordinates[i][y][0]
                                card.hitbox[1] = self.tableau_coordinates[i][y][1]


    def hidden_update(self):
        for pile in self.tableau:
            if len(pile) > 0:
                pile[-1].hidden = False

    def card_helper(self, card):
        for i in range(len(self.tableau)):
            for y in range(len(self.tableau[i])):
                if self.tableau[i][y] == card:
                    card_loc = (i, y)
                    return card_loc
        return 'x'

    def tabpile_to_tabpile(self, card, pile):
        card_loc = self.card_helper(card)
        num, suit = card.tuple
        if self.tableau[pile]:
            pile_last_card = self.tableau[int(pile)][-1]
        else:
           pile_last_card = None
        valid_move = True
        if num == 'king':
            if len(self.tableau[pile]) > 0:
                return None
        else:
            if self.color_valid[suit] == self.color_valid[pile_last_card.tuple[1]]:
                return None
            if pile_last_card.tuple[0] == 'ace':
                return None
            if self.nums.index(pile_last_card.tuple[0]) != self.nums.index(num)+1:
                return None

        if card == self.tableau[card_loc[0]][-1]:
            self.tableau[int(pile)].append(card)
            self.tableau[card_loc[0]].remove(card)
            self.hidden_update()
            return 1
        else:
            moving_cards = self.tableau[card_loc[0]][card_loc[1]:]
            for card in moving_cards:
                self.tableau[card_loc[0]].remove(card)
            self.tableau[int(pile)] += moving_cards
            self.hidden_update()
            return 2




    def tabpile_to_foundation(self, card, foundation):
        # top to bottom: 0-heart, 1-diamond, 2-club, 3-spade
        card_tuple = card.tuple
        num, suit = card_tuple
        card_loc = self.card_helper(card)
        if card != self.tableau[card_loc[0]][-1]:
            return None
        if self.suits[int(foundation)] != suit:
            return None
        if len(self.foundations[int(foundation)]) == 0:
            if num != 'ace':
                return None
        elif len(self.foundations[int(foundation)]) == 13:
            return None
        else:
            if self.nums.index(self.foundations[int(foundation)][-1].tuple[0]) + 1 != self.nums.index(num):
                return None
        self.foundations[int(foundation)].append(card)
        self.tableau[card_loc[0]].remove(card)
        return 1

    def draw_from_hand(self):
        if len(self.hand) == 0:
            if len(self.waste) == 0:
                return None
            while len(self.waste) > 0:
                waste_card = self.waste.pop()
                self.hand.append(waste_card)
                waste_card.hidden = True
            return 2
        else:
            drawn_card = self.hand.pop()
            drawn_card.x = self.waste_coordinate[0]
            drawn_card.y = self.waste_coordinate[1]
            drawn_card.hidden = False
            self.waste.append(drawn_card)
            return 1

            #print(drawn_card)


    def king_open(self,card,pile):
        card = card.tuple
        card_loc = self.card_helper(card)
        num, suit = card
        if len(self.tableau[int(pile)]) != 0:
            return None
        if num != 'king':
            return None
        self.tableau[int(pile)].append(card)
        self.tableau[card_loc[0]].remove(card)
        return 1

    def hand_to_foundation(self, card, foundation):
        card_tuple = card.tuple
        num, suit = card_tuple
        if card_tuple != self.waste[-1].tuple:
            return None
        if self.suits[int(foundation)] != suit:
            return None
        if len(self.foundations[int(foundation)]) == 0:
            if num != 'ace':
                return None
        elif len(self.foundations[int(foundation)]) == 13:
            return None
        else:
            if self.nums.index(self.foundations[int(foundation)][-1].tuple[0]) + 1 != self.nums.index(num):
                return None
        self.foundations[int(foundation)].append(card)
        self.waste.remove(card)
        return 1

    def hand_to_tab(self, card, pile):
        if card.num == 'king':
            if len(self.tableau[pile]) > 0:
                return None
        else:
            if card != self.waste[-1]:
                return None
            if self.color_valid[self.tableau[pile][-1].suit] == self.color_valid[card.suit]:
                return None
            if self.tableau[pile][-1].num == 'ace':
                return None
            if self.nums.index(card.num)!= self.nums.index(self.tableau[pile][-1].num)-1:
                return None
        self.waste.remove(card)
        self.tableau[pile].append(card)
        return 1

    def win_check(self):
        count = 0
        for foundation in self.foundations:
            count += len(foundation)
        if count == 52:
            return True
        else:
            return False

    def reset_pos(self, card):
        card.x = card.initial_x
        card.y = card.initial_y

    def handle_mouse_down(self, event):
        if self.hand_state == self.HOVERED_OVER:
            self.hand_state = self.CLICKED
        if len(self.waste) > 0:
            if self.waste[-1].state == self.waste[-1].HOVERED_OVER:
                self.waste[-1].initial_x = self.waste[-1].x
                self.waste[-1].initial_y = self.waste[-1].y
                self.waste[-1].state = self.waste[-1].CLICKED
        if self.selected_tab != None:
            print(self.selected_tab.x, self.selected_tab.y)
            self.selected_tab.state = self.selected_tab.CLICKED
        if self.moving_cards != None:
            for card in self.moving_cards:
                card.state = card.CLICKED




        #if not card.hidden:
            #if card.box.collidepoint(event.pos):
                #card.state = card.CLICKED

    def handle_mouse_up(self, event):
        #card.state = card.IDLE
        if self.hand_state == self.CLICKED:
            self.hand_state = self.IDLE
            if self.draw_from_hand() == 2:
                for card in self.hand:
                    card.x = self.hand_coordinate[0]
                    card.y = self.hand_coordinate[1]
        if len(self.waste) > 0:
            tab_val = False
            found_val = False
            if self.waste[-1].state == self.waste[-1].CLICKED:
                self.waste[-1].state = self.waste[-1].IDLE
                for index, foundation in enumerate(self.foundation_coordinates):
                    if pygame.Rect(foundation).collidepoint(event.pos):
                        x = self.hand_to_foundation(self.waste[-1], index)
                        if x == 1:
                            self.foundations[index][-1].x = foundation[0]
                            self.foundations[index][-1].y = foundation[1]
                            found_val = True
                            break
                if found_val == False:
                    for index, pile in enumerate(self.tableau):
                        if self.waste[-1].num != 'king':
                            if pile:
                                if pygame.Rect(pile[-1].x, pile[-1].y, pile[-1].width, pile[-1].length).collidepoint(event.pos):
                                    card = self.waste[-1]
                                    y = self.hand_to_tab(card, index)
                                    if y == 1:
                                        col, row = self.card_helper(card)
                                        card.x, card.y = self.tableau_coordinates[col][row]
                                        tab_val = True
                                        break
                        else:
                            if pygame.Rect(self.tableau_coordinates[index][0][0], self.tableau_coordinates[index][0][1], self.waste[-1].width, self.waste[-1].length).collidepoint(
                                    event.pos):
                                card = self.waste[-1]
                                y = self.hand_to_tab(card, index)
                                if y == 1:
                                    col, row = self.card_helper(card)
                                    card.x, card.y = self.tableau_coordinates[col][row]
                                    tab_val = True
                                    break
                if tab_val == False and found_val == False:
                        self.reset_pos(self.waste[-1])
        if self.selected_tab != None:
            single_card_move = False
            if self.selected_tab.state == self.selected_tab.CLICKED:
                self.selected_tab.state = self.selected_tab.IDLE
                if self.selected_tab.num == 'king':
                    for index, pile in enumerate(self.tableau):
                        if not pile:
                            x = self.tabpile_to_tabpile(self.selected_tab, index)
                            if x == 1:
                                self.selected_tab.x, self.selected_tab.y = self.tableau_coordinates[index][0]
                                single_card_move = True
                                break
                for index, foundation in enumerate(self.foundation_coordinates):
                    if pygame.Rect(foundation).collidepoint(event.pos):
                        x = self.tabpile_to_foundation(self.selected_tab, index)
                        if x == 1:
                            self.foundations[index][-1].x = foundation[0]
                            self.foundations[index][-1].y = foundation[1]
                            single_card_move = True
                            break
                if single_card_move == False:
                    for index, pile in enumerate(self.tableau):
                        if pile:
                            if pygame.Rect(self.tableau[index][-1].x, self.tableau[index][-1].y, self.tableau[index][-1].width, self.tableau[index][-1].length).collidepoint(event.pos):
                                z = self.tabpile_to_tabpile(self.selected_tab, index)
                                if z == 1:
                                    col, row = self.card_helper(self.selected_tab)
                                    self.selected_tab.x, self.selected_tab.y = self.tableau_coordinates[col][row]
                                    single_card_move = True
                                    break
                                '''
                                elif z == 2:
                                    for card in self.moving_cards:
                                        col, row = self.card_helper(card)
                                        card.x, card.y = self.tableau_coordinates[col][row]
                                        
                                                                else:
                                    if self.moving_cards != None:
                                        for card in self.moving_cards:
                                            self.reset_pos(card)
                                        self.moving_cards = None
                                '''



                if single_card_move == False:
                    self.reset_pos(self.selected_tab)
            self.selected_tab = None

        if self.moving_cards != None:
            multi_card_move = False
            pile_check = True
            if self.moving_cards[0].state == self.moving_cards[0].CLICKED:
                for card in self.moving_cards:
                    card.state = card.IDLE
            if self.moving_cards[0].num == 'king':
                pile_check = False
            for index, pile in enumerate(self.tableau):
                if pile_check:
                    if pile:
                        if pygame.Rect(self.tableau[index][-1].x, self.tableau[index][-1].y,self.tableau[index][-1].width, self.tableau[index][-1].length).collidepoint(event.pos):
                            z = self.tabpile_to_tabpile(self.moving_cards[0], index)
                            if z == 2:
                                multi_card_move = True
                                for card in self.moving_cards:
                                    col, row = self.card_helper(card)
                                    card.x, card.y = self.tableau_coordinates[col][row]
                            else:
                                for card in self.moving_cards:
                                    self.reset_pos(card)
                else:
                    if pygame.Rect(self.tableau_coordinates[index][0][0], self.tableau_coordinates[index][0][1], self.moving_cards[0].width, self.moving_cards[0].length).collidepoint(event.pos):
                        z = self.tabpile_to_tabpile(self.moving_cards[0], index)
                        if z == 2:
                            multi_card_move = True

                            for card in self.moving_cards:
                                col, row = self.card_helper(card)
                                card.x, card.y = self.tableau_coordinates[col][row]
                        else:
                            for card in self.moving_cards:
                                self.reset_pos(card)
            self.moving_cards = None









    def handle_mouse_motion(self, event):
        if pygame.Rect(self.hand_coordinate).collidepoint(event.pos):
            if self.hand_state != self.CLICKED:
                self.hand_state = self.HOVERED_OVER
        else:
            self.hand_state = self.IDLE
        if len(self.waste) > 0:
            if pygame.Rect(self.waste[-1].hitbox).collidepoint(event.pos):

                if self.waste[-1].state != self.waste[-1].CLICKED:
                    self.waste[-1].state = self.waste[-1].HOVERED_OVER
            else:
                if self.waste[-1].state == self.waste[-1].CLICKED:
                    self.waste[-1].x = event.pos[0]
                    self.waste[-1].y = event.pos[1]
        if self.selected_tab != None:
            if self.selected_tab.state == self.selected_tab.CLICKED:
                self.selected_tab.x = event.pos[0]
                self.selected_tab.y = event.pos[1]
        else:
            iterate = True
            col = None
            place = None

            for i in range(len(self.tableau)):
                for y in range(len(self.tableau[i])):
                    tab_card = self.tableau[i][y]
                    if pygame.Rect(tab_card.hitbox).collidepoint(event.pos) and not tab_card.hidden:
                        col = i
                        place = y
                        iterate = False
                        break
                if iterate == False:
                    break
            if col != None:
                if tab_card == self.tableau[col][-1]:
                    if tab_card.state != tab_card.CLICKED:
                        tab_card.state = tab_card.HOVERED_OVER
                        self.selected_tab = tab_card
                    else:
                        tab_card.state = tab_card.IDLE
                    self.selected_tab.initial_x = self.selected_tab.x
                    self.selected_tab.initial_y = self.selected_tab.y
                else:
                    moving_cards = self.tableau[col][place:]

                    self.moving_cards = moving_cards
                    for card in self.moving_cards:
                        card.initial_x = card.x
                        card.initial_y = card.y

                    for index, card in enumerate(self.moving_cards):
                        if card.state != card.CLICKED:
                            card.state = card.HOVERED_OVER
                        else:
                            card.x = event.pos[0]
                            card.y = event.pos[1] + index*30


def console_main():
    screen = None
    s = Solitaire(screen)
    s.add_card_obj()
    running = True
    while running:
        print('hand')
        for i in range(len(s.hand)-1,-1,-1):
            print(s.hand[i],end="")
        print()
        print('waste')
        print(s.waste)
        print('tableau')
        for pile in s.tableau:
            print(pile)
            print()
        print('foundations')
        for pile,suit in zip(s.foundations, s.suits):
            print(suit,pile)
            print()
        c = input('card')
        p = input('pile')
        if c == 'a' and p == 'a':
            s.draw_from_hand()
        else:
            s.hand_to_foundation(c,p)
        c = None
        p = None

def graphics_main():
    WIDTH = 1450
    HEIGHT = 800
    FPS = 60
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill("dark green")
    clock = pygame.time.Clock()
    running = True

    buttons = []
    s = Solitaire(screen)
    s.add_card_obj()
    cards = s.card_obj_list
    s.card_location_update()
    while running:
        s.divisions(screen)
        s.hidden_update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for b in buttons:
                    b.handle_mouse_down(event)
                s.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                for b in buttons:
                    b.handle_mouse_up(event)
                s.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                for b in buttons:
                    b.handle_mouse_motion(event)
                s.handle_mouse_motion(event)
            elif event.type == pygame.KEYDOWN:
                for b in buttons:
                    b.handle_key_press(event)
        for pile in s.tableau:
            for card in pile:
                card.update()
                card.draw(screen)
                #pygame.draw.rect(screen, 'black', (card.hitbox),1)
        for card in s.hand:
            card.update()
            card.draw(screen)
        for card in s.waste:
            card.update()
            card.draw(screen)
        for pile in s.foundations:
            for card in pile:
                card.draw(screen)



        clock.tick(FPS)
        pygame.display.flip()
        pygame.draw.rect(screen, 'dark green', (0,0,1450, 800))

if __name__ == '__main__':
    graphics_main()
    #console_main()


