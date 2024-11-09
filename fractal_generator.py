"""
Assignment 2: Fractal Generator

Author: Martin Forná

Description:
This script generates fractal patterns using recursive functions and geometric transformations.
"""

# Import necessary libraries
import math
import matplotlib.pyplot as plt
from shapely.geometry import LineString
import random

# Set a seed for the ability to recall previously produced patterns (or let it randomly be chosen)
while True:  
    Seed_input = input("Please input the desired seed, or type ? for a random seed: ")
    if Seed_input.isdigit():
        seed_value = int(Seed_input)      
        break
    elif Seed_input == '?':
        seed_value = random.randint(0,2**16)
        break
    else:
        print("please only input whole numbers or ? as seed value" )

random.seed(seed_value)
print("Seed used this iteration:", seed_value)

# Add attraction point and repulsion field (x,y)
attraction_point = (-200,350) # Point for the L-system to biasly grow towards
repulsion_field_center = (0,120) # Point for the L-system to biasly grow away from
repulsion_field_radius = 75

# Add the probability of the bias (0-0.5 (if one bias is set to 0 the other can be chosen in range 0-1))
attraction_bias = 0.2
repulsion_bias = 0.0

# Global list to store all line segments
line_list = []

def generate_fractal(start_point, angle, length, depth, max_depth, angle_change, length_scaling_factor,branching_factor, branch_probability, attraction_point, attraction_bias, repulsion_field_center, repulsion_bias, repulsion_field_radius):
    """
    Recursive function to generate fractal patterns.

    Parameters:
    - start_point: Tuple (x, y), starting coordinate.
    - angle: Float, current angle in degrees.
    - length: Float, length of the current line segment.
    - depth: Int, current recursion depth.
    - max_depth: Int, maximum recursion depth.
    - angle_change: Float, angle change at each recursion.
    - length_scaling_factor: Float, scaling factor for the length.
    - branching_factor: Float, scaling factor for point along the branch.
    - branch_probability: Float, percentage chance of a branch being generated at a point along a parant branch.
    - attraction_point: Tuple, a point where the tree will biasly grow towards.
    - attraction_bias: Float, the bias from with the tree will be affected by the attraction point.
    - repulsion_field_center: Tuple, a point where the tree will biasly grow away from.
    - Repulsion_bias: Float, the bias from with the tree will be affected by the repulsion point.
    - repulsion_field_radius: Float/Int, radius of the repulsion effect.
    """
    if depth > max_depth:
        return

    # Calculate the end point of the line segment
    end_x = start_point[0] + length * math.cos(math.radians(angle))
    end_y = start_point[1] + length * math.sin(math.radians(angle))
    end_point = (end_x, end_y)
   

    # Create a line segment using Shapely
    line = LineString([start_point, end_point])
    line_list.append((line,depth, max_depth))

    # Calulate the angle of a line towards both the attraction point and the repulsion point
    attraction_angle = math.degrees(math.atan2(attraction_point[1]- end_y, attraction_point[0] - end_x))
    repulsion_angle = math.degrees(math.atan2(end_y - repulsion_field_center[1], end_x - repulsion_field_center[0]))

    # Determine a branch's distance to the repulsion field
    distance_to_repulsion_field = math.sqrt((end_x - repulsion_field_center[0]) ** 2 + (end_y - repulsion_field_center[1]) ** 2)

    # Mix current angle with bias angles based on bias probability and if branches are within range of the force field
    if distance_to_repulsion_field <= repulsion_field_radius:
        bias_angle = angle * (1 - attraction_bias - repulsion_bias) + attraction_angle * attraction_bias + repulsion_angle * repulsion_bias
    else:
        bias_angle = angle * (1 - attraction_bias) + attraction_angle * attraction_bias

    # Update the length for the next recursion
    new_length = length * length_scaling_factor

    # Increment depth
    next_depth = depth + 1

    # Recursive calls for branches
    generate_fractal(end_point, bias_angle + angle_change, new_length, next_depth, max_depth, angle_change, length_scaling_factor, branching_factor, branch_probability, attraction_point, attraction_bias, repulsion_field_center, repulsion_bias, repulsion_field_radius)
    generate_fractal(end_point, bias_angle - angle_change, new_length, next_depth, max_depth, angle_change, length_scaling_factor, branching_factor, branch_probability, attraction_point, attraction_bias, repulsion_field_center, repulsion_bias, repulsion_field_radius)
    
    # Control check if angular changes are behaving as intended (Non-essential)
    # print(f"Depth: {depth}, Bias Angle: {bias_angle}, Angle Change: {angle_change}")

    # Branch at an intermediate point along the segment, if a branch is chosen to be created
    if random.random() < branch_probability:
        branch_x = start_point[0] + branching_factor * (end_x - start_point[0])
        branch_y = start_point[1] + branching_factor * (end_y - start_point[1])
        branch_point = (branch_x, branch_y)
        
        # Recursive call for aditional branches. Only branches to one side which is chosen at random.
        generate_fractal(branch_point, bias_angle + random.uniform(-angle_change, angle_change), new_length, next_depth, max_depth, angle_change, length_scaling_factor, branching_factor, branch_probability, attraction_point, attraction_bias, repulsion_field_center, repulsion_bias, repulsion_field_radius)

# Color map function for the fractal
def get_color(depth, max_depth):
      return plt.cm.autumn(depth / max_depth)


# Main execution
if __name__ == "__main__":
    # Parameters
    start_point = (0, 0)
    initial_angle = 90
    initial_length = 100
    recursion_depth = 0
    max_recursion_depth = 8
    angle_change = random.uniform(5,40)
    length_scaling_factor = random.uniform(0.6, 0.8)
    branching_factor = random.uniform(0.3, 0.7)
    branch_probability = 0.3
    
    # Print the random rolls used for generating the fractal
    print("length_scaling_factor:", length_scaling_factor)
    print("angle_change:", angle_change)


    # Clear the line list
    line_list.clear()

    # Generate the fractal
    generate_fractal(start_point, initial_angle, initial_length, recursion_depth, max_recursion_depth, angle_change, length_scaling_factor, branching_factor, branch_probability, attraction_point, attraction_bias, repulsion_field_center, repulsion_bias, repulsion_field_radius)

    # Visualization
    fig, ax = plt.subplots()
    for line, depth, max_depth in line_list:
        x, y = line.xy
        fractal_color = get_color(depth,max_depth)
        ax.plot(x, y, color=fractal_color, linewidth=1)

    # Optional: Customize the plot
    ax.plot(attraction_point[0],attraction_point[1], 'yo', markersize=5, label = "Attraction point")
    # ax.plot(repulsion_field_center[0],repulsion_field_center[1], 'ko', markersize=5, label = "Repulsion point")
    # ax.set_aspect('equal')
    # repulsion_field = plt.Circle(repulsion_field_center, repulsion_field_radius, color = 'black', alpha = 0.2, linestyle = '--', linewidth = 1, label = "Repulsion Field Area")
    # ax.add_patch(repulsion_field)
    ax.set_aspect('equal')
    plt.axis('off')
    plt.legend(loc=(0.4,0))
    plt.show()

    # Save the figure
    fig.savefig('images/fractal_tree-example_2.png', dpi=300, bbox_inches='tight')