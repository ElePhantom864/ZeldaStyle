import time
import pygame as pg
import Zsettings as s
from Ztilemap import collide_hit_rect
from itertools import chain
vec = pg.math.Vector2


def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(
            sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(
            sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + \
                    sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = s.PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.facing = s.Direction.DOWN
        self.is_moving = False
        self.image = self.game.player_images[self.facing][1]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.hit_rect = s.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.animation = True
        self.vel = vec(0, 0)
        self.next_animation_tick = 0
        self.animation_phase = 0
        self.is_sword = False
        self.health = s.PLAYER_HEALTH
        self.damaged = False

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(s.DAMAGE_ALPHA * 2)

    def sword(self):
        self.is_sword = True
        if self.facing == s.Direction.DOWN:
            pos = vec(self.rect.centerx, self.rect.bottom - 10)
            rot = 90
            Sword(self.game, pos, rot, (self._layer + 1))
        if self.facing == s.Direction.UP:
            pos = vec(self.rect.centerx, self.rect.top + 10)
            rot = -90
            Sword(self.game, pos, rot, (self._layer - 1))
        if self.facing == s.Direction.RIGHT:
            pos = vec(self.rect.right - 10, self.rect.centery)
            rot = 180
            Sword(self.game, pos, rot, (self._layer - 1))
        if self.facing == s.Direction.LEFT:
            pos = vec(self.rect.left + 10, self.rect.centery)
            rot = 0
            Sword(self.game, pos, rot, (self._layer - 1))

    def animate_movement(self):
        if pg.time.get_ticks() < self.next_animation_tick:
            return
        if self.is_moving:
            self.image = self.game.player_images[self.facing][self.animation_phase]
            self.animation_phase += 1
            if self.animation_phase == 1:
                self.animation_phase = 2
            if self.animation_phase > 2:
                self.animation_phase = 0
            self.next_animation_tick = pg.time.get_ticks() + 150
        else:
            self.image = self.game.player_images[self.facing][1]

    def handle_event(self, event: pg.event.Event):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -s.PLAYER_SPEED
            self.facing = s.Direction.LEFT
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = s.PLAYER_SPEED
            self.facing = s.Direction.RIGHT
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -s.PLAYER_SPEED
            self.facing = s.Direction.UP
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = s.PLAYER_SPEED
            self.facing = s.Direction.DOWN

        if event.type in [pg.KEYDOWN, pg.KEYUP]:
            if event.type in [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_UP, pg.K_LEFT, pg.K_DOWN, pg.K_RIGHT]:
                self.is_moving = True
            else:
                self.is_moving = False
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                self.facing = s.Direction.LEFT
                if event.type == pg.KEYDOWN:
                    self.vel.x = -s.PLAYER_SPEED

            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                self.facing = s.Direction.RIGHT
                if event.type == pg.KEYDOWN:
                    self.vel.x = s.PLAYER_SPEED

            if event.key == pg.K_UP or event.key == pg.K_w:
                self.facing = s.Direction.UP
                if event.type == pg.KEYDOWN:
                    self.vel.y = -s.PLAYER_SPEED

            if event.key == pg.K_DOWN or event.key == pg.K_s:
                self.facing = s.Direction.DOWN
                if event.type == pg.KEYDOWN:
                    self.vel.y = s.PLAYER_SPEED

            if event.key == pg.K_SPACE and not self.is_sword:
                self.sword()

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.facing = s.Direction.LEFT
            self.is_moving = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.is_moving = True
            self.facing = s.Direction.RIGHT
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.is_moving = True
            self.facing = s.Direction.UP
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.is_moving = True
            self.facing = s.Direction.DOWN

        if self.damaged:
            try:
                opacity = next(self.damage_alpha)
                new_image = self.game.player_images[self.facing][self.animation_phase].copy()
                new_image.fill((255, 0, 0, opacity),
                               special_flags=pg.BLEND_RGBA_MULT)
                self.image = new_image
            except StopIteration:
                self.damaged = False
                self.image = self.game.player_images[self.facing][self.animation_phase]

        if not self.is_sword and not self.damaged:
            self.animate_movement()
            self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Teleport(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, playerDestination, playerLocation):
        self.groups = game.teleports
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.destination = playerDestination
        self.location = playerLocation


class Sword(pg.sprite.Sprite):
    def __init__(self, game, pos, rot, layer):
        self._layer = layer
        self.groups = game.all_sprites, game.sword
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.sword_img
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.rot = rot
        self.angle = -5

    def update(self):
        self.angle += 15
        self.image = pg.transform.rotate(self.game.sword_img, self.rot - self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        if self.angle >= 180:
            self.kill()
            self.game.player.is_sword = False
        hits = pg.sprite.spritecollide(self.sword, self.enemies, False)
        for hit in hits:
            print('hit')


class TextBox(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, texts):
        self.groups = game.interactables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.texts = texts


class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, image, routes):
        self._layer = -2
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.facing = s.Direction.DOWN
        self.image = self.game.cobra_images[self.facing][1]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.rect.center = self.pos
        self.next_animation_tick = 0
        self.animation_phase = 0
        self.routes = routes + [vec(x, y)]
        self.vel = vec(0, 0)
        self.target = 0

    def animate_movement(self):
        if pg.time.get_ticks() < self.next_animation_tick:
            return
        self.image = self.game.cobra_images[self.facing][self.animation_phase]
        self.animation_phase += 1
        if self.animation_phase > 1:
            self.animation_phase = 0
        self.next_animation_tick = pg.time.get_ticks() + 150

    def update(self):
        target_dist = vec(self.routes[self.target].x, self.routes[self.target].y) - self.pos
        if target_dist.length_squared() > 5**2:
            if self.pos.x < self.routes[self.target].x:
                self.vel.x = s.COBRA_SPEED
                self.facing = s.Direction.RIGHT
            elif self.pos.x > self.routes[self.target].x:
                self.vel.x = -s.COBRA_SPEED
                self.facing = s.Direction.LEFT
            if self.pos.y < self.routes[self.target].y:
                self.vel.y = s.COBRA_SPEED
                self.facing = s.Direction.DOWN
                if -2 < self.pos.y - self.routes[self.target].y < 2:
                    self.pos.y = self.routes[self.target].y
            elif self.pos.y > self.routes[self.target].y:
                self.vel.y = -s.COBRA_SPEED
                self.facing = s.Direction.UP
                if -2 < self.pos.y - self.routes[self.target].y < 2:
                    self.pos.y = self.routes[self.target].y
            if self.vel.y != 0 and self.vel.x != 0:
                self.vel *= 0.7071
        else:
            self.target += 1
            if self.target == len(self.routes):
                self.target = 0
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        self.animate_movement()
