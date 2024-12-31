


print(" control keys: ")
print(" up arrow key = throttle \n down arrow key = reverse \n right arrow key = steer right \n left arrow key = steer left \n space bar = brake")
print(" 'd' key = object detection \n 'a' key = autopilot \n 's' key = save dataset \n ")

# ==============================================================================
# -- Find carla module ---------------------------------------------------------
# ==============================================================================

import glob
import os
import sys

# try:
#     sys.path.append(glob.glob(' C:/Users/sweetboihpincloud/WindowsNoEditor/PythonAPI/carla/dist/carla-0.9.14-py3.7-win-amd64.egg' % (
#         sys.version_info.major,
#         sys.version_info.minor,
#         'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
# except IndexError:
#     pass

try:
    # 直接添加完整的 .egg 文件路径
    sys.path.append('C:/Users/sweetboihpincloud/WindowsNoEditor/PythonAPI/carla/dist/carla-0.9.14-py3.7-win-amd64.egg')
except IndexError:
    pass


# ==============================================================================
# -- Imports -------------------------------------------------------------------
# ==============================================================================

import carla
from carla import ColorConverter as cc
import random

try:
    import pygame
    from pygame.locals import K_UP
    from pygame.locals import K_DOWN
    from pygame.locals import K_LEFT
    from pygame.locals import K_RIGHT
    from pygame.locals import K_a
    from pygame.locals import K_s
    from pygame.locals import K_d
    from pygame.locals import K_r
    from pygame.locals import K_c
    from pygame.locals import K_q
  
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_SPACE
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

import time
# from cv2 import cv2
import cv2
from PIL import Image
from io import StringIO

import torch 
from matplotlib import pyplot as plt 

#nextnetwork

from application_graph import ApplicationGraph  # 导入特征图模块

# 初始化特征图
app_graph = ApplicationGraph()

# 添加初始化任务到特征图
app_graph.add_task("Initialize Object Detection", compute_time=0.3, data_volume=2)


# ==============================================================================
# -- constants -----------------------------------------------------------------
# ==============================================================================

IM_WIDTH = 640
IM_HEIGHT = 480

# ==============================================================================
# -- World ---------------------------------------------------------------------
# ==============================================================================

'''
DESCRIPTION: 
    this class initiaties a world and spawn a vehicle (by default bmw grandtourer)
'''

class World():

    def __init__(self, vehicle="grandtourer"):
        

        # initializing a list of all of the actors in the world - assigning attributes to self  
        self.vehicle = vehicle
        self.surface = pygame.Surface((IM_WIDTH, IM_HEIGHT))

        # initiating world
        self.client = carla.Client("localhost", 2000)
        self.client.set_timeout(20.0)
        self.world = self.client.get_world()
        self.map = self.world.get_map()
        
        # reseting the world
        self.reset(vehicle)

    def spawn_vehicle(self, vehicle):
        # this method spawns the vehicle (by default grandtourer)

        # getting all of the blueprints
        self.blueprint_library = self.world.get_blueprint_library()
        
        # making the blueprint of vehicle
        self.vehicle_blueprint = self.blueprint_library.filter(vehicle)[0]

        # getting a random spawn point from the map 
        spawn_point = random.choice(self.world.get_map().get_spawn_points())

        # spawning the vehicle
        self.vehicle = self.world.spawn_actor(self.vehicle_blueprint, spawn_point)
        self.actor_list.append(self.vehicle)


    def spawn_camera_sensor(self):

        # setting up the camera sensor
        camera_blueprint = self.blueprint_library.find("sensor.camera.rgb")
        camera_blueprint.set_attribute("image_size_x", f"{IM_WIDTH}")
        camera_blueprint.set_attribute("image_size_y", f"{IM_HEIGHT}")
        camera_blueprint.set_attribute("fov", "110")

        # getting camera spawn point 
        camera_spawn_point = carla.Transform(carla.Location(x=2.5, z = 0.7))

        # spawning camera sensor
        self.camera_sensor = self.world.spawn_actor(camera_blueprint, camera_spawn_point, attach_to=self.vehicle)
        self.actor_list.append(self.camera_sensor)


    def reset(self, vehicle):
        # destorying everything in the world
        self.actor_list = []

        # re-spawning the actors 
        self.spawn_vehicle(vehicle)
        self.spawn_camera_sensor()

        # showing and rendering the image
        self.camera_sensor.listen(lambda data: self.process_image(data))

    def image_renderer(self, display):
        # renders the image onto the screen
        display.blit(self.surface, (0, 0))

    def process_image(self, image):
        # getting the image on display and converting it to surface 
        image.convert(cc.Raw)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        array = array[:, :, ::-1]
        self.image = array
        self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
    
    #find nearest stop sign and return the distance between them
    def get_nearest_stop_sign(self):
       
        stop_signs = self.world.get_actors().filter('traffic.stop')  # 获取所有 Stop Sign
        vehicle_location = self.vehicle.get_location()  # 获取当前车辆的位置

        # 找到最近的 Stop Sign
        nearest_stop_sign = None
        min_distance = float('inf')
        for stop_sign in stop_signs:
            stop_sign_location = stop_sign.get_location()
            distance = vehicle_location.distance(stop_sign_location)
            if distance < min_distance:
                min_distance = distance
                nearest_stop_sign = stop_sign

        return nearest_stop_sign, min_distance
    

    def get_focal_length_from_camera(self):
  
        """
        从摄像机配置计算焦距（像素）。
        """
        try:
            # 获取摄像机蓝图
            blueprint_library = self.world.get_blueprint_library()
            camera_blueprint = blueprint_library.find(self.camera_sensor.type_id)  # 使用传感器类型 ID 找到蓝图
            
            # 获取 FOV 属性值
            fov = float(camera_blueprint.get_attribute("fov").get())  # 使用 .get() 获取属性值

            # 使用摄像机的图像分辨率
            width = IM_WIDTH  # 图像宽度
            height = IM_HEIGHT  # 图像高度

            # 焦距计算公式
            focal_length = width / (2.0 * np.tan(np.radians(fov) / 2.0))
            return focal_length
        except Exception as e:
            print(f"Error calculating focal length: {e}")
            return None
        
    def exit(self):
        for actor in self.actor_list: 
            destroyed_sucessfully = actor.destroy()
            print(actor)
            print(destroyed_sucessfully)

# ==============================================================================
# -- Keyboard Control ----------------------------------------------------------
# ==============================================================================

'''
DESCRIPTION: 
    defining the key map
'''

class KeyboardControl(object):
    def __init__(self, model):

        self.model = model
        self.control = carla.VehicleControl()
        self.steer_cache = 0.0
        self.toggle_autopilot = False
        self.toggle_datasave = False 
        self.image_count = 0  # 初始化 image_count
        self.realtime_mode = False  # 标志位，用于实时检测模式
        self.last_detection_time = 0  # 上一次检测的时间

    def control_keys(self, world, clock):

        global mode  # 确保可以修改全局变量 mode

        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            self.control.gear = 1
            print("Throttle")
        if keys[K_DOWN]:
            self.control.gear = -1
            print("Reverse")
        if keys[K_LEFT]:
            print("Turn left")
        if keys[K_RIGHT]:
            print("Turn right")
        if keys[K_SPACE]:
            print("Brake")
        if keys[K_a]:
            self.autopilot(world)
            print("Autopilot toggled: ", self.toggle_autopilot)
        if keys[K_s]:
            self.toggle_datasave = not self.toggle_datasave
            print("Dataset toggled: ", self.toggle_datasave)
            
        
        for event in pygame.event.get():
            # what to do with each key pressed 
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                     self.exit_game(world)
                     print("Exit")

                elif event.key == K_c:
                    print("C key pressed: Starting real-time detection mode.")
                    mode = "C"
                elif event.key == K_q and mode == "C":
                    print("Q key pressed: Exiting real-time detection mode.")
                    mode = "manual"

                # if event.key == K_UP:
                #         self.control.gear = 1
                #         print("Throttle")
                # elif event.key == K_DOWN:
                #     self.control.gear = -1
                #     print("Reverse")
                # elif event.key == K_LEFT:
                #     print("Turn left")
                # elif event.key == K_RIGHT:
                #     print("Turn right")
                # elif event.key == K_ESCAPE:
                #     self.exit_game(world)
                #     print("Exit")
                # elif event.key == K_SPACE:
                #     print("Brake")
                # #autopilot by carla
                # elif event.key == K_a:
                #     self.autopilot(world)
                #     print("Autopilot toggled: ", self.toggle_autopilot)
                # elif event.key == K_s:
                #     self.toggle_datasave = not self.toggle_datasave
                #     print("Dataset toggled: ", self.toggle_datasave)



        
                
                # if mode == "manual":
                elif mode == "manual": 

                    



    ################################################################################################################
                    # capture and detxtion using yolov5, then download the pic
                    if event.key == K_d:
                        

                        #version4
                        try:
                            self.image_count += 1  # 递增计数器
                            print("D key pressed: Starting object detection.")
                            app_graph.add_task("Start Object Detection", ["Load YOLOv5 Model"], compute_time=0.2, data_volume=5)

                            # 1. 检查摄像头图像是否存在
                            if world.image is None:
                                print("Error: world.image is None. Camera image not initialized.")
                                return

                            # 2. 运行 YOLO 模型进行检测
                            yolo_output = self.model(world.image)  # YOLO 模型输出
                            print("YOLO model ran successfully.")
                            app_graph.add_task("Run YOLO Inference", ["Start Object Detection"], compute_time=2.0, data_volume=10)

                            detection_results = parse_yolo_results(yolo_output)
                            print("Detection results parsed successfully.")
                            app_graph.add_task("Parse Detection Results", ["Run YOLO Inference"], compute_time=0.5, data_volume=5)

                            # 3. 提取所有标签为 "car" 的检测结果
                            cars = [result for result in detection_results if result['class'] == 'car']

                            if not cars:
                                print("No cars detected in the image.")
                                return

                            # 4. 计算每辆车的像素高度和距离
                            real_height = 56.8  # Tesla Model 3 的真实高度（单位：英寸）
                            focal_length = 500  # 焦距（单位：像素）

                            # 获取 YOLO 渲染的图像
                            annotated_image = np.squeeze(yolo_output.render())
                            for car in cars:
                                bbox = car['bbox']
                                pixel_height = bbox[3] - bbox[1]  # 计算像素高度
                                distance = (real_height * focal_length) / pixel_height  # 计算距离（单位：英寸）
                                print(f"Car detected: Pixel Height = {pixel_height:.2f} pixels, Distance = {distance:.2f} inches")

                                # 在 YOLO 标注图像中添加距离标注
                                label_y_offset = 15 
                                cv2.putText(annotated_image, f"{distance:.2f} in", (int(bbox[0]), int(bbox[3])  + label_y_offset), 
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                            
                            annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

                            # 5. 保存带距离标注的 YOLO 图像
                            filename = f"detected_picture_{self.image_count}.jpg"
                            cv2.imwrite(filename, annotated_image)
                            app_graph.add_task("Save Detection Image", ["Parse Detection Results"], compute_time=0.1, data_volume=2)
                            print(f"Annotated image saved as {filename}")

                        except Exception as e:
                            print(f"Error in D key logic: {e}")              
    ################################################################################################################






    ################################################################################################################
                    #using the size of stop sign to calculate the focus depth of the cam

                    elif event.key == K_r:
                        try:
                            print("R key pressed: Starting Stop Sign detection.")
                            app_graph.add_task("Start Stop Sign Detection", ["Initialize Object Detection"], compute_time=0.2, data_volume=5)

                            
                            # 检查摄像头捕获的图像是否存在
                            if world.image is None:
                                print("Error: world.image is None. Camera image not initialized.")
                                return
                            print(f"world.image type: {type(world.image)}, shape: {world.image.shape}")

                            # 获取最近的 Stop Sign 和距离
                            stop_sign, measured_distance = world.get_nearest_stop_sign()
                            if not stop_sign:
                                print("No Stop Sign found!")
                                return
                            print(f"Nearest Stop Sign found at distance: {measured_distance:.2f} meters")
                            app_graph.add_task("Get Nearest Stop Sign", ["Start Stop Sign Detection"], compute_time=0.3, data_volume=3)

                            # # 获取 Carla 提供的焦距
                            # try:
                            #     carla_focal_length = world.get_focal_length_from_camera()
                            #     print(f"Carla Focal Length: {carla_focal_length:.2f} pixels")
                            # except Exception as e:
                            #     print(f"Error fetching focal length: {e}")
                            #     return

                            # 运行目标检测
                            try:
                                detection_results = self.model(world.image)
                                print("YOLO model ran successfully.")
                                app_graph.add_task("Run YOLO Detection", ["Get Nearest Stop Sign"], compute_time=1.5, data_volume=10)
                                detection_results = parse_yolo_results(detection_results)
                                print("Detection results parsed successfully.")
                                app_graph.add_task("Parse Detection Results", ["Run YOLO Detection"], compute_time=0.5, data_volume=5)
                            except Exception as e:
                                print(f"Error during YOLO detection: {e}")
                                return

                            # 获取 Stop Sign 的像素宽度
                            try:
                                pixel_width = get_object_pixel_width(detection_results, target_class="stop sign")
                                if not pixel_width:
                                    print("Stop Sign not detected!")
                                    return
                                print(f"Stop Sign pixel width: {pixel_width:.2f} pixels")
                                app_graph.add_task("Get Pixel Width", ["Parse Detection Results"], compute_time=0.3, data_volume=2)
                            except Exception as e:
                                print(f"Error fetching pixel width: {e}")
                                return

                            # 计算手动焦距
                            try:
                                real_width = 0.75  # Stop Sign 的实际宽度（单位：米）
                                manual_focal_length = calculate_focal_length_manual(measured_distance, real_width, pixel_width)
                                print(f"Manual Focal Length: {manual_focal_length:.2f} pixels")
                                app_graph.add_task("Calculate Focal Length", ["Get Pixel Width"], compute_time=0.4, data_volume=2)
                            except Exception as e:
                                print(f"Error calculating manual focal length: {e}")
                                return

                            # 标注图像
                            try:
                                # annotated_image = annotate_image_with_focal_lengths(world.image, carla_focal_length, manual_focal_length)
                                writable_image = world.image.copy()  # 确保图像副本是可写的
                                annotated_image = annotate_image_with_focal_lengths(writable_image, 0, manual_focal_length)
                                print("Image successfully annotated.")
                                app_graph.add_task("Annotate Image", ["Calculate Focal Length"], compute_time=0.3, data_volume=5)
                            except Exception as e:
                                print(f"Error during image annotation: {e}")
                                return

                            # 保存图像
                            try:
                                output_path = "calibrated_image.jpg"
                                cv2.imwrite(output_path, annotated_image)
                                print(f"Annotated image saved to {output_path}")
                                app_graph.add_task("Save Annotated Image", ["Annotate Image"], compute_time=0.1, data_volume=2)
        
                                
                            except Exception as e:
                                print(f"Error saving annotated image: {e}")
                                return

                        except Exception as e:
                            print(f"Error in R key logic: {e}")
                    
                    # elif event.key == K_c:

                    #     print("C key pressed: Starting real-time detection mode.")
                    #     self.realtime_running = True
                    #     mode = "C"  # 切换模式为实时检测
                
                # elif mode == "C":
                #     if event.key == K_q:  # 退出 C mode
                #         print("Q key pressed: Exiting real-time detection mode.")
                #         mode = "manual"
                #         self.realtime_mode = False
        

################################################################################################################




        
        # using the control function of vehicle 
        if isinstance(self.control, carla.VehicleControl):
            self.vehicle_control(pygame.key.get_pressed(), clock.get_time())
            self.control.reverse = self.control.gear < 0
        world.vehicle.apply_control(self.control)



################################################################################################################
    

    def realtime_detection(self, world, display):


        current_time = pygame.time.get_ticks()
        if current_time - self.last_detection_time < 200:  # 限制每 100 毫秒检测一次
            return
        self.last_detection_time = current_time

        app_graph.add_task("Start Real-time Detection", ["Run YOLO Inference"], compute_time=0.3, data_volume=3)

        if world.image is None:
            print("Error: world.image is None. Camera image not initialized.")
            return

        try:
            # image = torch.tensor(world.image).to(self.model.device)  # 模型和数据必须在同一设备上
            # yolo_output = self.model(image)
            # 执行 YOLO 模型检测
           
            yolo_output = self.model(world.image)
            detection_results = parse_yolo_results(yolo_output)

            # 渲染检测结果并计算距离
            annotated_image = np.squeeze(yolo_output.render())
            app_graph.add_task("Render Real-time Results", ["Start Real-time Detection"], compute_time=0.4, data_volume=5)

            real_height = 56.8  # Tesla Model 3 的真实高度（英寸）
            focal_length = 500  # 焦距（像素）

            for result in detection_results:
                if result['class'] == 'car':
                    bbox = result['bbox']
                    pixel_height = bbox[3] - bbox[1]
                    distance = (real_height * focal_length) / pixel_height
                    print(f"Real-time car detection: Distance = {distance:.2f} inches")
                    label_y_offset = 15
                    cv2.putText(annotated_image, f"{distance:.2f} in",
                                (int(bbox[0]), int(bbox[3]) + label_y_offset),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # 使用 display 进行 blit
            surface = pygame.surfarray.make_surface(annotated_image.swapaxes(0, 1))
            display.blit(surface, (0, 0))  # 使用 display 进行 blit
            pygame.display.flip()
            app_graph.add_task("Display Real-time Results", ["Render Real-time Results"], compute_time=0.1, data_volume=2)

        except Exception as e:
            print(f"Error in real-time detection: {e}")

         # 在实时检测中保持方向键控制逻辑
        keys = pygame.key.get_pressed()
        self.vehicle_control(keys, pygame.time.get_ticks())
################################################################################################################






    def vehicle_control(self, keys, milliseconds):

        # controlling the throttle
        self.control.throttle = 1.0 if keys[K_UP] or keys[K_DOWN] else 0.0

        # controlling the steering
        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT]:
            self.steer_cache -= steer_increment
        elif keys[K_RIGHT]:
            self.steer_cache += steer_increment
        else:
            self.steer_cache = 0.0
        self.steer_cache = min(0.7, max(-0.7, self.steer_cache))
        self.control.steer = round(self.steer_cache, 1)

        # controllign the brake and hand brake 
        self.control.brake = 1.0 if keys[K_SPACE] else 0.0

    def exit_game(self, world):
        world.exit()
        pygame.quite()
    
    def autopilot(self, world): 
        # turns autopilot on/off 
        self.toggle_autopilot = not self.toggle_autopilot
        if self.toggle_autopilot: 
            world.vehicle.set_autopilot(1)
        else: 
            world.vehicle.set_autopilot(0) 
        
    def get_dataset(self, world, temp_time):
        if self.toggle_datasave:
            pygame.image.save(world.surface, str(temp_time) + '.png')
        else: 
            pass





# ==============================================================================
# -- camera focus lenghth -----------------------------------------------------------------
# =============================================================================


def calculate_focal_length_manual(measured_distance, real_width, pixel_width):
    # 通过公式计算焦距
    return (measured_distance * pixel_width) / real_width



def annotate_image_with_focal_lengths(image, carla_focal_length, manual_focal_length):
    # 计算误差
    error = abs(carla_focal_length - manual_focal_length)
    # 在图片上绘制文字
    cv2.putText(image, f"Carla Focal Length: {carla_focal_length:.2f}px", 
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(image, f"Manual Focal Length: {manual_focal_length:.2f}px", 
                (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(image, f"Error: {error:.2f}px", 
                (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return image


def get_object_pixel_width(detection_results, target_class):
    """
    从目标检测结果中提取指定类别的像素宽度。
    :param detection_results: 模型检测的结果（可能是一个 Tensor 或解析后的字典）
    :param target_class: 目标类别名称（如 "stop sign"）
    :return: 目标的像素宽度（如果未找到目标，返回 None）
    """
    for result in detection_results:
        if result['class'] == target_class:  # 检查目标类别是否匹配
            x1, _, x2, _ = result['bbox']  # 获取边界框坐标
            return x2 - x1  # 返回像素宽度
    return None  # 如果没有找到目标类别

def parse_yolo_results(results):
    """
    解析 YOLO 模型的检测结果。
    :param results: YOLO 检测返回的结果对象
    :return: 标准化后的检测结果列表
    """
    parsed_results = []
    for result in results.xyxy[0]:  # 假设单帧检测，xyxy 是边界框格式
        parsed_results.append({
            'class': results.names[int(result[5])],  # 提取类别名称
            'bbox': [result[0].item(), result[1].item(), result[2].item(), result[3].item()],  # 边界框
            'confidence': result[4].item()  # 提取置信度
        })
    return parsed_results



# ==============================================================================
# -- Game Loop -----------------------------------------------------------------
# ==============================================================================

'''
DESCRIPTION: 
    this part is for the gameloop and user interface (image rendering)
'''


def game_loop():

    global mode
    mode = "manual"  # 初始化为普通模式

    #  # 检查 CUDA 是否可用
    # device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    # print(f"Using device: {device}")


    # initilizing the model
    try:
        
        model = torch.hub.load('ultralytics/yolov5', 'yolov5m6')
        app_graph.add_task("Load YOLOv5 Model", ["Initialize Object Detection"], compute_time=1.0, data_volume=50)

        # model = torch.hub.load('ultralytics/yolov5', 'yolov5m6')
        # model = model.autoshape()  # 保持 AutoShape 功能
        # model.to(device)  # 将模型移动到设备

        print("YOLOv5 model loaded successfully.")
    except:
        print("Error loading YOLOv5 model:", e)
        return

    # initializing pygame
    pygame.init()
    pygame.font.init()
    world = None
    # image size
    size = IM_WIDTH, IM_HEIGHT

    # color balck rgb
    black = 0, 0, 0

    temp_time_initial = 0
    temp_time_final = 0
    try: 
        # setting up the display
        display = pygame.display.set_mode(size,
                pygame.HWSURFACE | pygame.DOUBLEBUF)
        display.fill(black)
        
        # initializing the world
        world = World()
        controller = KeyboardControl(model)
        clock = pygame.time.Clock()

        while True:
            clock.tick_busy_loop(60)
            temp_time_final += clock.get_time()

            # # using the contorller 
            # if controller.control_keys(world, clock):
            #     return
            
            # if temp_time_final - temp_time_initial > 3000:
            #     temp_time_initial = temp_time_final
            #     controller.get_dataset(world, temp_time_final)
            
            # if temp_time_final > 5000000:
            #     controller.exit_game()
            

            # # rendering the image 
            # world.image_renderer(display)
            if mode == "manual":  # 普通模式
                 # using the contorller 
                if controller.control_keys(world, clock):
                    return
                
                if temp_time_final - temp_time_initial > 3000:
                    temp_time_initial = temp_time_final
                    controller.get_dataset(world, temp_time_final)
                
                if temp_time_final > 5000000:
                    controller.exit_game()
                
                if controller.control_keys(world, clock) == "C":
                    mode = "C"
                # rendering the image 
                world.image_renderer(display)



            elif mode == "C":  # 实时检测模式
                # controller.realtime_detection(world)  # 调用实时检测逻辑
                controller.realtime_detection(world,display)  # 调用实时检测逻辑

            pygame.display.flip()
            


    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except:
        print("couldn't initialize world")
    finally:
        # 在程序退出时清理资源并生成特征图
        if world is not None:
            world.exit()
        
        app_graph.analyze_graph()
        app_graph.visualize_graph()
    

# ==============================================================================
# -- Main ----------------------------------------------------------------------
# ==============================================================================

game_loop() 