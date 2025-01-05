import deap
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import Individual


def cost_function(self, family_choices: DataGrabber, individual: Individual) -> float:
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


def calculate_restriction_penalty(individual: Individual) -> int:
    restriction_penalty = 0
    for chosen_day in individual[0]:
        visitors_by_days = individual[1]
        if not (125 <= visitors_by_days[chosen_day] < 301):
            restriction_penalty += 100000

    return restriction_penalty


def calculate_choice_penalty(
    family_choices: DataGrabber, individual: Individual
) -> int:

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
                    + family_choices.get_family_size(family_id) * choices_penalty_scheme[choice][1]
                )

        if not chosen:
            choice_penalty += (
                choices_penalty_scheme[10][0]
                + family_choices.get_family_size(family_id) * choices_penalty_scheme[10][1]
            )

    return choice_penalty


def calculate_accounting_penalty(individual: Individual) -> float:
    accounting_penalty = 0
    visitors_by_days = individual[1]
    prev_visitors = visitors_by_days[100]
    print(visitors_by_days)

    for visitors in reversed(visitors_by_days.values()):
        print(abs(visitors - prev_visitors))
        accounting_penalty += max(
            (visitors - 125.0) / 400.0 * visitors ** (0.5 + abs(visitors - prev_visitors) / 50.0),
            0,
        )
        prev_visitors = visitors

    return max(0, accounting_penalty)
