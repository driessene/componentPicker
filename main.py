import itertools


class PassiveComponent:
    def __init__(self, nom_value, tolerance):
        self.nom_value = nom_value
        self.tolerance = tolerance

    @property
    def min_value(self):
        return self.nom_value * (1 - self.tolerance)

    @property
    def max_value(self):
        return self.nom_value * (1 + self.tolerance)

    def value(self, precent_error=0):
        value = self.nom_value * (1 + precent_error)
        if value > self.max_value:
            return self.max_value
        elif value < self.min_value:
            return self.min_value
        else:
            return value

    def __str__(self):
        return f'{self.value} ± {self.tolerance}'


class Resistor(PassiveComponent):
    def __init__(self, value, tolerance, max_power):
        super().__init__(value, tolerance)
        self.max_power = max_power

    def __str__(self):
        return f'{self.value} ± {self.tolerance}'


class Capacitor(PassiveComponent):
    def __init__(self, value, tolerance, max_voltage):
        super().__init__(value, tolerance)
        self.max_voltage = max_voltage

    def __str__(self):
        return f'{self.value} ± {self.tolerance}'


class System:
    def __init__(self, components: dict, outputs: dict):
        self.components = components  # A dictionary containing a single component assigned to a single key (id)
        self.outputs = outputs  # A dictionary containing equations representing outputs of the system based on its components

        # Verify if every parameter in every equation is in components and that it is the right type
        for output_name, equation in self.outputs.items():
            lambda_params = equation.__code__.co_varnames
            for param in lambda_params:
                if param not in self.components:
                    raise Exception(f'{param} not provided in components')
                component_type = param[0]  # Determine if it's a Resistor (R) or Capacitor (C)
                if (
                    (component_type == 'R' and not isinstance(self.components[param], Resistor)) or
                    (component_type == 'C' and not isinstance(self.components[param], Capacitor))
                ):
                    raise Exception(
                        f'{param} type does not match expected type')

    def evaluate_output(self, output_name):
        equation = self.outputs[output_name]
        lambda_params = equation.__code__.co_varnames
        component_values = [self.components[param].value() for param in lambda_params]
        return equation(*component_values)

    def result(self):
        result = {}
        for output in self.outputs.keys():
            result[output] = self.evaluate_output(output)
        return result


class Problem:
    def __init__(self, targets: dict, outputs: dict, components: dict):
        self.targets = targets  # A dictionary containing the targets for each output of the system
        self.outputs = outputs  # A dictionary containing the output equations for the system
        self.components = components  # A dictionary containing each possible component in equation in lists
        self.results = []

    def total_error(self, system):
        result = system.result()
        total_error = 0
        for output_name, target in self.targets.items():
            output_value = result[output_name]
            total_error += abs(target - output_value)
        return total_error

    def evaluate(self):

        for component_combination in itertools.product(*self.components.values()):
            # Get new system
            system = System(dict(zip(self.components.keys(), component_combination)), self.outputs)

            # Calculate the total error for the current combination
            total_error = self.total_error(system)

            self.results.append((system, total_error))

        # Sort the results by total error (lower is better)
        self.results.sort(key=lambda x: abs(x[1]))

        return self.results


def main():
    # All component values
    resistor_vals = [
        0, 1, 2.2, 4.7, 7.5, 10, 15, 22, 33, 39, 47, 56, 68, 100, 120, 150, 220, 330, 390, 470, 510, 680,
        1e3, 1.5e3, 2e3, 2.2e3, 3e3, 4.7e3, 5.1e3, 5.6e3, 7.5e3, 8.2e3, 10e3, 15e3, 22e3, 33e3, 47e3, 56e3,
        68e3, 75e3, 100e3, 150e3, 220e3, 330e3, 470e3, 580e3, 1e6, 2e6, 4.7e6, 5.6e6
    ]

    # Constants

    # All components
    r1 = [Resistor(val, 0.05, 0.25) for val in resistor_vals]
    r2 = [Resistor(val, 0.05, 0.25) for val in resistor_vals]

    # Component mapping
    components = {
        'R1': r1,
        'R2': r2
    }

    # Output functions
    def out1(R1, R2):
        try:
            return 10 * R2 / (R1 + R2) - 117e-6 * R1 * R2 / (R1 + R2) - 4.6
        except ZeroDivisionError:
            return float('inf')

    # Output mapping
    outputs = {
        'Ib': lambda R1, R2: out1(R1, R2)
    }

    # Output targets
    targets = {
        'Ib': 0
    }

    # Computation
    problem = Problem(targets, outputs, components)
    solutions = problem.evaluate()

    # Results
    print_prompt = input('display top _ (all for all): ')
    if print_prompt == 'all':
        print_top = len(solutions)
    else:
        print_top = int(print_prompt)

    best = solutions[:print_top]

    # Top results
    for system, total_error in best:
        print(f"Total Error: {total_error}")

        # Get the components for the current system and print their values
        components = system.components
        for component_name, component in components.items():
            print(f'{component_name}: {component.value()}')
        print("\n")


if __name__ == '__main__':
    main()
