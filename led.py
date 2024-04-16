import time
import random  # Import random module for random number generation

# Define constants
POS_X = 0
NEG_X = 1
POS_Z = 2
NEG_Z = 3
POS_Y = 4
NEG_Y = 5

# Define other constants
TOTAL_EFFECTS = 8
RAIN_TIME = 0
SEND_VOXELS_TIME = 0 #140
GLOW_TIME = 0#8
TEXT_TIME = 0#300

# Define global variables
cube = [[0] * 8 for _ in range(8)]
current_effect = 0
timer = 10 #0
loading = True
sending = False  

char_position = -1
char_counter = 0

glow_count = 0
glowing = False


characters = {
    'H': [
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'E': [
        [1, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'L': [
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'O': [
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
}




# Utility functions
def clear_cube():
    global cube
    cube = [[0] * 8 for _ in range(8)]

def set_voxel(x, y, z):
    global cube
    cube[7 - y][7 - z] |= (0x01 << x)

def get_voxel(x, y, z):
    global cube
    return (cube[7 - y][7 - z] & (0x01 << x)) == (0x01 << x)

def shift(direction):
    if direction == POS_X:
        for y in range(8):
            for z in range(8):
                cube[y][z] = cube[y][z] << 1
    elif direction == NEG_X:
        for y in range(8):
            for z in range(8):
                cube[y][z] = cube[y][z] >> 1
    elif direction == POS_Y:
        for y in range(1, 8):
            for z in range(8):
                cube[y - 1][z] = cube[y][z]
        for i in range(8):
            cube[7][i] = 0
    elif direction == NEG_Y:
        for y in range(7, 0, -1):
            for z in range(8):
                cube[y][z] = cube[y - 1][z]
        for i in range(8):
            cube[0][i] = 0
    elif direction == POS_Z:
        for y in range(8):
            for z in range(1, 8):
                cube[y][z - 1] = cube[y][z]
        for i in range(8):
            cube[i][7] = 0
    elif direction == NEG_Z:
        for y in range(8):
            for z in range(7, 0, -1):
                cube[y][z] = cube[y][z - 1]
        for i in range(8):
            cube[i][0] = 0

# Effects functions
def rain():
    global timer, loading
    if loading:
        clear_cube()
        loading = False
        print("Rain_load_working")
    timer += 1
    print(timer)
    if timer > RAIN_TIME:
        timer = 0
        shift(NEG_Y)
        num_drops = random.randint(0, 5)
        print("Rain_shift_working")
        for _ in range(num_drops):
            set_voxel(random.randint(0, 7), 7, random.randint(0, 7))
        print("Rain effect")


def send_voxels():
    global loading, timer, sending, selX, selY, selZ, sendDirection
    if loading:
        clear_cube()
        for x in range(8):
            for z in range(8):
                set_voxel(x, random.randint(0, 1) * 7, z)
                print('loading SV')
        loading = False

    timer += 1
    if timer > SEND_VOXELS_TIME:
        timer = 0
        if not sending:
            selX = random.randint(0, 7)
            selZ = random.randint(0, 7)
            if get_voxel(selX, 0, selZ):
                selY = 0
                sendDirection = POS_Y
            elif get_voxel(selX, 7, selZ):
                selY = 7
                sendDirection = NEG_Y
            sending = True
        else:
            if sendDirection == POS_Y:
                selY += 1
                set_voxel(selX, selY, selZ)
                clear_voxel(selX, selY - 1, selZ)
                if selY == 7:
                    sending = False
            else:
                selY -= 1
                set_voxel(selX, selY, selZ)
                clear_voxel(selX, selY + 1, selZ)
                if selY == 0:
                    sending = False

def glow():
    global timer, loading, glow_count, glowing
    if loading:
        clear_cube()
        glow_count = 0
        glowing = True
        loading = False
        print("load glow")

    timer += 1
    if timer > GLOW_TIME:
        timer = 0
        if glowing:
            if glow_count < 448:
                while True:
                    sel_x = random.randint(0, 7)
                    sel_y = random.randint(0, 7)
                    sel_z = random.randint(0, 7)
                    if not get_voxel(sel_x, sel_y, sel_z):
                        break
                set_voxel(sel_x, sel_y, sel_z)
                glow_count += 1
            elif glow_count < 512:
                light_cube()
                glow_count += 1
            else:
                glowing = False
                glow_count = 0
        else:
            if glow_count < 448:
                while True:
                    sel_x = random.randint(0, 7)
                    sel_y = random.randint(0, 7)
                    sel_z = random.randint(0, 7)
                    if get_voxel(sel_x, sel_y, sel_z):
                        break
                clear_voxel(sel_x, sel_y, sel_z)
                glow_count += 1
            else:
                clear_cube()
                glowing = True
                glow_count = 0

def text(string):
    global timer, loading, char_position, char_counter
    if loading:
        clear_cube()
        char_position = -1
        char_counter = 0
        loading = False
        print('load text')
    timer += 1
    if timer > TEXT_TIME:
        timer = 0
        shift('NEG_Z')
        char_position += 1
        if char_position == 7:
            char_counter += 1
            if char_counter > len(string) - 1:
                char_counter = 0
            char_position = 0
        if char_position == 0:
            for i in range(8):
                cube[i][0] = characters[string[char_counter]][i]


# Main loop
def loop():
    global timer, loading, current_effect
    print("Current effect:", current_effect)
    command = input("Enter command (0 to 7) or 'q' to quit: ")
    if command == 'q':
        return False
    try:
        current_effect = int(command)
        loading = True
        timer = 0
    except ValueError:
        print("Invalid input! Please enter a number between 0 and 7.")
    return True

# Main loop
while True:
    if not loop():
        break
    if current_effect == 1:
        print("Rain Effect")
        rain()
    elif current_effect == 2:
        print("Send Voxels Effect")
        send_voxels() 
    elif current_effect == 3:
        print("Glow Effect")
        glow()
    elif current_effect == 4:
        print("Text Effect")
        text("HELLO")  # Assuming "HELLO" is the text you want to display

