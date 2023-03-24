#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker as ticker

def read_file(f, box=False):
    gen = []
    games = []
    time = []
    if not box:
      with open(f) as file:
          lines = file.readlines()
          for line in lines[1:]:
              fixed_line = line.replace('\n', '').split(',')
              gen.append(fixed_line[0])
              games.append(fixed_line[1])
              time.append(sum([float(i.strip()) for i in fixed_line[2:]]) / len(fixed_line[2:]))
      return gen, games, time
    else:
      with open(f) as file:
          lines = file.readlines()
          line = lines[-1]
          fixed_line = line.replace('\n', '').split(',')
          time = fixed_line[2:]
      return time

def draw_plots1(plot_list):
  plot_colors = ['b', 'g', 'r', 'k', 'm']
  algorithms = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']
  plt.figure(figsize=(6, 6))
  plt.xlim(0, 500000)
  plt.ylim(0.6, 1)
  for (plot, color) in zip(plot_list, plot_colors):
    p, g, c = read_file(plot)
    plt.plot(np.asarray(g, int), c, color, linewidth=1)
  plt.xlabel("Rozegranych gier")
  plt.ylabel("Odsetek wygranych gier") 
  plt.legend(algorithms)
  plt.savefig('myplot1.pdf', bbox_inches='tight')
  plt.close()

def draw_plots2(plot_list):
  plot_colors = ['b', 'g', 'r', 'k', 'm']
  algorithms = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']
  markers = ['o', 'v', 'D', 's', 'd']
  plt.figure(figsize=(12, 6))
  fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

  for (plot, color, marker) in zip(plot_list, plot_colors, markers):
    p, g, c = read_file(plot)
    ax1.plot(np.asarray(g, int), c, color, linewidth=1, marker=marker, markeredgecolor=('black'), alpha=0.75, ms=4, markevery=25)
  ax1.set(xlabel=r"$Rozegranych\ gier\ (\times1000)$", ylabel=r"$Odsetek\ wygranych\ gier\ [\%]$", xlim=(0,500000), ylim=(0.6,1))
  ticks_x = ticker.FuncFormatter(lambda g, pos: '{0:g}'.format(g/1000))
  ax1.xaxis.set_major_formatter(ticks_x)
  ticks_y = ticker.FuncFormatter(lambda c, pos: '{0:g}'.format(c*100))
  ax1.yaxis.set_major_formatter(ticks_y)
  ax1.legend(algorithms, loc="lower right", numpoints=2)
  ax1.grid(color='#c8c8c8', linestyle=':')
  secax1 = ax1.twiny()
  secax1.set_xticks(np.asarray(p, int))
  secax1.set_xlim(0, 200)
  secax1.locator_params(axis='x', nbins=5)
  secax1.set_xlabel('Pokolenie')

  boxprops = dict(linewidth=1, color='blue')
  flierprops = dict(marker='+', markerfacecolor='blue', markeredgecolor='blue', markersize=4)
  medianprops = dict(linewidth=1, color='red')
  meanpointprops = dict(marker='o', markeredgecolor='black', markerfacecolor='blue', markersize=5)
  whiskerprops = dict(linestyle='--', color='blue')
  ax2_data = {}
  for (plot, algorithm) in zip(plot_list, algorithms):
    c = read_file(plot, box=True)
    conv = list(map(float, c))
    ax2_data[algorithm] = conv
  ax2.boxplot(ax2_data.values(), notch=True, boxprops=boxprops, flierprops=flierprops, medianprops=medianprops, meanprops=meanpointprops, whiskerprops=whiskerprops, showmeans=True)
  ax2.set_xticklabels(ax2_data.keys(), rotation=30)
  ax2.yaxis.set_visible(False)
  secax2 = ax2.twinx()
  secax2.set_ylim([60, 100])
  secax2.set_yticks([60, 65, 70, 75, 80, 85, 90, 95, 100])
  ax2.grid(color='#c8c8c8', linestyle=':')
  secax2.grid(color='#c8c8c8', linestyle=':', which='both', axis='both')
  
  plt.savefig('myplot2.pdf', bbox_inches='tight')
  plt.close()

def main():
    files = ['1ers.csv', '1crs.csv', '2crs.csv', '1c.csv', '2c.csv']
    draw_plots1(files)
    draw_plots2(files)
    
if __name__ == '__main__':
    main()