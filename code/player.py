from ursina import *
import threading

global time_walk_an, frame_walk_an
time_walk_an = None
frame_walk_an = 0



class CustomPlayer(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        # - Stamina
        global stamina_status, stamina_timeout, stamina_bar_entity
        from stamina_bar import StaminaBar
        stamina_timeout = None
        stamina_status = False
        stamina_bar_entity = StaminaBar(bar_color=color.hex("#fdc500"), roundness=0, max_value=100, value=50, scale=(.30,.055), origin=(-.5,15.5),)
        

        def sprint_check():
            while True:
                global stamina_timeout, stamina_status
                time.sleep(0.1)
                if stamina_status == True:
                    if stamina_timeout == None: stamina_timeout = time.time()
                    if time.time() - stamina_timeout > 0.4:
                        if not stamina_bar_entity.value == 0:
                            self.walk_speed = self.sprint_speed
                            if self.walking:
                                stamina_bar_entity.value -= 1
                        else: 
                            self.walk_speed = 8
                            stamina_status = False
                            stamina_bar_entity.status = "OFF"
                            stamina_bar_entity.text_entity.text = f'{stamina_bar_entity._value} / {stamina_bar_entity.max_value} Stamina - OFF'
                            stamina_timeout = None
                elif stamina_status == False and stamina_bar_entity.value <= 100:
                    self.walk_speed = 8
                    if stamina_timeout == None: stamina_timeout = time.time()
                    if time.time() - stamina_timeout > 10:
                        if not stamina_bar_entity.value == 100: stamina_bar_entity.value += 1
        
        threading.Thread(target=sprint_check, daemon=True, name="Sprint Check").start()
        # - Player
        self.model = 'cube'
        self.origin_y = -.5
        self.scale_y = 2
        self.color = color.orange
        self.collider = 'box'
    
        self.animator = Animator({'idle' : None, 'walk' : None, 'jump' : None})
        # self.animation_state_machine.state = 'jump'
        # self.idle_animation = None
        # self.walk_animation = None
        # self.jump_animation = None
        # self.idle_animation = Entity(parent=self, model='cube', color=color.gray, origin_y=-.5, scale_z=2)
        # self.walk_animation = Animation(parent=self, texture='ursina_wink', color=color.red, origin_y=-.5, scale=(2,2), double_sided=True)
        # self.model = None

        self.walk_speed = 8
        self.walking = False
        self.velocity = 0 # the walk direction is stored here. -1 for left and 1 for right.
        self.jump_height = 4
        self.jump_duration = .4
        self.jumping = False
        self.max_jumps = 1
        self.jumps_left = self.max_jumps
        self.gravity = 1
        self.grounded = True
        self.air_time = 0   # this increase while we're falling and used when calculating the distance we fall so we fall faster and faster instead of linearly.
        self.traverse_target = scene     # by default, it will collide with everything except itself. you can change this to change the boxcast traverse target.
        self.ignore_list = [self, ]
        self._start_fall_sequence = None # we need to store this so we can interrupt the fall call if we try to double jump.

        ray = raycast(self.world_position, self.down, distance=10, ignore=(self, ), traverse_target=self.traverse_target)
        if ray.hit:
            self.y = ray.world_point[1] + .01
        # camera.add_script(SmoothFollow(target=self, offset=[0,1,-30], speed=4))

        for key, value in kwargs.items():
            setattr(self, key, value)

        # delay_gravity one frame
        target_gravity = self.gravity
        self.gravity = 0
        invoke(setattr, self, 'gravity', target_gravity, delay=1/60)
        self._original_scale_x = self.scale_x

        Entity(model='cube', scale=.1, parent=self, color=color.hsv(0, 0, 1, 0), x=.5, y=.5)
        self.min_x = -99999
        self.max_x = 99999

    # @every(1/30)
    # def fixed_update(self):
        # # if boxcast(self.world_position, direction=self.right, distance=self.scale_x/2)
        # hit_info = raycast(self.world_position+Vec3(0,self.scale_y/2,0), direction=self.right, distance=5, traverse_target=self.traverse_target, ignore=self.ignore_list, debug=True)
        # # hit_info_head = raycast(self.world_position+Vec3(0,self.scale_y*.99,0), direction=self.right, distance=abs(self.scale_x/2)+(self.walk_speed/20), traverse_target=self.traverse_target, ignore=self.ignore_list)
        # # if not self.grounded:
        # #     hit_info_feet = raycast(self.world_position+Vec3(0,.01,0), direction=self.right, distance=abs(self.scale_x/2)+(self.walk_speed/20), traverse_target=self.traverse_target, ignore=self.ignore_list)
        # # else:
        # #     from ursina.hit_info import HitInfo
        # #     hit_info_feet = HitInfo(hit=False)
        # # hit_infos = (hit_info, hit_info_head, hit_info_feet)
        # hit_infos = (hit_info, )
        # #
        # self.min_x = -99999
        # self.max_x = 99999
        # if any(hit_infos):
        #     if self.velocity < 0:
        #         self.min_x = max([hinf.world_point.x for hinf in hit_infos if hinf.hit])
        #     else:
        #         self.max_x = min([hinf.world_point.x for hinf in hit_infos if hinf.hit])

    
    def update(self):
        if not boxcast(
            self.position+Vec3(self.velocity * time.dt * self.walk_speed,self.scale_y/2,0),
            # self.position+Vec3(sefl,self.scale_y/2,0),
            direction=Vec3(self.velocity,0,0),
            distance=abs(self.scale_x/2),
            ignore=self.ignore_list,
            traverse_target=self.traverse_target,
            thickness=(self.scale_x*.99, self.scale_y*.9),
            ).hit:

            self.x += self.velocity * time.dt * self.walk_speed

        # self.x += self.velocity * time.dt * self.walk_speed
        # self.x = clamp(self.x, self.min_x-.5, self.max_x+.5)

        self.walking = held_keys['a'] + held_keys['d'] > 0 and self.grounded

        # animations
        global time_walk_an, frame_walk_an
        if not self.grounded:
            self.animator.state = 'jump'
            self.texture = "assets/player.png"
        else:
            if self.walking:
                self.animator.state = 'walk'
                # logica animazione
                if time_walk_an == None or time.time() - time_walk_an > 0.15:
                    if frame_walk_an == 0:
                        frame_walk_an = 1
                        self.texture = "assets/player-walk.png"
                    else:
                        frame_walk_an = 0
                        self.texture = "assets/player.png"
                    time_walk_an = time.time()
            else:
                self.animator.state = 'idle'
                self.texture = "assets/player.png" # animazione idle


        # check if we're on the ground or not.
        ray = raycast(self.world_position+Vec3(0,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
        left_ray = raycast(self.world_position+Vec3(-self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)
        right_ray = raycast(self.world_position+Vec3(self.scale_x*.49,.1,0), self.down, distance=max(.15, self.air_time * self.gravity), ignore=self.ignore_list, traverse_target=self.traverse_target)

        # print(self.grounded)
        if any((ray.hit, left_ray.hit, right_ray.hit)):
            if not self.grounded:
                self.land()

            self.y = max((r.world_point.y for r in (ray, left_ray, right_ray) if r.hit))
            self.grounded = True
            return
        else:
            self.grounded = False

        # if not on ground and not on way up in jump, fall
        if not self.grounded and not self.jumping:
            # print(self.air_time)
            self.y -= min(self.air_time * self.gravity, ray.distance-.1)
            self.air_time += time.dt*4 * self.gravity   # fall faster and faster the long we've stayed in the air


        # if in jump and hit the ceiling, fall
        if self.jumping:
            # if boxcast(self.position+(0,.2,0), self.up, distance=self.scale_y, thickness=.95, ignore=self.ignore_list, traverse_target=self.traverse_target).hit:
            hit_above = raycast(self.world_position+Vec3(0,self.scale_y/2,0), self.up, distance=self.jump_height-(self.scale_y/2), traverse_target=self.traverse_target, ignore=self.ignore_list)
            hit_above_left = raycast(self.world_position+Vec3(-self.scale_x*.49,self.scale_y/2,0), self.up, distance=self.jump_height-(self.scale_y/2), traverse_target=self.traverse_target, ignore=self.ignore_list)
            hit_above_right = raycast(self.world_position+Vec3(self.scale_x*.49,self.scale_y/2,0), self.up, distance=self.jump_height-(self.scale_y/2), traverse_target=self.traverse_target, ignore=self.ignore_list)
            if any((hit_above.hit, hit_above_left.hit, hit_above_right.hit)):
                target_y = min(min((r.world_point.y for r in (hit_above, hit_above_left, hit_above_right) if r.hit)), self.y)
                if hasattr(self, 'y_animator'):
                    self.y_animator.kill()
                self.air_time = 0
                self.start_fall()



    def input(self, key):
        # - Sprint
        if key == "sprint":
            global stamina_status, stamina_timeout, stamina_bar_entity
            if stamina_status == False:
                
                if stamina_bar_entity.value > 0:
                    stamina_status = True
                    stamina_bar_entity.status = "ON"
                    stamina_bar_entity.text_entity.text = f'{stamina_bar_entity._value} / {stamina_bar_entity.max_value} Stamina - ON'

            elif stamina_status == True:
                stamina_status = False
                stamina_bar_entity.status = "OFF"
                stamina_bar_entity.text_entity.text = f'{stamina_bar_entity._value} / {stamina_bar_entity.max_value} Stamina - OFF'


                stamina_timeout = None
        if key == 'debug':
            print(self.x)
        # - Normal
        if key == 'space':
            self.jump()
        if key == 'd':
            self.velocity = 1
            self.scale_x = self._original_scale_x
        if key == 'd up':
            self.velocity = -held_keys['a']
        if key == 'a':
            self.velocity = -1
        if key == 'a up':
            self.velocity = held_keys['d']
        if held_keys['d'] or held_keys['a']:
            self.scale_x = self._original_scale_x * self.velocity


    def jump(self):
        if not self.grounded and self.jumps_left <= 1:
            return
        Audio("jump.mp3") # Jump Audio
        if self._start_fall_sequence:
            self._start_fall_sequence.kill()

        if hasattr(self, 'y_animator'):
            self.y_animator.kill()
        self.jump_dust = Entity(model=Circle(), scale=.5, color=color.white33, position=self.position)
        self.jump_dust.animate_scale(3, duration=.3, curve=curve.linear)
        self.jump_dust.fade_out(duration=.2)
        destroy(self.jump_dust, 2.1)

        self.jumping = True
        self.jumps_left -= 1
        self.grounded = False

        target_y = self.y + self.jump_height
        duration = self.jump_duration

        self.animate_y(target_y, duration, resolution=30, curve=curve.out_expo)
        self._start_fall_sequence = invoke(self.start_fall, delay=duration)


    def start_fall(self):
        if hasattr(self, 'y_animator'):
            self.y_animator.pause()
        self.jumping = False


    def land(self):
        # print('land')
        self.air_time = 0
        self.jumps_left = self.max_jumps
        self.grounded = True