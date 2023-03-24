#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')


def hsv2rgb(h, s, v): # different algorithm
    c = v * s
    hi = h * 6
    x = c*(1 - abs(hi % 2 - 1))
    m = v - c
    if hi < 1:
        return (c+m, x+m, 0+m)
    if hi < 2:
        return (x+m, c+m, 0+m)
    if hi < 3:
        return (0+m, c+m, x+m)
    if hi < 4:
        return (0+m, x+m, c+m)
    if hi < 5:
        return (x+m, 0+m, c+m)
    return (c+m, 0+m, x+m)


def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    if v < 0.5:
        return (0, 1-2*v, 2*v)
    else:
        v = v - 0.5
        return (2*v, 0, 1-2*v)


def gradient_rgb_gbr_full(v):
    if v < 0.25:
        return (0, 1, 4*v)
    elif v >= 0.25 and v < 0.5:
        v = v - 0.25
        return (0, 1-4*v, 1)
    elif v >= 0.5 and v < 0.75:
        v = v - 0.5
        return (4*v, 0, 1)
    else:
        v = v - 0.75
        return (1, 0, 1-4*v)


def gradient_rgb_wb_custom(v):
    # creating parameters for better precision
    ratio = 1/7
    parameter = 1/ratio - 0.00000000000001
    if v < ratio:
        return (1, 1-parameter*v, 1)
    elif v >= ratio and v < 2*ratio:
        v = v - ratio
        return (1-parameter*v, 0, 1)
    elif v >= 2*ratio and v < 3*ratio:
        v = v - 2*ratio
        return (0, parameter*v, 1)
    elif v >= 3*ratio and v < 4*ratio:
        v = v - 3*ratio
        return (0, 1, 1-parameter*v)
    elif v >= 4*ratio and v < 5*ratio:
        v = v - 4*ratio
        return (parameter*v, 1, 0)
    elif v >= 5*ratio and v < 6*ratio:
        v = v - 5*ratio
        return (1, 1-parameter*v, 0)
    else:
        v = v - 6*ratio
        return (1-parameter*v, 0, 0)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb(1/3 + (2/3*v), 1, 1)


def gradient_hsv_unknown(v):
    return hsv2rgb(1-(2/3 + 1/3*v), 0.35, 1)


def gradient_hsv_custom(v):
    return hsv2rgb(v, 1-v, 1)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
