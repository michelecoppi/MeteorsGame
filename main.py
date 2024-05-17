import pygame
import sys
import random
import pickle

pygame.init()

# Crea la finestra del gioco
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Meteor Survival")

# Colori RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

personaggio_img = pygame.image.load("./sprites/player.png")

# Posizione iniziale del personaggio
x = 280
y = 560

width = 31
height = 31

# Velocità del personaggio
vel = 0.25

# Velocità di caduta dei meteoriti
meteor_speed = 0.10

# Lista di meteoriti
meteors = []

# Punteggio e best score
score = 0
best_score = 0

# Caricamento del best score da file
try:
    with open('best_score.txt', 'rb') as f:
        best_score = pickle.load(f)
except:
    pass

class Personaggio:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 31
        self.height = 31
        self.vel = 0.10
        self.image = personaggio_img # Immagine del personaggio

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
# Classe per i meteoriti
class Meteor:
    def __init__(self):
        self.x = random.randint(0, 580)
        self.y = -20
        self.width = 10
        self.height = 10
        self.speed = meteor_speed

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.width, self.height])  
        pygame.draw.rect(screen, RED, [self.x, self.y, self.width, self.height])   

# Funzione per gestire la collisione tra il personaggio e i meteoriti
def check_collision():
    global score, best_score, x, y, vel, meteor_speed

    for meteor in meteors:
        if y < meteor.y + meteor.height and y + height > meteor.y:
            if x < meteor.x + meteor.width and x + width > meteor.x:
                # Collisione avvenuta
                if score > best_score:
                    best_score = score
                
                meteors.clear()

                
                # Creazione della scritta Game Over
                font = pygame.font.Font(None, 64)
                game_over_text = font.render("Game Over", True, BLACK)
                game_over_rect = game_over_text.get_rect(center=(300, 200))

                # Creazione della scritta del punteggio
                font = pygame.font.Font(None, 32)
                score_text = font.render(f"Score: {score}", True, BLACK)
                score_rect = score_text.get_rect(center=(300, 300))

                # Creazione della scritta del best score
                font = pygame.font.Font(None, 32)
                best_score_text = font.render(f"Best Score: {best_score}", True, BLACK)
                best_score_rect = best_score_text.get_rect(center=(300, 350))

                # Creazione della scritta di restart
                font = pygame.font.Font(None, 32)
                restart_text = font.render("Press R to Restart", True, BLACK)
                restart_rect = restart_text.get_rect(center=(300, 400))

                # Disegna tutte le scritte sullo schermo
                screen.blit(game_over_text, game_over_rect)
                screen.blit(score_text, score_rect)
                screen.blit(best_score_text, best_score_rect)
                screen.blit(restart_text, restart_rect)
                score = 0
                pygame.display.update()

                # Attendere il tasto di restart
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            # Salvataggio del best score su file
                            with open('best_score.txt', 'wb') as f:
                                pickle.dump(best_score, f)
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            # Resetta la posizione del personaggio, la velocità dei meteoriti e il punteggio
                            x = 280
                            y = 560
                            vel = 0.25
                            meteor_speed = 0.10
                            meteors.clear()
                            return False


# Loop di gioco
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Salvataggio del best score su file
            with open('best_score.txt', 'wb') as f:
                pickle.dump(best_score, f)
            pygame.quit()
            sys.exit()

    # Genera un nuovo meteorite ogni volta che la lista è vuota
        if not meteors:
            print("Nessun meteorite, generazione di uno nuovo...")
            for i in range(1):
                meteors.append(Meteor())


    # Muove e disegna i meteoriti
    for meteor in meteors:
        meteor.update()
        meteor.draw()

    # Controlla se il personaggio collide con un meteorite
    if check_collision():
        continue

    # Aggiorna il punteggio e la velocità dei meteoriti
    score += 1
    meteor_speed += 0.00001

    # Controlla se i tasti WASD sono premuti
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if y > 0:
            y -= vel
        else:
            y = 600 - height
    if keys[pygame.K_a]:
        if x > 0:
            x -= vel
        else:
            x = 600 - width
    if keys[pygame.K_s]:
        if y < 600 - height:
            y += vel
        else:
            y = 0
    if keys[pygame.K_d]:
        if x < 600 - width:
            x += vel
        else:
            x = 0
    if random.randint(0, 50) == 0:
        meteors.append(Meteor())

    # Disegna lo sfondo bianco
    screen.fill(WHITE)
       # Disegna il personaggio
    personaggio = Personaggio(x, y)
    personaggio.draw()

    # Disegna i meteoriti
    for meteor in meteors:
        meteor.update()
        meteor.draw()

        # Controlla le collisioni con il personaggio
        if meteor.y >= y and meteor.y <= y + height and meteor.x >= x and meteor.x <= x + width:
            # Fine del gioco
            if score > best_score:
                best_score = score
            score = 0
            meteors.clear()
            x = 280
            y = 560
            vel = 0.25
            meteor = Meteor()
            meteors.append(meteor)
            break

    # Aggiorna lo schermo
    pygame.display.update()
  



