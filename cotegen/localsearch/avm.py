import sys
import random

import logging


class AVM():
    def __init__(self, fitness_calculator, input_parameters, retry_count=10, constraints=None):
        self.fitness = fitness_calculator
        self.retry_count = retry_count

        self.input_parameters = input_parameters
        self.constraints = constraints

    def _generate_random_arguments(self):
        args = {}
        for id, value in self.input_parameters.items():
            argument_value = value.get_random()
            args[id] = argument_value

        return args

    def calculate_fitness(self, args_values, index, x):
        new_args_values = args_values[:]
        new_args_values[index] = x

        new_args = self.values_to_args(new_args_values)

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

    def values_to_args(self, args):
        return dict(zip(self.input_parameters.keys(), args))

    def increment(self, arg_value, k):
        if isinstance(arg_value, int):
            return arg_value + k

        elif isinstance(arg_value, list):
            return list(map(lambda x: x + k, arg_value))

    def decrement(self, arg_value, k):
        if isinstance(arg_value, int):
            return arg_value - k

        elif isinstance(arg_value, list):
            return list(map(lambda x: x - k, arg_value))

    def search_on_one_argument(self, args, index):
        fitness = self.fitness.calculate(args)

        args_values = list(args.values())

        x = args_values[index]
        if self.violates_constraints(args_values, x, index):
            return args, 10000

        while fitness > 0:
            fitness_left = self.calculate_fitness(args_values, index, self.decrement(x, 1))
            fitness_right = self.calculate_fitness(args_values, index, self.increment(x, 1))

            if fitness <= fitness_left and fitness <= fitness_right:
                args_values[index] = x
                return self.values_to_args(args_values), fitness

            k = -1 if fitness_left < fitness_right else 1

            while self.calculate_fitness(args_values, index, self.increment(x, k)) < fitness:
                x = self.increment(x, k)
                k = k * 2

                if self.violates_constraints(args_values, x, index):
                    return args, 10000
                fitness = self.calculate_fitness(args_values, index, x)

        args_values[index] = x
        return self.values_to_args(args_values), fitness

    def do_avm(self, args):
        minimised_args = []
        fitness = 0

        index = 0
        for i in range(max(len(args.values()), self.retry_count)):
            minimised_args, fitness = self.search_on_one_argument(args, index)
            if fitness == 0:
                return minimised_args, fitness

            index = (index + 1) % len(args.values())

        return minimised_args, fitness

    def minimise(self):
        minimised_args = []
        fitness = 10000
        for i in range(self.retry_count):
            initial_args = self._generate_random_arguments()

            minimised_args, fitness = self.do_avm(initial_args)
            if fitness == 0:
                return minimised_args, fitness

        return minimised_args, fitness
