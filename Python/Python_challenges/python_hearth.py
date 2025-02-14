import pygame
import math
import random

pygame.init()

ANCHO_VENTANA = 800
ALTURA_VENTANA = 600
COLOR_FONDO = (0, 0, 0)
TAMANO_PARTICULA = 10
DURACION_PARTICULA = 5
NUM_PARTICULAS = 10000
COLOR_PARTICULAS = [(234, 128, 176)]

screen = pygame.display.set_mode((ANCHO_VENTANA, ALTURA_VENTANA))
pygame.display.set_caption("I Love You <3")

class Particle:
    def __init__(self):
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.age = 0
        self.color = (0, 0, 0)
        self.alive = False

    def initialize(self, x, y, dx, dy, color):
        self.position = [x, y]
        self.velocity = [dx, dy]
        self.acceleration = [dx * -0.1, dy * -0.1]
        self.age = 0
        self.color = color
        self.alive = True

    def update(self, delta_time):
        if not self.alive:
            return
        self.age += delta_time
        if self.age > DURACION_PARTICULA:
            self.alive = False
            return
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time
        self.velocity[0] += self.acceleration[0] * delta_time
        self.velocity[1] += self.acceleration[1] * delta_time

    def draw(self, surface):
        if not self.alive:
            return
        size = TAMANO_PARTICULA * (1 - self.age / DURACION_PARTICULA)
        alpha = int(255 * (1 - self.age / DURACION_PARTICULA))
        pygame.draw.circle(surface, self.color + (alpha,), (int(self.position[0]), int(self.position[1])), int(size))

class ParticlePool:
    def __init__(self, length):
        self.particles = [Particle() for _ in range(length)]
        self.first_free = 0

    def add(self, x, y, dx, dy, color):
        particle = self.particles[self.first_free]
        particle.initialize(x, y, dx, dy, color)
        self.first_free = (self.first_free + 1) % NUM_PARTICULAS

    def update(self, delta_time):
        for particle in self.particles:
            particle.update(delta_time)

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

def point_on_heart(t):
    x = 16 * math.sin(t)**3
    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
    return x, y

particles = ParticlePool(NUM_PARTICULAS)
particle_rate = NUM_PARTICULAS / DURACION_PARTICULA

running = True
clock = pygame.time.Clock()
time = None


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    new_time = pygame.time.get_ticks() / 1000
    delta_time = new_time - (time or new_time)
    time = new_time

    screen.fill(COLOR_FONDO)

    amount = particle_rate * delta_time
    for _ in range(int(amount)):
        t = math.pi * 2 * random.random()
        heart_pos = point_on_heart(t)
        pos_x = ANCHO_VENTANA / 2 + heart_pos[0] * 15
        pos_y = ALTURA_VENTANA / 2 - heart_pos[1] * 15
        dir_x = random.uniform(-1, 1)
        dir_y = random.uniform(-1, 1)
        length = math.sqrt(dir_x ** 2 + dir_y ** 2)
        dir_x /= length
        dir_y /= length
        particles.add(pos_x, pos_y, dir_x, dir_y, random.choice(COLOR_PARTICULAS))

    particles.update(delta_time)
    particles.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


