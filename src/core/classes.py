#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:22:22 2023

@author: green-machine
"""

import io
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Any

import requests

from core.config import DATA_DIR
from core.constants import BASE_URL, DATASET_NAMES, INDEX_COL


class SeriesGroupingModel(str, Enum):
    """Defines grouping strategies for series IDs."""

    DOUGLAS_MODEL = "DOUGLAS"
    KENDRICK_MODEL = "KENDRICK"

    def compute_group_key(
        self,
        series_id: str,
        kendrick_separator: str = "S",
        douglas_prefix_len: int = 4,
    ) -> str:
        """
        Compute the group key for a given series ID based on the model.

        - KENDRICK_MODEL: group by prefix before the first separator
        - DOUGLAS_MODEL: group by fixed-length prefix
        """
        if self == SeriesGroupingModel.KENDRICK_MODEL:
            return series_id.split(kendrick_separator, 1)[0]
        if self == SeriesGroupingModel.DOUGLAS_MODEL:
            return series_id[:douglas_prefix_len]
        raise ValueError(f"Unsupported grouping model: {self!r}")


class Dataset(str, Enum):
    """
    Enum representing datasets with their respective file names and columns to
    be used.
    Each dataset can provide its configuration through the `get_kwargs` method.
    """

    DOUGLAS = "dataset_douglas.zip", (4, 7)
    USA_COBB_DOUGLAS = "dataset_usa_cobb-douglas.zip", (5, 8)
    USA_KENDRICK = "dataset_usa_kendrick.zip", (4, 7)
    USCB = "dataset_uscb.zip", (9, 12)

    def __new__(cls, value: str, range_tuple: tuple) -> None:
        """
        Custom initialization for the Enum class that also stores the
        `usecols` attribute for each dataset, computed from the range.
        """
        obj = str.__new__(cls)
        obj._value_ = value
        obj.usecols = range(*range_tuple)  # Convert the tuple to a range
        return obj

    def get_kwargs(self) -> dict[str, Any]:
        """
        Returns a dictionary of keyword arguments to be used for loading
        the dataset, including filepath, column configuration, and
        data processing options.

        Returns:
            dict: A dictionary of keyword arguments for dataset loading.
        """
        return {
            "filepath_or_buffer": DATA_DIR / self.value,
            "header": 0,
            "names": DATASET_NAMES,
            "index_col": INDEX_COL,
            "usecols": self.usecols,
        }


class URL(str, Enum):
    """
    Enum representing BEA data endpoints.
    Provides keyword arguments suitable for pandas readers.
    """

    FIAS = f"{BASE_URL}/FixedAssets/Release/TXT/FixedAssets.txt"
    NIPA = f"{BASE_URL}/Release/TXT/NipaDataA.txt"

    def get_kwargs(self) -> dict[str, Any]:
        """
        Build keyword arguments for loading the dataset.
        If the remote resource is reachable, load it into memory;
        otherwise, fall back to a local filename.
        """
        return {
            "filepath_or_buffer": self._resolve_source(),
            "header": 0,
            "names": DATASET_NAMES,
            "index_col": INDEX_COL,
            "thousands": ",",
        }

    def _resolve_source(self) -> str | io.BytesIO:
        """
        Resolve the data source to either an in-memory buffer
        or a local filename fallback.
        """
        response = requests.head(self.value)

        if response.status_code == HTTPStatus.OK:
            return io.BytesIO(requests.get(self.value).content)

        return self._filename

    @property
    def _filename(self) -> str:
        """Extract filename from URL."""
        return self.value.rsplit("/", 1)[-1]


@dataclass(frozen=True, eq=True)
class SeriesID:
    series_id: str
    source: Dataset | URL
