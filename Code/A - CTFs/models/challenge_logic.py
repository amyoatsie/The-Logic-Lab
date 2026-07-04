import csv #???
from datetime import datetime
from pathlib import Path

class ChallengeEvaluator:
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)

        # Correct answers for case 1
        self.correct_answers = {
            "q1": "Image editing",
            "q2": "Middle",
            "q3": "Image to File Data",
            "q4": "Pink & Blue"}
        
        # Ensure the CSV file and its headers exist upon initialisation ???
        self._initialise_csv()

    def _initialise_csv(self):
        """Creates the progress csv with header columns if it does not exist yet."""
        if not self.csv_path.exists():
            # Ensure the parent directory (e.g., data/) exists
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.csv_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Challenge", "Score", "Total Questions", "Status"])

    def validate_inputs(self, user_answers: dict) -> tuple[bool, str]:
        """
        Validates if the user completed all choices.
        Returns a tuple: (True/False, 'Error message string')
        """
        for key, value in user_answers.items():
            # If the user hasn't selected anything, a combobox returns an empty string
            if not value.strip():
                return False, "Please answer all questions before submitting!"
        return True, "Valid"

    def evaluate_answers(self, user_answers: dict) -> dict:
        """Compares user selections against the answer key and calculates statistics."""
        correct_count = 0
        total_questions = len(self.correct_answers)
        results_breakdown = {}

        for key, correct_val in self.correct_answers.items():
            user_val = user_answers.get(key, "")
            is_correct = (user_val == correct_val)
            
            if is_correct:
                correct_count += 1
                
            results_breakdown[key] = is_correct

        # Determine passing status (e.g., must get all correct, or at least half)
        passed = correct_count == total_questions

        return {
            "score": correct_count,
            "total": total_questions,
            "breakdown": results_breakdown,
            "passed": passed
        }

    def save_progress(self, challenge_name: str, score: int, total: int, passed: bool):
        """Appends a new tracking entry row to our external progress logging file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Pass" if passed else "Fail"
        
        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, challenge_name, score, total, status])
