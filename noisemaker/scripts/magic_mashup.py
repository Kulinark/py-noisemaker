import os
import random
import shutil
import sys
import tempfile

import click
import tensorflow as tf

import noisemaker.cli as cli
import noisemaker.effects as effects
import noisemaker.generators as generators
import noisemaker.util as util
import noisemaker.value as value

DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512


@click.group(help="""
        Magic Mashup - Animated collage tool

        https://github.com/aayars/py-noisemaker
        """, context_settings=cli.CLICK_CONTEXT_SETTINGS)
def main():
    pass


@main.command()
@cli.input_dir_option(required=True)
@cli.int_option('--seed', required=True)
@cli.name_option(default="mashup.gif")
@cli.option('--save-frames', default=None, type=click.Path(exists=True, dir_okay=True))
@cli.width_option(default=DEFAULT_WIDTH)
@cli.height_option(default=DEFAULT_HEIGHT)
@cli.option('--watermark', type=str)
@click.pass_context
def frames(ctx, input_dir, seed, name, save_frames, width, height, watermark):
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(30):
            filename = f'{tmp}/{i:04d}.png'

            util.check_call(['magic-mashup', 'frame',
                             '--input-dir', input_dir,
                             '--frame', str(i),
                             '--seed', str(seed),
                             '--width', str(width),
                             '--height', str(height),
                             '--filename', filename])

            util.check_call(['noisemaker', 'effect', 'crt', filename,
                             '--no-resize',
                             '--seed', str(seed),
                             '--speed', '0.25',
                             '--time', str(i / 30.0),
                             '--filename', filename])

            if save_frames:
                shutil.copy(filename, save_frames)

            if watermark:
                util.watermark(watermark, filename)

        util.magick(f'{tmp}/*png', name)

    print('magic-mashup')


@main.command()
@cli.input_dir_option(required=True)
@cli.int_option('--frame', required=True)
@cli.int_option('--seed', required=True)
@cli.name_option(default="mashup.png")
@cli.width_option(default=DEFAULT_WIDTH)
@cli.height_option(default=DEFAULT_HEIGHT)
@click.pass_context
def frame(ctx, input_dir, frame, seed, name, width, height):
    value.set_seed(seed)

    shape = [height, width, 3]

    dirnames = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]

    if not dirnames:
        click.echo("Couldn't determine directory names inside of input dir " + input_dir)
        sys.exit(1)

    collage_count = min(random.randint(4, 6), len(dirnames))
    collage_images = []

    for i in range(collage_count + 1):
        index = random.randint(0, len(dirnames) - 1)

        dirname = dirnames[index]

        filenames = [f for f in sorted(os.listdir(os.path.join(input_dir, dirname))) if f.endswith('.png')]

        if not filenames:
            continue

        input_filename = os.path.join(input_dir, dirname, filenames[frame])

        collage_images.append(tf.image.convert_image_dtype(util.load(input_filename, channels=3), dtype=tf.float32))

    base = generators.basic(freq=random.randint(2, 4), shape=shape, hue_range=random.random(), time=frame/30.0, speed=0.125, distrib="simplex")

    control = effects.value_map(collage_images.pop(), shape, keepdims=True)

    control = effects.convolve(kernel=effects.ValueMask.conv2d_blur, tensor=control, shape=[shape[0], shape[1], 1])

    with tf.compat.v1.Session().as_default():
        tensor = effects.blend_layers(control, shape, random.random() * .5, *collage_images)

        tensor = value.blend(tensor, base, .125 + random.random() * .125)

        tensor = effects.bloom(tensor, shape, alpha=.25 + random.random() * .125)
        tensor = effects.shadow(tensor, shape, alpha=.25 + random.random() * .125, reference=control)

        tensor = tf.image.adjust_brightness(tensor, .05)
        tensor = tf.image.adjust_contrast(tensor, 1.25)

        util.save(tensor, name)
