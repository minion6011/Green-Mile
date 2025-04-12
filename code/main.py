from ursina import *
from player import CustomPlayer
from ds_rpc import DiscordRPC
import threading

window.vsync = True # Max fps supported (Set to false to remove the limit)

app = Ursina(title="Green Mile", development_mode=False, borderless=False, icon="assets/rpc/logo.ico")
window.size = (800,600)
window.fullscreen = False
window.position = (300,100)

window.color = color.rgb32(144, 183, 198)

camera.orthographic = True
camera.fov = 20


# - Map1 - Spawn
sky1_A = Entity(model="cube", scale=(40,20,2), origin_y=-.5,origin_z=-10, texture="assets/background.png")
sky2_A = Entity(model="cube", scale=(40,20,2), origin_y=-.5,origin_z=-10,origin_x=1, texture="assets/background.png")
sky3_A = Entity(model="cube", scale=(40,20,2), origin_y=-.5,origin_z=-10,origin_x=-1, texture="assets/background.png")

game_title = Entity(model='cube', color=color.white, origin_y=.5, y=12, scale=(8, 2), origin_z=-2, texture="assets/title.png")
ico_title = Entity(model='cube', color=color.white, origin_y=.5, y=11.2, scale=(2, 2), origin_z=-2, texture="assets/title_ico.png")

ground = Entity(model='cube', origin_y=.5, scale=(120, 5, 1), collider='box', texture="assets/ground1.png")

tree1_bush = Entity(model='cube', origin_y=-.085, origin_x=-.5, scale=(5,7), x=-58, y=2.85, origin_z=-2, texture="assets/tree1.png")
flower1_bush  = Entity(model='cube', origin_y=-.5, origin_x=-.5, origin_z=-2, scale=(1.5,1.5), x=-53, texture="assets/flowers.png")
flower2_bush = Entity(model='cube', origin_y=-.5, origin_x=-.5, scale=(1.4,1.4,-2), x=-41, texture="assets/yellow_flower.png")
tree2_bush = Entity(model='cube', origin_y=-.085, origin_x=-.5, scale=(10,12), x=-41.5, y=4.95, origin_z=-2, texture="assets/tree3.png")
flower3_bush = Entity(model='cube', origin_y=-.5, origin_x=-.5, scale=(1.5,1.5,-2), x=-32.2, texture="assets/purple_flower2.png")
flower4_bush = Entity(model='cube', origin_y=-.5, origin_x=-.5, scale=(1,1,-2), x=-30, texture="assets/white_flower.png")


bush = Entity(model='cube', origin_y=.5, origin_x=-.5, scale=(7.5,3.4,-2), x=-50.05, y=3.4, collider='box', texture="assets/bush.png")
bush_barrier = Entity(model='cube', origin_y=.5, origin_x=-.5, scale=(4.45,20,-2), x=-47, y=20, collider='box', color=color.hsv(0, 0, 1, 0))

house = Entity(model='cube', origin_y=-0.44, origin_x=3.5, origin_z=-2, scale=(7,9.5), texture="assets/house.png")


box_m = Entity(model='cube', origin_y=.5, origin_x=-.5, scale=(4,4), x=10, y=4, collider='box', texture="assets/box.png")
box_s = Entity(model='cube', origin_y=.5, origin_x=-2.5, scale=(2,2), x=10, y=2, collider='box', texture="assets/box.png")

ext_platform = Entity(model='cube', color=color.white, origin_y=.5, scale=(10, 1), y=4, collider='box', texture="assets/ext_platform.png")

tree_1 = Entity(model='cube', origin_y=-.085, origin_x=5, scale=(5,7), x=10, y=2.85, origin_z=-1, texture="assets/tree1.png")
tree_2 = Entity(model='cube', origin_y=-.085, origin_x=-3.5, scale=(5,7), x=10, y=2.85, origin_z=-1, texture="assets/tree1.png")


bench_1 = Entity(model='cube', origin_y=-.45, origin_x=-.5, origin_z=-2, x=32, scale=(4,1.5), texture="assets/bench1.png")
fountain = Entity(model='cube', origin_y=-.45, origin_x=-.5, origin_z=-2, x=37.5, scale=(4,4), texture="assets/fountain1.png")
bench_2 = Entity(model='cube', origin_y=-.45, origin_x=-.5, origin_z=-2, x=43, scale=(4,1.5), texture="assets/bench2.png")

tree_3 = Entity(model='cube', origin_y=-.45, origin_x=-6, origin_z=-1, scale=(8.5,10.5), texture="assets/tree2.png")

flower_1 = Entity(model='cube', origin_y=-.5, origin_x=-2.5, scale=(2,2,-2), texture="assets/red_flower.png")
flower_2 = Entity(model='cube', origin_y=-.5, origin_x=6.5, scale=(1.4,1.4,-2), texture="assets/yellow_flower.png")
flower_3 = Entity(model='cube', origin_y=-.5, origin_x=1, scale=(1.35,1.35,-2), y=4, texture="assets/orange_flower.png")

flower_4 = Entity(model='cube', origin_y=-.5, origin_x=-.5, scale=(1.4,1.4, -2), x=-4, texture="assets/purple_flower3.png")

flower_5 = Entity(model='cube', origin_y=-.5, origin_x=-16.5, scale=(1.2,1.2,-2), texture="assets/purple_flower.png")
flower_6 = Entity(model='cube', origin_y=-.5, origin_x=-.5, origin_z=-1, scale=(1.5,1.5), x=30, texture="assets/flowers.png")
flower_7 = Entity(model='cube', origin_y=-.5, origin_x=-.5, origin_z=-1, scale=(1.5,1.5), x=41.5, texture="assets/purple_flower2.png")


city_ico = Entity(model='cube', origin_y=.5, scale=(2, 2, -2), y=6.5, x=56.5, texture="assets/ico_city.png")

pigeon1 = Entity(model='cube', origin_y=-.5, origin_x=-.5, origin_z=-2, scale=(1.5,1), x=55.5, texture="assets/pigeon1.png")

# - Map2

sky1_B = Entity(model="cube", scale=(40,20,2), origin_y=-.5,origin_z=-10,origin_x=-2, texture="assets/background2.png")
sky2_B = Entity(model="cube", scale=(40,20,2), origin_y=-.5,origin_z=-10,origin_x=-3, texture="assets/background2.png")
sky3_B = Entity(model="cube", scale=(40,20,2), origin_y=-.5,origin_z=-10,origin_x=-4, texture="assets/background2.png")

ground2 = Entity(model='cube', origin_y=.5,x=110,scale=(100,5),y=0, texture="assets/ground2.png", collider="box")

apartments1 = Entity(model='cube', origin_y=.5,x=62.6, scale=(10,20), origin_z=-2, y=19.82, texture="assets/apartments1.png")

street_lamp1 = Entity(model='cube', origin_y=.5,x=69.5, scale=(4,5.5,-2), y=5.5, texture="assets/street_lamp.png")

cafe = Entity(model='cube', origin_y=.5,x=78, scale=(13.5,18), origin_z=-2, y=17.55, texture="assets/cafe.png")

cafe_bin = Entity(model='cube', origin_y=.5,x=84.4, scale=(1.6,2.4,-2), y=2.4, texture="assets/cafe_bin.png")

cafe_chair1 = Entity(model='cube', origin_y=.5,x=87.7, scale=(1.1,1.8,-3), y=1.8, texture="assets/chair1.png")
cat = Entity(model='cube', origin_y=.5,x=87.75, scale=(1,1,-2), y=1.8, texture="assets/cat.png")
cafe_chair2 = Entity(model='cube', origin_y=.5,x=92.3, scale=(1.1,1.8,-3), y=1.8, texture="assets/chair2.png")

cafe_table = Entity(model='cube', origin_y=.5,x=90, scale=(3.5,3,-2), y=3, texture="assets/table.png")

ad_void = Entity(model='cube', origin_y=.5,x=95, scale=(8.5,14.5,-3), y=14.5, texture="assets/ad_void.png")
ad = Entity(model='cube', origin_y=.5,x=95, scale=(8,3.95,-2), y=13.8, texture=random.choice(["assets/ad/ad_stonks.png", "ad_pokwok.png", "ad_pizzatime.png", "ad_pill.png"]))

street_lamp2 = Entity(model='cube', origin_y=.5,x=98.5, scale=(4,5.5,-2), y=5.5, texture="assets/street_lamp.png")

vending_machine = Entity(model='cube', origin_y=.5,x=102, scale=(2.5,4.5,-2), y=4.5, texture="assets/vending_machine.png")

apartments2 = Entity(model='cube', origin_y=.5,x=124.5, scale=(15.5,18), origin_z=-2, y=17, texture="assets/apartments2.png")

pigeon2 = Entity(model='cube', origin_y=-.5, origin_x=-.5, origin_z=-2, scale=(1.5,1.3), x=116.4, texture="assets/pigeon2.png")
trash_bin = Entity(model='cube', origin_y=.5,x=119, scale=(1.5,2,-2), y=2, texture="assets/bin_city.png")

liquor_shop = Entity(model='cube', origin_y=.5,x=108, scale=(13.5,18), origin_z=-2, y=17.5, texture="assets/liquor.png")

street_lamp3 = Entity(model='cube', origin_y=.5,x=132, scale=(4,5.5,-2), y=5.5, texture="assets/street_lamp.png")

# -- Trash barrier

b_trash_box = Entity(model='cube', origin_y=.5,x=138, scale=(3,2,1), y=2, texture="assets/trash_box.png", collider="box")
b_trash_shack = Entity(model='cube', origin_y=.5,x=142.5, scale=(7,7,2), y=7, texture="assets/trash_shack.png", collider="box")
b_trash_alcohol = Entity(model='cube', origin_y=.5,x=138, scale=(0.4,1.2,3), y=1.2, texture="assets/trash_alcohol.png", collider="box")
b_trash_alcohol = Entity(model='cube', origin_y=.5,x=138, scale=(0.4,1.2,3), y=1.2, texture="assets/trash_alcohol.png", collider="box")
b_trash_bag = Entity(model='cube', origin_y=.5,x=138.35, scale=(1.7,1.3), y=3.3, texture="assets/trash_bag.png", collider="box")
b_trash_antenna = Entity(model='cube', origin_y=.5,x=140.3, scale=(2,2,4), y=5.5, texture="assets/trash_satellite.png", collider="box")
b_trash_washer = Entity(model='cube', origin_y=.5,x=146.75, scale=(1.5,2), y=2, texture="assets/trash_washer.png", collider="box")
b_trash = Entity(model='cube', origin_y=.5,x=138, scale=(3,20,1), y=20, collider="box", color=color.hsv(0, 0, 1, 0))

# - Player
player = CustomPlayer(scale_y=2.3,scale_x=1, collider='box', texture="assets/player.png", color=color.white, sprint_speed=11.5)

player.x=0
player.y = raycast(player.world_position, player.down).world_point[1] + .01
camera.add_script(SmoothFollow(target=player, offset=[0,5,-30], speed=4))

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')

input_handler.bind('shift', 'sprint')

def animation_loop():
	# - Animation Timeouts
	an_fountain_timeout = 0.3
	# - Animations
	def fountain_animation():
		while True:
			fountain.texture = "assets/fountain1.png"
			time.sleep(an_fountain_timeout)
			fountain.texture = "assets/fountain2.png"
			time.sleep(an_fountain_timeout)
			fountain.texture = "assets/fountain3.png"
			time.sleep(an_fountain_timeout)
	# - Start Animation
	threading.Thread(target=fountain_animation, daemon=True, name="Fountain Animation").start()

def music_manager():
	audio_map = Audio() #Void Audio
	audio_map1 = False
	audio_map2 = False
	while True:
		time.sleep(0.1)
		if not player.x < -59.6 and player.x < 54.3 and audio_map1 == False: # Map 1
			audio_map1 = True
			audio_map2 = False
			audio_map.stop()
			audio_map = Audio("sounds/song1.mp3", loop=True, volume=0.08, auto_destroy=True)
		elif player.x > 54.3 and player.x < 136 and audio_map2 == False: #Map 2
			audio_map2 = True
			audio_map1 = False
			audio_map.stop()
			audio_map = Audio("sounds/song2.mp3", loop=True, volume=0.2)

animation_loop() #Animation Manager
threading.Thread(target=music_manager, daemon=True, name="Music Manager").start() #Background Manager

threading.Thread(target=DiscordRPC, daemon=True, name="Discord RPC").start() #Discord RPC

app.run()
