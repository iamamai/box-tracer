# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import itertools
import math
import random

######################### FIRST SECTION ###################################
# First section: Create individual legs permutations based on lines that trace the edges of a box

# Define the points
# This block creates a dictionary of 3D points representing the corners of a box
# Points p0-p3 are on z=0 plane, p4-p7 are on z=360 plane
points = {
    'p0': (0, 0, 0),
    'p1': (174.76, 0, 0),
    'p2': (174.76, 442.72, 0),
    'p3': (0, 442.72, 0),
    'p4': (0, 0, 360),
    'p5': (174.76, 0, 360),
    'p6': (174.76, 442.72, 360),
    'p7': (0, 442.72, 360)
}

# Define the connection rules
# This block specifies allowed line connections between points
# 'start' defines initial lines, subsequent entries define possible next lines
# Ensures co-planar connections and specific path constraints
# Using exact rules provided to ensure 198 permutations
rules = {
    'start': [('p0', 'p4'), ('p0', 'p5'), ('p1', 'p5'), ('p1', 'p4')],
    ('p0', 'p4'): [('p4', 'p5'), ('p4', 'p7'), ('p4', 'p6'), ('p4', 'p3')],
    ('p0', 'p5'): [('p5', 'p4'), ('p5', 'p7'), ('p5', 'p6'), ('p5', 'p2')],
    ('p1', 'p4'): [('p4', 'p5'), ('p4', 'p7'), ('p4', 'p6'), ('p4', 'p3')],
    ('p1', 'p5'): [('p5', 'p4'), ('p5', 'p7'), ('p5', 'p6'), ('p5', 'p2')],
    ('p4', 'p5'): [('p5', 'p7'), ('p5', 'p2'), ('p5', 'p6')],
    ('p4', 'p7'): [('p7', 'p6'), ('p7', 'p3'), ('p7', 'p2')],
    ('p4', 'p6'): [('p6', 'p7'), ('p6', 'p2'), ('p6', 'p3')],
    ('p4', 'p3'): [('p3', 'p7'), ('p3', 'p6'), ('p3', 'p2')],
    ('p5', 'p4'): [('p4', 'p7'), ('p4', 'p6'), ('p4', 'p3')],
    ('p5', 'p7'): [('p7', 'p3'), ('p7', 'p6'), ('p7', 'p2')],  # First occurrence
    ('p5', 'p6'): [('p6', 'p7'), ('p6', 'p2'), ('p6', 'p3')],
    ('p5', 'p2'): [('p2', 'p6'), ('p2', 'p7'), ('p2', 'p3')],  # First occurrence
    ('p5', 'p7'): [('p7', 'p6'), ('p7', 'p3'), ('p7', 'p2')],  # Second occurrence
    ('p5', 'p2'): [('p2', 'p6'), ('p2', 'p3'), ('p2', 'p7')],  # Second occurrence
    ('p5', 'p6'): [('p6', 'p2'), ('p6', 'p7'), ('p6', 'p3')],  # Second occurrence
    ('p7', 'p6'): [('p6', 'p2'), ('p6', 'p3')],  # First occurrence
    ('p7', 'p3'): [('p3', 'p2'), ('p3', 'p6')],  # First occurrence
    ('p7', 'p2'): [('p2', 'p6'), ('p2', 'p3')],  # First occurrence
    ('p6', 'p7'): [('p7', 'p3'), ('p7', 'p2')],
    ('p6', 'p2'): [('p2', 'p3')],
    ('p6', 'p3'): [('p3', 'p2'), ('p3', 'p7')],
    ('p4', 'p7'): [('p7', 'p6'), ('p7', 'p3'), ('p7', 'p2')],
    ('p4', 'p6'): [('p6', 'p2'), ('p6', 'p3'), ('p6', 'p7')],
    ('p4', 'p3'): [('p3', 'p7'), ('p3', 'p6'), ('p3', 'p2')],
    ('p2', 'p6'): [('p6', 'p7'), ('p6', 'p3')],  # First occurrence
    ('p2', 'p3'): [('p3', 'p7'), ('p3', 'p6')],  # First occurrence
    ('p2', 'p7'): [('p7', 'p3')],
    ('p7', 'p6'): [('p6', 'p3'), ('p6', 'p2')],  # Second occurrence
    ('p7', 'p3'): [('p3', 'p6'), ('p3', 'p2')],  # Second occurrence
    ('p7', 'p2'): [('p2', 'p3'), ('p2', 'p6')],  # Second occurrence
    ('p2', 'p6'): [('p6', 'p7'), ('p6', 'p3')],  # Second occurrence
    ('p2', 'p3'): [('p3', 'p7'), ('p3', 'p6')],  # Second occurrence
    ('p2', 'p7'): [('p7', 'p3'), ('p7', 'p6')],  # Second occurrence
    ('p3', 'p2'): [('p2', 'p6'), ('p2', 'p7')],
    ('p3', 'p6'): [('p6', 'p2'), ('p6', 'p7')],
    ('p6', 'p3'): [('p3', 'p2'), ('p3', 'p7')],
    ('p3', 'p7'): [('p7', 'p6'), ('p7', 'p2')]
}

# Generate permutations based on the connection rules
# This function creates all possible paths of 3-5 lines following the rules
# Handles duplicate keys by processing all occurrences in sequence
def generate_permutations():
    permutations = []
    for first in rules['start']:
        second_options = rules.get(first, [])
        for second in second_options:
            third_options = rules.get(second, [])
            for third in third_options:
                fourth_options = rules.get(third, [])
                for fourth in fourth_options:
                    fifth_options = rules.get(fourth, [])
                    if fifth_options:
                        for fifth in fifth_options:
                            permutations.append([first, second, third, fourth, fifth])
                    else:
                        permutations.append([first, second, third, fourth])
    return permutations

# Draw a permutation in Rhino with optional rotation and labeling
# This function takes a permutation and draws its lines in Rhino
# Can rotate around p0 if a rotation angle is provided
# Adds a text label if label parameter is provided
# Places lines on "lines" layer and text on "numbers" layer
def draw_permutation(perm, offset_x, offset_y, rotation=0, label=None):
    # Ensure layers exist
    if not rs.IsLayer("lines"):
        rs.AddLayer("lines")
    if not rs.IsLayer("numbers"):
        rs.AddLayer("numbers")
    
    # Set initial layers (will be overridden later)
    rs.CurrentLayer("lines")
    
    lines = []
    center = points['p0']  # Common center point (p0)
    
    for line in perm:
        start = points[line[0]]
        end = points[line[1]]
        
        # Rotate around p0 (center)
        if rotation != 0:
            # Translate to origin
            start_x = start[0] - center[0]
            start_y = start[1] - center[1]
            end_x = end[0] - center[0]
            end_y = end[1] - center[1]
            
            # Convert rotation to radians
            rad = math.radians(rotation)
            
            # Rotate points
            new_start_x = start_x * math.cos(rad) - start_y * math.sin(rad)
            new_start_y = start_x * math.sin(rad) + start_y * math.cos(rad)
            new_end_x = end_x * math.cos(rad) - end_y * math.sin(rad)
            new_end_y = end_x * math.sin(rad) + end_y * math.cos(rad)
            
            # Translate back and apply offset
            start = (new_start_x + center[0] + offset_x, 
                    new_start_y + center[1] + offset_y, 
                    start[2])
            end = (new_end_x + center[0] + offset_x, 
                   new_end_y + center[1] + offset_y, 
                   end[2])
        else:
            # Just apply offset without rotation
            start = (start[0] + offset_x, start[1] + offset_y, start[2])
            end = (end[0] + offset_x, end[1] + offset_y, end[2])
        
        line_id = rs.AddLine(start, end)
        rs.ObjectLayer(line_id, "lines")  # Explicitly set to "lines" layer
        lines.append(line_id)
    
    # Add label at p2 if provided
    if label is not None:
        p2 = points['p2']
        if rotation != 0:
            # Rotate p2 position
            p2_x = p2[0] - center[0]
            p2_y = p2[1] - center[1]
            rad = math.radians(rotation)
            new_p2_x = p2_x * math.cos(rad) - p2_y * math.sin(rad)
            new_p2_y = p2_x * math.sin(rad) + p2_y * math.cos(rad)
            label_pos = (new_p2_x + center[0] + offset_x, 
                        new_p2_y + center[1] + offset_y, 
                        p2[2])
        else:
            label_pos = (p2[0] + offset_x, p2[1] + offset_y, p2[2])
        text_id = rs.AddText(str(label), label_pos, height=100)  # Reduced from 200 to 60 (70% smaller)
        rs.ObjectLayer(text_id, "numbers")  # Set to "numbers" layer
        lines.append(text_id)
    
    group_name = rs.AddGroup()
    if group_name and lines:
        rs.AddObjectsToGroup(lines, group_name)
    return group_name

# Main execution function
# This function orchestrates the creation of both sections
def main():
    # Generate all permutations
    permutations = generate_permutations()
    
    # First section: 20x20 grid of individual permutations
    # Creates a 20x20 grid of individual permutations
    # Spacing: 600mm horizontal, 1000mm vertical
    # Labels each permutation with numbers starting from 1 at p2
    grid_size = 20
    spacing_x = 600
    spacing_y = 1000
    
    for i in range(min(len(permutations), grid_size * grid_size)):
        row = i / grid_size
        col = i % grid_size
        offset_x = col * spacing_x
        offset_y = row * spacing_y
        draw_permutation(permutations[i], offset_x, offset_y, 0, label=i+1)
        
        # Redraw every 10 permutations to show progress in real-time
        if i % 5 == 0:
            rs.Redraw()
    
    print "First section: Generated " + str(len(permutations)) + " permutations"
    print "First section: Displayed " + str(min(len(permutations), grid_size * grid_size)) + " permutations in a " + str(grid_size) + "x" + str(grid_size) + " grid"
    
    ######################### SECOND SECTION ###################################
    # Second section: Combinations of 3 leg permutations with polar array
    # Generate all unique combinations of 3 permutations
    
    # Creates all possible unique combinations of 3 permutations
    # Uses itertools.combinations to ensure no repeats
    all_combinations = list(itertools.combinations(range(len(permutations)), 3))
    
    # Randomly select 100 combinations for display
    perm_combinations = random.sample(all_combinations, min(100, len(all_combinations)))
    
    # Define new grid parameters for second section
    # Sets up a 10x10 grid for the second section
    # Spacing: 1400mm both directions, starts 2000mm right of first grid
    second_grid_size = 10
    second_spacing_x = 1400
    second_spacing_y = 1400
    start_offset_x = grid_size * spacing_x + 2000
    
    # Draws each combination as a polar array (0 deg, 120 deg, 240 deg)
    # Labels each permutation with its original index from Section 1
    for i in range(min(len(perm_combinations), second_grid_size * second_grid_size)):
        row = i / second_grid_size
        col = i % second_grid_size
        offset_x = start_offset_x + col * second_spacing_x
        offset_y = row * second_spacing_y
        
        # Get the three permutations for this combination
        combo = perm_combinations[i]
        perm1 = permutations[combo[0]]
        perm2 = permutations[combo[1]]
        perm3 = permutations[combo[2]]
        
        # Draw each permutation with appropriate rotation and label using original indices
        draw_permutation(perm1, offset_x, offset_y, 0, label=combo[0]+1)
        draw_permutation(perm2, offset_x, offset_y, 120, label=combo[1]+1)
        draw_permutation(perm3, offset_x, offset_y, 240, label=combo[2]+1)
        
        # Redraw after each combination to show progress in real-time
        rs.Redraw()
    
    print "Second section: Generated " + str(len(all_combinations)) + " unique combinations of 3 permutations"
    print "Second section: Displayed " + str(len(perm_combinations)) + " randomly selected sets in a " + str(second_grid_size) + "x" + str(second_grid_size) + " grid"

# Entry point of the script
# Disables redraw for performance, runs main, then re-enables redraw
if __name__ == "__main__":
    rs.EnableRedraw(False)
    main()
    rs.EnableRedraw(True)