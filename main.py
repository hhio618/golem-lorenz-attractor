#!/usr/bin/env python3
import argparse
import asyncio
import subprocess
import os
import pathlib
import sys
import argparse

import yapapi
from yapapi.log import enable_default_logger, log_summary, log_event_repr  # noqa
from yapapi.runner import Engine, Task, vm
from yapapi.runner.ctx import WorkContext
from datetime import timedelta


async def main(duration, time_delta, num_trajectories=20, num_nodes=4, subnet_tag="devnet-alpha.2" ):
    package = await vm.repo(
        image_hash="cea36374b451274ac584f747fcf876ac15865ee319ebb4e7eea94c23",
        min_mem_gib=0.5,
        min_storage_gib=5.0,
    )
    print(duration, time_delta, num_trajectories, num_nodes)
    async def worker(ctx: WorkContext, tasks):
        async for task in tasks:
            node_no = task.data
            ctx.send_file("lorenz.py", "/golem/work/task.py")
            cmd = f"python3 /golem/work/task.py -d {duration} -n {node_no}/{num_nodes} -m {num_trajectories} -l {time_delta} "
            print(f"\033[36;1mRunning {cmd}\033[0m")
            ctx.run("sh", "-c", f"{cmd} >> /golem/output/log.txt 2>&1")
            ctx.download_file(f"/golem/output/log.txt", "log.txt")
            task_duration = duration/num_nodes
            # frame start stop index
            t0 = int(task_duration/time_delta) * (node_no-1)
            t1 = t0+int(task_duration/time_delta)
            for t in range(t0,t1):
                ctx.download_file(f"/golem/output/frame_{t:04d}.png", f"output/frame_{t:04d}.png")
            yield ctx.commit()
            task.accept_task()

        ctx.log("no more task to run")

    init_overhead: timedelta = timedelta(minutes=10)

    # By passing `event_emitter=log_summary()` we enable summary logging.
    # See the documentation of the `yapapi.log` module on how to set
    # the level of detail and format of the logged information.
    async with Engine(
        package=package,
        max_workers=num_nodes,
        budget=100.0,
        timeout=init_overhead + timedelta(minutes=num_nodes * 2),
        subnet_tag=subnet_tag,
        event_emitter=log_summary(),
    ) as engine:
        async for task in engine.map(worker, [Task(data=i+1) for i in range(num_nodes)]):
            print(f"\033[36;1mTask computed: {task}, result: {task.output}\033[0m")
        
     
    print(f"\033[36;1mConverting ppng files to a gif animation!\033[0m")
    i = "output/frame_%04d.png"
    o = "output.gif"
    subprocess.call(f"ffmpeg  -i {i} {o}", shell=True)


if __name__ == "__main__":
    my_parser =  argparse.ArgumentParser(description='Lorenz attractor simulation on Golem network')
    my_parser.add_argument('--output_dir',
                       '-o',
                       type=str,
                       default='/golem/output',
                       help='Output directory')
    my_parser.add_argument('--time_delta',
                       '-l',
                       type=float,
                       default=0.01,
                       help='Time delta for changes')
    my_parser.add_argument('--duration',
                       '-d',
                       type=int,
                       default=5,
                       help='Duration (seconds)')
    my_parser.add_argument('--num_trajectories',
                       '-m',
                       type=int,
                       default=20,
                       help='Duration (seconds)')
    args = my_parser.parse_args()

    enable_default_logger()
    loop = asyncio.get_event_loop()
    task = loop.create_task(main(args.duration, args.time_delta, args.num_trajectories))
    try:
        asyncio.get_event_loop().run_until_complete(task)

    except (Exception, KeyboardInterrupt) as e:
        print(e)
        task.cancel()
        asyncio.get_event_loop().run_until_complete(task)

