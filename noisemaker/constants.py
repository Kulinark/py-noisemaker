"""Constants used in Noisemaker"""

from enum import Enum


class DistanceMetric(Enum):
    """
    Specify the distance metric used in various operations, such as Voronoi cells, derivatives, and sobel operators.
    """

    none = 0

    # These require absolute inputs
    euclidean = 1
    manhattan = 2
    chebyshev = 3
    octagram = 4

    # These require signed inputs
    triangular = 101
    hexagram = 102

    @classmethod
    def all(cls):
        return [m for m in cls if m != cls.none]

    @classmethod
    def absolute_members(cls):
        return [m for m in cls if cls.is_absolute(m)]

    @classmethod
    def is_absolute(cls, member):
        return member != cls.none and member.value < cls.triangular.value

    @classmethod
    def signed_members(cls):
        return [m for m in cls if cls.is_signed(m)]

    @classmethod
    def is_signed(cls, member):
        return member != cls.none and not cls.is_absolute(member)


class InterpolationType(Enum):
    """
    Specify the spline point count for interpolation operations.
    """

    #:
    constant = 0

    #:
    linear = 1

    #:
    cosine = 2

    #:
    bicubic = 3


class PointDistribution(Enum):
    """
    Point cloud distribution, used by Voronoi and DLA
    """

    random = 1000000

    square = 1000001

    waffle = 1000002

    chess = 1000003

    h_hex = 1000010

    v_hex = 1000011

    spiral = 1000050

    circular = 1000100

    concentric = 1000101

    rotating = 1000102

    @classmethod
    def grid_members(cls):
        return [m for m in cls if cls.is_grid(m)]

    @classmethod
    def circular_members(cls):
        return [m for m in cls if cls.is_circular(m)]

    @classmethod
    def is_grid(cls, member):
        return member.value >= cls.square.value and member.value < cls.spiral.value

    @classmethod
    def is_circular(cls, member):
        return member.value >= cls.circular.value


class ValueDistribution(Enum):
    """
    Specify the value distribution function for basic noise.

    .. code-block:: python

       image = basic(freq, [height, width, channels], distrib=ValueDistribution.uniform)
    """

    uniform = 1
    exp = 2
    pow_inv_1 = 4

    @classmethod
    def is_noise(cls, member):
        return member and member.value < 5

    ones = 5
    mids = 6
    zeros = 7

    column_index = 10
    row_index = 11

    center_euclidean = 20
    center_manhattan = 21
    center_chebyshev = 22
    center_octagram = 23
    center_triangular = 24
    center_hexagram = 25

    @classmethod
    def is_center_distance(cls, member):
        return member and (member.value >= 20) and (member.value < 30)

    scan_up = 30
    scan_down = 31
    scan_left = 32
    scan_right = 33

    @classmethod
    def is_scan(cls, member):
        return member and (member.value >= 30) and (member.value < 40)

    @classmethod
    def is_native_size(cls, member):
        """The noise type is generated at full-size, rather than upsampled."""
        return cls.is_center_distance(member) \
            or cls.is_scan(member)


class ValueMask(Enum):
    """
    """

    square = 1
    waffle = 2
    chess = 3
    grid = 4
    h_bar = 5
    v_bar = 6

    h_hex = 10
    v_hex = 11
    h_tri = 12
    v_tri = 13

    alphanum_0 = 20
    alphanum_1 = 21
    alphanum_2 = 22
    alphanum_3 = 23
    alphanum_4 = 24
    alphanum_5 = 25
    alphanum_6 = 26
    alphanum_7 = 27
    alphanum_8 = 28
    alphanum_9 = 29
    alphanum_a = 30
    alphanum_b = 31
    alphanum_c = 32
    alphanum_d = 33
    alphanum_e = 34
    alphanum_f = 35

    tromino_i = 40
    tromino_l = 41
    tromino_o = 42
    tromino_s = 43

    halftone_0 = 50
    halftone_1 = 51
    halftone_2 = 52
    halftone_3 = 53
    halftone_4 = 54
    halftone_5 = 55
    halftone_6 = 56
    halftone_7 = 57
    halftone_8 = 58
    halftone_9 = 59

    lcd_0 = 60
    lcd_1 = 61
    lcd_2 = 62
    lcd_3 = 63
    lcd_4 = 64
    lcd_5 = 65
    lcd_6 = 66
    lcd_7 = 67
    lcd_8 = 68
    lcd_9 = 69  # nice

    fat_lcd_0 = 70
    fat_lcd_1 = 71
    fat_lcd_2 = 72
    fat_lcd_3 = 73
    fat_lcd_4 = 74
    fat_lcd_5 = 75
    fat_lcd_6 = 76
    fat_lcd_7 = 77
    fat_lcd_8 = 78
    fat_lcd_9 = 79
    fat_lcd_a = 80
    fat_lcd_b = 81
    fat_lcd_c = 82
    fat_lcd_d = 83
    fat_lcd_e = 84
    fat_lcd_f = 85
    fat_lcd_g = 86
    fat_lcd_h = 87
    fat_lcd_i = 88
    fat_lcd_j = 89
    fat_lcd_k = 90
    fat_lcd_l = 91
    fat_lcd_m = 92
    fat_lcd_n = 93
    fat_lcd_o = 94
    fat_lcd_p = 95
    fat_lcd_q = 96
    fat_lcd_r = 97
    fat_lcd_s = 98
    fat_lcd_t = 99
    fat_lcd_u = 100
    fat_lcd_v = 101
    fat_lcd_w = 102
    fat_lcd_x = 103
    fat_lcd_y = 104
    fat_lcd_z = 105

    truchet_lines_00 = 110
    truchet_lines_01 = 111

    truchet_curves_00 = 112
    truchet_curves_01 = 113

    truchet_tile_00 = 120
    truchet_tile_01 = 121
    truchet_tile_02 = 122
    truchet_tile_03 = 123

    mcpaint_00 = 130
    mcpaint_01 = 131
    mcpaint_02 = 132
    mcpaint_03 = 133
    mcpaint_04 = 134
    mcpaint_05 = 135
    mcpaint_06 = 136
    mcpaint_07 = 137
    mcpaint_08 = 138
    mcpaint_09 = 139
    mcpaint_10 = 140
    mcpaint_11 = 141
    mcpaint_12 = 142
    mcpaint_13 = 143
    mcpaint_14 = 144
    mcpaint_15 = 145
    mcpaint_16 = 146
    mcpaint_17 = 147
    mcpaint_18 = 148
    mcpaint_19 = 149
    mcpaint_20 = 150
    mcpaint_21 = 151
    mcpaint_22 = 152
    mcpaint_23 = 153
    mcpaint_24 = 154
    mcpaint_25 = 155
    mcpaint_26 = 156
    mcpaint_27 = 157
    mcpaint_28 = 158
    mcpaint_29 = 159
    mcpaint_30 = 160
    mcpaint_31 = 161
    mcpaint_32 = 162
    mcpaint_33 = 163
    mcpaint_34 = 164
    mcpaint_35 = 165
    mcpaint_36 = 166
    mcpaint_37 = 167
    mcpaint_38 = 168
    mcpaint_39 = 169
    mcpaint_40 = 170

    emoji_00 = 200
    emoji_01 = 201
    emoji_02 = 202
    emoji_03 = 203
    emoji_04 = 204
    emoji_05 = 205
    emoji_06 = 206
    emoji_07 = 207
    emoji_08 = 208
    emoji_09 = 209
    emoji_10 = 210
    emoji_11 = 211
    emoji_12 = 212
    emoji_13 = 213
    emoji_14 = 214
    emoji_15 = 215
    emoji_16 = 216
    emoji_17 = 217
    emoji_18 = 218
    emoji_19 = 219
    emoji_20 = 220
    emoji_21 = 221
    emoji_22 = 222
    emoji_23 = 223
    emoji_24 = 224
    emoji_25 = 225
    emoji_26 = 226
    emoji_27 = 227
    # emoji_28 = 228
    # emoji_29 = 229
    # emoji_30 = 230
    # emoji_31 = 231
    # emoji_32 = 232
    # emoji_33 = 233
    # emoji_34 = 234
    # emoji_35 = 235
    # emoji_36 = 236
    # emoji_37 = 237
    # emoji_38 = 238
    # emoji_39 = 239
    # emoji_40 = 240

    bank_ocr_0 = 250
    bank_ocr_1 = 251
    bank_ocr_2 = 252
    bank_ocr_3 = 253
    bank_ocr_4 = 254
    bank_ocr_5 = 255
    bank_ocr_6 = 256
    bank_ocr_7 = 257
    bank_ocr_8 = 258
    bank_ocr_9 = 259

    conv2d_blur = 800
    conv2d_deriv_x = 801
    conv2d_deriv_y = 802
    conv2d_edges = 803
    conv2d_emboss = 804
    conv2d_invert = 805
    conv2d_rand = 806
    conv2d_sharpen = 807
    conv2d_sobel_x = 808
    conv2d_sobel_y = 809
    conv2d_box_blur = 810

    rgb = 900
    rbggbr = 901
    rggb = 902
    rgbgr = 903
    roygbiv = 904
    rainbow = 910
    ace = 911
    nb = 912
    trans = 913

    sparse = 1000

    sparser = 1001

    invaders = 1002

    invaders_square = 1003

    matrix = 1004

    letters = 1005

    ideogram = 1006

    iching = 1007

    script = 1008

    white_bear = 1009

    tromino = 1010

    alphanum_binary = 1011
    alphanum_numeric = 1012
    alphanum_hex = 1013

    truetype = 1020

    halftone = 1021

    lcd = 1022
    lcd_binary = 1023

    fat_lcd = 1024
    fat_lcd_binary = 1025
    fat_lcd_numeric = 1026
    fat_lcd_hex = 1027

    arecibo_num = 1030
    arecibo_bignum = 1031
    arecibo_nucleotide = 1032
    arecibo_dna = 1033
    arecibo = 1034

    truchet_lines = 1040
    truchet_curves = 1041
    truchet_tile = 1042

    mcpaint = 1050

    emoji = 1051

    bar_code = 1060
    bar_code_short = 1061

    bank_ocr = 1070

    fake_qr = 1080

    dropout = 1100

    @classmethod
    def conv2d_members(cls):
        return [m for m in cls if cls.is_conv2d(m)]

    @classmethod
    def is_conv2d(cls, member):
        return member.name.startswith('conv2d')

    @classmethod
    def grid_members(cls):
        return [m for m in cls if cls.is_grid(m)]

    @classmethod
    def is_grid(cls, member):
        return member.value < cls.alphanum_0.value

    @classmethod
    def rgb_members(cls):
        return [m for m in cls if cls.is_rgb(m)]

    @classmethod
    def is_rgb(cls, member):
        return member.value >= cls.rgb.value and member.value < cls.sparse.value

    @classmethod
    def nonprocedural_members(cls):
        return [m for m in cls if not cls.is_procedural(m)]

    @classmethod
    def procedural_members(cls):
        return [m for m in cls if cls.is_procedural(m)]

    @classmethod
    def is_procedural(cls, member):
        return member.value >= cls.sparse.value


class VoronoiDiagramType(Enum):
    """
    Specify the artistic rendering function used for Voronoi diagrams.
    """

    #: No Voronoi
    none = 0

    #: Normalized neighbor distances
    range = 11

    #: Normalized neighbor distances blended with input Tensor
    color_range = 12

    #: Indexed regions
    regions = 21

    #: Color-mapped regions
    color_regions = 22

    #: Colorized neighbor distances blended with color-mapped regions
    range_regions = 31

    #: Edgeless voronoi. Natural logarithm of reduced distance sums.
    flow = 41

    #: Density-mapped flow diagram
    color_flow = 42

    @classmethod
    def flow_members(cls):
        return [cls.flow, cls.color_flow]

    @classmethod
    def is_flow_member(cls, member):
        return member in cls.flow_members()


class WormBehavior(Enum):
    """
    Specify the type of heading bias for worms to follow.

    .. code-block:: python

       image = worms(image, behavior=WormBehavior.unruly)
    """

    none = 0

    obedient = 1

    crosshatch = 2

    unruly = 3

    chaotic = 4

    random = 5

    meandering = 10  # like chaotic, but changes smoothly over time

    @classmethod
    def all(cls):
        return [m for m in cls if m != cls.none]


class OctaveBlending(Enum):
    """Specify the mode for flattening octaves."""

    # Traditional Perlinesque octave-over-octave persistence falloff
    falloff = 0

    # Take the maximum of each layer
    reduce_max = 10

    # Overlay each layer using the layer's alpha channel
    alpha = 20


class ColorSpace(Enum):
    """
    """

    grayscale = 1

    rgb = 11
    hsv = 21
    oklab = 31

    @classmethod
    def is_color(cls, m):
        return m and m.value > 1

    @classmethod
    def color_members(cls):
        return [m for m in cls if cls.is_color(m)]
