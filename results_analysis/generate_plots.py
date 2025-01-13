from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
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

    # plt.xticks([1], ["Runtimes"])

    for i, (runtime, path) in enumerate(zip(values, result_paths)):
        plt.text(1.1, runtime, str(path.stem), ha="left", va="center", fontsize=9)

    plt.title(title)
    plt.ylabel(ylabel)

    save_plot(path_to_save, title)


def generate_comparison_plot_multiple_y_axes(
        runtimes: list[float],
        fitness_values: list[float],
        results_scores: list[float],
        result_paths: list[Path],
        path_to_save: Path
) -> None:
    runs = [str(path.stem) for path in result_paths]

    fig, ax1 = plt.subplots()

    ax1.set_xlabel("Wykonanie algorytmu")
    ax1.set_ylabel("Czas wykonania (s)", color="blue")
    ax1.plot(runs, runtimes, marker="o", color="blue", label="Czas wykonania")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Wartość funkcji celu", color="green")
    ax2.plot(runs, fitness_values, marker="s", color="green", label="Wartość funkcji celu")
    ax2.tick_params(axis="y", labelcolor="green")

    ax3 = ax1.twinx()
    ax3.spines.right.set_position(("outward", 60))  # Offset the third axis
    ax3.set_ylabel("Ocena wyniku", color="red")
    ax3.plot(runs, results_scores, marker="^", color="red", label="Ocena wyniku")
    ax3.tick_params(axis="y", labelcolor="red")

    ax1.tick_params(axis='x', labelrotation=90)

    title = "Czasy wykonania, wartości funkcji celu i oceny wyniku dla różnych uruchomień"
    plt.title(title)

    fig.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.5)

    save_plot(path_to_save, title, True)


def generate_comparison_plot_normalized_y_axis(
        runtimes: list[float],
        fitness_values: list[float],
        results_scores: list[float],
        result_paths: list[Path],
        path_to_save: Path
) -> None:
    normalized_runtimes = (runtimes - np.min(runtimes)) / (np.max(runtimes) - np.min(runtimes))
    normalized_fitness = (fitness_values - np.min(fitness_values)) / (np.max(fitness_values) - np.min(fitness_values))
    normalized_scores = (results_scores - np.min(results_scores)) / (np.max(results_scores) - np.min(results_scores))

    runs = [str(path.stem) for path in result_paths]

    plt.plot(runs, normalized_runtimes, marker="o", label="Znormalizowany czas wykonania")
    plt.plot(runs, normalized_fitness, marker="s", label="Znormalizowana wartość funkcji celu")
    plt.plot(runs, normalized_scores, marker="^", label="Znormalizowana ocena wyniku")

    plt.xlabel("Wykonanie algorytmu")
    plt.ylabel("Znormalizowane wartości")

    title = "Znormalizowane czasy wykonania, wartości funkcji celu i oceny wyniku dla różnych uruchomień"
    plt.title(title)

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tick_params(axis='x', labelrotation=90)

    save_plot(path_to_save, title, True)


def save_plot(path_to_save: Path, title: str, tight: bool = False) -> None:
    logger.info(f"Saving '{title}' plot to: {path_to_save}")

    if tight:
        plt.savefig(str(path_to_save), bbox_inches='tight')
    else:
        plt.savefig(str(path_to_save))

    plt.close()
