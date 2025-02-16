import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as transforms
import numpy as np

def plot_staircase(ax, s1, s2, column_size_mm, length, width):
    """
    Plot a staircase layout within the grid (plan view).
    """
    # Staircase parameters (in meters)
    floor_to_floor_height = 6.0  # m
    riser_height = 0.15  # m
    tread_depth = 0.3  # m
    landing_length = 2  # m
    stair_width = 1.2  # m
    wall_width = 0.2
    Lift_external = 2.5

    # Calculate number of risers and treads
    num_risers = int(floor_to_floor_height / riser_height)
    num_treads_per_flight = (num_risers // 2) - 1

    # First flight of stairs 1
    for i in range(num_treads_per_flight):
        x_start = i * tread_depth + s1 + landing_length + column_size_mm/2
        x_end = x_start + tread_depth
        y_start = s2 - column_size_mm/2 - stair_width - wall_width
        y_end = y_start + stair_width
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)

    # Second flight of stairs 1
    for i in range(num_treads_per_flight):
        x_start = i * tread_depth + s1 + landing_length + column_size_mm/2
        x_end = x_start + tread_depth
        y_start = s2 - column_size_mm/2 - stair_width - stair_width - wall_width - wall_width
        y_end = y_start + stair_width
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)

    # Intermediate landing 1
    landing_start = s1 + column_size_mm/2
    landing_end = landing_start + landing_length
    y_start = s2 - column_size_mm/2 - stair_width - stair_width - wall_width - wall_width
    y_end = s2 - column_size_mm/2
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)

    # 2nd Intermediate landing 1
    landing_start = s1 + column_size_mm/2 + num_treads_per_flight*tread_depth + landing_length
    landing_end = landing_start + landing_length
    y_start = s2 - column_size_mm/2 - stair_width - stair_width - wall_width - wall_width
    y_end = y_start + stair_width + stair_width + wall_width
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)
    
    # Wall1
    wall_end = s1 + column_size_mm/2 + num_treads_per_flight*tread_depth + 2 * landing_length
    wall_start = s1 + column_size_mm/2
    wall_intermediate = s1 + column_size_mm/2 + landing_length
    ywall_start = s2 - column_size_mm/2 - stair_width - stair_width - wall_width - wall_width
    ywall_end = y_start + stair_width + stair_width + wall_width
    ax.plot([wall_start - wall_width, wall_start - wall_width, wall_end + wall_width, wall_end + wall_width, wall_intermediate], [ywall_end, ywall_start - wall_width, ywall_start - wall_width, ywall_end + wall_width, ywall_end + wall_width], color='black', linewidth=0.1)

    # lift1
    corner_x = s1 - column_size_mm/2
    corner_large = s2 + column_size_mm/2
    corner_small = s2 + column_size_mm/2 + wall_width
    ax.plot([corner_x, corner_x-Lift_external, corner_x-Lift_external, corner_x], [corner_large, corner_large, corner_large+Lift_external, corner_large+Lift_external], color='black', linewidth=0.1)
    ax.plot([corner_x, corner_x-Lift_external+wall_width, corner_x-Lift_external+wall_width, corner_x], [corner_small, corner_small, corner_small+Lift_external-wall_width-wall_width, corner_small+Lift_external-wall_width-wall_width], color='black', linewidth=0.1)

    # First flight of stairs 2
    for i in range(num_treads_per_flight):
        x_start = length + s1 - (i * tread_depth) - landing_length
        x_end = x_start - tread_depth
        y_start = width + s2 + column_size_mm/2 + wall_width
        y_end = y_start + stair_width 
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)

    # Second flight of stairs 2
    for i in range(num_treads_per_flight):
        x_start = length + s1 - (i * tread_depth) - landing_length 
        x_end = x_start - tread_depth
        y_start = width + s2 + column_size_mm/2 + wall_width + wall_width + stair_width
        y_end = y_start + stair_width
        ax.plot([x_start, x_end], [y_start, y_start], color='black', linewidth=0.1)
        ax.plot([x_start, x_end], [y_end, y_end], color='black', linewidth=0.1)
        ax.plot([x_start, x_start], [y_start, y_end], color='black', linewidth=0.1)
        
    # Intermediate landing 2
    landing_start = length + s1 - landing_length - column_size_mm/2 + tread_depth
    landing_end = landing_start + landing_length
    y_start = width + s2 + column_size_mm/2 + wall_width + wall_width + stair_width + stair_width
    y_end = width + s2 + column_size_mm/2 + wall_width
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)

    # 2nd Intermediate landing 2
    landing_start = length + s1 - landing_length - column_size_mm/2 + tread_depth - num_treads_per_flight*tread_depth - landing_length
    landing_end = landing_start + landing_length
    y_start = width + s2 + column_size_mm/2 + wall_width + wall_width + stair_width + stair_width
    y_end = width + s2 + column_size_mm/2
    ax.plot([landing_start, landing_end], [y_start, y_start], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_end], [y_end, y_end], color='black', linewidth=0.1)
    ax.plot([landing_start, landing_start], [y_start, y_end], color='black', linewidth=0.1)
    ax.plot([landing_end, landing_end], [y_start, y_end], color='black', linewidth=0.1)
    
     # Wall1
    wall_end = length + s1 - landing_length - column_size_mm/2 + tread_depth - num_treads_per_flight*tread_depth - landing_length + num_treads_per_flight*tread_depth + 2 * landing_length
    wall_start = length + s1 - landing_length - column_size_mm/2 + tread_depth - num_treads_per_flight*tread_depth - landing_length
    wall_intermediate = length + s1 - landing_length - column_size_mm/2 + tread_depth - num_treads_per_flight*tread_depth
    ywall_start = width + s2 + column_size_mm/2
    ywall_end = ywall_start + (2 * stair_width) + (3 * wall_width)
    ax.plot([wall_start - wall_width, wall_start - wall_width, wall_end + wall_width, wall_end + wall_width, wall_intermediate], [ywall_start, ywall_end, ywall_end, ywall_start, ywall_start], color='black', linewidth=0.1)

    # lift2
    corner_x = length + s1 + column_size_mm/2
    corner_large = width + s2 - column_size_mm/2
    corner_small = width + s2 - column_size_mm/2 + wall_width
    ax.plot([corner_x, corner_x+Lift_external, corner_x+Lift_external, corner_x], [corner_large, corner_large, corner_large-Lift_external, corner_large-Lift_external], color='black', linewidth=0.1)
    ax.plot([corner_x, corner_x+Lift_external+wall_width, corner_x+Lift_external+wall_width, corner_x], [corner_small, corner_small, corner_small-Lift_external-wall_width-wall_width, corner_small-Lift_external-wall_width-wall_width], color='black', linewidth=0.1)
    
    
def plot_crane(ax, width, length, s1, s2):
    # Determine number of cranes based on length
    if length <= 31:
        centers = [((length+2*s1) / 2, (width+2*s2) / 2)]
    elif 31 < length <= 61:
        centers = [((length+2*s1) / 3, (width+2*s2) / 2), (2 * (length+2*s1) / 3, (width+2*s2) / 2)]
    elif 61 < length <= 100:
        centers = [((length+2*s1) / 4, (width+2*s2) / 2), ((length+2*s1) / 2, (width+2*s2) / 2), (3 * (length+2*s1) / 4, (width+2*s2) / 2)]

    # Plot each crane
    for center_x, center_y in centers:
        # Define squares (relative to the crane center)
        square_2_3 = np.array([[-1.15, -1.15], [1.15, -1.15], [1.15, 1.15], [-1.15, 1.15], [-1.15, -1.15]]) + [center_x, center_y]
        square_5 = np.array([[-2.5, -2.5], [2.5, -2.5], [2.5, 2.5], [-2.5, 2.5], [-2.5, -2.5]]) + [center_x, center_y]

        # Plot squares
        ax.plot(square_2_3[:, 0], square_2_3[:, 1], color="blue", linewidth=1, label="2.3m Square" if center_x == centers[0][0] else None)
        ax.plot(square_5[:, 0], square_5[:, 1], color="green", linewidth=1, label="5m Square" if center_x == centers[0][0] else None)

        # Draw a cross in the 2.3m square
        ax.plot([center_x - 1.15, center_x + 1.15], [center_y, center_y], color="red", linewidth=1)  # Horizontal line
        ax.plot([center_x, center_x], [center_y - 1.15, center_y + 1.15], color="red", linewidth=1)  # Vertical line

        # Draw two circles (15m and 30m radius) centered at the crane
        circle_15 = plt.Circle((center_x, center_y), 15, color="purple", fill=False, linewidth=1, label="15m Circle" if center_x == centers[0][0] else None)
        circle_20 = plt.Circle((center_x, center_y), 20, color="blue", fill=False, linewidth=1, label="20m Circle" if center_x == centers[0][0] else None)
        circle_25 = plt.Circle((center_x, center_y), 25, color="green", fill=False, linewidth=1, label="25m Circle" if center_x == centers[0][0] else None)
        circle_30 = plt.Circle((center_x, center_y), 30, color="orange", fill=False, linewidth=1, label="30m Circle" if center_x == centers[0][0] else None)
        ax.add_patch(circle_15)
        ax.add_patch(circle_20)
        ax.add_patch(circle_25)
        ax.add_patch(circle_30)
        
        
# Function to create a grid plot based on user inputs
def create_grid_plot(length, width, s1, s2, live_load, selected_column, selected_beam, selected_slab, column_size_mm, column_weight_tonnes, b_s1_mm, d_s1_mm, b_s2_mm, d_s2_mm, b_s3_mm, d_s3_mm, slab_thickness_mm, slab_max_spacing_pt_mm, hcs_slab_thickness_mm):
    
    fig, ax = plt.subplots(figsize=(8, 6))

    # Draw boundary
    ax.plot([0, (length + 2* s1), (length + 2* s1), 0, 0], [0, 0, (width + 2 * s2), (width + 2 * s2), 0], color='black', linewidth=2)

    # Draw grid lines
    for x in np.arange(0, length + 2 * s1, s1):
        ax.axvline(x, color='gray', linestyle='--', linewidth= 0.3, alpha=0.7)
    for y in np.arange(0, width + 2 * s2, s2):
        ax.axhline(y, color='gray', linestyle='--', linewidth= 0.3, alpha=0.7)
    
     # Set primary axis labels (distances) in between grid lines
    xticks = np.arange(s1 / 2, length + 2 * s1, s1)  # Midpoints for X-axis
    yticks = np.arange(s2 / 2, width + 2 * s2, s2)  # Midpoints for Y-axis
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{s1*1000}" for _ in xticks], rotation=90, fontsize=8)  # Distance labels
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{s2*1000}" for _ in yticks], fontsize=8)  # Distance labels
    ax.yaxis.tick_right()


    # Add secondary axis labels (ABCDE and 12345)
    secondary_xticks = np.arange(0, length + 2 * s1, s1)  # Original gridline positions
    secondary_yticks = np.arange(0, width + 2 * s2, s2)  # Original gridline positions
    secondary_horizontal_labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:len(secondary_xticks)]
    secondary_vertical_labels = list(range(1, len(secondary_yticks) + 1))

    # Add secondary labels above the X-axis
    for i, label in enumerate(secondary_horizontal_labels):
        ax.text(
            secondary_xticks[i],
            ax.get_ylim()[1],  # Offset above the axis
            label,
            ha="center",
            va="center",
            fontsize=8,
            color="black"
        )

    # Add secondary labels to the left of the Y-axis
    for i, label in enumerate(secondary_vertical_labels):
        ax.text(
            ax.get_xlim()[0] - 1,  # Offset to the left of the axis
            secondary_yticks[i],
            label,
            ha="center",
            va="center",
            fontsize=8,
            color="black"
        )

    # Remove tick lines
    ax.tick_params(axis="both", which="major", length=0)


    # Set axis limits and labels
    ax.set_xlim(0, length + 2 * s1)
    ax.set_ylim(0, width + 2 * s2)
    ax.set_aspect('equal')
    

    # Plot Columns
    for x in np.arange(s1, length + 2 * s1, s1):
        for y in np.arange(s2, width + 2 * s2, s2):
            ax.fill([
                x - column_size_mm/2, x + column_size_mm/2, x + column_size_mm/2, x - column_size_mm/2, x - column_size_mm/2
            ], [
                y - column_size_mm/2, y - column_size_mm/2, y + column_size_mm/2, y + column_size_mm/2, y - column_size_mm/2
            ], color='black', linewidth=0.3)
    
    if selected_column == "CIS Column":
        column_legend = mpatches.Patch(color='black', label=f"Column {column_size_mm*1000:.0f} x {column_size_mm*1000:.0f}mm ")
        
    if selected_column == "PC Column":
        column_legend = mpatches.Patch(color='black', label=f"PC Column {column_size_mm*1000:.0f} x {column_size_mm*1000:.0f}mm ")
    

            
            
    # Call secondary element plot function
    plot_staircase(ax, s1, s2, column_size_mm, length, width)
    plot_crane(ax, width, length, s1, s2)
    
    # Plot Slab
    if selected_slab == "CIS Slab":
        for x in np.arange(s1, length + s1, s1):
            for y in np.arange(s2, width + s2, s2):        
                ax.text(x + s1/2, y + s2/2, '~', fontsize=8, color='black', ha='center', va='center')
    
        slab_legend = mpatches.Rectangle(
        (0, 0),  # Dummy position
        width = 1,
        height = 0.5,
        edgecolor="black",
        facecolor="none",
        label=f"~ One Way Slab{slab_thickness_mm:.0f} mm"
        )            
    
                
    if selected_slab == "1.2HC Slab":
        # Rectangle dimensions in meters
        rectangle_width = 1.2  # Width of each rectangle in meters
        rectangle_length = s1  # Length of each rectangle in meters

        # Calculate the starting y-coordinate range
        y_positions = np.arange((s2 + 2*column_size_mm), width + s2, s2)  # Midpoints of y-grid

        # Plot rectangles along both axes
        for x in np.arange(s1 * 1.5, length + s1, s1):  # Iterate through x-grid positions
            for y in y_positions:  # Iterate through y-grid positions
                # Number of stacked rectangles
                num_stacked_rectangles = int((s2 -column_size_mm) / rectangle_width)  # Number of rectangles to stack
                
                for i in range(num_stacked_rectangles):  # Iterate for stacking
                    y_offset = i * rectangle_width  # Offset for stacking rectangles
                    
                    # Calculate the coordinates of each rectangle
                    ax.fill(
                        [
                            x - rectangle_length / 2, x + rectangle_length / 2,  # Left and Right x-coordinates
                            x + rectangle_length / 2, x - rectangle_length / 2,  # Close rectangle
                        ],
                        [
                            y - rectangle_width / 2 + y_offset, y - rectangle_width / 2 + y_offset,  # Bottom y-coordinates
                            y + rectangle_width / 2 + y_offset, y + rectangle_width / 2 + y_offset,  # Top y-coordinates
                        ],
                        color="lightgray", edgecolor="black", linewidth=0.5, alpha=0.7
                    )
        
        slab_legend = mpatches.Rectangle(
        (0, 0),  # Dummy position
        width = 1,
        height = 0.5,
        edgecolor="black",
        facecolor="lightgray",
        alpha=0.7,
        label=f"1.2m HCS {hcs_slab_thickness_mm:.0f} mm thick"
        )    
                    
    if selected_slab == "2.4HC Slab":
        # Rectangle dimensions in meters
        rectangle_width = 2.4  # Width of each rectangle in meters
        rectangle_length = s1  # Length of each rectangle in meters

        # Calculate the starting y-coordinate range
        y_positions = np.arange((s2 + 2*column_size_mm), width + s2, s2)  # Midpoints of y-grid

        # Plot rectangles along both axes
        for x in np.arange(s1 * 1.5, length + s1, s1):  # Iterate through x-grid positions
            for y in y_positions:  # Iterate through y-grid positions
                # Number of stacked rectangles
                num_stacked_rectangles = int((s2) / rectangle_width)  # Number of rectangles to stack
                
                for i in range(num_stacked_rectangles):  # Iterate for stacking
                    y_offset = i * rectangle_width  # Offset for stacking rectangles
                    
                    # Calculate the coordinates of each rectangle
                    ax.fill(
                        [
                            x - rectangle_length / 2, x + rectangle_length / 2,  # Left and Right x-coordinates
                            x + rectangle_length / 2, x - rectangle_length / 2,  # Close rectangle
                        ],
                        [
                            y - rectangle_width / 2 + y_offset, y - rectangle_width / 2 + y_offset,  # Bottom y-coordinates
                            y + rectangle_width / 2 + y_offset, y + rectangle_width / 2 + y_offset,  # Top y-coordinates
                        ],
                        color="lightgray", edgecolor="black", linewidth=0.5, alpha=0.7
                    )
                    
        slab_legend = mpatches.Rectangle(
        (0, 0),  # Dummy position
        width = 1,
        height = 0.5,
        edgecolor="black",
        facecolor="lightgray",
        alpha=0.7,
        label=f"2.4m HCS {hcs_slab_thickness_mm:.0f} mm thick"
        )  
        
        
    if selected_slab == "1.2HCS_S3":
        # Rectangle dimensions in meters
        rectangle_width = 1.2  # Width of each rectangle in meters
        rectangle_length = (s1/2)  # Length of each rectangle in meters

        # Calculate the starting y-coordinate range
        y_positions = np.arange((s2 + 2*column_size_mm), width + s2, s2)  # Midpoints of y-grid

        # Plot rectangles along both axes
        for x in np.arange(s1 * 1.5, length + s1, s1/2):  # Iterate through x-grid positions
            for y in y_positions:  # Iterate through y-grid positions
                # Number of stacked rectangles
                num_stacked_rectangles = int((s2 - column_size_mm) / rectangle_width)  # Number of rectangles to stack
                
                for i in range(num_stacked_rectangles):  # Iterate for stacking
                    y_offset = i * rectangle_width  # Offset for stacking rectangles
                    
                    # Calculate the coordinates of each rectangle
                    ax.fill(
                        [
                            x - rectangle_length, x + rectangle_length,  # Left and Right x-coordinates
                            x + rectangle_length, x - rectangle_length,  # Close rectangle
                        ],
                        [
                            y - rectangle_width / 2 + y_offset, y - rectangle_width / 2 + y_offset,  # Bottom y-coordinates
                            y + rectangle_width / 2 + y_offset, y + rectangle_width / 2 + y_offset,  # Top y-coordinates
                        ],
                        color="lightgray", edgecolor="black", linewidth=0.5, alpha=0.7
                    )

        # Add the slab legend
        slab_legend = mpatches.Rectangle(
            (0, 0),  # Dummy position
            width=1,
            height=0.5,
            edgecolor="black",
            facecolor="lightgray",
            alpha=0.7,
            label=f"1.2m HCS {hcs_slab_thickness_mm:.0f} mm thick"
        )

        # Plot the 'S3' columns within the same block
        for x in np.arange(s1, length + s1, s1):
            for y in np.arange(s2, width+s2, s2):        
            
                ax.plot([
                    x - column_size_mm/2 + s1/2, x - column_size_mm/2+ s1/2, x + column_size_mm/2+ s1/2, x + column_size_mm/2+ s1/2, x - column_size_mm/2+ s1/2
                ], [
                    y + column_size_mm/2, y + column_size_mm/2 + s2, y + column_size_mm/2 + s2, y + column_size_mm/2, y + column_size_mm/2
                ], color='black', linewidth=0.3, linestyle=':')

                
    if selected_slab == "PT Flat Slab":
        # Define the slab boundaries based on the grid
        x_min_boundary = s1 - column_size_mm/2
        x_max_boundary = length + s1 + column_size_mm/2
        y_min_boundary = s2 - column_size_mm/2
        y_max_boundary = width + s2 + column_size_mm/2

        # Iterate through grid positions
        for x in np.arange(s1, length + 2 * s1, s1):  # Iterate through x-grid positions
            for y in np.arange(s2, width + 2 * s2, s2):  # Iterate through y-grid positions
                # Calculate the coordinates of the drop panel
                x_min = max(x - column_size_mm, x_min_boundary)  # Ensure the drop panel does not extend beyond the left boundary
                x_max = min(x + column_size_mm, x_max_boundary)  # Ensure the drop panel does not extend beyond the right boundary
                y_min = max(y - column_size_mm, y_min_boundary)  # Ensure the drop panel does not extend beyond the bottom boundary
                y_max = min(y + column_size_mm, y_max_boundary)  # Ensure the drop panel does not extend beyond the top boundary

                # Plot the adjusted drop panel
                ax.plot(
                    [x_min, x_max, x_max, x_min, x_min],  # Adjusted x-coordinates
                    [y_min, y_min, y_max, y_max, y_min],  # Adjusted y-coordinates
                    color='black', linewidth=0.3  # Define the color and line width of the square
                )
                
        slab_legend = mpatches.Rectangle(
        (0, 0),  # Dummy position
        width = 1,
        height = 0.5,
        edgecolor="black",
        facecolor="white",
        label=f"Drop Panel {slab_thickness_mm * 2:.0f} mm thick "
        )  
    
    #label Beams                
    if selected_beam in ["CIS Beam", "PT Beam"]:
        ax.text(length + (0.5*s1), 0.5* s2, f"{b_s1_mm:.0f} × \n {d_s1_mm}(d) mm" ,  # Text content
                fontsize=4,
                color='black',
                ha='center',  # Horizontal alignment
                va='center',  # Vertical alignment
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
        
        ax.text(length + (1.5*s1), 1.5* s2, f"{b_s2_mm:.0f} × \n {d_s2_mm}(d) mm" ,  # Text content
                fontsize=4,
                color='black',
                ha='center',  # Horizontal alignment
                va='center',  # Vertical alignment
                bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
        
            # Plot s1
        for x in np.arange(s1, length+s1, s1):
            for y in np.arange(s2, width + 2*s2, s2):        
            
                ax.plot([
                    x + column_size_mm/2, x + column_size_mm/2, x + s1 - column_size_mm/2, x + s1 - column_size_mm/2, x + column_size_mm/2
                ], [
                    y - column_size_mm/2, y + column_size_mm/2, y + column_size_mm/2, y - column_size_mm/2, y - column_size_mm/2
                ], color='black', linewidth=0.3, linestyle='--')
            
            # Plot s2
        for x in np.arange(s1, length + 2*s1, s1):
            for y in np.arange(s2, width+s2, s2):        
            
                ax.plot([
                    x - column_size_mm/2, x - column_size_mm/2, x + column_size_mm/2, x + column_size_mm/2, x - column_size_mm/2
                ], [
                    y + column_size_mm/2, y + column_size_mm/2 + s2, y + column_size_mm/2 + s2, y + column_size_mm/2, y + column_size_mm/2
                ], color='black', linewidth=0.3, linestyle=':')

    #label Beams                
    if selected_beam in ["PT Flat Slab"]:
        ax.plot([
                    s1- column_size_mm/2, s1- column_size_mm/2, s1 + length + column_size_mm/2, s1 + length + column_size_mm/2, s1- column_size_mm/2
                ], [
                    s2 - column_size_mm/2, s2 + width + column_size_mm/2, s2 + width + column_size_mm/2, s2 - column_size_mm/2, s2 - column_size_mm/2
                ], color='black', linewidth=0.6)

    
    # Add legend with the filled square
    ax.legend(handles=[column_legend, slab_legend], loc='upper left',
    bbox_to_anchor=(0.0, -0.2),  # Place the legend below the plot
    ncol=1,  # Arrange the legend entries in 2 columns
    fontsize=4)
    
    return fig
