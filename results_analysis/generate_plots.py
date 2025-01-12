from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from loguru import logger

from results_analysis.statistics import get_statistics


def generate_line_plot(xpoints: list[Any], ypoints: list[Any], xlabel: str, ylabel: str, title: str, path_to_save: Path) -> None:
    plt.plot(xpoints, ypoints)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.title(title)

    save_plot(path_to_save, title)


def generate_statistics_plot(
        generations: list[int],
        population_statistics: list[tuple[float, float, float, float]],
        path_to_save: Path
) -> None:

    mean_values, std_dev_values, min_values, max_values = get_statistics(population_statistics)

    plt.figure(figsize=(10, 6))

    plt.plot(generations, mean_values, label="Średnia wartość", marker='o', color='blue')
    plt.plot(generations, std_dev_values, label="Odchylenie standardowe", marker='s', color='green')
    plt.plot(generations, min_values, label="Minimalna wartość", marker='^', color='red')
    plt.plot(generations, max_values, label="Maksymalna wartość", marker='v', color='orange')

    title = "Statystyki funkcji celu na generację"
    plt.title(title)

    plt.xlabel("Generacja")
    plt.ylabel("Wartość funkcji celu")

    plt.legend()

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    save_plot(path_to_save, title)


def generate_boxplot(values: list[float], result_paths: list[Path], path_to_save: Path, title: str, ylabel: str) -> None:
    plt.boxplot(values)

    plt.xticks([1], ["Runtimes"])

    for i, (runtime, path) in enumerate(zip(values, result_paths)):
        plt.text(1.1, runtime, str(path.stem), ha="left", va="center", fontsize=9)

    plt.title(title)
    plt.ylabel(ylabel)

    save_plot(path_to_save, title)


def save_plot(path_to_save: Path, title: str) -> None:
    logger.info(f"Saving '{title}' plot to: {path_to_save}")
    plt.savefig(str(path_to_save))
    plt.close()
