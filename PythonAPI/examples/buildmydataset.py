# import carla
# import random
# import os
# import numpy as np
# from PIL import Image
# from queue import Queue

# # 初始化 CARLA 客户端
# client = carla.Client('localhost', 2000)
# client.set_timeout(10.0)
# world = client.get_world()

# # 设置同步模式
# settings = world.get_settings()
# settings.synchronous_mode = True  # 启用同步模式
# settings.fixed_delta_seconds = 0.05  # 时间步长，确保传感器和模拟器同步
# world.apply_settings(settings)

# # 获取蓝图库
# bp_lib = world.get_blueprint_library()

# # 初始化队列用于传感器数据
# sensor_queue = Queue()

# # 创建车辆并设置自动驾驶
# vehicle_bp = bp_lib.find('vehicle.lincoln.mkz_2020')
# spawn_points = world.get_map().get_spawn_points()
# vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
# vehicle.set_autopilot(True)  # 自动驾驶模式

# # 创建并附加相机传感器，确保分辨率为 256 的倍数
# camera_bp = bp_lib.find('sensor.camera.rgb')
# camera_bp.set_attribute('image_size_x', '1024')  # 设置宽度为 256 的倍数
# camera_bp.set_attribute('image_size_y', '768')   # 设置高度为 256 的倍数
# camera_bp.set_attribute('bloom_intensity', '1')
# camera_bp.set_attribute('fov', '100')
# camera_bp.set_attribute('sensor_tick', '0.1')  # 设置传感器每 0.1 秒更新一次

# # 将相机附加到车辆上
# camera_init_trans = carla.Transform(carla.Location(x=1.5, z=1.5))
# camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)

# # 图像保存路径
# output_path = 'C:/Users/sweetboihpincloud/WindowsNoEditor/image'
# os.makedirs(output_path, exist_ok=True)

# # 定义传感器数据回调
# def sensor_callback(image, queue, name):
#     image.convert(carla.ColorConverter.Raw)  # 确保图像为原始格式
#     array = np.frombuffer(image.raw_data, dtype=np.uint8)
#     array = array.reshape((image.height, image.width, 4))  # 高度、宽度、RGBA
#     array = array[:, :, :3]  # 丢弃 alpha 通道
#     img = Image.fromarray(array)
#     img.save(os.path.join(output_path, f"{image.frame}.png"))

# camera.listen(lambda image: sensor_callback(image, sensor_queue, "camera"))

# try:
#     # 主循环
#     while True:
#         world.tick()  # 每帧更新世界状态，确保同步
# except KeyboardInterrupt:
#     print("脚本已停止")
# finally:
#     # 停止传感器并清理
#     camera.stop()
#     vehicle.destroy()
#     print("清理完成")
import carla
import random
import os
import numpy as np
from PIL import Image
from queue import Queue, Empty

# 初始化 CARLA 客户端
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

# 设置同步模式
settings = world.get_settings()
settings.synchronous_mode = True
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# 获取蓝图库
bp_lib = world.get_blueprint_library()

# 初始化队列用于传感器数据
sensor_queue = Queue()

# 创建车辆并设置自动驾驶
vehicle_bp = bp_lib.find('vehicle.lincoln.mkz_2020')
spawn_points = world.get_map().get_spawn_points()
vehicle = world.try_spawn_actor(vehicle_bp, random.choice(spawn_points))
vehicle.set_autopilot(True)

# 创建相机传感器，分辨率设置为 256 的倍数
camera_bp = bp_lib.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '1024')
camera_bp.set_attribute('image_size_y', '768')
camera_bp.set_attribute('bloom_intensity', '1')
camera_bp.set_attribute('fov', '100')
camera_bp.set_attribute('sensor_tick', '1.0w')  # 与 world.tick() 同步

# 将相机附加到车辆上
camera_init_trans = carla.Transform(carla.Location(x=1.5, z=1.5))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)

# 图像保存路径
output_path = 'C:/Users/sweetboihpincloud/WindowsNoEditor/image'
os.makedirs(output_path, exist_ok=True)

# 定义传感器数据回调
def sensor_callback(image, queue):
    queue.put(image)

camera.listen(lambda image: sensor_callback(image, sensor_queue))

try:
    # 主循环
    while True:
        # 进行一次世界更新
        world.tick()
       

        # 等待新图像到达并从队列获取
        try:
            image = sensor_queue.get(timeout=1.0)
            array = np.frombuffer(image.raw_data, dtype=np.uint8)
            array = array.reshape((image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]  # 将 BGR 转为 RGB
            img = Image.fromarray(array)
            img.save(os.path.join(output_path, f"{image.frame}.png"))
        except Empty:
            print("未收到图像帧，可能存在问题")

except KeyboardInterrupt:
    print("脚本已停止")
finally:
    # 停止传感器并清理
    camera.stop()
    vehicle.destroy()
    print("清理完成")
