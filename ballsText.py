from PIL import Image, ImageDraw, ImageFont
import numpy as np
def mktext(string, cx, cy, vrand = 0.1, vrot = 0, maxwidth = 12, maxheight = 5):
    '''Renders text string as a raster of balls.
    - cx, cy are the center of the text.
    - vrand and vrot are the random and rotational components of the balls' initial velocity
    - maxwidth and maxheight determine the size of the text raster
    
    Outputs a list of tuples, one tuple per ball. Each tuple contains 6 elements:
    - x: coordinate of ball center
    - y: coordinate of ball center
    - r: radius of ball
    - vx: x component of the ball's velocity
    - vy: y component of the ball's velocity
    - cs: color of the ball (range 0-1).
    '''
  
    #font = ImageFont.load_default()
    font = ImageFont.truetype('data/Artesania.otf', 8)
    bbox = font.getbbox(string)
    size = (bbox[2] - bbox[0], bbox[3] - bbox[1]) # width = right - left (2 - 0) and height = top - bottom (3 - 1)
    image = Image.new('1', size)
    draw = ImageDraw.Draw(image)
    draw.text((0,0), string,  font=font, fill=255)
    image = np.asarray(image)
    if not image[:,-1].any():
        image = image[:,:-1]
    if not image[0,:].any():
        image = image[1:,:]    
    psize = min(maxheight/image.shape[0], maxwidth/image.shape[1])
    twidth = psize*image.shape[1]
    theight = psize*image.shape[0]
    xs,ys = np.meshgrid(np.linspace(0,twidth,image.shape[1]),
                        np.linspace(theight,0,image.shape[0]))
    rs = np.full(xs.shape, psize/2*0.9)
    va = np.random.uniform(0, 2 * np.pi, size=xs.shape)
    c2xs = (xs-twidth/2)
    c2ys = (ys-theight/2)
    dists = (c2xs**2 + c2ys**2)**0.5
    angs = np.arctan2(c2ys, c2xs)
    vxs = vrand * np.cos(va) + vrot * dists * -np.sin(angs)
    vys = vrand * np.sin(va) + vrot * dists * +np.cos(angs)
    cs = ys/theight/2+0.25
    xs = xs - twidth/2 + cx
    ys = ys - theight/2 + cy
    return list(zip(xs[image], ys[image], rs[image], vxs[image], vys[image], cs[image]))