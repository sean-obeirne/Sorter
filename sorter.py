import pygame, sys, os, random, time, threading

# Color constants
WHITE = (255,255,255)
BLACK = (0,0,0)
DGRAY = (20,20,20)
LGRAY = (120,120,120)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
DRED = (100,20,20)

# Window property / layout constants
RES_WID = 1100
RES_HGT = 800
RESOLUTION = [RES_WID,RES_HGT]
TOP_BAR_HGT = 100

# Initialize game
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)

# Initialize font
pygame.font.init()
font = pygame.font.SysFont('monospace', 40)


####################
# Global Variables #
####################

running = True
sorting = False

arr_ct = 2
arr = list()

UI_x_offset = 0     # how far from left of screen UI begins
bar_x_offset = 38   # how far from left of screen bars are drawn
UI_x_cur = 25 + UI_x_offset # next UI component's x value
UI_components = list()




###########
# Classes #
###########

# An item of the UI to be interacted with
class Component:
    def __init__(self, x, y, text, wid=100, hgt=40, bcolor=LGRAY, tcolor=BLACK):
        self.x = x
        self.y = y
        self.text = text
        self.wid = wid
        self.hgt = hgt
        self.bcolor = bcolor
        self.tcolor = tcolor
        self.textsurface = font.render(self.text, True, self.tcolor)
        self.Component = pygame.draw.rect(screen, self.bcolor, (self.x, self.y, wid, hgt))

    def set_text(self, new):
        self.text = new
        self.textsurface = font.render(self.text, True, self.tcolor)

    def draw(self, surface):
        pygame.draw.rect(surface, self.bcolor, (self.x, self.y, self.wid, self.hgt))
        text_rect = self.textsurface.get_rect(center=(self.wid/2 + self.x, self.hgt/2 + self.y))
        surface.blit(self.textsurface,text_rect)

# A Bar is simple a white bar to be drawn in order to reflect some value in our list to be sorted
class Bar:
    def __init__(self, val, factor=20, bcolor=WHITE, tcolor=BLACK):
        self.val = val
        self.hgt = val * factor
        self.bcolor = bcolor
        self.tcolor = tcolor
        self.textsurface = font.render(str(self.val), True, self.tcolor)

    def draw(self, surface, x, y, wid):
        pygame.draw.rect(surface, self.bcolor, (x, y, wid, self.hgt))
        text_rect = self.textsurface.get_rect(center=(wid/2 + x, self.hgt/2 + y))
        # surface.blit(self.textsurface,text_rect)

# Randomize the order of bars so they may be sorted
def randomize_bars():
    global arr
    arr = sorted(arr, key = lambda x: random.random() )

# Initialize array of Bars
def init_bars():
    arr.clear()
    fact = 600 / arr_ct
    for i in range(1, arr_ct + 1):
        arr.append(Bar(i, factor=fact))
    randomize_bars()

# Intelligently draw bars within the confines of the screen
def draw_bars():
    global arr
    bwidth = int((1024 / arr_ct) - 1)
    x_cur = bar_x_offset
    for bar in arr:
        bar.draw(screen, x_cur, TOP_BAR_HGT, bwidth)
        x_cur += 1 + bwidth


####################
# Button Functions #
####################

# Divide the number of total Bars by 2
#   comp: the component to change the text of
def div2(comp):
    global arr_ct
    if not sorting and arr_ct > 2:
        arr_ct //= 2
        comp.set_text(str(arr_ct))
        init_bars()

# Multiply the number of total Bars by 2
#   comp: the component to change the text of
def mul2(comp):
    global arr_ct
    if not sorting and arr_ct < 512:
        arr_ct *= 2
        comp.set_text(str(arr_ct))
        init_bars()

# Cancel all sorting and reinitialize the Bars on screen
def reset():
    global sorting
    sorting = False
    init_bars()
    pass

# Quick Sort #
# recursive quicksort helper
def qsort():
    global arr
    
    if len(arr) <= 1:
        return arr

    pivot = random.randint(0, len(arr))
    lt = list()
    gt = list()
    for bar in arr:
        if bar.val <= pivot:
            lt.append(bar)
        if bar.val > pivot:
            gt.append(bar)

    return qsort(lt) + qsort(gt)


def quick_sort():
    global sorting
    global arr
    sorting = True

    qsort()

    sorting = False


# Heap Sort #
# Heapify the node at index i in heap of length n
#   i: the index of the root of this heap
#   n: the bound for how large the heap is
def heapify(i, n):
    global arr

    largest = i
    li = 2*i + 1
    ri = 2*i + 2

    # check if left exists and is bigger than root
    if li < n and arr[li].val > arr[largest].val:
        largest = li

    # check if right exists and is bigger than root
    if ri < n and arr[ri].val > arr[largest].val:
        largest = ri

    # swap if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        time.sleep(1/(arr_ct))
        heapify(largest, n)

# Build the max heap using heapify, then extract the root and heapify.
# Repeat to extract all values in order
def heap_sort():
    global sorting
    global arr
    sorting = True

    n = arr_ct

    # Build max heap
    for i in range(n//2 - 1, -1, -1):
        heapify(i, n)
        if not sorting:
            return

    # Extract top
    while n > 0:
        arr[n-1], arr[0] = arr[0], arr[n-1]
        heapify(0, n-1)
        n -= 1
        if not sorting:
            return

    sorting = False

# Merge Sort #
def merge_sort():
    global sorting
    global arr
    sorting = True

    sorting = False

# Bubble Sort #
# Loop through the list, swapping each entry which is larger than its successor
def bubble_sort():
    global sorting
    global arr
    sorting = True

    for bar in arr:
        for i in range(len(arr)-1):
            if not sorting:
                return
            if arr[i].val > arr[i+1].val:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                time.sleep(1/(arr_ct*2))

    sorting = False


#
# Initialize UI components
#
div2_comp = Component(UI_x_cur,30,'/2',wid=75)
UI_components.append(div2_comp)
UI_x_cur += 75

arr_ct_comp = Component(UI_x_cur,30,str(arr_ct),bcolor=BLACK, tcolor=WHITE)
UI_components.append(arr_ct_comp)
UI_x_cur += 100

mul2_comp = Component(UI_x_cur,30,'*2',wid=75)
UI_components.append(mul2_comp)
UI_x_cur += 100

reset_comp = Component(UI_x_cur,30,'reset',wid=125)
UI_components.append(reset_comp)
UI_x_cur += 150

bar_comp = Component(UI_x_cur,15,'',wid=2, hgt=70)
UI_components.append(bar_comp)
UI_x_cur += 27

quick_comp = Component(UI_x_cur,30,'quick',wid=125)
UI_components.append(quick_comp)
UI_x_cur += 150

heap_comp = Component(UI_x_cur,30,'heap',wid=100)
UI_components.append(heap_comp)
UI_x_cur += 125

merge_comp = Component(UI_x_cur,30,'merge',wid=125)
UI_components.append(merge_comp)
UI_x_cur += 150

bubble_comp = Component(UI_x_cur,30,'bubble',wid=150)
UI_components.append(bubble_comp)

init_bars()

#
# Main game loop
#
while(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            leftm, middlem, rightm = pygame.mouse.get_pressed()
            if leftm:
                mpos = pygame.mouse.get_pos()
                if div2_comp.Component.collidepoint(mpos):
                    div2(arr_ct_comp)
                elif mul2_comp.Component.collidepoint(mpos):
                    mul2(arr_ct_comp)
                elif reset_comp.Component.collidepoint(mpos):
                    reset()
                if not sorting:
                    if quick_comp.Component.collidepoint(mpos):
                        th = threading.Thread(target=quick_sort)
                        th.start()
                    elif heap_comp.Component.collidepoint(mpos):
                        th = threading.Thread(target=heap_sort)
                        th.start()
                    elif merge_comp.Component.collidepoint(mpos):
                        th = threading.Thread(target=merge_sort)
                        th.start()
                    elif bubble_comp.Component.collidepoint(mpos):
                        th = threading.Thread(target=bubble_sort)
                        th.start()
                break



    ## draw ##
    screen.fill(BLACK)
    pygame.draw.rect(screen, DGRAY, (0, 0, RES_WID, TOP_BAR_HGT)) # top bar
    for comp in UI_components:
        comp.draw(screen)
    draw_bars()
    pygame.display.flip()
pygame.quit()
