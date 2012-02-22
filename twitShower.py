import pygame
import time
import glob
import os
from random import choice
import urllib

def mtime(filename):
  return os.stat(filename).st_mtime

def get_random_img(path, resolution):
  
  good_img = False

  while(not good_img):
    try:
      img = choice(get_files(path))

      image = pygame.image.load( img )
      image = pygame.transform.smoothscale( image, resolution)
      good_img = True
    except(KeyboardInterrupt):
      exit(0)
    except:
      pass

  text_content = img.replace(path, "")
  text_content = text_content[:text_content.find("/")]
  text_content = urllib.unquote_plus(text_content)

  return image, text_content

def get_files(path):
  biglist = []
  baselist = sorted(glob.glob(path+'*'), key=mtime, reverse=True)
  for path in baselist:
    for img_file in sorted(glob.glob(path+"/*"), key=mtime):
      biglist.append(img_file)
  return biglist

def main():
    
    pygame.init() 

    resolution = pygame.display.list_modes()[0]
    
    screen = pygame.display.set_mode( resolution, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.HWACCEL )

    background = pygame.Surface( screen.get_size() )

    background.fill( (0,0,0) )

    image, text_content = get_random_img('./images/', resolution)

    screen.blit( background, (0,0) )
    screen.blit( image, (0,0) )

    pygame.display.flip()

    colora = (0,0,0)
    colorb = (255,255,255)
    
    rounds = 0

    while 1:
        
        pygame.event.pump()
        keyinput = pygame.key.get_pressed()

        if keyinput[pygame.K_ESCAPE] or pygame.event.peek( pygame.QUIT ):
            break

        screen.blit( background, (0,0) )
        screen.blit( image, (0,0) )

        font = pygame.font.Font(None, 60)

        temp = colora
        colora = colorb
        colorb = temp

        text = font.render(text_content, 1, colora)
        screen.blit(text, (100,100))
        screen.blit(text, (110,110))
        screen.blit(text, (110,100))
        screen.blit(text, (100,110))

        text = font.render(text_content, 1, colorb)
        screen.blit(text, (105,105))

        pygame.display.flip()

        rounds += 1

        if rounds == 20:
          image, text_content = get_random_img('./images/',resolution)
          rounds = 0

        time.sleep(0.1)

if __name__ == '__main__': main()