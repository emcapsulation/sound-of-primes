import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
import math
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from PrimeGenerator import PrimeGenerator


# Graph will stop at x = NUM_X-1
NUM_X = 1001

# Number of segments in the step animation
SEGMENTS = 4


# Create a color map for prime factor counts
def get_color_for_prime_count(count):
    norm = mcolors.Normalize(vmin=1, vmax=10)
    cmap = plt.cm.viridis  
    return cmap(norm(count))


# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_xlim(0, NUM_X)
ax.set_ylim(0, 20)
ax.set_aspect('auto')
ax.tick_params(axis='both', which='both', bottom=False, left=False, color="white", labelcolor="white")


# Inset_axes for frequency chart in bottom right corner
axins = inset_axes(ax, width="30%", height="30%", loc="lower right", borderpad=4)
axins.set_ylim(0, 2)
axins.set_facecolor('black')


# Initialize data for the second figure (column graph)
# 10 bars for 10 prime factors
bar_x = np.arange(1, 11)  
bar_heights = np.zeros(10)
bars = axins.bar(bar_x, bar_heights, color=[get_color_for_prime_count(x) for x in bar_x])
axins.set_xticks(bar_x, color="white")
axins.set_xticklabels(bar_x, color="white")


# Initialise the plot elements
# Store each line segment as a separate Line2D object
lines = []  
caption = ax.text(0.5, 0.95, "", size="20", color='white', ha='center', va='center', transform=ax.transAxes)


# Prepare for the animation
pg = PrimeGenerator()
x_vals = np.arange(2, NUM_X)
factors = [pg.get_prime_factors(x) for x in x_vals]
y_vals = [pg.get_num_prime_factors(x) for x in x_vals]


# Initialise the state of the line
x = 1
y = 0
current_x = 1
current_y = 0
current_max_y = 0
color = ""


def init():
    for line in lines:
        line.set_data([], [])
    caption.set_text('')
    return lines, caption


def animate(i):
    global current_x, current_y, current_max_y, x, y, color

    # Start of a new step
    if i%SEGMENTS == 0:    
        # Get the x value and corresponding number of prime factors
        x = x_vals[math.floor(i/SEGMENTS)]
        y = y_vals[math.floor(i/SEGMENTS)]

        # Update the caption with the factorization
        factorization = ' x '.join(map(str, factors[math.floor(i/SEGMENTS)]))
        caption.set_text(f"{x} = {factorization}")
        caption.set_color(get_color_for_prime_count(y))

        # Get the color for the current step based on the number of prime factors
        color = get_color_for_prime_count(y)    

        # Update the data for the frequency chart
        # Add one to the counts for y prime factors
        bar_heights[y-1] += 1;
        for j, bar in enumerate(bars):
            bar.set_height(bar_heights[j])
        axins.set_ylim(0, max(bar_heights) + 1)
    

    if i%SEGMENTS < SEGMENTS/2:
        # Create the horizontal line segment (move right)
        line = Line2D([current_x, current_x + 2*1/SEGMENTS], [current_y, current_y], color=color, lw=3)
        ax.add_line(line)
        lines.append(line)
        current_x += 2*1/SEGMENTS

        # To scroll the screen: ax.set_xlim(max(0, current_x - 40), current_x + 10)
        ax.set_xlim(0, current_x + 10)
    

    elif i%SEGMENTS >= SEGMENTS/2:
        # Create the vertical line segment (move up)    
        line = Line2D([current_x, current_x], [current_y, current_y + 2*y*1/SEGMENTS], color=color, lw=3)
        ax.add_line(line)
        lines.append(line)
        current_y += 2*y*1/SEGMENTS

        # Update the y-axis limits dynamically to follow the highest point reached
        current_max_y = max(current_max_y, current_y + y)
        ax.set_ylim(0, current_max_y + 5)    
    

    return lines, caption, *bars


# Create the animation
ani = animation.FuncAnimation(fig, animate, frames=len(x_vals)*SEGMENTS, init_func=init, blit=False, interval=320/SEGMENTS)


# Save the animation
# ani.save('out/prime_omega.mp4', writer="ffmpeg")


# Show the plot
plt.get_current_fig_manager().full_screen_toggle()
plt.show()
