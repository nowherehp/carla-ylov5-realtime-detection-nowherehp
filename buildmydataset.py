
import carla
import random
import os
import numpy as np
from PIL import Image
from queue import Queue, Empty
from application_graph import ApplicationGraph  # 导入特征图模块

app_graph = ApplicationGraph()

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

 #添加 "Spawn Vehicle" 任务到特征图
app_graph.add_task("Spawn Vehicle", ["Initialize World"], compute_time=0.3, data_volume=5)

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

# 添加 "Initialize Camera Sensor" 任务到特征图
app_graph.add_task("Initialize Camera Sensor", ["Spawn Vehicle"], compute_time=0.2, data_volume=10)

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


    # 分析并可视化特征图
    app_graph.analyze_graph()
    app_graph.visualize_graph()
