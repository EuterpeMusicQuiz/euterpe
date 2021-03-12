# -*- coding: utf-8 -*-

from euterpe.validation.utils import simplify_str
from euterpe.validation.config import *

def n_different_characters(first_str, second_str):
    n = abs(len(first_str) - len(second_str))
    for i in range(min(len(first_str), len(second_str))):
        if (first_str[i] != second_str[i]):
            n +=1
    return n

def is_similar_to(first_str, second_str):
    n = n_different_characters(first_str, second_str)
    l1 = len(first_str)
    l2 = len(second_str)
    if (l2 <= SHORT):
        if (l2 == l1 and n == 0):
            return True
        elif (abs(l1 - l2) == 1):
            if (l1 > l2):
                if (first_str[:l1-1] == second_str or first_str[1:l1] == second_str):
                    return True
                else:
                    return False
            else:
                if (second_str[:l2-1] == first_str or second_str[1:l2] == first_str):
                    return True
                else:
                    return False
        else:
            return False
    elif (l2 > SHORT and l2 <= MEDIUM):
        if (abs(l1 - l2) > 1):
            return False
        if (l2 == l1):
            if (n < 2):
                return True
            else:
                return False
        elif (l2 < l1):
            for i in range(l1):
                if (first_str[:i] + first_str[i + 1:] == second_str):
                    return True
            return False
        else:
            for i in range(l2):
                if (second_str[:i] + second_str[i + 1:] == first_str):
                    return True
            return False
    elif (l2 > MEDIUM and l2 <= LONG):
        if (abs(l1 - l2) > 2):
            return False
        if (l2 == l1):
            if (n < 3):
                return True
            else:
                return False
        elif (l2 < l1):
            if (abs(l1 - l2) == 1):
                for i in range(l1):
                    if (n_different_characters(first_str[:i] + first_str[i + 1:], second_str) < 2):
                        return True
                return False
            else:
                for i in range(l1):
                    for j in range(i + 1, l1):
                        if (n_different_characters(first_str[:i] + first_str[i + 1:j] + first_str[j + 1:], second_str) < 1):
                            return True
                return False
        else:
            if (abs(l1 - l2) == 1):
                for i in range(l2):
                    if (n_different_characters(second_str[:i] + second_str[i + 1:], first_str) < 2):
                        return True
                return False
            else:
                for i in range(l2):
                    for j in range(i + 1, l2):
                        if (n_different_characters(second_str[:i] + second_str[i + 1:j] + second_str[j + 1:], first_str) < 1):
                            return True
                return False
    else:
        if (abs(l1 - l2) > 3):
            return False
        if (l2 == l1):
            if (n < 4):
                return True
            else:
                return False
        elif (l2 < l1):
            if (abs(l1 - l2) == 1):
                for i in range(l1):
                    if (n_different_characters(first_str[:i] + first_str[i + 1:], second_str) < 3):
                        return True
                return False
            elif (abs(l1 - l2) == 2):
                for i in range(l1):
                    for j in range(i + 1, l1):
                        if (n_different_characters(first_str[:i] + first_str[i + 1:j] + first_str[j + 1:], second_str) < 2):
                            return True
                return False
            else:
                for i in range(l1):
                    for j in range(i + 1, l1):
                        for k in range(j + 1, l1):
                            if (n_different_characters(first_str[:i] + first_str[i + 1:j] + first_str[j + 1:k] + first_str[k + 1:], second_str) < 1):
                                return True
                return False
        else:
            if (abs(l1 - l2) == 1):
                for i in range(l2):
                    if (n_different_characters(second_str[:i] + second_str[i + 1:], first_str) < 3):
                        return True
                return False
            elif (abs(l1 - l2) == 2):
                for i in range(l2):
                    for j in range(i + 1, l2):
                        if (n_different_characters(second_str[:i] + second_str[i + 1:j] + second_str[j + 1:], first_str) < 2):
                            return True
                return False
            else:
                for i in range(l2):
                    for j in range(i + 1, l2):
                        for k in range(j + 1, l2):
                            if (n_different_characters(second_str[:i] + second_str[i + 1:j] + second_str[j + 1:k] + second_str[k + 1:], first_str) < 1):
                                return True
                return False

def validate(_input, truth):
    _input, truth = simplify_str(_input), simplify_str(truth)
    return is_similar_to(_input, truth)
