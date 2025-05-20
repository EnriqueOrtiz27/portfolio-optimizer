import numpy as np
import pandas as pd
from io import StringIO
from fastapi import UploadFile


class InvalidFileError(ValueError):
    pass


def read_returns_csv(file: UploadFile) -> pd.DataFrame:
    """
    Reads an uploaded CSV file and returns a cleaned pandas DataFrame
    containing daily returns. Raises InvalidFileError if invalid.
    """
    try:
        content = file.file.read().decode('utf-8')
        df = pd.read_csv(StringIO(content), index_col=0)

        # Drop empty rows or columns, especially the first one
        df = df.dropna(how='all')

        # Validate it's numeric data
        if not all(df.dtypes.apply(lambda dt: np.issubdtype(dt, np.number))):
            raise InvalidFileError("CSV contains non-numeric data.")

        return df
    except Exception as e:
        raise InvalidFileError("Invalid CSV format or unable to read file.") from e
