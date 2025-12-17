import numpy as np
import plotly.graph_objects as go
import random
from stair_damage_evaluator import evaluate_stair_damage

WIDTH = 0.30
DEPTH = 0.30
HEIGHT = 0.18
GRID_RES = 70
NUM_FRAMES = 100
STEPS_PER_FRAME = 15

WEAR_PER_STEP = 0.00025
MAX_VIS_WEAR = 0.02

FOOT_RADIUS = 0.08  
FRONT_BIAS = 0.25  

x_vals = np.linspace(-WIDTH/2, WIDTH/2, GRID_RES)
y_vals = np.linspace(0, DEPTH, GRID_RES)
X, Y = np.meshgrid(x_vals, y_vals)
Total_Wear = np.zeros_like(X)

def select_footstep(center_x, radius):
    left_foot_x = center_x - radius
    right_foot_x = center_x + radius
    
    left_on_stair = -WIDTH/2 <= left_foot_x <= WIDTH/2
    right_on_stair = -WIDTH/2 <= right_foot_x <= WIDTH/2
    
    if left_on_stair and right_on_stair:
        return random.choice([left_foot_x, right_foot_x])
    elif left_on_stair:
        return left_foot_x
    elif right_on_stair:
        return right_foot_x
    else:
        return center_x 

def add_footprint(current_wear, center_x, center_y):
    shoe_width = 0.11 + np.random.uniform(-0.01, 0.01)
    shoe_len = 0.25 + np.random.uniform(-0.02, 0.02)
    
    rx = (X - center_x) / (shoe_width / 2)
    ry = (Y - center_y) / (shoe_len / 2)
    R = np.sqrt(rx**2 + ry**2)
    
    impact = np.maximum(0, 1 - R)**2
    step_wear = WEAR_PER_STEP * impact
    return current_wear + step_wear

frames = []
total_steps_simulated = 0
Z_start = HEIGHT * np.ones_like(X)

def get_wall(x_lin, y_lin, z_top_lin):
    return (np.vstack([x_lin, x_lin]), np.vstack([y_lin, y_lin]), np.vstack([np.zeros_like(z_top_lin), z_top_lin]))

for k in range(NUM_FRAMES):
    last_x, last_y = 0, 0
    for _ in range(STEPS_PER_FRAME):
        center_x = (np.random.beta(3, 3) - 0.5) * WIDTH
        rand_y = np.random.beta(2, 5) * FRONT_BIAS
        rand_x = select_footstep(center_x, FOOT_RADIUS)
        
        Total_Wear = add_footprint(Total_Wear, rand_x, rand_y)
        last_x, last_y = rand_x, rand_y
        total_steps_simulated += 1

    Z_new = HEIGHT - Total_Wear
    max_depth_now = np.max(Total_Wear)

    Xf, Yf, Zf = get_wall(x_vals, np.zeros_like(x_vals), Z_new[0, :])
    Xb, Yb, Zb = get_wall(x_vals, np.full_like(x_vals, DEPTH), Z_new[-1, :])
    Xl, Yl, Zl = get_wall(np.full_like(y_vals, -WIDTH/2), y_vals, Z_new[:, 0])
    Xr, Yr, Zr = get_wall(np.full_like(y_vals, WIDTH/2), y_vals, Z_new[:, -1])

    status_text = (
        f"<b>SIMULATION PROGRESS</b><br>"
        f"Total Steps: <b>{total_steps_simulated}</b><br>"
        f"Max Wear Depth: <b>{(max_depth_now * 1000):.2f} mm</b><br><br>"
        f"<b>Center-Biased Model</b><br>"
        f"Foot Radius: {FOOT_RADIUS:.3f} m<br>"
        f"Front Bias: {FRONT_BIAS:.3f} m<br><br>"
        f"<b>Last Footprint Location:</b><br>"
        f"x_foot: {last_x:.3f} m<br>"
        f"y_foot: {last_y:.3f} m"
    )

    frames.append(go.Frame(
        data=[
            go.Surface(z=Z_new, surfacecolor=Total_Wear, cmin=0, cmax=MAX_VIS_WEAR), 
            go.Surface(z=np.zeros_like(Z_new)),
            go.Surface(z=Zf), go.Surface(z=Zb), go.Surface(z=Zl), go.Surface(z=Zr)
        ],
        layout=go.Layout(annotations=[dict(
            text=status_text,
            align='left', showarrow=False, xref='paper', yref='paper', x=1.0, y=0.9,
            font=dict(family="Courier New", size=14), bgcolor="white", bordercolor="black", borderwidth=1
        )]),
        name=f"{k}"
    ))

Xi, Yi, Zi_wall = get_wall(x_vals, np.zeros_like(x_vals), Z_start[0,:])

init_text = (
    "<b>SIMULATION READY</b><br>Total Steps: 0<br>Max Wear Depth: 0.00 mm<br><br>"
    f"<b>Model:</b> Center & Front-Biased<br>"
    f"Radius: {FOOT_RADIUS:.3f}m, Front: {FRONT_BIAS:.3f}m<br>"
    f"Press Play or Move Slider"
)

fig = go.Figure(
    data=[
        go.Surface(x=X, y=Y, z=Z_start, surfacecolor=np.zeros_like(X), colorscale='Magma', cmin=0, cmax=MAX_VIS_WEAR, name='Top'),
        go.Surface(x=X, y=Y, z=np.zeros_like(X), showscale=False, opacity=0.5, name='Base'),
        go.Surface(x=x_vals, y=np.zeros_like(x_vals), z=Zi_wall, showscale=False, colorscale=[[0,'gray'],[1,'gray']], name='Front'),
        go.Surface(x=x_vals, y=np.full_like(x_vals, DEPTH), z=Zi_wall, showscale=False, colorscale=[[0,'gray'],[1,'gray']], name='Back'),
        go.Surface(x=np.full_like(y_vals, -WIDTH/2), y=y_vals, z=Zi_wall, showscale=False, colorscale=[[0,'gray'],[1,'gray']], name='Left'),
        go.Surface(x=np.full_like(y_vals, WIDTH/2), y=y_vals, z=Zi_wall, showscale=False, colorscale=[[0,'gray'],[1,'gray']], name='Right'),
    ],
    frames=frames
)

sliders = [dict(
    steps=[dict(method='animate', args=[[f'{k}'], dict(mode='immediate', frame=dict(duration=0, redraw=True))], label=f'{k*STEPS_PER_FRAME}') for k in range(NUM_FRAMES)],
    active=0,
    currentvalue=dict(prefix="Total Steps: ", visible=True),
    x=0.1, len=0.9
)]

fig.update_layout(
    title="Stochastic Stair Wear (Center-Biased Distribution)",
    scene=dict(
        xaxis_title="Width", yaxis_title="Depth", zaxis_title="Height",
        aspectmode="data", camera=dict(eye=dict(x=1.6, y=-1.6, z=1.2))
    ),
    sliders=sliders,
    margin=dict(r=250),
    annotations=[dict(
        text=init_text, align='left', showarrow=False, xref='paper', yref='paper', x=1.0, y=0.9,
        font=dict(family="Courier New", size=14), bgcolor="white", bordercolor="black", borderwidth=1
    )]
)

fig.show()

# Evaluate final damage
Z_final = HEIGHT - Total_Wear
volume_lost = evaluate_stair_damage(X, Y, Z_final, HEIGHT)
print(f"Total steps simulated: {total_steps_simulated}")
print(f"Volume of material lost: {volume_lost:.8f} cubic meters")
print(f"Max wear depth: {(np.max(Total_Wear) * 1000):.2f} mm")