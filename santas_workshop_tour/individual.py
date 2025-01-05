from typing import Tuple, List, Dict
from deap import creator, base, tools
from santas_workshop_tour.data_grabber import DataGrabber
import random
import heapq


class Individual:
    def __init__(self):
        if not hasattr(creator, "FitnessMin"):
            creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", tuple, fitness=creator.FitnessMin)

    def create_toolbox(self, init_func) -> base.Toolbox:
        toolbox = base.Toolbox()
        toolbox.register("individual", tools.initIterate, creator.Individual, init_func)
        return toolbox

    def init_individual(self, family_choices: DataGrabber) -> Tuple[List[int], Dict[int, int]]:
        visits_day = [-1 for _ in range(5000)]
        visitors_by_days = {i: 0 for i in range(1, 101)}

        preferences_random_order = self.randomize_preferences_order(family_choices)

        for family_id, preferences in preferences_random_order.items():
            family_size = family_choices.get_family_size(family_id)
            choices_skipped = 0

            for preference in preferences:
                if self.check_visiting_restriction(family_size, preference, visitors_by_days):
                    visits_day, visitors_by_days = self.schedule_family(
                        family_id, preference, visits_day, visitors_by_days, family_size
                    )
                    break
                else:
                    choices_skipped += 1

            if choices_skipped == 10:
                least_occupied_day = min(visitors_by_days, key=visitors_by_days.get)
                visits_day, visitors_by_days = self.schedule_family(
                    family_id, least_occupied_day, visits_day, visitors_by_days, family_size
                )

        visits_day, visitors_by_days = self.verify_lower_bound(
            family_choices, visits_day, visitors_by_days
        )
        return visits_day, visitors_by_days

    def randomize_preferences_order(self, preferences: DataGrabber) -> dict:
        preferences_dict = self.make_preferences_dict(preferences)
        shuffled_items = random.sample(list(preferences_dict.items()), len(preferences_dict))

        return dict(shuffled_items)

    def make_preferences_dict(self, preferences: DataGrabber) -> dict:

        return {i: preferences.get_family_choices(i) for i in range(5000)}

    def check_visiting_restriction(
        self, family_size: int, preference: DataGrabber, visitors_by_days: dict
    ) -> bool:
        return visitors_by_days[preference] + family_size < 301

    def schedule_family(
        self, family_id: int, day: int, visits_day: list, visitors_by_days: dict, family_size: int
    ) -> Tuple[list, dict]:
        visits_day[family_id] = day
        visitors_by_days[day] += family_size

        return visits_day, visitors_by_days

    def verify_lower_bound(
        self, family_choices: DataGrabber, visits_day: list, visitors_by_days: dict
    ) -> Tuple[list, dict]:
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
                                visits_day, visitors_by_days = self.change_visit_day(
                                    family_id,
                                    preference,
                                    day,
                                    family_choices,
                                    visits_day,
                                    visitors_by_days,
                                )
                                switch = True

                    if not switch:
                        day_to_swap = random.choice(ten_largest_days)
                        visits_day, visitors_by_days = self.change_visit_day(
                            family_id,
                            day_to_swap,
                            day,
                            family_choices,
                            visits_day,
                            visitors_by_days,
                        )

            if all_verified:
                return visits_day, visitors_by_days

    def change_visit_day(
        self,
        family_id: int,
        previous_day: int,
        new_day: int,
        family_choices: DataGrabber,
        visits_day: list,
        visitors_by_days: dict,
    ) -> Tuple[list, dict]:

        visitors_by_days[previous_day] -= family_choices.get_family_size(family_id)
        visitors_by_days[new_day] += family_choices.get_family_size(family_id)
        visits_day[family_id] = new_day

        return visits_day, visitors_by_days
