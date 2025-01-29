import json
import os


def string_test(i, hyperparameters, best_fitness, results_dir, runtime):
    s = (
        "\\subsection{Test " + f"{i}" + "}\n"
        "\n"
        "\\subsubsection{Konfiguracja hiperparametrów}\n"
        "\\begin{itemize}\n"
        "\\item prawdopodobieństwo krzyżowania: $" + f"{hyperparameters.get("crossover_probability")}" + "$,\n"
        "\\item prawdopodobieństwo $P_m$ zostania wybranym do mutacji: $" + f"{hyperparameters.get("mutation_probability")}" + "$,\n"
        "\\item prawdopodobieństwo $P_{mf}$ na zmianę przypisanego dnia na inny podczas mutacji: $" + f"{hyperparameters.get("family_mutation_probability")}" + "$,\n"
        "\\item liczba rodziców do krzyżowania: $" + f"{hyperparameters.get("parents")}" + "$,\n"
        "\\item rozmiar elity: $" + f"{hyperparameters.get("elite_size")}" + "$,\n"
        "\\item liczba generacji: $" + f"{hyperparameters.get("generations")}" + "$,\n"
        "\\item wielkość populacji: $" + f"{hyperparameters.get("population_size")}" + "$\n"
        "\\end{itemize}\n"
        "\n"
        "\\subsubsection{Otrzymane wyniki}\n"
        "\n"
        "Otrzymana wartość funkcji celu najlepszego osobnika: $" + f"{best_fitness}" + "$\n"
        "\n"
        "Wykres przedstawiający zmianę wartości funkcji celu najlepszego osobnika od generacji:\n"
        "\n"
        "\\begin{figure}[H]\n"
        "\\centering\n"
        "\\includegraphics[width=0.9\\linewidth]{" + f"{results_dir}/best_individuals_fitness_values_plot.png" + "}\n"
        "\\end{figure}\n"
        "\n"
        "Wykres przedstawiający wartość średnią, minimalną, maksymalną oraz odchylenie standardowe funkcji celu populacji od generacji:\n"
        "\n"
        "\\begin{figure}[H]\n"
        "\\centering\n"
        "\\includegraphics[width=0.9\\linewidth]{" + f"{results_dir}/statistics_plot.png" + "}\n"
        "\\end{figure}\n"
        "\n"
        f"Czas działania algorytmu: ${runtime}$ sekund\n"
    )

    return s


def string_compare(results_dir, test_num, score):
    s = (
        "\\section{Porównanie uzyskanych wyników}\n"
        "\n"
        "Wykres przedstawiający rozkład wartości funkcji celu najlepszego osobnika z każdego testu:\n"
        "\n"
        "\\begin{figure}[H]\n"
        "\\centering\n"
        "\\includegraphics[width=0.9\\linewidth]{" + f"{results_dir}/fitness_value_distribution.png" + "}\n"
        "\\end{figure}\n"
        "\n"
        "Wykres przedstawiający rozkład czasu działania algorytmu z każdego testu:\n"
        "\n"
        "\\begin{figure}[H]\n"
        "\\centering\n"
        "\\includegraphics[width=0.9\\linewidth]{" + f"{results_dir}/runtime_distribution.png" + "}\n"
        "\\end{figure}\n"
        "\n"
        "Wykres przedstawiający czasy działania algorytmu, wartości funkcji celu najlepszego osobnika oraz ocenę wyniku obliczaną ze wzoru:\n"
        "\\begin{equation} \\label{score}\n"
        "score = 0.7 * fitness\\_function\\_value + 0.3 * time\n"
        "\\end{equation}\n"
        "\n"
        "\\begin{figure}[H]\n"
        "\\centering\n"
        "\\includegraphics[width=0.9\\linewidth]{" + f"{results_dir}/comparison_plot.png" + "}\n"
        "\\end{figure}\n"
        "\n"
        "Wykres przedstawiający znormalizowane czasy działania algorytmu, wartości funkcji celu najlepszego osobnika oraz ocenę wyniku obliczaną ze wzoru \\ref{score}:\n"
        "\n"
        "\\begin{figure}[H]\n"
        "\\centering\n"
        "\\includegraphics[width=0.9\\linewidth]{" + f"{results_dir}/comparison_normalized_plot.png" + "}\n"
        "\\end{figure}\n"
        "\n"
        f"Test {test_num} osiągnął najlepszy wynik o wartości $" + f"{score}" + "$ (obliczonej ze wzoru \\ref{score}).\n"
    )

    return s


def print_sections_test():
    evolutionary_results_dir = "evolutionary_algorithm"

    timestamps = sorted(os.listdir(evolutionary_results_dir))

    for index, timestamp in enumerate(timestamps):
        timestamp_dir = os.path.join(evolutionary_results_dir, timestamp)

        if os.path.isdir(timestamp_dir):
            hyperparams_file = os.path.join(timestamp_dir, "hyperparameters.json")
            fitness_file = os.path.join(timestamp_dir, "fitness_function_value.txt")
            runtime_file = os.path.join(timestamp_dir, "time.txt")

            hyperparameters = {}
            if os.path.exists(hyperparams_file):
                with open(hyperparams_file, "r") as f:
                    hyperparameters = json.load(f)

            fitness_value = 0
            if os.path.exists(fitness_file):
                with open(fitness_file, "r") as f:
                    fitness_value = f.read().strip()

            runtime = 0
            if os.path.exists(runtime_file):
                with open(runtime_file, "r") as f:
                    runtime = f.read().strip()

            print(string_test(index + 1, hyperparameters, fitness_value, f"results/{timestamp_dir}", runtime))
            print()

    return timestamps


def extract_timestamp_and_value(json_file_path):
    with open(json_file_path, "r") as f:
        data = json.load(f)

    for path, value in data.items():
        timestamp = os.path.basename(path)
        return timestamp, value


def print_section_comparison(timestamp, timestamps):
    comparison_results_dir = "comparisons"
    timestamp_dir = os.path.join(comparison_results_dir, timestamp)

    best_result_timestamp, best_result_value = extract_timestamp_and_value(os.path.join(timestamp_dir, "best_result.json"))
    test_num = timestamps.index(best_result_timestamp) + 1

    print(string_compare(f"results/{timestamp_dir}", test_num, best_result_value))


if __name__ == "__main__":
    timestamps = print_sections_test()
    print_section_comparison("20250125_123918", timestamps)

