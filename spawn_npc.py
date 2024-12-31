

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import argparse
import logging
import random

from application_graph import ApplicationGraph  # 导入特征图模块

app_graph = ApplicationGraph()

def main():
    # 添加初始化任务到特征图
    app_graph.add_task("Initialize NPC Spawner", compute_time=0.2, data_volume=1)
    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-n', '--number-of-vehicles',
        metavar='N',
        default=10,
        type=int,
        help='number of vehicles (default: 10)')
    argparser.add_argument(
        '-d', '--delay',
        metavar='D',
        default=2.0,
        type=float,
        help='delay in seconds between spawns (default: 2.0)')
    argparser.add_argument(
        '--safe',
        action='store_true',
        help='avoid spawning vehicles prone to accidents')
    args = argparser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    actor_list = []
    client = carla.Client(args.host, args.port)
    client.set_timeout(2.0)

    # 添加连接到客户端任务到特征图
    app_graph.add_task("Connect to Client", ["Initialize NPC Spawner"], compute_time=0.5, data_volume=1)

    try:

        world = client.get_world()
        # blueprints = world.get_blueprint_library().filter('vehicle.*')
        # blueprints = world.get_blueprint_library().filter('vehicle.*').find('vehicle.tesla.model3')
        blueprints = [world.get_blueprint_library().find('vehicle.tesla.model3')]

        if args.safe:
            blueprints = [x for x in blueprints if int(x.get_attribute('number_of_wheels')) == 4]
            blueprints = [x for x in blueprints if not x.id.endswith('isetta')]
            blueprints = [x for x in blueprints if not x.id.endswith('carlacola')]

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)

        if args.number_of_vehicles < number_of_spawn_points:
            random.shuffle(spawn_points)
        elif args.number_of_vehicles > number_of_spawn_points:
            msg = 'requested %d vehicles, but could only find %d spawn points'
            logging.warning(msg, args.number_of_vehicles, number_of_spawn_points)
            args.number_of_vehicles = number_of_spawn_points

        # 添加生成 NPC 任务到特征图
        app_graph.add_task("Generate Spawn Points", ["Connect to Client"], compute_time=0.8, data_volume=10)


        # @todo cannot import these directly.
        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        FutureActor = carla.command.FutureActor

        batch = []
        for n, transform in enumerate(spawn_points):
            if n >= args.number_of_vehicles:
                break
            blueprint = random.choice(blueprints)
            if blueprint.has_attribute('color'):
                color = random.choice(blueprint.get_attribute('color').recommended_values)
                blueprint.set_attribute('color', color)
            blueprint.set_attribute('role_name', 'autopilot')
            batch.append(SpawnActor(blueprint, transform).then(SetAutopilot(FutureActor, True)))

        for response in client.apply_batch_sync(batch):
            if response.error:
                logging.error(response.error)
            else:
                actor_list.append(response.actor_id)
        
         # 添加批量生成车辆任务到特征图
        app_graph.add_task("Spawn NPC Vehicles", ["Generate Spawn Points"], compute_time=2.0, data_volume=50)

        print('spawned %d vehicles, press Ctrl+C to exit.' % len(actor_list))

        while True:
            world.wait_for_tick()

    finally:

        print('\ndestroying %d actors' % len(actor_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])

        # 添加清理任务到特征图
        app_graph.add_task("Cleanup NPC Vehicles", ["Spawn NPC Vehicles"], compute_time=0.5, data_volume=1)
        
        # 分析并可视化特征图
        app_graph.analyze_graph()
        app_graph.visualize_graph()

if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print('\ndone.')
