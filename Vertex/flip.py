import pygame
import sys

def surfaceFlip(img,w,h, fx, fy):        
    r = img.get_rect()        
    target = pygame.Surface( r.size, 0, img )    
    tmp = pygame.Surface( (w,h), 0, img)        
    ix, iy = r.width/w, r.height/h
    dst = pygame.Rect(0,0,w,h)
    r.topleft = (0,0)
    r.size = (w,h)
    for y in range(0,iy):
        r.left = 0
        for x in range(0,ix):
            tmp.blit(img, dst,r)
            tmp = pygame.transform.flip(tmp,fx,fy)
            target.blit(tmp,r)
            tmp.fill( (0,0,0,0) )
            r.left += w
        r.top += h    
    return target
    
if __name__ == '__main__':
	if len(sys.argv) < 5:
		print "flip.py <file> <tile_w> <tile_h> <x|y>"
		exit()

	file = sys.argv[1]
	w, h = sys.argv[2], sys.argv[3]
	o = sys.argv[4]
	img = pygame.image.load(file)
	dst = None
    
	fx, fy = False, False
	if o=="x":
		fx, fy = True, False
	elif o=="y":
		fx, fy = False, True
	if fx or fy: 
		dst = surfaceFlip(img, int(w), int(h), fx, fy)
		if dst:
			pygame.image.save(dst,file+"_flipped"+o+".png")
	else:
		print "No orientation? x|y"

