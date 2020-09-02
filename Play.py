import pygame
import math
from List import pick


# Setup display
pygame.init()
WIDTH, HEIGHT = 1200, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman GUI")


# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 350
SPACE = [450, 450, 300, 40, True]
yes_no = [[400, 300, 100, 50, "yes"], [700, 300, 100, 50, "no"]]

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 80)

# button position assignment
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(65 + i), True])


# load images
images = []
for i in range(7):
    images.append(pygame.image.load("hangman" + str(i) + ".png"))


# game variables
hangman_status = 0
word = pick()
guessed = []


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (83, 86, 90)


# Setup game loop
FPS = 60
clock = pygame.time.Clock()


def draw():
    # Background color
    win.fill(GREY)

    # draw title
    text = TITLE_FONT.render("HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    # draw space button
    x, y, w, h, visible = SPACE
    if visible:
        rectangle = pygame.Rect(x, y, w, h)
        pygame.draw.rect(win, BLACK, rectangle, 3)
        text = LETTER_FONT.render("SPACE", 1, BLACK)
        win.blit(text, ((WIDTH - text.get_width()) // 2, 455))

    # draw images
    win.blit(images[hangman_status], (100, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(500)
    win.fill(GREY)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()//2, HEIGHT/2 - text.get_height()//2))
    text = WORD_FONT.render(word, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()//2, HEIGHT/2 - text.get_height()//2 + 100))
    pygame.display.update()
    pygame.time.delay(2000)


def again():
    win.fill(GREY)
    text = WORD_FONT.render("Do you want to play again?", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()//2, HEIGHT/2 - text.get_height()//2))
    for i in yes_no:
        x, y, w, h = i
        rectangle = pygame.Rect(x, y, w, h)
        pygame.draw.rect(win, BLACK, rectangle, 3)

    text = LETTER_FONT.render("YES", 1, BLACK)
    win.blit(text, (350, 310))
    text = LETTER_FONT.render("NO", 1, BLACK)
    win.blit(text, (550, 310))

    pygame.display.update()

    run2 = True
    while run2:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                run2 = False
                run3 = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for i in yes_no:
                    x, y, w, h, yn = i
                    if x < m_x < x + w and y < m_y < y + h:
                        if yn == "yes":
                            run = False
                            run2 = False
                        else:
                            run = False
                            run2 = False
                            run3 = False


run3 = True
while run3:

    run = True
    while run:
        clock.tick(FPS)

        draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                run3 = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1

                x, y, w, h, visible = SPACE
                if x < m_x < x + w and y < m_y < y + h and visible:
                    if " " not in word:
                        hangman_status += 1
                    guessed.append(" ")
                    SPACE[4] = False

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message("You WON!")
            again()

        if hangman_status == 7:
            display_message("You LOST!")
            again()


pygame.quit()
