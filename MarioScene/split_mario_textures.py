import pygame
pygame.display.set_mode()
sprite_sheet = pygame.image.load('./textures/mario/mario_sprites.png').convert_alpha()
sprite_width = sprite_sheet.get_width()//14
sprite_height = sprite_sheet.get_height()//12
sprites_per_row = sprite_sheet.get_width() // sprite_width
sprites_per_col = sprite_sheet.get_height() // sprite_height
frames = []
count = 0
for row in range(sprites_per_col):
    for col in range(sprites_per_row):
        x = col * sprite_width
        y = row * sprite_height
        sprite = sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
        pygame.image.save(sprite,f"./textures/mario/{count}.png")
        count += 1