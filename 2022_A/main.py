from track import generate_track

def main():
    # Generate a track with default parameters
    print("Generating track...")
    track = generate_track(n_points=100, total_length=1000) # Reduced points for readable output
    
    print(f"Generated track with {len(track.points)} points.")
    
    # Print the list of points
    # This will print the standard dataclass representation for each point
    print("\nTrack Points:")
    print(track.points)

    # Optional: Print a more formatted table for the first few points
    print("\n(First 5 points details):")
    print(f"{'Index':<6} | {'X':<8} | {'Y':<8} | {'Z':<8} | {'Slope':<8} | {'Angle':<8} | {'Rough':<6}")
    print("-" * 70)
    for i, p in enumerate(track.points[:5]):
        print(f"{i:<6} | {p.x:<8.2f} | {p.y:<8.2f} | {p.z:<8.2f} | {p.slope:<8.4f} | {p.turning_angle:<8.4f} | {p.roughness:<6.2f}")

if __name__ == "__main__":
    main()
