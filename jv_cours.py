import pygame
import random

pygame.init()
pygame.mixer.init()


# fenêtre
w = 1280
h = 800
screen = pygame.display.set_mode((w, h))

#horloge
clock = pygame.time.Clock()
FPS = 60

deltaTime = 1/FPS

# variable joueur

class Joueur:
    def __init__(self, x_player, y_player, r_player):
        self.x = x_player
        self.y = y_player
        self.r = r_player
        self.vitesse = 4
        self.pv = 5
        self.cooldown = False
        self.cooldown_timer = 0

    def est_mort(self):
        return self.pv <=0

    def dessiner(self, screen):
        color = "cyan"
        if(self.cooldown):
            color = "grey"
            color = "pink"
        pygame.draw.circle(screen, color, (self.x, self.y), self.r)

    def afficher_pv(self, screen):
        font = pygame.font.Font(None, 25)
        text = font.render(f"PV : {self.pv}", True, "white")
        screen.blit(text, (5, 5))

    def est_touche(self):
        if(not self.cooldown):
            self.cooldown = True
            self.pv -= 1
            self.cooldown_timer = 1


    def etat_cooldown(self, deltaTime):
        if self.cooldown:
            self.cooldown_timer -= deltaTime
            if self.cooldown_timer <= 0:
                self.cooldown = False

    def deplacer(self, cadre):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.x > cadre.x + self.r + cadre.b:
                self.x -= self.vitesse

        if keys[pygame.K_RIGHT]:
            if self.x < cadre.x + cadre.w - self.r - cadre.b:
                self.x += self.vitesse

        if keys[pygame.K_UP]:
            if self.y > cadre.y + self.r + cadre.b:
                self.y -= self.vitesse

        if keys[pygame.K_DOWN]:
            if self.y < cadre.y + cadre.h - self.r - cadre.b:
                self.y += self.vitesse

player = Joueur(w//2, h//2, 15)

# variables du cadre
class Cadre:
    def __init__(self, w_cadre, h_cadre, x_cadre, y_cadre, b_cadre):
        self.w = w_cadre
        self.h = h_cadre
        self.x = x_cadre
        self.y = y_cadre
        self.b = b_cadre
    


    def dessiner(self, screen):
        pygame.draw.rect(screen, "white", (self.x, self.y, self.w, self.h), self.b)
    

w_cadre = 800
h_cadre = 400

cadre = Cadre(w_cadre, h_cadre, w//2 - w_cadre//2, h//2 - h_cadre//2, 2)


class Projectile:
    def __init__(self, x, y, r, dir_x, dir_y, vitesse):
        self.x = x
        self.y = y
        self.r = r
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.vitesse = vitesse
        self.actif = True

    def dessiner(self, screen):
        pygame.draw.circle(screen, "white", (self.x, self.y), self.r)

    def deplacer(self):
        self.x += self.dir_x * self.vitesse
        self.y += self.dir_y * self.vitesse

    def collision(self, player):
        if(abs(self.x - player.x) < self.r + player.r):
            if(abs(self.y - player.y) < self.r + player.r):
                player.est_touche()



    def est_hors_ecran(self):
        
        # s'il va à droite
        if(self.dir_x > 0):
            if(self.dir_x > w):
                self.actif = False

        # s'il va à gauche
        if(self.dir_x < 0):
            if(self.x < 0):
                self.actif = False

        # s'il va en bas
        if(self.dir_y > 0):
            if(self.y > h):
                self.actif = False

        # s'il va en haut
        if(self.dir_y < 0):
            if(self.y < 0):
                self.actif = False
        #print(self.actif)



class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def dessiner(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def est_clique(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False



            
pygame.mixer.music.load("Megalovania.mp3")
pygame.mixer.music.play()

# PROJECTILES

projectiles = []
projectile_timer = 0


phase = 0

game_over = False
running = True
timer_phase = 10
pause_timer = 3


etat = "menu"    

bouton_start = Button(w//2 - 100, h//2 - 60, 200, 50, "START", "white", "black")
bouton_quitter = Button(w//2 - 100, h//2 + 20, 200, 50, "QUITTER", "white", "black")


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

         if etat == "menu":
                if bouton_start.is_clicked(e):
                    etat = "jeu"
                if bouton_quitter.is_clicked(e):
                    running = False


    screen.fill("black")


    if(etat == "menu"):
        bouton_start.draw(screen)
        bouton_quitter.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)
        continue
    

    if(timer_phase <= 0):
        phase += 1
        timer_phase = 10
        projectiles = []
        pause_timer = 3

    if(phase == 3):
        font = pygame.font.Font(None, 50)
        text = font.render ("VICTOIRE", True, "white")
        screen.blit(text, (w/2 - 80, h/2 - 30))

        pygame.display.flip()
        clock.tick(FPS)
        continue

    if(game_over):
        font = pygame.font.Font(None, 50)
        text = font.render("GAME OVER", True, "white")
        screen.blit(text, (w/2 - 100, h/2 - 30))

        pygame.display.flip()
        clock.tick(FPS)
        continue



    if(pause_timer > 0):
        pause_timer -= deltaTime

       
        player.deplacer(cadre)
        player.etat_cooldown(deltaTime)

        font = pygame.font.Font(None, 30)
        text = font.render(f"PHASE {phase + 1}", True, "white")
        screen.blit(text, (cadre.x + cadre.w/2 - text.get_width()/2, cadre.y - 30))

        cadre.dessiner(screen)
        player.dessiner(screen)
        player.afficher_pv(screen)

        pygame.display.flip()
        clock.tick(FPS)
        continue


    if (projectile_timer <= 0):
        if(phase ==0):
            x_projectile = random.randint(cadre.x, cadre.x + cadre.w)
            projectiles.append(Projectile(x_projectile, 0, 10, 0, 1, 2))

            projectile_timer = 0.2

            
        elif(phase == 1):
            y_projectile = random.randint(cadre.y, cadre.y + cadre.h)
            projectiles.append(Projectile(0, y_projectile, 10, 1, 0, 5))
            y_projectile = random.randint(cadre.y, cadre.y + cadre.h)
            projectiles.append(Projectile(w, y_projectile, 10, -1, 0, 5))
            projectile_timer = 0.4

            
        elif(phase == 2):
            x_projectile = random.randint(cadre.x, cadre.x + cadre.w)
            projectiles.append(Projectile(x_projectile, h, 10, 0, -1, 4))
            projectile_timer = 0.2

            
    else :
        projectile_timer -= deltaTime
        projectile_timer -= deltaTime 


    # DEPLACEMENTS 
    
    player.deplacer(cadre)
    player.etat_cooldown(deltaTime)


    
    

    projectiles_actifs = []
    for i in range(len(projectiles)):
        projectiles[i].deplacer()
        projectiles[i].collision(player)
        projectiles[i].dessiner(screen)
        projectiles[i].est_hors_ecran()
        
        if(projectiles[i].actif):
            projectiles_actifs.append(projectiles[i])

    projectiles = projectiles_actifs

    

    # AFFICHAGE
    
    cadre.dessiner(screen)
    player.dessiner(screen)
    player.afficher_pv(screen)
    
    
    
    
  
    timer_phase -= deltaTime

    if(player.est_mort()):
        game_over = True

    pygame.display.flip()
    
    clock.tick(FPS)

pygame.quit()
