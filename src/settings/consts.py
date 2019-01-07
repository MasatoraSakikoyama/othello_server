# -*- coding: utf-8 -*-
X_AXIS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
Y_AXIS = ('1', '2', '3', '4', '5', '6', '7', '8')

AXIS_CHOICES = tuple([('{}{}'.format(x, y), '{}{}'.format(x, y))
    for x in X_AXIS for y in Y_AXIS])
