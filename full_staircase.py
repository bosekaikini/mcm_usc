import numpy as np
import plotly.graph_objects as go
import random
from stair_damage_evaluator import evaluate_stair_damage

WIDTH, DEPTH, HEIGHT = 0.30, 0.30, 0.18
GRID_RES = 50 
NUM_STAIRS = 5
NUM_FRAMES = 30
STEPS_PER_FRAME = 50 
MAX_VIS_WEAR = 0.02 
WEAR_RATE = 0.000055

def create_stair_geometry(stair_idx, wear_matrix):
    x_vals = np.linspace(-WIDTH/2, WIDTH/2, GRID_RES)
    y_vals = np.linspace(0, DEPTH, GRID_RES)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    Z_offset = stair_idx * HEIGHT
    Y_offset = stair_idx * DEPTH
    
    Z_surface = (HEIGHT - wear_matrix) + Z_offset
    return X, Y + Y_offset, Z_surface

def get_footprint_impact(X, Y, cx, cy):
    rx, ry = (X - cx) / 0.055, (Y - cy) / 0.125
    R = np.sqrt(rx**2 + ry**2)
    return np.maximum(0, 1 - R)**2

stair_wear_data = [np.zeros((GRID_RES, GRID_RES)) for _ in range(NUM_STAIRS)]
frames = []
total_steps = 0

drift_profiles = [1.5 if (i == 0 or i == NUM_STAIRS-1) else 1.0 for i in range(NUM_STAIRS)]

for f in range(NUM_FRAMES):
    for _ in range(STEPS_PER_FRAME):
        total_steps += 1
        current_x = (np.random.beta(3, 3) - 0.5) * WIDTH 

        for i in range(NUM_STAIRS):
            wobble = np.random.normal(0, 0.02) 
            current_x = np.clip(current_x + wobble, -WIDTH/2, WIDTH/2)
            current_y = np.random.beta(2, 5) * 0.25 
            x_lin = np.linspace(-WIDTH/2, WIDTH/2, GRID_RES)
            y_lin = np.linspace(0, DEPTH, GRID_RES)
            tx, ty = np.meshgrid(x_lin, y_lin)
            rx = (tx - current_x) / 0.055
            ry = (ty - current_y) / 0.125
            R = np.sqrt(rx**2 + ry**2)
            impact = np.maximum(0, 1 - R)**2

            stair_wear_data[i] += (WEAR_RATE * drift_profiles[i]) * impact

    frame_surfaces = []
    current_total_vol = 0
    
    for i in range(NUM_STAIRS):
        X_p, Y_p, Z_p = create_stair_geometry(i, stair_wear_data[i])
        frame_surfaces.append(go.Surface(
            x=X_p, y=Y_p, z=Z_p,
            surfacecolor=stair_wear_data[i],
            colorscale='Magma', cmin=0, cmax=MAX_VIS_WEAR,
            showscale=(i == 0),
            name=f"Stair {i}"
        ))
        current_total_vol += evaluate_stair_damage(X_p, Y_p, Z_p - (i * HEIGHT), HEIGHT)

    status_text = f"Steps: {total_steps} | Total Vol Lost: {current_total_vol:.5f} m3"
    frames.append(go.Frame(data=frame_surfaces, name=str(total_steps),
                           layout=go.Layout(annotations=[dict(text=status_text, x=0, y=1, showarrow=False)])))

initial_data = []
for i in range(NUM_STAIRS):
    X_p, Y_p, Z_p = create_stair_geometry(i, np.zeros((GRID_RES, GRID_RES)))
    initial_data.append(go.Surface(x=X_p, y=Y_p, z=Z_p, colorscale='Magma', cmin=0, cmax=MAX_VIS_WEAR))

fig = go.Figure(data=initial_data, frames=frames)
sliders = [dict(
    steps=[dict(method='animate', args=[[f.name], dict(mode='immediate', frame=dict(duration=0, redraw=True))], label=f.name) for f in frames],
    active=0, transition={'duration': 0}, x=0, len=1.0
)]

fig.update_layout(
    title="Full Staircase Markov Drift Simulation",
    scene=dict(aspectmode="data", camera=dict(eye=dict(x=2, y=-2, z=2))),
    sliders=sliders
)

fig.show()