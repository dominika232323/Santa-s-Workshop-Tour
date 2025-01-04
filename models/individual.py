from deap import creator, base, tools
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA
import random


def make_preferences_dict(preferences):
    return {i: preferences.get_family_choices(i) for i in range(5000)}

def randomize_preferences_order(preferences):
    preferences_dict = make_preferences_dict(preferences)
    shuffled_items = random.sample(list(preferences_dict.items()), len(preferences_dict))
    return dict(shuffled_items)

def init_individual(family_choices):
    visits_day = [-1 for _ in range(5000)]
    visitors_by_days = {i: 0 for i in range(1,101)}

    preferences_random_order = randomize_preferences_order(family_choices)

    for family_id, preferences in preferences_random_order.items():
        family_size = family_choices.get_family_size(family_id)
        choices_skipped = 0

        for preference in preferences:
            if check_visiting_restriction(family_size, preference, visitors_by_days):
                visits_day[family_id] = preference
                visitors_by_days[preference] += family_size
                break
            else:
                choices_skipped += 1

        if choices_skipped == 10:
            least_occupied_day = min(visitors_by_days, key=visitors_by_days.get)
            visits_day[family_id] = least_occupied_day
            visitors_by_days[least_occupied_day] += family_size

    return visits_day, visitors_by_days

def check_visiting_restriction(family_size, preference, visitors_by_days):
    return visitors_by_days[preference] + family_size < 301


def create_population(family_choices, N):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,)) #temporary for testing
    creator.create("Individual", tuple, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, lambda: init_individual(family_choices))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    return toolbox.population(n=N)

