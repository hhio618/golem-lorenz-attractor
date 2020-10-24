# Lorenz attractor on Golem network
![gif animation](./output.gif?raw=true)    
The Lorenz Equations are a system of three coupled, first-order, nonlinear differential equations which describe the trajectory of a particle through time. The system was originally derived by Lorenz as a model of atmospheric convection, but the deceptive simplicity of the equations have made them an often-used example in fields beyond atmospheric physics.
## Tutorial (Youtube)
[![Lorenz attractor on Golem network](https://youtu.be/SPCUOPL6gqs/0.jpg)](https://youtu.be/SPCUOPL6gqs "Lorenz attractor on Golem network")
## Prerequisites
### Install yagna
```$ sh curl -sSf https://join.golem.network/as-requestor | bash -```
### Install ffmpeg (required for converting png files to gif animation)
```bash
$ sudo apt-get install ffmpeg
```
### Install python requirements
```sh
$ # Using python3.6+
$ source ~/your/virtual/env
$ pip install -r requirements.txt
```
### Build using docker
```sh
$ docker build -t golem-lorenza:latest
```
### Build/push Golem vm
```sh
$ gvmkit-build golem-lorenz:latest
$ gvmkit-build golem-lorenz:latest --push
```
### Run yagna daemon
```sh
$ yagna service run
```
### Run Lorenz attractor on Golem!
```sh
$ yagna app-key create requestor
$ yagna payment init -r
$ export YAGNA_APPKEY=<your-key>
$ python main.py
usage: main.py [-h] [--output_dir OUTPUT_DIR] [--time_delta TIME_DELTA] [--duration DURATION] [--num_trajectories NUM_TRAJECTORIES]

Lorenz attractor simulation on Golem network

optional arguments:
  -h, --help            show this help message and exit
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory
  --time_delta TIME_DELTA, -l TIME_DELTA
                        Time delta for changes
  --duration DURATION, -d DURATION
                        Duration (seconds)
  --num_trajectories NUM_TRAJECTORIES, -m NUM_TRAJECTORIES
                        Number of trajectories

```
#### Watch full steps on [Youtube](https://youtu.be/SPCUOPL6gqs)!
