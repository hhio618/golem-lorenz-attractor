import argparse
import numpy as np
from scipy import integrate
import matplotlib
matplotlib.use("agg")
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames

def lorentz_deriv(X, t0, sigma=10., beta=8./3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    (x, y, z) = X
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts


def run(node, time_delta=0.01, duration=20,  output_dir="/golem/output", num_trajectories=20):
    node_no, num_nodes = map(int, node.split("/"))
    task_duration = duration/num_nodes
    frames = np.arange(1, int(duration/time_delta)+1)
    # frame start stop index
    t0 = int(task_duration/time_delta) * (node_no-1)
    t1 = t0+int(task_duration/time_delta)
    # Choose random starting points, uniformly distributed from -15 to 15
    np.random.seed(1)
    x0 = -15 + 30 * np.random.random((num_trajectories, 3))

    # Solve for the trajectories
    t = np.linspace(0, duration, int(duration/time_delta))
    x_t = np.asarray([integrate.odeint(lorentz_deriv, x0i, t)
                      for x0i in x0])

    # Set up figure & 3D axis for animation
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    ax.axis('off')

    # choose a different color for each trajectory
    colors = plt.cm.jet(np.linspace(0, 1, num_trajectories))

    # set up lines and points
    lines = sum([ax.plot([], [], [], '-', c=c)
                 for c in colors], [])
    pts = sum([ax.plot([], [], [], 'o', c=c)
               for c in colors], [])

    # prepare the axes limits
    ax.set_xlim((-25, 25))
    ax.set_ylim((-35, 35))
    ax.set_zlim((5, 55))

    # set point-of-view: specified by (altitude degrees, azimuth degrees)
    ax.view_init(30, 0)


    # instantiate the animator.
    # anim = animation.FuncAnimation(fig, animate, init_func=init,
    #                               frames=500, interval=30, blit=True)
    j = t0 
    print(t0, t1 , frames.shape)
    for i in frames[t0:t1]:
        i = (2 * i) % x_t.shape[1]
        for line, pt, xi in zip(lines, pts, x_t):
            x, y, z = xi[:i].T
            line.set_data(x, y)
            line.set_3d_properties(z)

            pt.set_data(x[-1:], y[-1:])
            pt.set_3d_properties(z[-1:])

        ax.view_init(30, 0.3 * i)
        print(f"\033[36;1mNode({node}): generating {output_dir}/frame_{j:04d}.png\033[0m")
        fig.savefig(f"{output_dir}/frame_{j:04d}.png")
        j += 1



if __name__ == "__main__":
    my_parser =  argparse.ArgumentParser(description='Lorenz System in 3D on Golem network')
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
                       default=20,
                       help='Duration (seconds)')
    my_parser.add_argument('--num_trajectories',
                       '-m',
                       type=int,
                       default=20,
                       help='Duration (seconds)')
    my_parser.add_argument('--node',
                       '-n',
                       type=str,
                       default="1/4",
                       help='Node number, format: #node/#all_nodes')
    args = my_parser.parse_args()

    print(f"\033[36;1mStart processing Lorenz System in 3D on Golem using:\n\
            Node: {args.node}\n \
            Number of trajectories: {args.num_trajectories}\n \
            Time delta: {args.time_delta}\n \
            Overall duration: {args.duration})\033[0m")
    print(args.node, args.time_delta, args.duration, args.output_dir)
    run(args.node, args.time_delta, args.duration, args.output_dir, args.num_trajectories)
