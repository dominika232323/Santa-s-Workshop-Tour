import pandas as pd

from pathlib import Path


class DataGrabber:
    def __init__(self, path_to_dataset: Path, *, sep: str = ',', config: dict = None) -> None:
        self._path_to_dataset = path_to_dataset
        self._sep = sep
        self._config = config

        if config is None:
            self._data_frame = pd.read_csv(path_to_dataset, sep=sep)
        else:
            if "sep" not in config.keys():
                self._data_frame = pd.read_csv(path_to_dataset, sep=sep, **config)
            else:
                self._data_frame = pd.read_csv(path_to_dataset, **config)

    @property
    def path_to_dataset(self) -> Path:
        return self._path_to_dataset

    @property
    def data_frame(self) -> pd.DataFrame:
        return self._data_frame

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}("
            f"path_to_dataset={self._path_to_dataset!r}, "
            f"sep={self._sep!r}, "
            f"config={self._config!r})"
        )

    def data(self) -> list[list[any]]:
        return self._data_frame.values.tolist()

    def columns(self) -> list[str]:
        return self._data_frame.columns.tolist()

    def get_family_choices(self, family_id: int) -> list[int] | None:
        family_data = self._data_frame[self._data_frame["family_id"] == family_id]

        if not family_data.empty:
            choices = family_data.iloc[0, 1:-1].tolist()
            return choices
        else:
            return None
