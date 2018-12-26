""" Presets library for artmaker/artmangler scripts """

from collections import deque
from copy import deepcopy

import random

from noisemaker.constants import PointDistribution, ValueDistribution, ValueMask

import noisemaker.generators as generators


# Baked presets go here
EFFECTS_PRESETS = {}

PRESETS = {}

# Use a lambda to permit re-eval with new seed
_EFFECTS_PRESETS = lambda: {
    "be-kind-rewind": lambda: extend("crt", {
        "with_vhs": True,
    }),

    "bloom": lambda: {
        "with_bloom": .125 + random.random() * .125,
    },

    "convolution-feedback": lambda: {
        "conv_feedback_alpha": .5,
        "with_conv_feedback": 500,
    },

    "corrupt": lambda: {
        "warp_freq": [random.randint(2, 4), random.randint(1, 3)],
        "warp_octaves": random.randint(1, 3),
        "warp_range": .05 + random.random() * .25,
        "warp_interp": 0,
    },

    "crt": lambda: extend("snow", {
        "with_aberration": .0075 + random.random() * .0075,
        "with_crt": True,
        "with_scan_error": random.randint(0, 1),
    }),

    "density-map": lambda: {
        "invert": 1,
        "with_density_map": True,
    },

    "erosion-worms": lambda: {
        "erosion_worms_alpha": .25 + random.random() * .75,
        "erosion_worms_contraction": .5 + random.random() * .5,
        "erosion_worms_density": random.randint(25, 100),
        "erosion_worms_iterations": random.randint(25, 100),
        "with_erosion_worms": True,
    },

    "extract-derivative": lambda: {
        "deriv": random.randint(1, 3),
    },

    "falsetto": lambda: {
        "with_false_color": True
    },

    "filthy": lambda: {
        "with_grime": True,
        "with_stray_hair": True,
    },

    "funhouse": lambda: {
        "warp_interp": 3,
        "warp_freq": [random.randint(2, 4), random.randint(1, 4)],
        "warp_octaves": random.randint(1, 4),
        "warp_range": .25 + random.random() * .5,
    },

    "glitchin-out": lambda: extend("bloom", "corrupt", "crt", {
        "with_glitch": True,
        "with_ticker": random.randint(0, 1),
    }),

    "glowing-edges": lambda: {
        "with_glowing_edges": 1.0,
    },

    "glyph-map": lambda: {
        "with_glyph_map": "truetype",
    },

    "invert": lambda: {
        "invert": 1,
    },

    "light-leak": lambda: extend("bloom", ["vignette-bright", "vignette-dark"][random.randint(0, 1)], {
        "with_light_leak": .5 + random.random() * .5,
    }),

    "mosaic": lambda: extend("bloom", "voronoi", {
        "voronoi_alpha": .75 + random.random() * .25,
        "with_voronoi": 5,
    }),

    "needs-more-jpeg": lambda: {
        "with_jpeg_decimate": random.randint(10, 25),
    },

    "noirmaker": lambda: extend("bloom", "vignette-dark", {
        "post_contrast": 5,
        "post_saturation": 0,
        "with_dither": .25 + random.random() * .125,
        "with_light_leak": .25 + random.random() * .25,
    }),

    "normals": lambda: {
        "with_normal_map": True,
    },

    "octave-warp": lambda: extend("bloom", {
        "warp_range": random.randint(3, 5),
        "warp_octaves": 3,
        "warp_freq": random.randint(2, 4),
        "with_shadow": random.random(),
    }),

    "one-art-please": lambda: extend("light-leak", {
        "post_contrast": 1.25,
        "post_saturation": .75,
        "with_dither": .25 + random.random() * .125,
    }),

    "pixel-sort": lambda: {
        "with_sort": True
    },

    "pop-art": lambda: {
        "with_pop": True
    },

    "posterize-outline": lambda: {
        "posterize_levels": random.randint(3, 7),
        "with_outline": 1,
    },

    "random-effect": lambda:
        preset(random_member([m for m in EFFECTS_PRESETS if m != "random-effect"])),

    "reflect-domain-warp": lambda: {
        "reflect_range": .125 + random.random() * 2.5,
    },

    "refract-domain-warp": lambda: {
        "refract_range": .125 + random.random() * 2.5,
    },

    "reindex": lambda: {
        "reindex_range": .125 + random.random() * 2.5,
    },

    "reverb": lambda: {
        "reverb_iterations": random.randint(1, 4),
        "with_reverb": random.randint(3, 6),
    },

    "rgb-composite": lambda: {
        "composite_scale": [.5, 1, 2, 4][random.randint(0, 3)],
        "with_composite": True,
    },

    "ripples": lambda: {
        "ripple_freq": random.randint(2, 3),
        "ripple_kink": 2.5 + random.random() * 1.25,
        "ripple_range": .05 + random.random() * .25,
    },

    "shadows": lambda: extend("vignette-dark", {
        "with_shadow": .5 + random.random() * .5,
    }),

    "shake-it-like": lambda: {
        "with_frame": True,
    },

    "snow": lambda: {
        "with_dither": .05 + random.random() * .025,
        "with_snow": .05 + random.random() * .35,
    },

    "sobel-operator": lambda: {
        "invert": random.randint(0, 1),
        "with_sobel": random.randint(1, 3),
    },

    "spooky-ticker": lambda: {
        "with_ticker": True,
    },

    "swerve-h": lambda: {
        "warp_freq": [random.randint(3, 6), 1],
        "warp_octaves": 1,
        "warp_range": 1.0 + random.random(),
    },

    "swerve-v": lambda: {
        "warp_freq": [1, random.randint(3, 6)],
        "warp_octaves": 1,
        "warp_range": 1.0 + random.random(),
    },

    "tensor-tone": lambda: {
        "glyph_map_colorize": random.randint(0, 1),
        "with_glyph_map": "halftone",
    },

    "vignette-bright": lambda: {
        "with_vignette": .5 + random.random() * .5,
        "vignette_brightness": 1,
    },

    "vignette-dark": lambda: {
        "with_vignette": .65 + random.random() * .35,
        "vignette_brightness": 0,
    },

    "voronoi": lambda: {
        "point_distrib": "random" if random.randint(0, 1) else random_member(PointDistribution),
        "point_freq": random.randint(4, 10),
        "voronoi_func": random.randint(1, 3),
        "voronoi_inverse": random.randint(0, 1),
        "voronoi_nth": random.randint(0, 2),
        "with_voronoi": random.randint(0, 6),
    },

    "voronoid": lambda: extend("voronoi", {
        "voronoi_refract": .5 + random.random() * .5,
        "with_voronoi": [1, 3, 6][random.randint(0, 2)]
    }),

    "vortex": lambda: {
        "vortex_range": random.randint(16, 48),
    },

    "wormhole": lambda: {
        "with_wormhole": True,
        "wormhole_stride": .025 + random.random() * .05,
        "wormhole_kink": .5 + random.random(),
    },

    "worms": lambda: {
        "with_worms": random.randint(1, 4),
        "worms_alpha": .75 + random.random() * .25,
        "worms_density": 500,
        "worms_duration": 1,
        "worms_kink": 2.5,
        "worms_stride": 2.5,
        "worms_stride_deviation": 2.5,
    },

}

_PRESETS = lambda: {
    "2001": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 13 * random.randint(10,20),
        "invert": 1,
        "mask": "bank_ocr",
        "posterize_levels": 1,
        "spline_order": 1,
        "vignette_brightness": 1,
        "with_aberration": .0075 + random.random() * .0075,
        "with_vignette": 1,
    }),

    "2d-chess": lambda: {
        "corners": True,
        "distrib": "ones",
        "freq": 8,
        "mask": "chess",
        "point_corners": True,
        "point_distrib": "square",
        "point_freq": 8,
        "spline_order": 0,
        "voronoi_alpha": 0.5 + random.random() * .5,
        "voronoi_nth": random.randint(0, 1) * random.randint(0, 63),
        "with_voronoi": 2 if random.randint(0, 1) else random.randint(1, 5),
    },

    "acid-droplets": lambda: extend("bloom", "density-map", "multires-low", {
        "freq": random.randint(12, 18),
        "hue_range": 0,
        "mask": "sparse",
        "post_hue_rotation": random.random(),
        "post_saturation": .25,
        "reflect_range": .75 + random.random() * .75,
        "ridges": random.randint(0, 1),
        "saturation": 1.5,
        "with_shadow": 1,
        "with_dither": .075 * random.random() * .075,
    }),

    "acid-grid": lambda: extend("bloom", "funhouse", "sobel-operator", "voronoid", {
        "lattice_drift": random.randint(0, 1),
        "point_distrib": random_member(PointDistribution.grid_members()),
        "point_freq": 4,
        "point_generations": 2,
        "voronoi_alpha": .333 + random.random() * .333,
        "voronoi_func": 1,
        "with_voronoi": 2,
    }),

    "acid-wash": lambda: extend("funhouse", "reverb", "symmetry", {
        "hue_range": 1,
        "point_distrib": random_member(PointDistribution.circular_members()),
        "point_freq": random.randint(6, 10),
        "post_ridges": True,
        "ridges": True,
        "saturation": .25,
        "voronoi_alpha": .333 + random.random() * .333,
        "warp_octaves": 8,
        "with_shadow": 1,
        "with_voronoi": 2,
    }),

    "activation-signal": lambda: extend("glitchin-out", {
        "distrib": "ones",
        "freq": 4,
        "mask": "white_bear",
        "rgb": random.randint(0, 1),
        "spline_order": 0,
        "with_vhs": random.randint(0, 1),
    }),

    "alien-terrain-multires": lambda: extend("bloom", "multires", {
        "deriv": 1,
        "deriv_alpha": .333 + random.random() * .333,
        "freq": random.randint(4, 8),
        "invert": random.randint(0, 1),
        "lattice_drift": 1,
        "post_saturation": .075 + random.random() * .075,
        "saturation": 2,
        "with_shadow": .75 + random.random() * .25,
    }),

    "alien-terrain-worms": lambda: extend("bloom", "erosion-worms", "multires-ridged", {
        "deriv": 1,
        "deriv_alpha": 0.25 + random.random() * .125,
        "erosion_worms_alpha": .025 + random.random() * .015,
        "erosion_worms_density": random.randint(150, 200),
        "erosion_worms_inverse": True,
        "erosion_worms_xy_blend": .42,
        "freq": random.randint(3, 5),
        "hue_rotation": .875,
        "hue_range": .25 + random.random() * .25,
        "point_freq": 10,
        "post_contrast": 1.25,
        "post_saturation": .25,
        "saturation": 2,
        "voronoi_alpha": 0.125 + random.random() * .125,
        "voronoi_refract": 0.25 + random.random() * .25,
        "with_dither": .125 + random.random() * .125,
        "with_shadow": .333,
        "with_voronoi": 6,
    }),

    "alien-transmission": lambda: extend("glitchin-out", {
        "distrib": "ones",
        "freq": random.randint(100, 200),
        "invert": random.randint(0, 1),
        "mask": random_member(ValueMask.procedural_members()),
        "reindex_range": .02 + random.random() * .02,
        "spline_order": 2,
    }),

    "analog-glitch": lambda: {
        "deriv": 2,
        "distrib": "ones",
        "freq": 13 * random.randint(10, 25),
        "mask": ["hex", "lcd", "fat_lcd"][random.randint(0, 2)],
        "spline_order": 2,
    },

    "anticounterfeit": lambda: extend("wormhole", {
        "freq": 2,
        "invert": 1,
        "point_freq": 1,
        "voronoi_refract": 1,
        "with_dither": .125,
        "with_fibers": True,
        "with_voronoi": 6,
        "with_watermark": True,
        "wormhole_kink": 6,
    }),

    "are-you-human": lambda: extend("density-map", "funhouse", "multires", "snow", {
        "distrib": "ones",
        "freq": 15,
        "hue_range": random.random() * .25,
        "hue_rotation": random.random(),
        "invert": random.randint(0, 1),
        "mask": "truetype",
        "saturation": random.random() * .125,
        "spline_order": 0,
        "with_aberration": .0075 + random.random() * .0075,
    }),

    "aztec-waffles": lambda: {
        "freq": 7,
        "invert": random.randint(0, 1),
        "point_freq": random.randint(2, 4),
        "point_generations": 2,
        "point_distrib": "circular",
        "posterize_levels": random.randint(6, 18),
        "reflect_range": random.random() * 2,
        "spline_order": 0,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(2, 4),
        "with_outline": 3,
        "with_voronoi": random.randint(1, 5),
    },

    "band-together": lambda: {
        "freq": random.randint(6, 12),
        "reindex_range": random.randint(8, 12),
        "warp_range": 1,
        "warp_octaves": 8,
        "warp_freq": 2,
        "with_shadow": .25 + random.random() * .25,
    },

    "berkeley": lambda: extend("multires-ridged", {
        "freq": random.randint(12, 16),
        "post_ridges": True,
        "reindex_range": .375 + random.random() * .125,
        "rgb": random.randint(0, 1),
        "sin": 2 * random.random() * 2,
        "with_shadow": 1,
    }),

    "bit-by-bit": lambda: extend("bloom", "crt", {
        "distrib": "ones",
        "freq": 6 * random.randint(25, 125),
        "mask": random_member(["binary", "hex", "numeric"]),
        "spline_order": 1,
        "with_shadow": random.random(),
    }),

    "bitmask": lambda: extend("bloom", "multires-low", {
        "distrib": "ones",
        "freq": random.randint(13, 27),
        "mask": random_member(ValueMask.procedural_members()),
        "ridges": True,
        "spline_order": 2,
    }),

    "blacklight-fantasy": lambda: extend("bloom", "sobel-operator", {
        "invert": 1,
        "post_hue_rotation": -.125,
        "posterize_levels": 3,
        "rgb": True,
        "voronoi_func": random.randint(1, 3),
        "voronoi_nth": random.randint(0, 3),
        "voronoi_refract": 1.0 + random.random() * 2.5,
        "warp_octaves": random.randint(1, 4),
        "warp_range": random.randint(0, 1) * random.random() * 2.0,
        "with_dither": .075 + random.random() * .075,
        "with_voronoi": random.randint(1, 7),
    }),

    "blobby": lambda: extend("funhouse", "reverb", {
        "deriv": random.randint(1, 3),
        "distrib": "uniform",
        "freq": random.randint(6, 12) * 2,
        "saturation": .25 + random.random() * .5,
        "hue_range": .25 + random.random() * .5,
        "hue_rotation": random.randint(0, 1) * random.random(),
        "invert": 1,
        "mask": random_member(ValueMask),
        "outline": 1,
        "spline_order": random.randint(2, 3),
        "warp_freq": random.randint(6, 12),
        "warp_interp": random.randint(1, 3),
        "with_shadow": 1,
    }),

    "blockchain-stock-photo-background": lambda: extend("glitchin-out", "vignette-dark", {
        "distrib": "ones",
        "freq": random.randint(20, 30) * 15,
        "mask": ["truetype", "binary", "hex", "numeric"][random.randint(0, 3)],
        "spline_order": random.randint(0, 2),
    }),

    "branemelt": lambda: extend("multires", {
        "freq": random.randint(6, 12),
        "post_reflect_range": .075 + random.random() * .025,
        "sin": random.randint(32, 64),
    }),

    "branewaves": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": random.randint(16, 24) * 2,
        "mask": random_member(ValueMask.grid_members()),
        "ridges": True,
        "ripple_freq": 2,
        "ripple_kink": 1.5 + random.random() * 2,
        "ripple_range": .075 + random.random() * .075,
    }),

    "bringing-hexy-back": lambda: extend("bloom", {
        "lattice_drift": 1,
        "point_distrib": "v_hex" if random.randint(0, 1) else "v_hex",
        "point_freq": 10,
        "post_deriv": random.randint(0, 1) * random.randint(1, 3),
        "voronoi_alpha": 0.5,
        "voronoi_refract": random.randint(0, 1) * random.random(),
        "warp_octaves": 1,
        "warp_range": random.random() * .5,
        "with_voronoi": 5,
    }),

   "broken": lambda: extend("multires-low", {
       "freq": random.randint(3, 4),
       "lattice_drift": 2,
       "post_brightness": .125,
       "post_saturation": .25,
       "posterize_levels": 3,
       "reindex_range": random.randint(3, 4),
       "rgb": True,
       "with_glowing_edges": 1,
       "with_dither": .125 + random.random() * .075,
   }),

    "bubble-machine": lambda: extend("wormhole", {
        "corners": True,
        "distrib": "uniform",
        "freq": random.randint(3, 6) * 2,
        "invert": random.randint(0, 1),
        "mask": ["h_hex", "v_hex"][random.randint(0, 1)],
        "posterize_levels": random.randint(8, 16),
        "reverb_iterations": random.randint(1, 3),
        "spline_order": random.randint(1, 3),
        "with_reverb": random.randint(3, 5),
        "with_outline": 1,
        "wormhole_kink": 1.0 + random.random() * 5,
    }),

    "bubble-multiverse": lambda: extend("bloom", {
        "point_freq": 10,
        "post_hue_rotation": random.random(),
        "post_refract_range": .125 + random.random() * .05,
        "voronoi_refract": 1.25 + random.random() * .5,
        "with_density_map": True,
        "with_shadow": 1.0,
        "with_voronoi": 6,
    }),

    "cell-reflect": lambda: extend("bloom", {
        "invert": random.randint(0, 1),
        "point_freq": random.randint(2, 3),
        "post_deriv": random.randint(1, 3),
        "post_reflect_range": random.randint(2, 4),
        "post_saturation": .5,
        "voronoi_alpha": .333 + random.random() * .333,
        "voronoi_func": random.randint(1, 3),
        "voronoi_nth": random.randint(0, 1),
        "with_density_map": True,
        "with_dither": .075 + random.random() * .075,
        "with_voronoi": 2,
    }),

    "cell-refract": lambda: {
        "point_freq": random.randint(3, 4),
        "post_ridges": True,
        "reindex_range": 1.0 + random.random() * 1.5,
        "rgb": random.randint(0, 1),
        "ridges": True,
        "voronoi_refract": random.randint(8, 12),
        "with_voronoi": 1,
    },

    "cell-refract-2": lambda: extend("bloom", "density-map", "voronoi", {
        "point_freq": random.randint(2, 3),
        "post_deriv": random.randint(0, 3),
        "post_refract_range": random.randint(2, 4),
        "post_saturation": .5,
        "voronoi_alpha": .333 + random.random() * .333,
        "with_dither": .075 + random.random() * .075,
        "with_voronoi": 2,
    }),

    "cell-worms": lambda: extend("bloom", "density-map", "multires-low", "voronoi", {
        "freq": random.randint(3, 7),
        "hue_range": .125 + random.random() * .875,
        "point_distrib": random_member(PointDistribution),
        "point_freq": random.randint(2, 4),
        "post_hue_rotation": random.random(),
        "saturation": .125 + random.random() * .25,
        "voronoi_alpha": .75,
        "with_dither": .125,
        "with_shadow": .75 + random.random() * .25,
        "with_worms": random.randint(1, 5),
        "worms_alpha": .875,
        "worms_density": 1500,
        "worms_kink": random.randint(16, 32),
    }),

    "chiral": lambda: extend("sobel-operator", "symmetry", "voronoi", {
        "point_freq": 1,
        "post_reindex_range": .05,
        "post_refract_range": random.randint(24, 48),
        "voronoi_alpha": .95,
        "with_density_map": True,
        "with_voronoi": 6,
    }),

    "circulent": lambda: extend("invert", "reverb", "symmetry", "voronoi", "wormhole", {
        "point_distrib": random_member(["spiral"] + [m.value for m in PointDistribution.circular_members()]),
        "point_corners": True,
        "voronoi_alpha": .5 + random.random() * .5,
        "wormhole_kink": random.randint(3, 6),
        "wormhole_stride": .05 + random.random() * .05,
    }),

    "conference": lambda: extend("sobel-operator", {
        "distrib": "ones",
        "freq": 5 * random.randint(15, 30),
        "mask": "halftone",
        "spline_order": 2,
    }),

    "cool-water": lambda: extend("bloom", {
        "distrib": "uniform",
        "freq": 16,
        "hue_range": .05 + random.random() * .05,
        "hue_rotation": .5125 + random.random() * .025,
        "lattice_drift": 1,
        "octaves": 4,
        "reflect_range": .333 + random.random() * .333,
        "refract_range": .5 + random.random() * .25,
        "ripple_range": .01 + random.random() * .005,
        "ripple_kink": random.randint(2, 4),
        "ripple_freq": random.randint(2, 4),
        "warp_range": .125 + random.random() * .125,
        "warp_freq": random.randint(2, 3),
    }),

    "corner-case": lambda: extend("bloom", "multires-ridged", {
        "corners": True,
        "freq": random.randint(2, 4),
        "lattice_drift": random.randint(0, 1),
        "saturation": random.randint(0, 1) * random.random() * .25,
        "spline_order": 0,
        "with_density_map": True,
        "with_dither": .25,
    }),

    "crop-spirals": lambda: {
        "distrib": "laplace",
        "freq": random.randint(4, 6) * 2,
        "hue_range": 1,
        "saturation": .75,
        "mask": ["h_hex", "v_hex"][random.randint(0, 1)],
        "reindex_range": .1 + random.random() * .1,
        "spline_order": 2,
        "with_reverb": random.randint(2, 4),
        "with_worms": 3,
        "worms_alpha": .9 + random.random() * .1,
        "worms_density": 500,
        "worms_duration": 1,
        "worms_kink": 2 + random.random(),
        "worms_stride": .333 + random.random() * .333,
        "worms_stride_deviation": .04 + random.random() * .04,
    },

    "cubic": lambda: extend("bloom", {
        "freq": random.randint(2, 5),
        "point_distrib": "concentric",
        "point_freq": random.randint(3, 5),
        "voronoi_alpha": 0.25 + random.random() * .5,
        "voronoi_nth": random.randint(2, 8),
        "with_outline": 1,
        "with_voronoi": random.randint(1, 2),
    }),

    "cyclic-dilation": lambda: {
        "with_voronoi": 2,
        "post_reindex_range": random.randint(4, 6),
        "freq": random.randint(24, 48),
        "hue_range": .25 + random.random() * 1.25,
    },

    "deadbeef": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 6 * random.randint(9, 24),
        "mask": "hex",
        "spline_order": 0,
        "warp_freq": [random.randint(4, 7), random.randint(1, 3)],
        "warp_octaves": random.randint(3, 5),
        "warp_range": .05 + random.random() * .45,
    }),

    "deadlock": lambda: {
        "hue_range": random.random(),
        "hue_rotation": random.random(),
        "saturation": random.random(),
        "point_corners": random.randint(0, 1),
        "point_distrib": random_member(PointDistribution.grid_members()),
        "point_drift": random.randint(0, 1) * random.random(),
        "point_freq": 4,
        "point_generations": 2,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(0, 15),
        "voronoi_alpha": .5 + random.random() * .5,
        "sin": random.random() * 2,
        "with_outline": 3,
        "with_voronoi": 1,
    },

    "death-star-plans": lambda: extend("crt", "sobel-operator", {
        "point_freq": random.randint(2, 4),
        "post_refract_range": random.randint(0, 1),
        "posterize_levels": random.randint(3, 5),
        "voronoi_alpha": 1,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(1, 3),
        "with_voronoi": 1,
    }),

    "defocus": lambda: extend("bloom", "multires", {
        "freq": 12,
        "mask": random_member(ValueMask),
        "sin": 10,
    }),

    "density-wave": lambda: {
        "corners": True,
        "freq": random.randint(2, 4),
        "reflect_range": random.randint(4, 12),
        "saturation": 0,
        "with_density_map": True,
        "with_shadow": 1,
    },

    "different": lambda: extend("multires", {
        "freq": random.randint(8, 12),
        "reflect_range": 1.5 + random.random(),
        "reindex_range": .25 + random.random() * .25,
        "sin": random.randint(15, 25),
        "warp_range": .075 * random.random() * .075,
    }),

    "diffusion-feedback": lambda: extend("bloom", "sobel-operator", {
        "corners": True,
        "distrib": "normal",
        "freq": 8,
        "dla_padding": 5,
        "point_distrib": "square",
        "point_freq": 1,
        "saturation": 0,
        "with_aberration": .005 + random.random() * .005,
        "with_conv_feedback": 125,
        "with_density_map": True,
        "with_dla": .75,
        "with_vignette": .75,
    }),

    "distance": lambda: extend("bloom", "multires", {
        "deriv": random.randint(1, 3),
        "distrib": "exp",
        "lattice_drift": 1,
        "saturation": .06125 + random.random() * .125,
        "with_shadow": 1,
    }),

    "dla-cells": lambda: extend("bloom", {
        "dla_padding": random.randint(2, 8),
        "hue_range": random.random() * 1.5,
        "point_distrib": random_member(PointDistribution),
        "point_freq": random.randint(2, 8),
        "voronoi_alpha": random.random(),
        "with_dla": .5 + random.random() * .5,
        "with_voronoi": random.randint(0, 1) * random.randint(1, 5),
    }),

    "dla-forest": lambda: extend("bloom", {
        "dla_padding": random.randint(2, 8),
        "reverb_iterations": random.randint(2, 4),
        "with_dla": 1,
        "with_reverb": random.randint(3, 6),
    }),

    "domain-warp": lambda: extend("multires-ridged", {
        "post_refract_range": .5 + random.random() * .5,
    }),

    "ears": lambda: {
        "freq": 22,
        "distrib": "uniform",
        "hue_range": random.random() * 2.5,
        "mask": random_member([m.value for m in ValueMask if m.name != "chess"]),
        "with_worms": 3,
        "worms_alpha": .875,
        "worms_density": 188.07,
        "worms_duration": 3.20,
        "worms_stride": 0.40,
        "worms_stride_deviation": 0.31,
        "worms_kink": 6.36,
    },

    "electric-worms": lambda: extend("bloom", "density-map", {
        "blur": 1,
        "freq": random.randint(3, 6),
        "lattice_drift": 1,
        "point_freq": 10,
        "voronoi_alpha": .25 + random.random() * .25,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(0, 3),
        "with_glowing_edges": .75 + random.random() * .25,
        "with_voronoi": 2,
        "with_worms": 5,
        "worms_alpha": .666 + random.random() * .333,
        "worms_density": 1000,
        "worms_duration": 1,
        "worms_kink": random.randint(7, 9),
        "worms_stride_deviation": 16,
    }),

    "emo": lambda: {
        "distrib": "ones",
        "freq": 13 * random.randint(15, 30),
        "mask": "emoji",
        "spline_order": random.randint(0, 2),
        "voronoi_func": random.randint(2, 3),
        "voronoi_refract": .25 + random.random() * .5,
        "with_voronoi": 1,
    },

    "eyes": lambda: {
        "corners": True,
        "distrib": ["ones", "uniform"][random.randint(0, 1)],
        "freq": 12 * random.randint(1, 2),
        "hue_range": random.random(),
        "invert": 1,
        "mask": random_member([m.value for m in ValueMask if m.name != "chess"]),
        "ridges": True,
        "spline_order": random.randint(2, 3),
        "with_outline": 1,
        "warp_freq": 2,
        "warp_octaves": 1,
        "warp_range": random.randint(1, 4),
        "with_shadow": 1,
    },

    "fake-fractal-flame": lambda: extend("bloom", "density-map", "multires-low", {
        "hue_range": random.random(),
        "post_hue_rotation": random.random(),
        "post_saturation": .25 + random.random() * .25,
        "ridges": True,
        "with_aberration": .0075 + random.random() * .0075,
        "with_dither": .075,
        "with_shadow": .75 + random.random() * .25,
        "with_worms": 5,
        "worms_alpha": .975 + random.random() * .025,
        "worms_density": 1500,
        "worms_stride": random.randint(150, 350),
    }),

    "fast-eddies": lambda: extend("bloom", "density-map", {
        "hue_range": .25 + random.random() * .75,
        "hue_rotation": random.random(),
        "octaves": random.randint(1, 3),
        "point_freq": random.randint(2, 10),
        "post_contrast": 1.5,
        "post_saturation": .125 + random.random() * .375,
        "ridges": random.randint(0, 1),
        "voronoi_alpha": .5 + random.random() * .5,
        "voronoi_refract": 2.0,
        "with_dither": .175 + random.random() * .175,
        "with_shadow": .75 + random.random() * .25,
        "with_voronoi": 6,
        "with_worms": 4,
        "worms_alpha": .5 + random.random() * .5,
        "worms_density": 1000,
        "worms_duration": 6,
        "worms_kink": random.randint(125, 375),
    }),

    "figments": lambda: extend("bloom", "funhouse", "multires-low", "wormhole", {
        "freq": 2,
        "hue_range": 2,
        "lattice_drift": 1,
        "voronoi_refract": 1,
        "with_voronoi": 6,
        "wormhole_stride": .05,
        "wormhole_kink": 4,
    }),

    "financial-district": lambda: {
        "point_freq": 2,
        "voronoi_func": 2,
        "voronoi_nth": random.randint(1, 3),
        "with_voronoi": 5,
    },

    "flowbie": lambda: extend("bloom", "wormhole", {
        "freq": random.randint(2, 4),
        "octaves": random.randint(1, 2),
        "with_worms": random.randint(1, 3),
        "refract_range": random.randint(0, 3),
        "wormhole_alpha": .333 + random.random() * .333,
        "wormhole_kink": .25 + random.random() * .25,
        "wormhole_stride": random.random() * 2.5,
        "worms_alpha": .125 + random.random() * .125,
        "worms_stride": .25 + random.random() * .25,
    }),

    "fractal-forms": lambda: extend("bloom", "density-map", "multires-low", {
        "freq": random.randint(2, 3),
        "hue_range": random.random() * 3,
        "saturation": .05,
        "with_dither": .125,
        "with_shadow": .5 + random.random() * .5,
        "with_worms": 4,
        "worms_alpha": .9 + random.random() * .1,
        "worms_density": random.randint(750, 1500),
        "worms_kink": random.randint(256, 512),
    }),

    "fractal-smoke": lambda: extend("bloom", "density-map", "multires-low", {
        "freq": random.randint(2, 4),
        "hue_range": random.random() * 3,
        "saturation": .05,
        "with_dither": .125,
        "with_shadow": .5 + random.random() * .5,
        "with_worms": 4,
        "worms_alpha": .9 + random.random() * .1,
        "worms_density": random.randint(750, 1500),
        "worms_stride": random.randint(128, 256),
    }),

    "fractile": lambda: extend("bloom", "symmetry", {
        "point_distrib": random_member(PointDistribution.grid_members()),
        "point_freq": random.randint(2, 10),
        "reverb_iterations": random.randint(2, 4),
        "voronoi_alpha": min(.75 + random.random() * .5, 1),
        "voronoi_func": random.randint(1, 3),
        "voronoi_nth": random.randint(0, 3),
        "with_reverb": random.randint(4, 8),
        "with_voronoi": random.randint(1, 5),
    }),

    "fundamentals": lambda: extend("density-map", {
        "freq": random.randint(3, 5),
        "point_freq": random.randint(3, 5),
        "post_deriv": random.randint(1, 3),
        "post_saturation": .333 + random.random() * .333,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(3, 5),
        "voronoi_refract": .125 + random.random() * .125,
        "with_voronoi": 2,
        "with_dither": .175 + random.random() * .175,
    }),

    "funky-glyphs": lambda: {
        "distrib": ["ones", "uniform"][random.randint(0, 1)],
        "freq": 20 * random.randint(1, 3),
        "mask": [
            "binary",
            "numeric",
            "hex",
            "lcd",
            "lcd_binary",
            "fat_lcd",
            "fat_lcd_binary",
            "fat_lcd_numeric",
            "fat_lcd_hex"
        ][random.randint(0, 8)],
        "octaves": random.randint(1, 2),
        "post_refract_range": .125 + random.random() * .125,
        "spline_order": random.randint(1, 3),
    },

    "fuzzy-squares": lambda: {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(6, 24) * 2,
        "mask": random_member(ValueMask),
        "post_contrast": 1.5,
        "spline_order": 1,
        "with_worms": 5,
        "worms_alpha": 1,
        "worms_density": 1000,
        "worms_duration": 2.0,
        "worms_stride": .75 + random.random() * .75,
        "worms_stride_deviation": random.random(),
        "worms_kink": 1 + random.random() * 5.0,
    },

    "fuzzy-swirls": lambda: {
        "freq": random.randint(2, 32),
        "hue_range": random.random() * 2,
        "point_freq": random.randint(8, 10),
        "spline_order": random.randint(1, 3),
        "voronoi_alpha": 0.5 * random.random() * .5,
        "with_voronoi": 6,
        "with_worms": random.randint(1, 4),
        "worms_density": 64,
        "worms_duration": 1,
        "worms_kink": 25,
    },

    "fat-led": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 10 * random.randint(25, 40),
        "mask": ["fat_lcd", "fat_lcd_binary", "fat_lcd_numeric", "fat_lcd_hex"][random.randint(0, 3)],
        "spline_order": random.randint(1, 2),
    }),

    "fuzzy-thorns": lambda: {
        "point_freq": random.randint(2, 4),
        "point_distrib": "waffle",
        "point_generations": 2,
        "voronoi_inverse": True,
        "voronoi_nth": random.randint(6, 12),
        "with_voronoi": 2,
        "with_worms": random.randint(1, 3),
        "worms_density": 500,
        "worms_duration": 1.22,
        "worms_kink": 2.89,
        "worms_stride": 0.64,
        "worms_stride_deviation": 0.11,
    },

    "galalaga": lambda: extend("crt", {
        "distrib": ["ones", "uniform"][random.randint(0, 1)],
        "freq": 6 * random.randint(1, 3),
        "glyph_map_zoom": 1.0 + random.random() * 10.0,
        "hue_range": random.random() * 2.5,
        "mask": "invaders_square",
        "posterize_levels": 6,
        "spline_order": 0,
        "with_glowing_edges": .125 + random.random() * .125,
        "with_glyph_map": "invaders_square",
    }),

    "game-show": lambda: extend("be-kind-rewind", {
        "distrib": "normal",
        "freq": random.randint(8, 16) * 2,
        "mask": ["h_tri", "v_tri"][random.randint(0, 1)],
        "posterize_levels": random.randint(2, 5),
        "spline_order": 2,
    }),

    "glass-onion": lambda: {
        "point_freq": random.randint(3, 6),
        "post_deriv": random.randint(1, 3),
        "post_refract_range": .75 + random.random() * .5,
        "voronoi_inverse": random.randint(0, 1),
        "with_reverb": random.randint(3, 5),
        "with_voronoi": 2,
    },

    "globules": lambda: extend("multires-low", {
        "distrib": "ones",
        "freq": random.randint(6, 12),
        "hue_range": .25 + random.random() * .5,
        "lattice_drift": 1,
        "mask": "sparse",
        "reflect_range": 1,
        "saturation": .175 + random.random() * .175,
        "with_density_map": True,
        "with_shadow": 1,
    }),

    "glom": lambda: extend("bloom", {
        "freq": 2,
        "hue_range": .25 + random.random() * .25,
        "lattice_drift": 1,
        "octaves": 2,
        "post_reflect_range": random.randint(1, 2),
        "post_refract_range": random.randint(1, 2),
        "reflect_range": random.randint(1, 2) * .25,
        "refract_range": random.randint(1, 2) * .25,
        "warp_range": .25 + random.random() * .25,
        "warp_octaves": 1,
        "with_shadow": .75 + random.random() * .25,
    }),

    "graph-paper": lambda: extend("bloom", "crt", "sobel-operator", {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(4, 12) * 2,
        "hue_range": 0,
        "hue_rotation": random.random(),
        "saturation": 0.27,
        "mask": "chess",
        "spline_order": 0,
        "voronoi_alpha": .25 + random.random() * .75,
        "voronoi_refract": random.random() * 4,
        "with_voronoi": 6,
    }),

    "gravy": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 24 * random.randint(2, 6),
        "mask": random_member(ValueMask),
        "post_deriv": 2,
        "spline_order": random.randint(1, 2),
        "warp_range": .25 + random.random() * .5,
        "warp_octaves": 3,
        "warp_freq": random.randint(2, 4),
        "warp_interp": 3,
    }),

    "hairy-diamond": lambda: {
        "erosion_worms_alpha": .75 + random.random() * .25,
        "erosion_worms_contraction": .5 + random.random(),
        "erosion_worms_density": random.randint(25, 50),
        "erosion_worms_iterations": random.randint(25, 50),
        "freq": random.randint(2, 6),
        "hue_range": random.random(),
        "hue_rotation": random.random(),
        "saturation": random.random(),
        "point_corners": True,
        "point_distrib": random_members(PointDistribution.circular_members()),
        "point_freq": random.randint(3, 6),
        "point_generations": 2,
        "spline_order": random.randint(0, 3),
        "voronoi_func": random.randint(2, 3),
        "voronoi_inverse": True,
        "voronoi_alpha": .25 + random.random() * .5,
        "with_erosion_worms": True,
        "with_voronoi": [1, 6][random.randint(0, 1)],
    },

    "halt-catch-fire": lambda: extend("glitchin-out", "multires-low", {
        "freq": 2,
        "hue_range": .05,
        "lattice_drift": 1,
        "spline_order": 0,
    }),

    "hex-machine": lambda: extend("multires", {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(1, 3) * 2,
        "mask": "h_tri",
        "post_deriv": 3,
        "sin": random.randint(-25, 25),
    }),

    "hsv-gradient": lambda: {
        "freq": random.randint(2, 3),
        "hue_range": .125 + random.random() * 2.0,
        "lattice_drift": random.random(),
    },

    "hydraulic-flow": lambda: extend("bloom", "multires", {
        "deriv": random.randint(0, 1),
        "deriv_alpha": .25 + random.random() * .25,
        "distrib": random_member([m for m in ValueDistribution if m.name not in ("ones", "mids")]),
        "erosion_worms_alpha": .125 + random.random() * .125,
        "erosion_worms_contraction": .75 + random.random() * .5,
        "erosion_worms_density": random.randint(5, 250),
        "erosion_worms_iterations": random.randint(50, 250),
        "freq": random.randint(2, 3),
        "hue_range": random.random(),
        "invert": random.randint(0, 1),
        "refract_range": random.random() * 2,
        "ridges": random.randint(0, 1),
        "rgb": random.randint(0, 1),
        "saturation": random.random(),
        "with_dither": .125,
        "with_erosion_worms": True,
        "with_density_map": True,
        "with_shadow": 1,
    }),

    "i-dream-of-tweegee": lambda: {
        "reindex_range": 2,
        "point_corners": True,
        "point_freq": 2,
        "point_distrib": "square",
        "post_reindex_range": 2,
        "rgb": True,
        "voronoi_alpha": .625,
        "with_voronoi": 4,
    },

    "inkling": lambda: extend("density-map", {
        "distrib": "ones",
        "freq": random.randint(4, 8),
        "mask": "sparse",
        "point_freq": 4,
        "post_refract_range": .125 + random.random() * .05,
        "post_saturation": 0,
        "post_contrast": 10,
        "ripple_range": .025 + random.random() * .0125,
        "voronoi_refract": .5 + random.random() * .25,
        "with_dither": .175,
        "with_fibers": True,
        "with_grime": True,
        "with_voronoi": 6,
    }),

    "interference": lambda: extend("symmetry", {
        "sin": random.randint(250, 500),
        "with_interference": True
    }),

    "isoform": lambda: extend("bloom", {
        "hue_range": random.random(),
        "invert": random.randint(0, 1),
        "post_deriv": random.randint(0, 1) * random.randint(1, 3),
        "post_refract_range": .25 + random.random() * .25,
        "ridges": random.randint(0, 1),
        "voronoi_alpha": .75 + random.random() * .25,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(0, 1),
        "with_outline":  random.randint(1, 3),
        "with_voronoi": random.randint(1, 2),
    }),

    "jovian-clouds": lambda: {
        "point_freq": 10,
        "voronoi_refract": 2,
        "with_voronoi": 6,
        "with_worms": 4,
        "worms_density": 500,
        "worms_duration": 0.5,
        "worms_kink": 96,
    },

    "just-refracts-maam": lambda: {
        "corners": True,
        "freq": random.randint(2, 3),
        "post_refract_range": random.randint(0, 1),
        "post_ridges": random.randint(0, 1),
        "refract_range": random.randint(4, 8),
        "ridges": random.randint(0, 1),
        "with_shadow": random.randint(0, 1),
    },

    "knotty-clouds": lambda: extend("bloom", {
        "point_freq": random.randint(6, 10),
        "voronoi_alpha": .125 + random.random() * .25,
        "with_shadow": 1,
        "with_voronoi": 2,
        "with_worms": 1,
        "worms_alpha": .666 + random.random() * .333,
        "worms_density": 1000,
        "worms_duration": 1,
        "worms_kink": 4,
    }),

    "later": lambda: extend("multires", {
        "distrib": "ones",
        "freq": random.randint(8, 16),
        "mask": random_member(ValueMask.procedural_members()),
        "point_freq": random.randint(4, 8),
        "spline_order": 0,
        "voronoi_refract": random.randint(1, 4),
        "warp_freq": random.randint(2, 4),
        "warp_interp": 3,
        "warp_octaves": 2,
        "warp_range": .25 + random.random() * .125,
        "with_glowing_edges": 1,
        "with_voronoi": 6,
    }),

    "lattice-noise": lambda: extend("density-map", {
        "deriv": random.randint(1, 3),
        "freq": random.randint(5, 12),
        "octaves": random.randint(1, 3),
        "post_deriv": random.randint(1, 3),
        "ridges": random.randint(0, 1),
        "saturation": random.random(),
        "with_dither": .125,
        "with_shadow": random.random(),
    }),

    "lcd": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 40 * random.randint(1, 4),
        "invert": 1,
        "mask": ["lcd", "lcd_binary"][random.randint(0, 1)],
        "saturation": .05,
        "spline_order": random.randint(0, 3),
        "with_shadow": random.random(),
    }),

    "led": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 40 * random.randint(1, 4),
        "mask": ["lcd", "lcd_binary"][random.randint(0, 1)],
        "spline_order": random.randint(0, 3),
    }),

    "lightcycle-derby": lambda: extend("bloom", {
        "freq": random.randint(16, 32),
        "rgb": random.randint(0, 1),
        "spline_order": 0,
        "lattice_drift": 1,
        "with_erosion_worms": True,
    }),

    "magic-squares": lambda: extend("bloom", "multires-low", {
        "channels": 3,
        "distrib": random_member([m.value for m in ValueDistribution if m.name not in ("ones", "mids")]),
        "edges": .25 + random.random() * .5,
        "freq": [9, 12, 15, 18][random.randint(0, 3)],
        "hue_range": random.random() * .5,
        "point_distrib": random_member([m.value for m in PointDistribution.grid_members()]),
        "point_freq": [3, 6, 9][random.randint(0, 2)],
        "spline_order": 0,
        "voronoi_alpha": .25,
        "with_dither": random.randint(0, 1) * random.random() * .125,
        "with_voronoi": random.randint(0, 1) * 4,
    }),

    "magic-smoke": lambda: {
        "freq": random.randint(2, 4),
        "octaves": random.randint(1, 3),
        "with_worms": random.randint(1, 2),
        "worms_alpha": 1,
        "worms_density": 750,
        "worms_duration": .25,
        "worms_kink": random.randint(1, 3),
        "worms_stride": random.randint(64, 256),
    },

    "mcpaint": lambda: {
        "corners": True,
        "distrib": ["ones", "uniform", "normal"][random.randint(0, 2)],
        "freq": random.randint(2, 8),
        "glyph_map_colorize": random.randint(0, 1),
        "glyph_map_zoom": random.randint(3, 6),
        "mask": "mcpaint",
        # "posterize_levels": 12,
        "spline_order": 2,
        "vortex": 10,
        "with_glyph_map": "mcpaint",
    },

    "misaligned": lambda: extend("multires", {
        "distrib": random_member(ValueDistribution),
        "freq": random.randint(12, 24),
        "mask": random_member(ValueMask),
        "spline_order": 0,
        "with_outline": 1,
    }),

    "moire-than-a-feeling": lambda: extend("wormhole", {
        "freq": random.randint(2, 4),
        "octaves": random.randint(1, 2),
        "point_freq": random.randint(1, 3),
        "saturation": 0,
        "with_density_map": True,
        "with_voronoi": random.randint(0, 1),
        "wormhole_kink": 128,
        "wormhole_stride": .0005,
    }),

    "multires": lambda: {
        "octaves": random.randint(4, 8),
    },

    "multires-low": lambda: {
        "octaves": random.randint(2, 4),
    },

    "multires-ridged": lambda: extend("multires", {
        "ridges": True
    }),

    "multires-voronoi-worms": lambda: {
        "point_freq": random.randint(8, 10),
        "reverb_ridges": False,
        "with_reverb": 2,
        "with_voronoi": [0, 1, 6][random.randint(0, 2)],
        "with_worms": 1,
        "worms_density": 1000,
    },

    "muppet-skin": lambda: extend("bloom", {
        "freq": random.randint(2, 3),
        "hue_range": random.random() * .5,
        "lattice_drift": random.randint(0, 1) * random.random(),
        "with_worms": 3 if random.randint(0, 1) else 1,
        "worms_alpha": .75 + random.random() * .25,
        "worms_density": 500,
    }),

    "nerdvana": lambda: extend("bloom", "density-map", "symmetry", {
        "point_distrib": random_member(PointDistribution.circular_members()),
        "point_freq": random.randint(5, 10),
        "reverb_ridges": False,
        "with_voronoi": 2,
        "with_reverb": 2,
        "voronoi_nth": 1,
    }),

    "neon-cambrian": lambda: extend("bloom", "sobel-operator", "wormhole", {
        "hue_range": 1,
        "posterize_levels": 24,
        "with_aberration": 0.01,
        "with_voronoi": 6,
        "wormhole_stride": 0.25,
    }),

    "neon-plasma": lambda: extend("multires", {
        "channels": 3,
        "freq": random.randint(2, 5),
        "lattice_drift": random.randint(0, 1),
        "ridges": True,
    }),

    "noise-blaster": lambda: extend("multires", {
        "freq": random.randint(3, 4),
        "lattice_drift": 1,
        "post_reindex_range": 2,
        "reindex_range": 4,
        "with_shadow": .25 + random.random() * .25,
    }),

    "now": lambda: extend("multires-low", {
        "channels": 3,
        "freq": random.randint(3, 10),
        "hue_range": random.random(),
        "saturation": .5 + random.random() * .5,
        "lattice_drift": random.randint(0, 1),
        "point_freq": random.randint(3, 10),
        "spline_order": 0,
        "voronoi_refract": random.randint(1, 4),
        "warp_freq": random.randint(2, 4),
        "warp_interp": 3,
        "warp_octaves": 1,
        "warp_range": .075 + random.random() * .075,
        "with_outline": 1,
        "with_voronoi": 6,
    }),

    "numberwang": lambda: extend("bloom", {
        "distrib": "ones",
        "freq": 6 * random.randint(15, 30),
        "mask": "numeric",
        "spline_order": random.randint(0, 2),
        "warp_range": .5 + random.random() * 1.5,
        "warp_freq": random.randint(2, 4),
        "warp_interp": 3,
        "warp_octaves": 1,
        "with_false_color": True
    }),

    "octave-rings": lambda: extend("sobel-operator", {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(1, 3) * 2,
        "mask": "waffle",
        "octaves": random.randint(1, 2),
        "post_reflect_range": random.randint(0, 2),
        "reverb_ridges": False,
        "with_reverb": random.randint(4, 8),
    }),

    "oldschool": lambda: {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(2, 5) * 2,
        "mask": "chess",
        "rgb": True,
        "spline_order": 0,
        "point_distrib": random_member(PointDistribution),
        "point_freq": random.randint(4, 8),
        "voronoi_refract": random.randint(8, 12),
        "with_voronoi": 6,
    },

    "oracle": lambda: extend("snow", {
        "corners": True,
        "freq": [14, 8],
        "invert": random.randint(0, 1),
        "distrib": "ones",
        "mask": "iching",
        "spline_order": 0,
    }),

    "outer-limits": lambda: extend("be-kind-rewind", "symmetry", {
        "reindex_range": random.randint(8, 16),
        "saturation": 0,
        "with_dither": .075 + random.random() * .077,
    }),

    "pearlescent": lambda: extend("bloom", {
        "hue_range": random.randint(3, 5),
        "octaves": random.randint(1, 8),
        "point_freq": random.randint(6, 10),
        "ridges": random.randint(0, 1),
        "saturation": .175 + random.random() * .25,
        "voronoi_alpha": .333 + random.random() * .333,
        "voronoi_refract": 1.5 + random.random(),
        "with_shadow": .333 + random.random() * .333,
        "with_voronoi": 6,
    }),

    "plaid": lambda: extend("multires-low", {
        "deriv": 3,
        "distrib": "ones",
        "hue_range": random.random() * .5,
        "freq": random.randint(3, 6) * 2,
        "mask": "chess",
        "spline_order": random.randint(1, 3),
        "warp_freq": random.randint(2, 3),
        "warp_range": random.random() * .25,
        "warp_octaves": 1,
        "with_dither": random.random() * 0.25,
    }),

    "pluto": lambda: extend("bloom", "multires-ridged", "voronoi", {
        "freq": random.randint(4, 8),
        "deriv": random.randint(1, 3),
        "deriv_alpha": .333 + random.random() * .333,
        "hue_rotation": .575,
        "refract_range": .075 + random.random() * .075,
        "saturation": .125 + random.random() * .075,
        "voronoi_alpha": .75,
        "with_dither": .075 + random.random() * .075,
        "with_shadow": .75 + random.random() * .25,
        "with_voronoi": 2,
    }),

    "political-map": lambda: extend("bloom", {
        "freq": 5,
        "saturation": 0.35,
        "lattice_drift": 1,
        "octaves": 2,
        "posterize_levels": 4,
        "warp_octaves": 8,
        "warp_range": 1,
        "with_dither": 0.25,
        "with_outline": 1,
    }),

    "precision-error": lambda: extend("bloom", "invert", "symmetry", {
        "deriv": random.randint(1, 3),
        "post_deriv": random.randint(1, 3),
        "reflect_range": .125 + random.random() * 4.0,
        "with_density_map": True,
        "with_shadow": 1,
    }),

    "procedural-mask": lambda: extend("bloom", "crt", {
        "distrib": "ones",
        "freq": 24 * random.randint(1, 8),
        "mask": random_member(ValueMask.procedural_members()),
        "spline_order": 0,
    }),

    "procedural-muck": lambda: {
        "distrib": "ones",
        "freq": random.randint(100, 250),
        "mask": random_member(ValueMask),
        "saturation": 0,
        "spline_order": 0,
        "warp_freq": random.randint(2, 5),
        "warp_interp": 2,
        "warp_range": .5 + random.random(),
    },

    "prophesy": lambda: {
        "distrib": "ones",
        "emboss": .5 + random.random() * .5,
        "freq": 48,
        "invert": random.randint(0, 1),
        "mask": "invaders_square",
        "octaves": 2,
        "refract_range": .5,
        "saturation": .125 + random.random() * .075,
        "spline_order": random.randint(1, 2),
        "posterize_levels": random.randint(4, 8),
        "with_shadow": .5,
    },

    "quilty": lambda: extend("bloom", {
        "freq": random.randint(2, 6),
        "saturation": random.random() * .5,
        "point_distrib": random_member(PointDistribution.grid_members()),
        "point_freq": random.randint(3, 8),
        "spline_order": 0,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(0, 4),
        "voronoi_refract": random.randint(1, 3),
        "with_dither": random.random() * .5,
        "with_voronoi": random.randint(1, 2),
    }),

    "random-preset": lambda:
        preset(random_member([m for m in PRESETS if m != "random-preset"])),

    "rasteroids": lambda: extend("bloom", "crt", "sobel-operator", {
        "distrib": ["uniform", "ones"][random.randint(0, 1)],
        "freq": 6 * random.randint(2, 3),
        "mask": random_member(ValueMask),
        "spline_order": 0,
        "warp_freq": random.randint(3, 5),
        "warp_octaves": random.randint(3, 5),
        "warp_range": .25 + random.random() * .125,
    }),

    "redmond": lambda: extend("bloom", "snow", {
        "corners": True,
        "distrib": "uniform",
        "freq": 8,
        "hue_range": random.random() * 4.0,
        "invert": random.randint(0, 1),
        "mask": "square",
        "point_generations": 2,
        "point_freq": 2,
        "point_distrib": ["chess", "square"][random.randint(0, 1)],
        "point_corners": True,
        "reverb_iterations": random.randint(1, 3),
        "spline_order": 0,
        "voronoi_alpha": .5 + random.random() * .5,
        "voronoi_inverse": random.randint(0, 1),
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(0, 3),
        "with_reverb": random.randint(3, 6),
        "with_voronoi": random.randint(1, 7),
    }),

    "refractal": lambda: {
        "invert": 1,
        "lattice_drift": 1,
        "octaves": random.randint(1, 3),
        "point_freq": random.randint(8, 10),
        "post_reflect_range": random.randint(96, 192),
        "sin": random.random() * 10.0,
        "voronoi_alpha": .5 + random.random() * .5,
        "with_voronoi": 6,
    },

    "remember-logo": lambda: extend("crt", "density-map", "symmetry", {
        "point_distrib": random_member(PointDistribution.circular_members()),
        "point_freq": random.randint(3, 7),
        "voronoi_alpha": 1.0,
        "voronoi_nth": random.randint(0, 4),
        "post_deriv": 2,
        "with_vignette": .25 + random.random() * .25,
        "with_voronoi": 3,
    }),

    "rgb-shadows": lambda: {
        "brightness_distrib": "mids",
        "distrib": "uniform",
        "freq": random.randint(6, 16),
        "hue_range": random.randint(1, 4),
        "lattice_drift": random.random(),
        "saturation_distrib": "ones",
        "with_shadow": 1,
    },

    "ridged-bubbles": lambda: extend("invert", "symmetry", {
        "point_distrib": random_member(PointDistribution),
        "point_freq": random.randint(4, 10),
        "post_ridges": True,
        "reverb_iterations": random.randint(1, 4),
        "rgb": random.randint(0, 1),
        "voronoi_alpha": .333 + random.random() * .333,
        "with_density_map": random.randint(0, 1),
        "with_reverb": random.randint(2, 4),
        "with_voronoi": 2,
    }),

    "ridged-ridges": lambda: extend("multires-ridged", {
        "freq": random.randint(2, 8),
        "lattice-drift": random.randint(0, 1),
        "post_ridges": True,
        "rgb": random.randint(0, 1),
    }),

    "ripple-effect": lambda: extend("bloom", {
        "freq": random.randint(2, 5),
        "invert": 1,
        "lattice_drift": 1,
        "ridges": random.randint(0, 1),
        "ripple_freq": random.randint(2, 3),
        "ripple_kink": random.randint(3, 18),
        "ripple_range": .05 + random.random() * .2,
        "sin": 3,
        "with_shadow": .5 + random.random() * .25,
    }),

    "runes-of-arecibo": lambda: {
        "distrib": "ones",
        "freq": 30 * random.randint(3, 6),
        "mask": ['arecibo_num', 'arecibo_bignum'][random.randint(0, 1)],
        "spline_order": random.randint(0, 2),
    },

    "sands-of-time": lambda: {
        "freq": random.randint(3, 5),
        "octaves": random.randint(1, 3),
        "with_worms": random.randint(3, 4),
        "worms_alpha": 1,
        "worms_density": 750,
        "worms_duration": .25,
        "worms-kink": random.randint(1, 2),
        "worms_stride": random.randint(128, 256),
    },

    "satori": lambda: extend("bloom", {
        "freq": random.randint(3, 8),
        "hue_range": random.random(),
        "lattice_drift": 1,
        "point_distrib": random_member(["random"] + PointDistribution.circular_members()),
        "point_freq": random.randint(2, 8),
        "post_ridges": random.randint(0, 1),
        "rgb": random.randint(0, 1),
        "ridges": True,
        "sin": random.random() * 2.5,
        "voronoi_alpha": .5 + random.random() * .5,
        "voronoi_refract": random.randint(6, 12),
        "with_shadow": 1.0,
        "with_voronoi": 6,
    }),

    "scribbles": lambda: extend("sobel-operator", {
        "deriv": random.randint(1, 3),
        "freq": random.randint(4, 8),
        "lattice_drift": random.random(),
        "octaves": 2,
        "post_contrast": 5,
        "post_deriv": random.randint(1, 3),
        "post_saturation": 0,
        "ridges": True,
        "with_density_map": True,
        "with_dither": .25,
        "with_fibers": True,
        "with_grime": True,
        "with_vignette": .075 + random.random() * .05,
        "with_shadow": random.random(),
    }),

    "seether-reflect": lambda: extend("symmetry", {
        "hue_range": 1.0 + random.random(),
        "invert": True,
        "point_distrib": random_member(PointDistribution.circular_members()),
        "point_freq": random.randint(4, 6),
        "post_reflect_range": random.randint(8, 12),
        "post_ridges": True,
        "ridges": True,
        "voronoi_alpha": .25 + random.random() * .25,
        "warp_range": .5,
        "warp_octaves": 6,
        "with_glowing_edges": 1,
        "with_reverb": 1,
        "with_shadow": 1,
        "with_voronoi": 2,
    }),

    "seether-refract": lambda: extend("symmetry", {
        "hue_range": 1.0 + random.random(),
        "invert": True,
        "point_distrib": random_member(PointDistribution.circular_members()),
        "point_freq": random.randint(4, 6),
        "post_refract_range": random.randint(4, 8),
        "post_ridges": True,
        "ridges": True,
        "voronoi_alpha": .25 + random.random() * .25,
        "warp_range": .5,
        "warp_octaves": 6,
        "with_glowing_edges": 1,
        "with_reverb": 1,
        "with_shadow": 1,
        "with_voronoi": 2,
    }),

    "shatter": lambda: {
        "freq": random.randint(2, 4),
        "invert": random.randint(0, 1),
        "point_freq": random.randint(3, 6),
        "post_refract_range": random.randint(3, 5),
        "posterize_levels": random.randint(4, 6),
        "rgb": random.randint(0, 1),
        "voronoi_func": [1, 3][random.randint(0, 1)],
        "voronoi_inverse": random.randint(0, 1),
        "with_outline": random.randint(1, 3),
        "with_voronoi": 5,
    },

    "shmoo": lambda: {
        "freq": random.randint(4, 6),
        "hue_range": 2 + random.random(),
        "invert": 1,
        "posterize_levels": random.randint(3, 5),
        "rgb": random.randint(0, 1),
        "with_outline": 1,
    },

    "shmootype": lambda: {
        "distrib": "ones",
        "freq": random.randint(4, 6) * 150,
        "mask": "truetype",
        "spline_order": random.randint(0, 2),
        "warp_freq": 3,
        "warp_interp": 3,
        "warp_octaves": 1,
        "warp_range": 2,
    },

    "sideways": lambda: extend("bloom", "crt", "multires-low", "pixel-sort", {
        "freq": random.randint(6, 12),
        "distrib": "ones",
        "mask": "script",
        "reflect_range": 1,
        "saturation": .06125 + random.random() * .125,
        "sin": random.random() * 4,
        "spline_order": random.randint(1, 3),
        "with_shadow": .5 + random.random() * .5,
    }),

    "sine-here-please": lambda: extend("multires", {
        "freq": random.randint(2, 4),
        "sin": 25 + random.random() * 200,
        "with_shadow": 1,
    }),

    "sined-multifractal": lambda: extend("bloom", "multires-ridged", {
        "distrib": "uniform",
        "freq": random.randint(2, 12),
        "hue_range": random.random(),
        "hue_rotation": random.random(),
        "lattice_drift": .75,
        "sin": -3,
    }),

    "skeletal-lace": lambda: extend("wormhole", {
        "lattice_drift": 1,
        "point_freq": 3,
        "voronoi_nth": 1,
        "voronoi_refract": 25,
        "with_voronoi": 6,
        "wormhole_stride": 0.01,
    }),

    "slimer": lambda: {
        "freq": random.randint(3, 4),
        "hue_range": .5,
        "point_freq": random.randint(1, 3),
        "post_reindex_range": .25 + random.random() * .333,
        "reindex_range": .5 + random.random() * .666,
        "ripple_range": .025 + random.random() * .0333,
        "voronoi_alpha": .5 + random.random() * .333,
        "voronoi_refract": random.randint(3, 5),
        "warp_range": .075 + random.random() * .075,
        "with_voronoi": 2,
    },

    "soft-cells": lambda: extend("bloom", {
        "point_distrib": random_member(PointDistribution),
        "point_freq": random.randint(4, 8),
        "voronoi_alpha": .5 + random.random() * .5,
        "with_voronoi": 5,
    }),

    "soften": lambda: extend("bloom", {
        "freq": 2,
        "hue_range": .25 + random.random() * .25,
        "hue_rotation": random.random(),
        "lattice_drift": 1,
        "octaves": random.randint(1, 4),
        "rgb": random.randint(0, 1),
    }),

    "solar": lambda: extend("bloom", "multires", {
        "freq": random.randint(20, 28),
        "hue_range": .225 + random.random() * .05,
        "hue_rotation": .975,
        "reflect_range": .666 + random.random() * .333,
        "refract_range": .666 + random.random() * .333,
        "saturation": 4 + random.random() * 2.5,
        "sin": 3,
        "warp_range": .2 + random.random() * .1,
        "warp_freq": 2,
    }),

    "soup": lambda: extend("bloom", "density-map", {
        "point_freq": random.randint(2, 4),
        "post_refract_range": random.randint(8, 12),
        "voronoi_inverse": True,
        "with_shadow": 1.0,
        "with_voronoi": 6,
        "with_worms": 5,
        "worms_alpha": .5 + random.random() * .45,
        "worms_density": 500,
        "worms_kink": 4.0 + random.random() * 2.0,
    }),

    "spaghettification": lambda: extend("bloom", "density-map", "multires-low", {
        "point_freq": 1,
        "voronoi_func": random.randint(1, 3),
        "voronoi_inverse": True,
        "with_aberration": .0075 + random.random() * .0075,
        "with_shadow": .75 + random.random() * .25,
        "with_voronoi": 6,
        "with_worms": 4,
        "worms_alpha": .75,
        "worms_density": 1500,
        "worms_stride": random.randint(150, 350),
    }),

    "spectrogram": lambda: {
        "distrib": "row_index",
        "freq": random.randint(256, 512),
        "hue_range": .5 + random.random() * .5,
        "mask": "bar_code",
        "spline_order": 0,
    },

    "spiral-clouds": lambda: extend("multires", "wormhole", {
        "freq": random.randint(2, 4),
        "lattice_drift": 1.0,
        "saturation-distrib": "ones",
        "shadow": 1,
        "wormhole_alpha": .333 + random.random() * .333,
        "wormhole_stride": .001 + random.random() * .0005,
        "wormhole_kink": random.randint(40, 50),
    }),

    "spiral-in-spiral": lambda: {
        "point_distrib": "spiral" if random.randint(0, 1) else "rotating",
        "point_freq": 10,
        "reverb_iterations": random.randint(1, 4),
        "with_reverb": random.randint(0, 6),
        "with_voronoi": random.randint(1, 2),
        "with_worms": random.randint(1, 4),
        "worms_density": 500,
        "worms_duration": 1,
        "worms_kink": random.randint(5, 25),
    },

    "spiraltown": lambda: extend("wormhole", {
        "freq": 2,
        "hue_range": 1,
        "reflect_range": random.randint(3, 6),
        "spline_order": random.randint(1, 3),
        "wormhole_kink": random.randint(5, 20),
        "wormhole_stride": random.random() * .05,
    }),

    "square-stripes": lambda: {
        "hue_range": random.random(),
        "point_distrib": random_member(PointDistribution.grid_members()),
        "point_freq": 2,
        "point_generations": random.randint(2, 3),
        "voronoi_alpha": .5 + random.random() * .5,
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(1, 3),
        "voronoi_refract": 1.46,
        "with_voronoi": 2,
    },

    "star-cloud": lambda: extend("bloom", "sobel-operator", {
        "deriv": 1,
        "freq": 2,
        "hue_range": random.random() * 2.0,
        "point_freq": 10,
        "reflect_range": random.random() + .5,
        "spline_order": 2,
        "voronoi_refract": random.randint(2, 4),
        "with_voronoi": 6,
    }),

    "starfiald": lambda: extend("bloom", "multires-low", {
        "distrib": "exp",
        "freq": random.randint(200, 300),
        "mask": "sparse",
        "post_brightness": -.333,
        "post_contrast": 3,
        "spline_order": 1,
        "with_aberration": .00125 + random.random() * .00125,
        "with_vignette": .25 + random.random() * .25,
    }),

    "stepper": lambda: extend("voronoi", {
        "hue_range": random.random(),
        "saturation": random.random(),
        "point_corners": random.randint(0, 1),
        "point_distrib": random_member(PointDistribution.circular_members()),
        "voronoi_func": random.randint(2, 3),
        "voronoi_nth": random.randint(0, 48),
        "with_outline": 3,
    }),

    "symmetry": lambda: {
        "corners": True,
        "freq": 2,
    },

    "teh-matrex-haz-u": lambda: extend("bloom", "crt", {
        "distrib": "exp",
        "freq": (random.randint(2, 4), random.randint(48, 96)),
        "glyph_map_zoom": random.randint(2, 4),
        "hue_rotation": .4 + random.random() * .2,
        "hue_range": .25,
        "lattice_drift": 1,
        "mask": "sparse",
        "post_saturation": 2,
        "spline_order": 1,
        "with_glyph_map": [
            ["binary", "numeric", "hex"][random.randint(0, 2)],
            "truetype",
            "ideogram",
            "invaders_square",
            ["fat_lcd", "fat_lcd_binary", "fat_lcd_numeric", "fat_lcd_hex"][random.randint(0, 3)],
            "emoji",
        ][random.randint(0, 5)],
    }),

    "tensorflower": lambda: extend("bloom", "symmetry", {
        "hue_range": random.random(),
        "point_corners": True,
        "point_distrib": ["square", "h_hex", "v_hex"][random.randint(0, 2)],
        "point_freq": 2,
        "rgb": random.randint(0, 1),
        "spline_order": 0,
        "vortex_range": random.randint(8, 25),
        "with_voronoi": 5,
    }),

    "the-arecibo-response": lambda: extend("snow", {
        "distrib": "ones",
        "freq": random.randint(42, 210),
        "mask": 'arecibo',
        "spline_order": random.randint(0, 2),
    }),

    "the-data-must-flow": lambda: extend("bloom", "sobel-operator", {
        "freq": 2,
        "hue_range": random.random() * 2.5,
        "with_worms": 1,
        "worms_alpha": .9 + random.random() * .1,
        "worms_density": 1.5 + random.random(),
        "worms_duration": 1,
        "worms_stride": 8,
        "worms_stride_deviation": 6,
    }),

    "the-inward-spiral": lambda: {
        "point_freq": 1,
        "voronoi_func": random.randint(1, 3),
        "with_voronoi": 2,
        "with_worms": random.randint(1, 5),
        "worms_alpha": 1,
        "worms_duration": random.randint(1, 4),
        "worms_density": 500,
        "worms_kink": random.randint(6, 24),
    },

    "time-to-reflect": lambda: extend("symmetry", {
        "post_reflect_range": random.randint(0, 1),
        "post_ridges": random.randint(0, 1),
        "reflect_range": random.randint(7, 14),
        "ridges": random.randint(0, 1),
        "with_shadow": random.randint(0, 1),
    }),

    "timeworms": lambda: extend("bloom", "density-map", {
        "freq": random.randint(8, 36),
        "hue_range": 0,
        "mask": "sparse",
        "octaves": random.randint(1, 3),
        "reflect_range": random.randint(0, 1) * random.random() * 4,
        "spline_order": random.randint(1, 3),
        "with_worms": 1,
        "worms_alpha": 1,
        "worms_density": .25,
        "worms_duration": 10,
        "worms_stride": 2,
        "worms_kink": .25 + random.random() * 2.5,
    }),

    "traceroute": lambda: extend("multires", {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(2, 6),
        "mask": random_member(ValueMask),
        "with_worms": random.randint(1, 3),
        "worms_density": 500,
        "worms_kink": random.randint(5, 25),
    }),

    "triangular": lambda: extend("multires", "sobel-operator", {
        "corners": True,
        "distrib": ["ones", "uniform"][random.randint(0, 1)],
        "freq": random.randint(1, 4) * 2,
        "mask": ["h_tri", "v_tri"][random.randint(0, 1)],
    }),

    "tribbles": lambda: extend("bloom", {
        "freq": random.randint(4, 10),
        "hue_rotation": random.random() if random.randint(0, 1) else 0.375 + random.random() * .15,
        "hue_range": random.random() * 2.5 if random.randint(0, 1) else 0.125 + random.random() * .125,
        "saturation": .375 + random.random() * .15,
        "invert": 1,
        "octaves": 3,
        "point_distrib": "h_hex",
        "point_freq": random.randint(2, 5) * 2,
        "ridges": True,
        "voronoi_alpha": 0.5 + random.random() * .25,
        "warp_freq": random.randint(2, 4),
        "warp_octaves": random.randint(2, 4),
        "warp_range": 0.05 + random.random() * .01,
        "with_voronoi": 5,
        "with_worms": 3,
        "worms_alpha": .75 + random.random() * .25,
        "worms_density": 750,
        "worms_duration": .5,
        "worms_stride_deviation": .5,
    }),

    "triblets": lambda: extend("bloom", "multires", {
        "distrib": "uniform",
        "freq": random.randint(3, 15) * 2,
        "mask": random_member(ValueMask),
        "hue_rotation": 0.875 + random.random() * .15,
        "saturation": .375 + random.random() * .15,
        "warp_octaves": random.randint(1, 2),
        "warp_freq": random.randint(2, 3),
        "warp_range": 0.05 + random.random() * .1,
        "with_worms": 3,
        "worms_alpha": .875 + random.random() * .125,
        "worms_density": 750,
        "worms_duration": .5,
        "worms_stride": .5,
        "worms_stride_deviation": .25,
    }),

    "trominos": lambda: extend("bloom", "crt", "sobel-operator", {
        "distrib": "ones",
        "freq": 4 * random.randint(25, 50),
        "mask": "tromino",
        "spline_order": 0,
    }),

    "truchet-maze": lambda: {
        "distrib": "ones",
        "freq": 6 * random.randint(50, 100),
        "mask": "truchet_maze",
        "spline_order": random.randint(0, 3),
    },

    "turf": lambda: extend("multires", {
        "freq": random.randint(6, 12),
        "hue_rotation": .25 + random.random() * .05,
        "lattice_drift": 1,
        "saturation": .625 + random.random() * .25,
        "with_dither": .1 + random.random() * .05,
        "with_worms": 4,
        "worms_alpha": .9,
        "worms_density": 50 + random.random() * 25,
        "worms_duration": 1.125,
        "worms_stride": .875,
        "worms_stride_deviation": .125,
        "worms_kink": .125 + random.random() * .5,
    }),

    "twister": lambda: extend("wormhole", {
        "freq": random.randint(12, 24),
        "octaves": 2,
        "wormhole_kink": 1 + random.random() * 3,
        "wormhole_stride": .0333 + random.random() * .0333,
    }),

    "unicorn-puddle": lambda: extend("bloom", "multires", {
        "distrib": "uniform",
        "freq": random.randint(8, 12),
        "hue_range": 2.5,
        "invert": .5 * random.random() * .5,
        "lattice_drift": 1,
        "post_contrast": 1.5,
        "post_hue_rotation": random.random(),
        "reflect_range": .25 + random.random() * .125,
        "ripple_freq": [random.randint(12, 64), random.randint(12, 64)],
        "ripple_kink": .5 + random.random() * .25,
        "ripple_range": .25 + random.random() * .125,
        "with_light_leak": .5 + random.random() * .25,
        "with_shadow": 1,
    }),

    "vectoroids": lambda: extend("crt", {
        "freq": 25,
        "distrib": "ones",
        "mask": "sparse",
        "point_freq": 10,
        "point_drift": .25 + random.random() * .75,
        "post_deriv": 1,
        "spline_order": 0,
        "with_voronoi": 4,
    }),

    "velcro": lambda: extend("wormhole", {
        "freq": 2,
        "hue_range": random.randint(0, 3),
        "octaves": random.randint(1, 2),
        "reflect_range": random.randint(6, 8),
        "spline_order": random.randint(2, 3),
        "wormhole_stride": random.random() * .0125,
    }),

    "vortex-checkers": lambda: {
        "freq": random.randint(4, 10) * 2,
        "distrib": ["ones", "uniform", "laplace"][random.randint(0, 2)],
        "mask": "chess",
        "hue_range": random.random(),
        "saturation": random.random(),
        "outline": 3,
        "posterize": random.randint(10, 15),
        "reverb_iterations": random.randint(2, 4),
        "sin": .5 + random.random(),
        "spline_order": 0,
        "vortex_range": 2.5 + random.random() * 5,
        "with_reverb": random.randint(3, 5),
    },

    "warped-cells": lambda: {
        "invert": 1,
        "point_distrib": random_member(PointDistribution),
        "point_freq": random.randint(6, 10),
        "post_ridges": True,
        "voronoi_alpha": .333 + random.random() * .333,
        "warp_range": .5 + random.random() * .5,
        "with_voronoi": 2,
    },

    "warped-grid": lambda: extend("bloom", "sobel-operator", {
        "corners": True,
        "distrib": "ones",
        "freq": random.randint(4, 48) * 2,
        "hue_range": 3,
        "saturation": 0.27,
        "mask": random_member(ValueMask),
        "posterize_levels": 12,
        "spline_order": 0,
        "warp_interp": random.randint(1, 3),
        "warp_freq": random.randint(2, 4),
        "warp_range": .25 + random.random() * .75,
        "warp_octaves": 1,
        "with_aberration": random.random() * .125,
    }),

    "whatami": lambda: {
        "freq": random.randint(7, 9),
        "hue_range": 3,
        "invert": 1,
        "post_reindex_range": 2,
        "reindex_range": 2,
        "voronoi_alpha": .75 + random.random() * .125,
        "with_voronoi": 2,
    },

    "wireframe": lambda: extend("bloom", "multires-low", "sobel-operator", {
        "freq": random.randint(2, 5),
        "hue_range": random.random(),
        "saturation": random.random(),
        "lattice_drift": random.random(),
        "point_distrib": random_member(PointDistribution.grid_members()),
        "point_freq": random.randint(7, 10),
        "voronoi_alpha": 0.25 + random.random() * .5,
        "voronoi_nth": random.randint(1, 5),
        "warp_octaves": random.randint(1, 3),
        "warp_range": random.randint(0, 1) * random.random() * .5,
        "with_voronoi": 5,
    }),

    "wild-kingdom": lambda: extend("bloom", {
        "freq": 25,
        "invert": random.randint(0, 1),
        "lattice_drift": 1,
        "mask": "sparse",
        "post_hue_rotation": random.random(),
        "posterize_levels": 3,
        "rgb": True,
        "ridges": True,
        "warp_octaves": 2,
        "warp_range": .05,
        "with_outline": 2,
    }),

    "woahdude-voronoi-refract": lambda: {
        "freq": 4,
        "hue_range": 2,
        "lattice_drift": 1,
        "point_freq": 8,
        "sin": 100,
        "voronoi_alpha": 0.875,
        "voronoi_refract": 1,
        "with_voronoi": 1,
    },

    "woahdude-octave-warp": lambda: extend("bloom", {
        "freq": random.randint(2, 3),
        "hue_range": random.random() * 3.0,
        "sin": random.randint(5, 15),
        "warp_range": random.randint(3, 5),
        "warp_octaves": 3,
        "with_shadow": random.random(),
    }),

    "wooly-bully": lambda: {
        "hue_range": random.random() * 1.5,
        "point_corners": True,
        "point_distrib": random_member(PointDistribution.circular_members()),
        "point_freq": random.randint(2, 3),
        "point_generations": 2,
        "reverb_iterations": random.randint(1, 2),
        "refract_range": random.randint(0, 2),
        "voronoi_func": 3,
        "voronoi_nth": random.randint(1, 3),
        "voronoi_alpha": .5 + random.random() * .5,
        "with_reverb": random.randint(0, 2),
        "with_voronoi": 2,
        "with_worms": 4,
        "worms_alpha": .75 + random.random() * .25,
        "worms_density": 250 + random.random() * 250,
        "worms_duration": 1 + random.random() * 1.5,
        "worms_kink": 5 + random.random() * 2.0,
        "worms_stride": 2.5,
        "worms_stride_deviation": 1.25,
    },

    "wormstep": lambda: extend("bloom", {
        "corners": True,
        "freq": random.randint(2, 4),
        "lattice_drift": random.randint(0, 1),
        "octaves": random.randint(1, 3),
        "with_worms": 4,
        "worms_alpha": .5 + random.random() * .5,
        "worms_density": 500,
        "worms_kink": 1.0 + random.random() * 4.0,
        "worms_stride": 8.0 + random.random() * 4.0,
    }),

}


# Call after setting seed
def bake_presets(seed):
    generators.set_seed(seed)

    global EFFECTS_PRESETS
    EFFECTS_PRESETS = _EFFECTS_PRESETS()

    global PRESETS
    PRESETS = _PRESETS()


def random_member(collection):
    return sorted(collection)[random.randint(0, len(collection) - 1)]


def extend(*args):
    args = deque(args)

    settings = {}

    while args:
        arg = args.popleft()

        if isinstance(arg, str):
            settings.update(preset(arg))

        else:
            settings.update(arg)

    del(settings["name"])

    return settings


def preset(name):
    """
    Load the named settings.

    The `artmaker` and `artmangler` scripts demonstrate how presets are used.

    :param str name: Name of the preset to load
    :return: dict
    """

    presets = EFFECTS_PRESETS if name in EFFECTS_PRESETS else PRESETS

    settings = presets[name]()

    if "name" not in settings:
        settings["name"] = name

    return settings


bake_presets(None)
