from deap import creator, base, tools
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA
import random
import heapq
from functools import partial


class EvolutionaryAlgorithm:
    def __init__(self):
        self.toolbox = base.Toolbox()

    def make_preferences_dict(self, preferences):
        return {i: preferences.get_family_choices(i) for i in range(5000)}

    def randomize_preferences_order(self, preferences):
        preferences_dict = self.make_preferences_dict(preferences)
        shuffled_items = random.sample(list(preferences_dict.items()), len(preferences_dict))
        return dict(shuffled_items)

    def verify_lower_bound(self, family_choices, visits_day, visitors_by_days):
        while True:
            all_verified = True
            for day, visitors in visitors_by_days.items():
                switch = False
                if visitors < 125:
                    all_verified = False
                    ten_largest = heapq.nlargest(
                        10, visitors_by_days.items(), key=lambda item: item[1]
                    )
                    ten_largest_days = [i[0] for i in ten_largest]
                    for family_id, preference in enumerate(visits_day):
                        if preference in ten_largest_days:
                            if day in family_choices.get_family_choices(family_id):
                                visitors_by_days[preference] -= family_choices.get_family_size(
                                    family_id
                                )
                                visitors_by_days[day] += family_choices.get_family_size(family_id)
                                visits_day[family_id] = day
                                switch = True
                    if not switch:
                        day_to_swap = random.choice(ten_largest_days)
                        visitors_by_days[day_to_swap] -= family_choices.get_family_size(family_id)
                        visitors_by_days[day] += family_choices.get_family_size(family_id)
                        visits_day[family_id] = day
            if all_verified:
                return visits_day, visitors_by_days

    def check_visiting_restriction(self, family_size, preference, visitors_by_days):
        return visitors_by_days[preference] + family_size < 301

    def init_individual(self, family_choices):
        visits_day = [-1 for _ in range(5000)]
        visitors_by_days = {i: 0 for i in range(1, 101)}

        preferences_random_order = self.randomize_preferences_order(family_choices)

        for family_id, preferences in preferences_random_order.items():
            family_size = family_choices.get_family_size(family_id)
            choices_skipped = 0

            for preference in preferences:
                if self.check_visiting_restriction(family_size, preference, visitors_by_days):
                    visits_day[family_id] = preference
                    visitors_by_days[preference] += family_size
                    break
                else:
                    choices_skipped += 1

            if choices_skipped == 10:
                least_occupied_day = min(visitors_by_days, key=visitors_by_days.get)
                visits_day[family_id] = least_occupied_day
                visitors_by_days[least_occupied_day] += family_size

        visits_day, visitors_by_days = self.verify_lower_bound(
            family_choices, visits_day, visitors_by_days
        )
        return visits_day, visitors_by_days

    def create_population(self, family_choices, N):
        creator.create("FitnessMin", base.Fitness, weights=(1.0,))  # temporary for testing
        creator.create("Individual", tuple, fitness=creator.FitnessMin)

        self.toolbox.register(
            "individual",
            tools.initIterate,
            creator.Individual,
            lambda: self.init_individual(family_choices),
        )
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        return self.toolbox.population(n=N)

    def cost_function(self, individual, family_choices):
        restriction_penalty = self.calculate_restriction_penalty(individual)
        choice_penalty = self.calculate_choice_penalty(family_choices, individual)
        accounting_penalty = self.calculate_accounting_penalty(individual)
        print(
            "restriction_penalty:",
            restriction_penalty,
            "choice_penalty:",
            choice_penalty,
            "accounting_penalty",
            accounting_penalty,
        )
        return (restriction_penalty + choice_penalty + accounting_penalty,)

    def calculate_restriction_penalty(self, individual):
        restriction_penalty = 0
        for chosen_day in individual[0]:
            visitors_by_days = individual[1]
            if not (125 <= visitors_by_days[chosen_day] < 301):
                restriction_penalty += 100000

        return restriction_penalty

    def calculate_choice_penalty(self, family_choices, individual):
        choice_penalty = 0
        choices_penalty_scheme = {
            0: (0, 0),
            1: (50, 0),
            2: (50, 9),
            3: (100, 9),
            4: (200, 9),
            5: (200, 18),
            6: (300, 18),
            7: (300, 36),
            8: (400, 36),
            9: (500, 235),
            10: (500, 434),
        }
        for family_id, chosen_day in enumerate(individual[0]):
            chosen = False
            for choice, day in enumerate(family_choices.get_family_choices(family_id)):
                if day == chosen_day:
                    chosen = True
                    choice_penalty += (
                        choices_penalty_scheme[choice][0]
                        + family_choices.get_family_size(family_id)
                        * choices_penalty_scheme[choice][1]
                    )
            if not chosen:
                choice_penalty += (
                    choices_penalty_scheme[10][0]
                    + family_choices.get_family_size(family_id) * choices_penalty_scheme[10][1]
                )
        return choice_penalty

    def calculate_accounting_penalty(self, individual):
        accounting_penalty = 0
        visitors_by_days = individual[1]
        prev_visitors = visitors_by_days[100]
        for visitors in reversed(visitors_by_days.values()):
            # print(visitors)
            # print(abs(visitors-prev_visitors))
            accounting_penalty += (
                (visitors - 125.0)
                / 400.0
                * visitors ** (0.5 + abs(visitors - prev_visitors) / 50.0)
            )
            # print(accounting_penalty)
            prev_visitors = visitors
        return max(0, accounting_penalty)


algorithm = EvolutionaryAlgorithm()
grabber = DataGrabber(FAMILY_DATA, sep=",")
population = algorithm.create_population(grabber, 10)
algorithm.toolbox.register(
    "evaluate",
    partial(
        algorithm.cost_function,
        family_choices=grabber,
    ),
)
for ind in population:
    print(algorithm.toolbox.evaluate(ind))
