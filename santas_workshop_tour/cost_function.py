from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import Individual
import numpy as np
import pandas as pd


def cost_function(individual: Individual, family_choices: DataGrabber) -> tuple:
    restriction_penalty = calculate_restriction_penalty(individual)
    choice_penalty = calculate_choice_penalty(individual, family_choices)
    accounting_penalty = calculate_accounting_penalty(individual)
    fitness = restriction_penalty + choice_penalty + accounting_penalty
    print(
        "restriction_penalty:",
        restriction_penalty,
        "choice_penalty:",
        choice_penalty,
        "accounting_penalty",
        accounting_penalty,
    )
    return fitness, restriction_penalty, choice_penalty, accounting_penalty


def calculate_restriction_penalty(individual: Individual) -> int:
    restriction_penalty = 0
    visitors_counts = np.array(list(individual[1].values()))
    restriction_penalty = np.sum((visitors_counts < 125) | (visitors_counts > 300)) * 100000000

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
    prev_visitors[0] = prev_visitors[1]
    diff = np.abs(visitors_by_days-prev_visitors)
    penalty = np.sum((visitors_by_days - 125.0)/400 * visitors_by_days**(0.5 + diff/50.0))
    accounting_penalty = np.sum(penalty)
    return max(accounting_penalty, 0)


# taken from example kaggle implementation
# added to verify correctness
def alternate_cost_function(individual, family_data):
    individual = individual[0]
    data = pd.read_csv("data/family_data.csv", index_col='family_id')
    penalty = 0


    family_size_dict = data[['n_people']].to_dict()['n_people']

    cols = [f'choice_{i}' for i in range(10)]
    choice_dict = data[cols].to_dict()

    N_DAYS = 100
    MAX_OCCUPANCY = 300
    MIN_OCCUPANCY = 125

    # from 100 to 1
    days = list(range(N_DAYS,0,-1))
    daily_occupancy = {k:0 for k in days}

    choice_penalty = 0
    # Looping over each family; d is the day for each family f
    for f, d in enumerate(individual):

        # Using our lookup dictionaries to make simpler variable names
        n = family_size_dict[f]
        choice_0 = choice_dict['choice_0'][f]
        choice_1 = choice_dict['choice_1'][f]
        choice_2 = choice_dict['choice_2'][f]
        choice_3 = choice_dict['choice_3'][f]
        choice_4 = choice_dict['choice_4'][f]
        choice_5 = choice_dict['choice_5'][f]
        choice_6 = choice_dict['choice_6'][f]
        choice_7 = choice_dict['choice_7'][f]
        choice_8 = choice_dict['choice_8'][f]
        choice_9 = choice_dict['choice_9'][f]

        # add the family member count to the daily occupancy
        daily_occupancy[d] += n

        # Calculate the penalty for not getting top preference
        if d == choice_0:
            choice_penalty += 0
        elif d == choice_1:
            choice_penalty  += 50
        elif d == choice_2:
            choice_penalty  += 50 + 9 * n
        elif d == choice_3:
            choice_penalty  += 100 + 9 * n
        elif d == choice_4:
            choice_penalty  += 200 + 9 * n
        elif d == choice_5:
            choice_penalty  += 200 + 18 * n
        elif d == choice_6:
            choice_penalty  += 300 + 18 * n
        elif d == choice_7:
            choice_penalty  += 300 + 36 * n
        elif d == choice_8:
            choice_penalty  += 400 + 36 * n
        elif d == choice_9:
            choice_penalty  += 500 + 36 * n + 199 * n
        else:
            choice_penalty  += 500 + 36 * n + 398 * n

    penalty += choice_penalty
    # print(daily_occupancy)
    # print("choice_cost", choice_penalty)
    # for each date, check total occupancy
    #  (using soft constraints instead of hard constraints)
    restrict_penalty = 0
    for _, v in daily_occupancy.items():
        if (v > MAX_OCCUPANCY) or (v < MIN_OCCUPANCY):
            restrict_penalty += 100000000
    # print("restrict_cost", restrict_penalty)
    penalty += restrict_penalty
    # Calculate the accounting cost
    # The first day (day 100) is treated special
    accounting_cost = (daily_occupancy[days[0]]-125.0) / 400.0 * daily_occupancy[days[0]]**(0.5)
    # using the max function because the soft constraints might allow occupancy to dip below 125
    accounting_cost = max(0, accounting_cost)

    # Loop over the rest of the days, keeping track of previous count
    yesterday_count = daily_occupancy[days[0]]
    for day in days[1:]:
        today_count = daily_occupancy[day]
        diff = abs(today_count - yesterday_count)
        accounting_cost += max(0, (daily_occupancy[day]-125.0) / 400.0 * daily_occupancy[day]**(0.5 + diff / 50.0))
        yesterday_count = today_count
    # print("accounting_cost", accounting_cost)
    penalty += accounting_cost

    return penalty, restrict_penalty, choice_penalty, accounting_cost