
import numpy as np
import svgwrite
from svgwrite import cm
import svgutils
import random
from handwriting_synthesis import drawing
from perlin_noise import PerlinNoise
import svgpathtools as svg

import logging
import os


def displace_func(noiseVal, input_filename):
    print('DISPLACING')
    # Initialize Perlin Noise generators for three layers
    noise_layers = {
        # x and y noise for layer 1
        'layer1': [PerlinNoise(octaves=1), PerlinNoise(octaves=1)],
        # x and y noise for layer 2
        'layer2': [PerlinNoise(octaves=4), PerlinNoise(octaves=4)],
        # x and y noise for layer 3
        'layer3': [PerlinNoise(octaves=2), PerlinNoise(octaves=20)]
    }

    def displace_point(pt, scales, noise_scales):
        dx = 0
        dy = 0
        for i, (noise_x, noise_y) in enumerate(noise_layers.values()):
            dx += noise_x([pt.real * noise_scales[i], pt.imag *
                          noise_scales[i]]) * scales[i][0]
            dy += noise_y([pt.imag * noise_scales[i], pt.real *
                          noise_scales[i]]) * scales[i][1]
        return complex(pt.real + dx, pt.imag + dy)

    def displace_path(path, scales, noise_scales):
        new_path = []
        for segment in path:
            if isinstance(segment, (svg.Line, svg.CubicBezier)):
                points = [segment.start, segment.control1, segment.control2, segment.end] if isinstance(
                    segment, svg.CubicBezier) else [segment.start, segment.end]
                displaced_points = [displace_point(
                    pt, scales, noise_scales) for pt in points]
                if isinstance(segment, svg.Line):
                    displaced_segment = svg.Line(
                        displaced_points[0], displaced_points[1])
                else:
                    displaced_segment = svg.CubicBezier(
                        displaced_points[0], displaced_points[1], displaced_points[2], displaced_points[3])
            else:
                displaced_segment = segment  # Add other segments as is
            new_path.append(displaced_segment)
        return svg.Path(*new_path)

    def process_file(input_filename, output_suffix, scales, noise_scales):
        paths, attributes, svg_attributes = svg.svg2paths2(input_filename)

        displaced_paths = []
        for path in paths:
            displaced_path = displace_path(path, scales, noise_scales)
            displaced_paths.append(displaced_path)

        output_filename = f"{input_filename.rsplit('.', 1)[0]}{output_suffix}.{input_filename.rsplit('.', 1)[1]}"

        svg.wsvg(displaced_paths, attributes=attributes,
                 svg_attributes=svg_attributes, filename=output_filename)
        return output_filename

    # Displacement scales and noise scales for each layer
    scales = [
        (5.0, 5.0),  # scale_x and scale_y for layer 1
        (1.0, 1.0),  # scale_x and scale_y for layer 2
        (2.0, 2.0)  # scale_x and scale_y for layer 3
    ]

    noise_scales = [
        0.005 * noiseVal,      # noise_scale for layer 1
        0.004 * noiseVal,       # noise_scale for layer 2
        0.003 * noiseVal        # noise_scale for layer 3
    ]

    # Process the specified input file
    # input_filename = "Letters V2/Adelheids-20th
    # S10_B2_L2_D4_N10_G10.svg"  # Change this to your desired input file
    name = process_file(input_filename, '_displaced', scales, noise_scales)

    # Process the "testLines.svg" file but save it with the input filename's base name and '-test-lines-displaced' suffix
    test_lines_filename = 'testLines.svg'

    # Ensure testLines paths are processed with the same displacement configuration
    paths, attributes, svg_attributes = svg.svg2paths2(test_lines_filename)

    displaced_paths = []
    for path in paths:
        displaced_path = displace_path(path, scales, noise_scales)
        displaced_paths.append(displaced_path)

    # Create the output filename using the original input filename
    output_filename_test_lines = f"{input_filename.rsplit('.', 1)[0]}_test_lines_displaced.{input_filename.rsplit('.', 1)[1]}"
    svg.wsvg(displaced_paths, attributes=attributes,
             svg_attributes=svg_attributes, filename=output_filename_test_lines)

    return name


def _draw(strokes, lines, filename, stroke_colors=None, stroke_widths=None, dither=0, line_height=30, margins=50, line_break=0.5, noiseVal=1):
    print("DRAWING")
    stroke_colors = stroke_colors or ['black'] * len(lines)
    stroke_widths = stroke_widths or [2] * len(lines)
    left_margin = 0
    dwg = svgwrite.Drawing(filename=filename)

    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')
    current_y = 0

    for index, (offsets, line, color, width) in enumerate(zip(strokes, lines, stroke_colors, stroke_widths)):
        random_x = random.randint((-1 * dither), dither)
        random_y = random.randint((-1 * dither), dither)

        if not line:
            current_y -= line_height * line_break
            if index != 0 and index != (len(lines) - 1):
                current_y += line_height * line_break
            continue

        offsets[:, :2] *= 1.5
        strokes = drawing.offsets_to_coords(offsets)
        strokes = drawing.denoise(strokes)
        strokes[:, :2] = drawing.align(strokes[:, :2])
        strokes[:, 1] *= -1
        strokes[:, :2] -= strokes[:, :2].min()
        strokes[:, 0] += left_margin + random_x
        strokes[:, 1] -= current_y

        local_max_x = strokes[:, 0].max()
        local_max_y = strokes[:, 1].max()
        if local_max_x > max_x:
            max_x = local_max_x
        if local_max_y > max_y:
            max_y = local_max_y

        prev_eos = 1.0
        p = "M{},{} ".format(0, 0)
        for x, y, eos in zip(*strokes.T):
            p += '{}{},{} '.format('M' if prev_eos == 1.0 else 'L', x, y)
            prev_eos = eos
        path = svgwrite.path.Path(p)
        path = path.stroke(color=color, width=width,
                           linecap='round').fill("none")
        dwg.add(path)
        current_y -= line_height + random_y

    # Size of generated SVG
    svg_width = max_x - min_x
    svg_height = max_y - min_y
    
    # Desired size
    desired_width = 595
    desired_height = 841

    # Calculate scale (preserve aspect ratio)
    scale = min((desired_width - (2 * margins)) / max_x,
                (desired_height - (2 * margins)) / max_y)

    dwg.viewbox(width=max_x, height=max_y)
    dwg['width'] = f"{max_x}px"
    dwg['height'] = f"{max_y}px"

    # Save the original SVG data first
    dwg.save()

    displaced_file = displace_func(noiseVal, filename)

    # Open the SVG file with svgutils
    SVGfile = svgutils.transform.fromfile(displaced_file)

    max_x = float(SVGfile.width[:-2])
    max_y = float(SVGfile.height[:-2])

    scale = min((desired_width - (2 * margins)) / max_x,
                (desired_height - (2 * margins)) / max_y)

    # # Get the root of the SVG document
    originalSVG = SVGfile.getroot()
    # originalSVG.moveto(min_x * -1, 0)

    # # Scale the SVG elements
    originalSVG.scale(scale)
    originalSVG.moveto(
        margins + (((desired_width - margins - margins) - (max_x * scale))/2), 
        margins)

    # Create a new SVG figure
    figure = svgutils.compose.Figure(
        desired_width, desired_height, originalSVG)

    basename, ext = os.path.splitext(displaced_file)
    newfilename = "{}A4{}".format(basename, ext)
    # Save the new SVG to filename
    figure.save(newfilename)

    # return newfilename
