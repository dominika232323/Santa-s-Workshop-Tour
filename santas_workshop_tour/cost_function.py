from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import Individual
import numpy as np


def cost_function(individual: Individual, family_choices: DataGrabber) -> float:
    restriction_penalty = calculate_restriction_penalty(individual)
    choice_penalty = calculate_choice_penalty(individual, family_choices)
    accounting_penalty = calculate_accounting_penalty(individual)
    # print(
    #     "restriction_penalty:",
    #     restriction_penalty,
    #     "choice_penalty:",
    #     choice_penalty,
    #     "accounting_penalty",
    #     accounting_penalty,
    # )
    return (restriction_penalty + choice_penalty + accounting_penalty,)


def calculate_restriction_penalty(individual: Individual) -> int:
    restriction_penalty = 0
    visitors_counts = np.array(list(individual[1].values()))
    restriction_penalty = np.sum((visitors_counts < 125) | (visitors_counts > 300)) * 100000

    return restriction_penalty


def calculate_choice_penalty(individual: Individual, family_choices: DataGrabber) -> int:
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
        choices = np.array(family_choices.get_family_choices(family_id))
        match = np.where(choices == chosen_day)[0]
        if match.size > 0:
            choice = match[0]
            choice_penalty += (
                    choices_penalty_scheme[choice][0]
                    + family_choices.get_family_size(family_id) * choices_penalty_scheme[choice][1]
                )
        else:
            choice_penalty += (
                choices_penalty_scheme[10][0]
                + family_choices.get_family_size(family_id) * choices_penalty_scheme[10][1]
            )

    return choice_penalty


def calculate_accounting_penalty(individual: Individual) -> float:
    visitors_by_days = np.array(list(individual[1].values()))
    prev_visitors = np.roll(visitors_by_days, shift=1)
    prev_visitors[0] = visitors_by_days[-1]

    diff = np.abs(visitors_by_days-prev_visitors)
    penalty = np.sum((visitors_by_days - 125.0)/400 * visitors_by_days**(0.5 + diff/50.0))
    accounting_penalty = np.sum(penalty)
    return max(accounting_penalty, 0)
