"""
L-System Utilities - Usage Examples

This file demonstrates various uses of the L-System utilities module.
"""

import os
from mod import (
    LSystem, LSystemType, ClassicLSystems,
    generate_lsystem, interpret_lsystem, lsystem_to_svg,
    count_characters, get_string_length, analyze_lsystem
)


def example_1_basic_generation():
    """Example 1: Basic L-system generation"""
    print("\n" + "="*60)
    print("Example 1: Basic L-system Generation")
    print("="*60)
    
    # Simple L-system: F -> FF (each iteration doubles the F's)
    lsystem = LSystem(
        axiom="F",
        rules={"F": "FF"},
        angle=90
    )
    
    for i in range(5):
        result = lsystem.generate(i)
        print(f"Iteration {i}: {result} (length: {len(result)})")
    
    print("\nKey insight: Each F doubles, resulting in 2^n growth")


def example_2_koch_curve():
    """Example 2: Koch Curve"""
    print("\n" + "="*60)
    print("Example 2: Koch Curve")
    print("="*60)
    
    koch = ClassicLSystems.koch_curve()
    
    print("Koch curve iterations:")
    for i in range(4):
        result = koch.generate(i)
        f_count = result.count("F")
        print(f"  Iteration {i}: {f_count} line segments")
    
    # Generate SVG
    string = koch.generate(3)
    svg = koch.to_svg(string, width=400, height=200)
    
    # Save to file
    os.makedirs("output", exist_ok=True)
    with open("output/koch_curve.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/koch_curve.svg")


def example_3_koch_snowflake():
    """Example 3: Koch Snowflake"""
    print("\n" + "="*60)
    print("Example 3: Koch Snowflake")
    print("="*60)
    
    snowflake = ClassicLSystems.koch_snowflake()
    
    # Show growth
    for i in range(4):
        string = snowflake.generate(i)
        length = len(string)
        f_count = string.count("F")
        print(f"Iteration {i}: {length} chars, {f_count} line segments")
    
    # Generate SVG
    string = snowflake.generate(4)
    svg = snowflake.to_svg(string, width=600, height=600, 
                           stroke_color="#0066cc", background="#ffffff")
    
    with open("output/koch_snowflake.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/koch_snowflake.svg")


def example_4_sierpinski_triangle():
    """Example 4: Sierpinski Triangle"""
    print("\n" + "="*60)
    print("Example 4: Sierpinski Triangle")
    print("="*60)
    
    st = ClassicLSystems.sierpinski_triangle()
    
    for i in range(5):
        string = st.generate(i)
        f_count = string.count("F")
        g_count = string.count("G")
        print(f"Iteration {i}: F={f_count}, G={g_count}")
    
    string = st.generate(6)
    svg = st.to_svg(string, width=600, height=600,
                    stroke_color="#ff6600", background="#ffffff")
    
    with open("output/sierpinski_triangle.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/sierpinski_triangle.svg")


def example_5_dragon_curve():
    """Example 5: Dragon Curve"""
    print("\n" + "="*60)
    print("Example 5: Dragon Curve")
    print("="*60)
    
    dragon = ClassicLSystems.dragon_curve()
    
    for i in range(12):
        string = dragon.generate(i)
        print(f"Iteration {i}: {len(string)} characters")
    
    string = dragon.generate(12)
    svg = dragon.to_svg(string, width=600, height=400,
                        stroke_color="#9900cc", stroke_width=0.5)
    
    with open("output/dragon_curve.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/dragon_curve.svg")


def example_6_hilbert_curve():
    """Example 6: Hilbert Curve (Space-filling)"""
    print("\n" + "="*60)
    print("Example 6: Hilbert Curve")
    print("="*60)
    
    hilbert = ClassicLSystems.hilbert_curve()
    
    for i in range(6):
        string = hilbert.generate(i)
        f_count = string.count("F")
        print(f"Iteration {i}: {f_count} line segments")
    
    string = hilbert.generate(5)
    svg = hilbert.to_svg(string, width=600, height=600,
                        stroke_color="#006600", stroke_width=1)
    
    with open("output/hilbert_curve.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/hilbert_curve.svg")


def example_7_plant_structures():
    """Example 7: Plant Structures"""
    print("\n" + "="*60)
    print("Example 7: Plant Structures")
    print("="*60)
    
    plants = {
        "simple_plant": ClassicLSystems.plant_simple(),
        "branching_plant": ClassicLSystems.plant_branching(),
        "bushy_tree": ClassicLSystems.tree_bushy(),
        "willow_tree": ClassicLSystems.tree_willow(),
    }
    
    os.makedirs("output/plants", exist_ok=True)
    
    for name, plant in plants.items():
        string = plant.generate(4)
        svg = plant.to_svg(string, width=400, height=400,
                          stroke_color="#228B22", background="#ffffff")
        
        filename = f"output/plants/{name}.svg"
        with open(filename, "w") as f:
            f.write(svg)
        print(f"Saved: {filename}")


def example_8_stochastic_plant():
    """Example 8: Stochastic Plant (Random Variation)"""
    print("\n" + "="*60)
    print("Example 8: Stochastic Plant (Random Variation)")
    print("="*60)
    
    plant = ClassicLSystems.plant_stochastic()
    
    os.makedirs("output/stochastic", exist_ok=True)
    
    # Generate multiple variants with same starting point
    for i in range(5):
        string = plant.generate(5, seed=i*100)
        svg = plant.to_svg(string, width=400, height=400,
                          stroke_color="#228B22", background="#ffffff")
        
        filename = f"output/stochastic/plant_variant_{i+1}.svg"
        with open(filename, "w") as f:
            f.write(svg)
        print(f"Generated variant {i+1}: seed={i*100}")
    
    print("\nEach variant is different but statistically similar!")


def example_9_custom_lsystem():
    """Example 9: Creating Custom L-systems"""
    print("\n" + "="*60)
    print("Example 9: Custom L-systems")
    print("="*60)
    
    # Custom fractal: Quadratic Koch Island variant
    custom = LSystem(
        axiom="F+F+F+F",  # Square
        rules={"F": "F+F-F-FF+F+F-F"},
        angle=90,
        step=10
    )
    
    print("Custom L-system: Quadratic Koch Island Variant")
    print("  Axiom: F+F+F+F (square)")
    print("  Rule: F → F+F-F-FF+F+F-F")
    
    string = custom.generate(2)
    svg = custom.to_svg(string, width=600, height=600,
                       stroke_color="#FF4500", background="#ffffff")
    
    with open("output/custom_fractal.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/custom_fractal.svg")


def example_10_gosper_curve():
    """Example 10: Gosper Curve (Flowsnake)"""
    print("\n" + "="*60)
    print("Example 10: Gosper Curve (Flowsnake)")
    print("="*60)
    
    gosper = ClassicLSystems.gosper_curve()
    
    for i in range(5):
        string = gosper.generate(i)
        print(f"Iteration {i}: {len(string)} characters")
    
    string = gosper.generate(4)
    svg = gosper.to_svg(string, width=800, height=600,
                       stroke_color="#00CED1", stroke_width=1)
    
    with open("output/gosper_curve.svg", "w") as f:
        f.write(svg)
    print("\nSaved: output/gosper_curve.svg")


def example_11_convenience_functions():
    """Example 11: Using Convenience Functions"""
    print("\n" + "="*60)
    print("Example 11: Convenience Functions")
    print("="*60)
    
    # Quick generation
    result = generate_lsystem("F", {"F": "F[+F][-F]"}, 3)
    print(f"Quick generation: {result[:50]}...")
    
    # Quick interpretation
    lines = interpret_lsystem("F+F+F+F", angle=90, step=10)
    print(f"Interpretation: {len(lines)} line segments")
    
    # Quick SVG
    svg = lsystem_to_svg("F", {"F": "FF"}, 5, 90, 5, 400, 300)
    print(f"SVG generated: {len(svg)} bytes")
    
    # Character counting
    counts = count_characters("FF+F-FF+FF-F", "FG+-")
    print(f"Character counts: {counts}")


def example_12_analysis():
    """Example 12: Analyzing L-systems"""
    print("\n" + "="*60)
    print("Example 12: L-system Analysis")
    print("="*60)
    
    # Analyze Koch snowflake
    analysis = analyze_lsystem("F--F--F", {"F": "F+F--F+F"})
    
    print("Koch Snowflake Analysis:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")
    
    # Predict string length
    predicted_length = get_string_length("F", {"F": "F+F--F+F"}, 5)
    print(f"\nPredicted length at iteration 5: {predicted_length}")
    
    # Verify
    actual = generate_lsystem("F", {"F": "F+F--F+F"}, 5)
    print(f"Actual length: {len(actual)}")


def example_13_all_classic_fractals():
    """Example 13: Generate All Classic Fractals"""
    print("\n" + "="*60)
    print("Example 13: All Classic Fractals Gallery")
    print("="*60)
    
    os.makedirs("output/gallery", exist_ok=True)
    
    fractals = [
        ("Koch Curve", ClassicLSystems.koch_curve(), 4),
        ("Koch Snowflake", ClassicLSystems.koch_snowflake(), 4),
        ("Sierpinski Triangle", ClassicLSystems.sierpinski_triangle(), 6),
        ("Dragon Curve", ClassicLSystems.dragon_curve(), 12),
        ("Hilbert Curve", ClassicLSystems.hilbert_curve(), 5),
        ("Levy C Curve", ClassicLSystems.levy_c_curve(), 15),
        ("Gosper Curve", ClassicLSystems.gosper_curve(), 4),
        ("Peao Curve", ClassicLSystems.peano_curve(), 3),
        ("Terdragon", ClassicLSystems.terdragon(), 8),
        ("Sierpinski Arrowhead", ClassicLSystems.sierpinski_arrowhead(), 8),
        ("Minkowski Sausage", ClassicLSystems.minkowski_sausage(), 4),
        ("Cesaro Fractal", ClassicLSystems.cesaro_fractal(), 4),
        ("Quadratic Koch", ClassicLSystems.quadratic_koch(), 3),
        ("Moore Curve", ClassicLSystems.moore_curve(), 4),
    ]
    
    colors = [
        "#E74C3C", "#3498DB", "#2ECC71", "#9B59B6",
        "#F39C12", "#1ABC9C", "#E91E63", "#00BCD4",
        "#FF5722", "#607D8B", "#8BC34A", "#FF9800",
        "#673AB7", "#009688"
    ]
    
    for i, (name, lsystem, iterations) in enumerate(fractals):
        string = lsystem.generate(iterations)
        svg = lsystem.to_svg(string, width=600, height=600,
                           stroke_color=colors[i % len(colors)],
                           stroke_width=1)
        
        safe_name = name.lower().replace(" ", "_")
        filename = f"output/gallery/{safe_name}.svg"
        with open(filename, "w") as f:
            f.write(svg)
        print(f"  {name}: {len(string)} characters")


def example_14_bounds_calculation():
    """Example 14: Calculating Bounds for Scaling"""
    print("\n" + "="*60)
    print("Example 14: Bounds Calculation")
    print("="*60)
    
    fractals = [
        ("Koch Snowflake", ClassicLSystems.koch_snowflake()),
        ("Dragon Curve", ClassicLSystems.dragon_curve()),
        ("Hilbert Curve", ClassicLSystems.hilbert_curve()),
    ]
    
    for name, lsystem in fractals:
        string = lsystem.generate(4)
        bounds = lsystem.get_bounds(string, step=10)
        min_x, min_y, max_x, max_y = bounds
        width = max_x - min_x
        height = max_y - min_y
        print(f"{name}:")
        print(f"  Bounds: ({min_x:.1f}, {min_y:.1f}) to ({max_x:.1f}, {max_y:.1f})")
        print(f"  Size: {width:.1f} x {height:.1f}")


def example_15_customizing_appearance():
    """Example 15: Customizing SVG Appearance"""
    print("\n" + "="*60)
    print("Example 15: Customizing SVG Appearance")
    print("="*60)
    
    dragon = ClassicLSystems.dragon_curve()
    string = dragon.generate(10)
    
    # Various color schemes
    schemes = [
        ("dark", "#00FF00", "#000000"),      # Neon on black
        ("ocean", "#0066CC", "#E6F3FF"),      # Blue on light blue
        ("fire", "#FF4500", "#FFF5EE"),       # Orange-red on seashell
        ("nature", "#228B22", "#F0FFF0"),     # Green on honeydew
        ("royal", "#4B0082", "#FFF8DC"),      # Indigo on cornsilk
    ]
    
    os.makedirs("output/custom_styles", exist_ok=True)
    
    for name, stroke, bg in schemes:
        svg = dragon.to_svg(string, width=600, height=400,
                           stroke_color=stroke, background=bg,
                           stroke_width=0.5)
        
        filename = f"output/custom_styles/dragon_{name}.svg"
        with open(filename, "w") as f:
            f.write(svg)
        print(f"  Created: dragon_{name}.svg")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("L-SYSTEM UTILITIES - COMPREHENSIVE EXAMPLES")
    print("="*60)
    
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    # Run examples
    example_1_basic_generation()
    example_2_koch_curve()
    example_3_koch_snowflake()
    example_4_sierpinski_triangle()
    example_5_dragon_curve()
    example_6_hilbert_curve()
    example_7_plant_structures()
    example_8_stochastic_plant()
    example_9_custom_lsystem()
    example_10_gosper_curve()
    example_11_convenience_functions()
    example_12_analysis()
    example_13_all_classic_fractals()
    example_14_bounds_calculation()
    example_15_customizing_appearance()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("Check the 'output' directory for generated SVG files.")
    print("="*60)


if __name__ == "__main__":
    main()