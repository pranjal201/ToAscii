import sys
import pygame as pg
import cv2

class ArtConverter:
    def __init__(self, path, font_size=12):
        pg.init() #pygame.init() initialize all imported pygame modules.
        self.path = path
        self.output = path[:-4]+'_converted'+path[-4:]
        self.image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)# Initialize a window or screen for display of size RES
        self.clock = pg.time.Clock()#create an object to help track time

        self.ASCII_CHARS = '.",:;!~+-xmo*#W&8@"'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.CHAR_STEP = int(font_size * 0.6)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False,'aquamarine3') for char in self.ASCII_CHARS]

    # This function gets an image 
    def get_image(self):
        self.cv2_image = cv2.imread(self.path)
        transposed_image = cv2.transpose(self.cv2_image)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2GRAY)
        return gray_image

    # This function draws the ascii image
    # this function map the charater to the pygame window with the coordinates
    def draw_converted_image(self):
        self.surface.fill('black')
        char_indices = self.image // self.ASCII_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x,y]
                if char_index:
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x,y))


        
    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface) # this method converts the pygame surface to 3D array
        cv2_image = cv2.transpose(pygame_image)
        cv2.imwrite(self.output, cv2_image)

    # This for the running of the loop
    def run(self):
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
            self.draw_converted_image()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Please Enter the File name:')
        print('------------ python3 ascii_art.py <input-file> <output-file>')
    else:
        try:
            app = ArtConverter(sys.argv[1])
            app.run()
        except IndexError:
            print('------------ python3 ascii_art.py <input-file> <output-file>')
            
