from dataclasses import dataclass

@dataclass #doesn't do anything!
class Task: #a model of data, identifies each of the columns, defines what the data would look like
    sale_id: int #type hints, for the programmer rather than the computer
    num_workers: int
    num_queens: int
    distance_km: float
    bonus_code: str
    final_cost: float