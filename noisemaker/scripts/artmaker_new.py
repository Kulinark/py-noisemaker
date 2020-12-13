import random
import click

import click

from noisemaker.composer import Preset
from noisemaker.util import logger
from noisemaker.new_presets import PRESETS

import noisemaker.cli as cli
import noisemaker.value as value


@click.command(help="""
        Artmaker - Presets for Noisemaker

        https://github.com/aayars/py-noisemaker
        """, context_settings=cli.CLICK_CONTEXT_SETTINGS)
@cli.width_option()
@cli.height_option()
@cli.channels_option()
@cli.time_option()
@cli.clut_option()
@cli.seed_option()
@cli.name_option(default='art.png')
@click.argument('preset_name', type=click.Choice(["random"] + sorted(PRESETS)))
@click.pass_context
def main(ctx, width, height, channels, time, clut, seed, name, preset_name):
    value.set_seed(seed)

    if preset_name == "random":
        preset_name = list(PRESETS)[random.randint(0, len(PRESETS) - 1)]

    print(preset_name)

    preset = Preset(preset_name, PRESETS)

    shape = [height, width, channels]

    try:
        preset.render(shape=shape, name=name)

    except Exception as e:
        logger.error(f"preset.render() failed: {e}\nSeed: {seed}\nArgs: {preset.__dict__}")
        raise