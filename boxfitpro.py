import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Box:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth

class Container:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        self.volume = width * height * depth

def calculate_boxes_in_container(container, boxes):
    total_boxes = 0
    current_arrangement = []

    remaining_volume = container.volume

    # Sort the boxes by volume (largest first) for better packing efficiency.
    sorted_boxes = sorted(boxes, key=lambda b: b.width * b.height * b.depth, reverse=True)

    for box in sorted_boxes:
        box_volume = box.width * box.height * box.depth
        count_for_box = remaining_volume // box_volume
        remaining_volume -= count_for_box * box_volume
        current_arrangement.extend([box] * int(count_for_box))

    if current_arrangement:
        total_boxes += len(current_arrangement)

    return total_boxes, current_arrangement

def display_box_dimensions(box):
    return f"{box.width}x{box.height}x{box.depth} cm"

def display_container_details(container):
    return f"Container dimensions: {container.width}x{container.height}x{container.depth} cm"

def get_percentage_filled(container, arrangement):
    total_volume_filled = sum(box.width * box.height * box.depth for box in arrangement)
    return (total_volume_filled / container.volume) * 100

def visualize_packing(container, arrangement):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    container_vertices = np.array([
        [0, 0, 0],
        [container.width, 0, 0],
        [0, container.height, 0],
        [0, 0, container.depth],
        [container.width, container.height, 0],
        [container.width, 0, container.depth],
        [0, container.height, container.depth],
        [container.width, container.height, container.depth]
    ])

    container_faces = [[container_vertices[j] for j in [0, 1, 4, 2]],
                       [container_vertices[j] for j in [0, 2, 6, 3]],
                       [container_vertices[j] for j in [0, 1, 5, 3]],
                       [container_vertices[j] for j in [1, 4, 7, 5]],
                       [container_vertices[j] for j in [2, 4, 7, 6]],
                       [container_vertices[j] for j in [3, 5, 7, 6]]]

    ax.add_collection3d(Poly3DCollection(container_faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

    # Updated positioning for each box
    for i, box in enumerate(arrangement):
        box_x = (container.width - box.width) * np.random.rand()  # Randomly position along X-axis
        box_y = (container.height - box.height) * np.random.rand()  # Randomly position along Y-axis
        box_z = (container.depth - box.depth) * np.random.rand()  # Randomly position along Z-axis
        ax.bar3d(box_x, box_y, box_z, box.width, box.height, box.depth, shade=True)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Packing Visualization')
    plt.show()

def main():
    print("Welcome to the Advanced 3D Box Packing Algorithm!")

    try:
        container_width = float(input("Enter the container width in cm: "))
        container_height = float(input("Enter the container height in cm: "))
        container_depth = float(input("Enter the container depth in cm: "))
        container = Container(width=container_width, height=container_height, depth=container_depth)

        num_boxes = int(input("Enter the number of box sizes: "))
        boxes = []
        for i in range(num_boxes):
            print(f"Enter dimensions for box {i + 1} (in cm):")
            box_width = float(input("Width: "))
            box_height = float(input("Height: "))
            box_depth = float(input("Depth: "))
            boxes.append(Box(width=box_width, height=box_height, depth=box_depth))

        total_boxes_fit, arrangement = calculate_boxes_in_container(container, boxes)

        print(f"\n{display_container_details(container)}")
        print(f"Total boxes that fit in the container: {total_boxes_fit}")
        print(f"Percentage of container filled: {get_percentage_filled(container, arrangement):.2f}%")

        visualize_packing(container, arrangement)

    except ValueError:
        print("Invalid input. Please enter valid numeric values for dimensions.")

if __name__ == "__main__":
    main()

