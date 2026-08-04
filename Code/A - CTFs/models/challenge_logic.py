import csv
from datetime import datetime
from pathlib import Path

class ChallengeEvaluator:
    def __init__(self, csv_path):
        self.csv_path = csv_path

        # Correct answers for case 1
        self.correct_answers = {"q1": "Image editing", "q2": "Middle",
            "q3": "Image to File Data", "q4": "Pink & Blue"}
        
        # Ensure the CSV file and its headers exist upon initialisation ???
        #self._initialise_csv()

    def validate_inputs(self, user_answers: dict) -> tuple[bool, str]:
        # Validate if the user completed all choices. Return a tuple: (True/False, 'Error message string')
        
        for key, value in user_answers.items(): # If the user hasn't selected anything return an empty string
            if not value or value.strip() == "":
                return False, "Please answer all questions before submitting!"
        return True, None

    def evaluate_answers(self, selections):
        correct_count = 0
        total_questions = len(self.correct_answers)
        results_breakdown = {}

        for key, correct_val in self.correct_answers.items():
            user_val = selections.get(key, "")
            is_correct = (user_val == correct_val)
            
            if is_correct:
                correct_count += 1
                
            results_breakdown[key] = is_correct

        # Passing status (must get all correct)
        passed = correct_count == total_questions

        return {"score": correct_count,
            "total": total_questions,
            "breakdown": results_breakdown,
            "passed": passed}

    def save_progress(self, username: str, challenge_name: str, score: int, total: int, passed: bool):
        # Append a new entry row to the file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Pass" if passed else "Fail"
        
        with open(self.csv_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([username, timestamp, challenge_name, score, total, status])
