import math
import random
from dataclasses import dataclass
from typing import List

@dataclass
class TrackPoint:
    x: float
    y: float
    z: float
    segment_length: float
    slope: float  # fraction (rise/run)
    turning_angle: float # radians
    roughness: float # 0 to 1

class Track:
    def __init__(self, points: List[TrackPoint]):
        self.points = points

    @property
    def total_length(self) -> float:
        return sum(p.segment_length for p in self.points)

    @property
    def total_slope(self) -> float:
        return sum(p.slope for p in self.points)

    @property
    def total_turning_angle(self) -> float:
        return sum(p.turning_angle for p in self.points)

    def is_closed(self, tolerance=1.0) -> bool:
        if not self.points: return False
        start = self.points[0]
        end = self.points[-1] # Actually, the track generated ends at 0,0, but usually points layout is 0..N-1
        # The generator returns points relative to the start/end being closed.
        # Let's check the last point coordinates vs 0 (start).
        # Actually our generator logic forces end to 0,0.
        dist = math.sqrt(end.x**2 + end.y**2 + end.z**2) 
        # But wait, end.z might not be 0 if slope noise didn't perfectly cancel?
        # We enforced slope mean 0, so sum(slope)*len should be 0.
        return dist < tolerance

def _convolve_smooth(data: List[float], window_size: int) -> List[float]:
    """Simple moving average smoothing."""
    result = []
    for i in range(len(data)):
        start = max(0, i - window_size // 2)
        end = min(len(data), i + window_size // 2 + 1)
        window = data[start:end]
        result.append(sum(window) / len(window))
    return result

def generate_track(n_points: int = 1000, total_length: float = 10000.0) -> Track:
    segment_len = total_length / n_points
    
    # --- 1. Slope / Elevation ---
    # Generate random slopes
    raw_slopes = [random.gauss(0, 0.05) for _ in range(n_points)]
    
    # Smooth slopes
    smooth_slopes = _convolve_smooth(raw_slopes, 50)
    
    # Enforce mean 0 (Total Slope = 0)
    avg_slope = sum(smooth_slopes) / len(smooth_slopes)
    slopes = [s - avg_slope for s in smooth_slopes]
    
    # --- 2. Geometry (Turning Angles & Position) ---
    attempt = 0
    max_attempts = 50
    
    final_points = []
    
    while attempt < max_attempts:
        attempt += 1
        
        # Generate random turning angles
        raw_angles = [random.gauss(0, 0.1) for _ in range(n_points)]
        smooth_angles = _convolve_smooth(raw_angles, 50)
        
        # Enforce sum = 0 (for net angle 0)
        avg_angle = sum(smooth_angles) / len(smooth_angles)
        angles = [a - avg_angle for a in smooth_angles]
        
        # Integrate to get position
        xs = [0.0]
        ys = [0.0]
        curr_heading = 0.0
        
        for a in angles:
            curr_heading += a
            xs.append(xs[-1] + segment_len * math.cos(curr_heading))
            ys.append(ys[-1] + segment_len * math.sin(curr_heading))
            
        # Closure Error (end vs start)
        x_err = xs[-1] - xs[0]
        y_err = ys[-1] - ys[0]
        
        # Linear correction
        xs_closed = []
        ys_closed = []
        for i in range(len(xs)):
            factor = i / n_points
            xs_closed.append(xs[i] - x_err * factor)
            ys_closed.append(ys[i] - y_err * factor)
            
        # Recompute turning angles from the closed path
        new_headings = []
        for i in range(len(xs_closed) - 1):
            dx = xs_closed[i+1] - xs_closed[i]
            dy = ys_closed[i+1] - ys_closed[i]
            new_headings.append(math.atan2(dy, dx))
            
        new_turning_angles = []
        for i in range(len(new_headings)):
            if i == 0:
                t = 0.0 
            else:
                diff = new_headings[i] - new_headings[i-1]
                while diff > math.pi: diff -= 2*math.pi
                while diff < -math.pi: diff += 2*math.pi
                t = diff
            new_turning_angles.append(t)
            
        # Check constraints
        sharp_count = sum(1 for a in new_turning_angles if abs(a) > 0.08)
        net_angle = sum(new_turning_angles)
        
        if sharp_count >= 4 and abs(net_angle) < 1.0:
            # Success
            z = 0.0
            
            for i in range(n_points):
                slope = slopes[i]
                z += slope * segment_len
                # Roughness
                r = min(max(random.gauss(0.5, 0.1), 0.0), 1.0)
                
                tp = TrackPoint(
                    x = xs_closed[i+1],
                    y = ys_closed[i+1],
                    z = z,
                    segment_length = segment_len,
                    slope = slope,
                    turning_angle = new_turning_angles[i],
                    roughness = r
                )
                final_points.append(tp)
            
            return Track(final_points)
            
    print("Warning: Could not satisfy all constraints perfectly.")
    return Track(final_points) # Return whatever we got
