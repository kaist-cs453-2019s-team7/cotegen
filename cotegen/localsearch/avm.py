import sys
import random

import logging


class AVM():
    def __init__(self, fitness_calculator, input_parameters, retry_count=10, constraints=None):
        self.fitness = fitness_calculator
        self.retry_count = retry_count

        self.input_parameters = input_parameters
        self.constraints = constraints

    def _generate_random_integers(self):
        args = []
        for id, value in self.input_parameters.items():
            integer = value.get_random()
            args.append(integer)

        return args

    def calculate_fitness(self, args, index, x):
        new_args = args[:]
        new_args[index] = x

        return self.fitness.calculate(new_args)

    def violates_constraints(self, args, x, index):
        parameter = list(self.input_parameters.values())[index]

        if not parameter.is_valid(x):
            return True

        if not self.constraints:
            return False

        x_id = list(self.input_parameters.keys())[index]
        for constraint in self.constraints:
            for index, id in enumerate(self.input_parameters.keys()):
                test = {
                    x_id: x,
                    id: args[index]
                }
                if constraint.is_defined(test):
                    if not constraint.is_valid(test):
                        return True
    
        return False

    def search_on_one_argument(self, args, index):
        fitness = self.fitness.calculate(args)

        x = args[index]
        if self.violates_constraints(args, x, index):
            return args, 10000

        while fitness > 0:
            new_args = args[:]
            new_args[index] = x
            logging.debug((new_args, fitness))

            fitness_left = self.calculate_fitness(args, index, x - 1)
            fitness_right = self.calculate_fitness(args, index, x + 1)

            if fitness <= fitness_left and fitness <= fitness_right:
                args[index] = x
                return args, fitness

            k = -1 if fitness_left < fitness_right else 1

            while self.calculate_fitness(args, index, x + k) < fitness:
                x = x + k
                k = k * 2

                if self.violates_constraints(args, x, index):
                    return args, 10000
                fitness = self.calculate_fitness(args, index, x)

        args[index] = x
        return args, fitness

    def do_avm(self, args):
        minimised_args = []
        fitness = 0

        index = 0
        for i in range(max(len(args), self.retry_count)):
            minimised_args, fitness = self.search_on_one_argument(args, index)
            if fitness == 0:
                return minimised_args, fitness

            index = (index + 1) % len(args)

        return minimised_args, fitness

    def minimise(self):
        minimised_args = []
        fitness = 10000
        for i in range(self.retry_count):
            initial_args = self._generate_random_integers()

            minimised_args, fitness = self.do_avm(initial_args)
            if fitness == 0:
                return minimised_args, fitness
        
        return minimised_args, fitness
