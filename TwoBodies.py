import pygame
import math 

pygame.init()
pygame.font.init() # надпись

def Calc_sec(x1_, y1_, x2_, y2_, v1x_, v1y_, v2x_, v2y_, sec_):
    dist_ = (x2_ - x1_)*(x2_ - x1_) + (y2_ - y1_)*(y2_ - y1_)
    a1x_ = g * ((x2_ - x1_) / math.sqrt(dist_)) / dist_ * m2 
    a1y_ = g * ((y2_ - y1_) / math.sqrt(dist_)) / dist_ * m2
    a2x_ = g * ((x1_ - x2_) / math.sqrt(dist_)) / dist_ * m1
    a2y_ = g * ((y1_ - y2_) / math.sqrt(dist_)) / dist_ * m1

    #a2x_, a2y_ = 0, 0

    v1x_ += a1x_ * sec_ 
    v1y_ += a1y_ * sec_ 
    v2x_ += a2x_ * sec_ 
    v2y_ += a2y_ * sec_

    K1_ = (v1x_ * v1x_ + v1y_ * v1y_) * m1 / 2
    K2_ = (v2x_ * v2x_ + v2y_ * v2y_) * m2 / 2
    U_ =  - g * m1 * m2 / math.sqrt(dist_)
    E_ = K1_ + K2_ + U_

    x1_ += v1x_ * sec_
    y1_ += v1y_ * sec_
    x2_ += v2x_ * sec_
    y2_ += v2y_ * sec_

    return math.fabs((E_ - E0)) / E0


def Calc_values(x1, y1, x2, y2, v1x, v1y, v2x, v2y):
    dist = (x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1)
    a1x = g * ((x2 - x1) / math.sqrt(dist)) / dist * m2 
    a1y = g * ((y2 - y1) / math.sqrt(dist)) / dist * m2
    a2x = g * ((x1 - x2) / math.sqrt(dist)) / dist * m1
    a2y = g * ((y1 - y2) / math.sqrt(dist)) / dist * m1

    #a2x, a2y = 0, 0

    v1x += a1x * sec
    v1y += a1y * sec
    v2x += a2x * sec
    v2y += a2y * sec

    K1 = (v1x * v1x + v1y * v1y) * m1 / 2
    K2 = (v2x * v2x + v2y * v2y) * m2 / 2
    U =  - g * m1 * m2 / math.sqrt(dist)
    E = K1 + K2 + U

    x1 += v1x * sec
    y1 += v1y * sec
    x2 += v2x * sec
    y2 += v2y * sec

    return x1, y1, x2, y2, v1x, v1y, v2x, v2y, K1, K2, U, E, dist

clock = pygame.time.Clock()


screen_width, screen_height = 1900, 1000

screen = pygame.display.set_mode((screen_width, screen_height)) #flags=pygame.NOFRAME
pygame.display.set_caption("Two Bodies")
icon = pygame.image.load('images/sansan.png')
pygame.display.set_icon(icon)

screen.fill('Black')

data_bg = pygame.Surface((200,500))
data_bg.fill('black')

my_font = pygame.font.SysFont('serif', 24)
 

r1 = 1
r2 = 1
sec = 2
g = 10
m1 = 40
m2 = 40
alpha = m2 / m1
K1,K2 = 1,1


text_coll = my_font.render('COLLISION', True, 'Red')
text_mm = my_font.render('m2 / m1 = ' + str(alpha), True, 'Red')
text_g = my_font.render('g = ' + str(g), True, 'Red')


x1_0, y1_0 = 800, 700
x2_0, y2_0 = 800, 400

x1, y1 = x1_0, y1_0
x2, y2 = x2_0, y2_0

v1x_0, v1y_0 = 1.0, 0.0
v2x_0, v2y_0 = -0.5, 0.0

v1x, v1y = v1x_0, v1y_0
v2x, v2y = v2x_0, v2y_0

dist_0 = (x2_0 - x1_0)*(x2_0 - x1_0) + (y2_0 - y1_0)*(y2_0 - y1_0)
dist = dist_0

U0 =  - g * m1 * m2 / math.sqrt(dist_0)
K0 = (m1 * (v1x_0 * v1x_0 + v1y_0 * v1y_0) + m2 * (v2x_0 * v2x_0 + v2y_0 * v2y_0)) / 2
E0 = U0 + K0

U, K, E = U0, K0, E0

x_CM = x1 + (x2 - x1) * m2 / (m1 + m2)
y_CM = y1 + (y2 - y1) * m2 / (m1 + m2)

Diff = Calc_sec(x1, y1, x2, y2, v1x, v1y, v2x, v2y, sec)

delta_E = 0

intersection = False
running = True
while running:

    #screen.fill('Black')
    pygame.draw.circle(screen, 'Blue', (x1, y1), r2)
    #pygame.draw.circle(screen, 'Black', (x2,y2), r1 + 2)
    pygame.draw.circle(screen, 'Yellow', (x2, y2), r1)
    #pygame.draw.circle(screen, 'Red', (x_CM, y_CM), 1)

    
    if (intersection == True):
        screen.blit(text_coll, (x_CM + 25, y_CM + 25))
        pygame.display.update()
        pygame.time.delay(3000)

        x1, y1 = x1_0, y1_0
        x2, y2 = x2_0, y2_0

        v1x, v1y = v1x_0, v1y_0
        v2x, v2y = v2x_0, v2y_0

        intersection = False
        screen.fill('Black')
    
    pygame.display.update()


    while ((Diff < 0.01) and (sec < 0.66)):
        sec *= 1.2
        print("<: sec", round(sec, 5)," Diff", round(Diff, 5))
        Diff = Calc_sec(x1, y1, x2, y2, v1x, v1y, v2x, v2y, sec)

    while ((Diff > 0.02) and (sec > 0.01)):
        sec /= 1.5
        print(">: sec", round(sec, 5)," Diff", round(Diff, 5))
        Diff = Calc_sec(x1, y1, x2, y2, v1x, v1y, v2x, v2y, sec)
    

    x1, y1, x2, y2, v1x, v1y, v2x, v2y, K1, K2, U, E, dist = Calc_values(x1, y1, x2, y2, v1x, v1y, v2x, v2y)

    if (v1x*v1x + v1y*v1y < 0.000000001):
        u1x = 0
        u1y = 0
    else:
        u1x = v1x / math.sqrt(v1x*v1x + v1y*v1y) * 25
        u1y = v1y / math.sqrt(v1x*v1x + v1y*v1y) * 25

    if (v2x*v2x + v2y*v2y < 0.000000001):
        u2x = 0
        u2y = 0
    else:
        u2x = v2x / math.sqrt(v2x*v2x + v2y*v2y) * 25
        u2y = v2y / math.sqrt(v2x*v2x + v2y*v2y) * 25
    

    x_CM = x1 + (x2 - x1) * m2 / (m1 + m2)
    y_CM = y1 + (y2 - y1) * m2 / (m1 + m2)

    if (y1 and y2) > screen_height: 
        y1 -= screen_height
        y2 -= screen_height
        screen.fill('Black')
    if (y1 and y2) < 0:
        y1 += screen_height
        y2 += screen_height
        screen.fill('Black')
    if (x1 and x2) > screen_width: 
        x1 -= screen_width
        x2 -= screen_width
        screen.fill('Black')
    if (x1 and x2) < 0:
        x1 += screen_width
        x2 += screen_width
        screen.fill('Black')



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print(delta_E)
            pygame.quit()
    

    if (dist <= (r1 + r2)*(r1 + r2)):
        intersection = True


    text_dist = my_font.render('dist = ' + str(round(math.sqrt(dist), 2)), True, 'Red')
    text_K1 = my_font.render('K1 = ' + str(round(K1, 5)), True, 'Red')
    text_K2 = my_font.render('K2 = ' + str(round(K2, 5)), True, 'Red')
    text_K = my_font.render('K = ' + str(round(K1 + K2, 5)), True, 'Red')
    text_U = my_font.render('U = ' + str(round(U, 5)), True, 'Red')
    text_E = my_font.render('E = ' + str(round(K1 + K2 + U, 5)), True, 'Red') 
    text_E0 = my_font.render('E0 = ' + str(round(K0 + U0, 5)), True, 'Red')
    text_sec = my_font.render('sec = ' + str(round(sec, 5)), True, 'Red')
    
    screen.blit(data_bg, (0, 0))
    screen.blit(text_g, (25, 150))
    screen.blit(text_mm, (25, 175))
    screen.blit(text_dist, (25, 205))
    screen.blit(text_K1, (25, 230))
    screen.blit(text_K2, (25, 255))
    screen.blit(text_K, (25, 280))
    screen.blit(text_U, (25, 305))
    screen.blit(text_E, (25, 335))
    screen.blit(text_E0, (25, 360))
    screen.blit(text_sec, (25, 385))

    pygame.draw.line(screen, 'Blue', [100, 100], [100 + u1x, 100 + u1y], 2)
    pygame.draw.line(screen, 'Yellow', [50, 100], [50 + u2x, 100 + u2y], 2)
    pygame.draw.circle(screen, 'Blue', (100, 100), 2)
    pygame.draw.circle(screen, 'Yellow', (50, 100), 2)

    if (math.fabs(E0 - (K1 + K2 + U))/E0 > delta_E):
        delta_E = math.fabs(E0 - (K1 + K2 + U))/E0

    clock.tick(100)

    


