#!/usr/bin/env python
# Martin Kersner, 2016/03/11 

from __future__ import print_function
import sys
import re
import numpy as np
import matplotlib.pyplot as plt

from utils import strstr

def main():
  log_files = process_arguments(sys.argv)

  train_iteration = []
  train_loss      = []
  train_accuracy0 = []
  train_accuracy1 = []
  train_accuracy2 = []

  base_train_iter = 0

  for log_file in log_files:
    with open(log_file, 'rb') as f:
      if len(train_iteration) != 0:
        base_train_iter = train_iteration[-1]

      for line in f:
        if strstr(line, 'Iteration') and strstr(line, 'loss'):
          matched = match_loss(line)
          train_loss.append(float(matched.group(1)))

          matched = match_iteration(line)
          train_iteration.append(int(matched.group(1))+base_train_iter)

        elif strstr(line, 'Train net output #0'):
          matched = match_net_accuracy(line)
          train_accuracy0.append(float(matched.group(1)))

        elif strstr(line, 'Train net output #1'):
          matched = match_net_accuracy(line)
          train_accuracy1.append(float(matched.group(1)))

        elif strstr(line, 'Train net output #2'):
          matched = match_net_accuracy(line)
          train_accuracy2.append(float(matched.group(1)))

  print('ITERATION', train_iteration)
  print('LOSS',      train_loss)
  print('ACCURACY0', train_accuracy0)
  print('ACCURACY1', train_accuracy1)
  print('ACCURACY2', train_accuracy2)

  ## loss
  plt.plot(train_iteration, train_loss, 'k', label='Train loss')
  plt.legend()
  plt.ylabel('Loss')
  plt.xlabel('Number of iterations')
  plt.savefig('loss.png')

  ## evaluation
  plt.clf()
  plt.plot(range(len(train_accuracy0)), train_accuracy0, 'k', label='train accuracy 0')
  plt.plot(range(len(train_accuracy1)), train_accuracy1, 'r', label='train accuracy 1')
  plt.plot(range(len(train_accuracy2)), train_accuracy2, 'g', label='train accuracy 2')
  plt.legend(loc=0)
  plt.savefig('evaluation.png')

def match_iteration(line):
  return re.search(r'Iteration (.*),', line)

def match_loss(line):
  return re.search(r'loss = (.*)', line)

def match_net_accuracy(line):
  return re.search(r'accuracy = (.*)', line)

def process_arguments(argv):
  if len(argv) < 2:
    help()

  log_files = argv[1:]
  return log_files

def help():
  print('Usage: python loss_from_log.py [LOG_FILE]+\n'
        'LOG_FILE is text file containing log produced by caffe.'
        'At least one LOG_FILE has to be specified.'
        'Files has to be given in correct order (the oldest logs as the first ones).'
        , file=sys.stderr)

  exit()

if __name__ == '__main__':
  main()
