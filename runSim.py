from IPython.display import YouTubeVideo, HTML
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import pymunk
from pymunk.vec2d import Vec2d
from ballsText import mktext

def setup_space(width, height, elasticity):
    """
    Returns a pymunk Space object initialized with gravity pointing down and walls on the left,

    bottom and right side of a rectangle with the specified width and height dimensions.

    The walls have elasticity elasticity.
    """
    space = pymunk.Space()
    space.gravity = 0, -9.820
    space.damping = 0.9999
    static_body = space.static_body
    gap = 0.1
    static_lines = [
        # Bottom floor
        pymunk.Segment(static_body, (gap, gap), (width - gap, gap), 0.01),
        # Right wall
        pymunk.Segment(
            static_body, (width - gap, gap), (width - gap, height * 100), 0.01
        ),
        # Left wall
        pymunk.Segment(static_body, (gap, gap), (gap, height * 100), 0.01),
    ]
    for line in static_lines:
        line.elasticity = elasticity
        line.friction = 0
    space.add(*static_lines)
    return space


def mk_ball(x, y, vx, vy, radius, elasticity, space):
    """
    Creates a ball at specified (x,y) position with initial velocity (vx,vy),

    radius "radius" and elasticity "elasticity". It then adds the ball to the simulation space.
    """
    body = pymunk.Body(0, 0)
    body.position = Vec2d(x, y)
    body.velocity = Vec2d(vx, vy)
    # body.start_position = Vec2d(*body.position)
    shape = pymunk.Circle(body, radius)
    shape.density = 1
    shape.elasticity = elasticity
    space.add(body, shape)
    body.radius = radius
    return body


def sim(space, balls, T, dt, height):
    """
    Given a space to be simulated, populated with some balls, this function simulates from t=0 to t=T with step dt. 

    Any ball reaching above the given height is removed from the simulation.

    The function returns two lists with the same length: one with timestamps, and one with (x,y) positions of each ball.
    """
    ts = np.arange(0, T, dt)
    positions = []
    for t in ts:
        # log ball positions
        positions.append([np.array(b.position) for b in balls])
        # Step the simulation
        space.step(dt)
        for b in balls:
            if (b in space.bodies):
                r = list(b.shapes)[0].radius
                if b.position[1] > height + r:  # ball is out of view
                    space.remove(b, list(b.shapes)[0])
        if len(space.bodies) == 0:  # no balls left in the simulation
            break
    return ts[: len(positions)], positions


def initialize():
    """
    Change this function to generate different animations
    
    A circle of balls moving a swirling way
    """
    width, height = 16, 9
    elasticity = 0.99  # Elasticity of objects.  Must be <=1.
    # Values closer to 1 mean the bounces do not lose much energy.
    space = setup_space(width, height, elasticity)

    # Create a circle with radius R, composed of N balls with radius r
    N, R, r = 1000, 2.5, 0.05
    # center of the circle (8, 4.5)
    cx, cy = width / 2, height / 2
    # velocity of each ball in the tangential direction
    vt = 3.0
    # random component of each ball's velocity (uniform)
    vrand = 0.5
    balls_data = mktext("THIS IS ROCKET LEAGUE!!!!",cx=8,cy=4.5,vrand=0.5,vrot=3.0,maxwidth=12,maxheight=5)
    balls = []
    
    np.random.seed(0)  # make sure that outputs of this function are repeatable
    i = 0
    x_eq = 1
    y_eq = 2

    # for t in np.linspace(0, 2 * np.pi, N, endpoint=False):
    for cx, cy, r, vx,vy,cs in balls_data: 
        balls.append(mk_ball(cx,cy,vx,vy,r,elasticity,space))
        # balls.append(mk_ball(
        #     x = cx + (np.cos(t)**3),
        #     y = cy + (np.sin(t)**3),
        #     vx=vt*np.cos(t+np.pi/2) + np.random.lognormal(-vrand, +vrand),
        #     vy=vt*np.sin(t+np.pi/2) + np.random.lognormal(-vrand, +vrand),
        #     radius=r,
        #     elasticity=elasticity,
        #     space=space)),

    return width, height, space, balls

"""
Actually run the simulations
"""
BALL_COLOR = "gnuplot2"
T = 4  # how long to simulate?
dt = 1/300  # we simulate 300 timesteps per second
# ------------------->
# Forward simulation >
# ------------------->
width, height, space, balls = initialize()
f_ts, f_positions = sim(
    space, balls, T, dt, height
)

# Backward simulation
width, height, space, balls = initialize()
# To simulate backwards, we invert the initial velocity of each ball
# and set the elasticity of each object to the reciprocal of the true value

for b in balls:
    s = list(b.shapes)[0]
    s.elasticity = 1 / s.elasticity
    b.velocity = -1 * b.velocity
for s in space.static_body.shapes:
    s.elasticity = 1 / s.elasticity
b_ts, b_positions = sim(
    space, balls, T, dt, height
)

# Stitch the resulting trajectories together
ts = list(-1 * b_ts[-1:0:-1]) + list(f_ts)
positions = b_positions[-1:0:-1] + f_positions

"""
Render sim (visualize 0.0)

fps = timesteps per second / subsampling 
Example: 300 / 10 = 30fps

dpi = dots per inch [note inch here]
example: width-to-height ratio (width, height) = 16:9 with dpi = 30
16*30 = width in pixels | 9 * 30 = height in pixels
yields 480x270 pixels

Higher dpi = better quality but slower processing and larger files. 
Lower dpi = faster processing and smaller files but poorer quality.

subsampling controls frame rate.
-------------Examples-------------------
T = 4, dt = 1/300, subsampling = 10, and dpi = 30:
    Simulate 4 seconds, with 1200 total timesteps (4 * 300), render 120 frames (1200 / 10 = 30 fps), at low resolution (30 dpi).
T = 8, subsampling = 5, and dpi = 120:
    Simulate 8 seconds, 2400 timesteps (8 * 300), render 480 frames (2400 / 5 = 60 fps), at full HD resolution (120 dpi).
"""
subsampling = 10 # render one out of this number of timesteps.
# Since we have 300 timesteps per second, 10 yields 30 fps. 5 yields 60 fps.

dpi = 30 # use low values for preview. dpi=120 yields fullhd video if width,height are 16,9

# Prepare the figure and axes
fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
ax.set(xlim=[0, width], ylim=[0, height])
ax.set_aspect("equal")
ax.set_position([0, 0, 1, 1])
fig.set(facecolor="y")

# Prepare the patches for the balls
cmap = plt.get_cmap(BALL_COLOR)
circles = [plt.Circle((0, 0), radius=b.radius, facecolor=cmap(i/len(balls)))
           for i,b in enumerate(balls)]
[ax.add_patch(c) for c in circles]

# Draw the walls as black lines
for s in space.static_body.shapes:
    ax.plot([s.a.x, s.b.x], [s.a.y, s.b.y], linewidth=2, color="k")

# animation function. This is called for each frame, passing an entry in positions
def drawframe(p):
    for i, c in enumerate(circles):
        c.set_center(p[i])
    return circles

anim = animation.FuncAnimation(
    fig,
    drawframe,
    frames=positions[::subsampling],
    interval=dt * subsampling * 1000,
    blit=True,
)

plt.close(fig)
print(f"Rendering {len(positions[::subsampling])} frames at {1/(dt * subsampling)} fps")

output_file = "bouncing_balls.gif"
anim.save(output_file, writer='pillow', fps=1/(dt * subsampling), dpi=dpi)
print(f"Animation saved as {output_file}")