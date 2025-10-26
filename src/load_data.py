import pandas as pd
def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load sensor data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {filepath} was not found.")
    except pd.errors.ParserError:
        raise pd.errors.ParserError(f"Error parsing the CSV file at {filepath}.")