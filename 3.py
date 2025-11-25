import time
import random
import os

# --- 1. CONFIGURATION & PHYSICS CONSTANTS ---
WIDTH = 90
HEIGHT = 30
GRAVITY = -20.0  # Gravity strength
DAMPING = 0.8  # Bounciness (0.8 = loses 20% energy)
FRICTION = 0.99  # Air resistance
DT = 0.04  # Speed of simulation

# ANSI Codes for smooth rendering (No Curses)
CURSOR_HOME = "\033[H"
CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"


class Particle:
    def __init__(self, x, y, vx=0.0, vy=0.0, state="dynamic", char="*"):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.state = state  # 'dynamic' moves, 'static' stays still
        self.char = char

    def update(self, dt):
        if self.state == "static":
            return

        # Apply Physics
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Floor Collision
        if self.y <= 1:
            self.y = 1
            self.vy *= -DAMPING
            self.vx *= FRICTION
            if abs(self.vy) < 1:
                self.vy = 0  # Stop vibrating

        # Ceiling
        if self.y >= HEIGHT - 1:
            self.y = HEIGHT - 1
            self.vy *= -DAMPING

        # Walls
        if self.x <= 1:
            self.x = 1
            self.vx *= -DAMPING
        elif self.x >= WIDTH - 2:
            self.x = WIDTH - 2
            self.vx *= -DAMPING


# --- 2. YOUR MATH FUNCTIONS (Restored) ---


def get_line(start, end):
    # Bresenham's Line Algorithm
    x1, y1 = int(start[0]), int(start[1])
    x2, y2 = int(end[0]), int(end[1])
    points = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append((x1, y1))
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points


def circleBres(xc, yc, r):
    points = []
    x = 0
    y = r
    d = 3 - 2 * r

    def add_octants(xc, yc, x, y):
        return [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x),
        ]

    points.extend(add_octants(xc, yc, x, y))
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        points.extend(add_octants(xc, yc, x, y))
    return list(set(points))


# --- 3. YOUR INSERTION LOGIC (Adapted for Particles) ---


def insertion(vertices, triangles, rectangles, circles, particles_list):
    lines_coords = []

    # 1. Process Triangles
    for i in range(0, len(triangles), 3):
        # A->B, B->C, C->A
        lines_coords.append((vertices[triangles[i]], vertices[triangles[i + 1]]))
        lines_coords.append((vertices[triangles[i + 1]], vertices[triangles[i + 2]]))
        lines_coords.append((vertices[triangles[i + 2]], vertices[triangles[i]]))

    # 2. Process Rectangles
    for i in range(0, len(rectangles), 4):
        # A->B, B->C, C->D, D->A
        lines_coords.append((vertices[rectangles[i]], vertices[rectangles[i + 1]]))
        lines_coords.append((vertices[rectangles[i + 1]], vertices[rectangles[i + 2]]))
        lines_coords.append((vertices[rectangles[i + 2]], vertices[rectangles[i + 3]]))
        lines_coords.append((vertices[rectangles[i + 3]], vertices[rectangles[i]]))

    # 3. Generate Line Particles (Static Walls)
    for start, end in lines_coords:
        line_points = get_line(start, end)
        for p in line_points:
            # Create STATIC particles for lines (walls)
            particles_list.append(Particle(p[0], p[1], state="static", char="#"))

    # 4. Process Circles (Dynamic Objects)
    for i in range(0, len(circles), 3):
        xc, yc, r = circles[i], circles[i + 1], circles[i + 2]
        circle_points = circleBres(xc, yc, r)

        for p in circle_points:
            # Give circles some random velocity so they explode/fall
            vx = random.uniform(-5, 5)
            vy = random.uniform(0, 5)
            # Create DYNAMIC particles for circles
            particles_list.append(
                Particle(p[0], p[1], vx, vy, state="dynamic", char="O")
            )


# --- 4. MAIN LOOP ---


def main():
    # A. Setup Data
    particles = []

    # Vertices (A0, B1, C2, D3) - These form the outer box
    vertices = [
        [1, 1],  # A
        [88, 1],  # B (Width adjusted to fit screen)
        [88, 28],  # C
        [1, 28],  # D
        [45, 15],  # E (Middle point for a triangle example)
        [35, 1],  # F
        [55, 1],  # G
    ]

    # Define Shapes using indices of vertices
    rectangles = [0, 1, 2, 3]  # The outer box
    triangles = [4, 5, 6]  # A triangle inside the box
    circles = [
        20,
        20,
        3,  # Circle 1
        60,
        20,
        4,
    ]  # Circle 2

    # Run your insertion logic
    insertion(vertices, triangles, rectangles, circles, particles)

    # B. Prepare Terminal
    os.system("cls" if os.name == "nt" else "clear")
    print(CURSOR_HIDE, end="")

    empty_row = [" "] * WIDTH

    try:
        while True:
            # 1. Create Grid
            grid = [empty_row[:] for _ in range(HEIGHT)]

            # 2. Physics & Drawing
            for p in particles:
                p.update(DT)

                # Transform Physics Coords to Grid Indices
                # (Invert Y because grid[0] is top, physics 0 is bottom)
                gx = int(p.x)
                gy = int(HEIGHT - 1 - p.y)

                # Boundary Check before drawing
                if 0 <= gy < HEIGHT and 0 <= gx < WIDTH:
                    grid[gy][gx] = p.char

            # 3. Render to String
            output = []
            output.append(CURSOR_HOME)
            output.append(f"Particles: {len(particles)} (Ctrl+C to Quit)\n")
            for row in grid:
                output.append("".join(row))

            print("\n".join(output), end="", flush=True)
            time.sleep(DT)

    except KeyboardInterrupt:
        print(CURSOR_SHOW)
        print("\nDone.")


if __name__ == "__main__":
    main()
