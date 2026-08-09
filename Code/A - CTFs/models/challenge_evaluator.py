
class ChallengeEvaluator: # Handle answer validation, evaluation and progress storage for challenges
    def __init__(self, csv_path):
        self.csv_path = csv_path

        # Dictionary to store each question ID with its correct answer
        # Using a dictionary allows answers to be retrieved efficiently using the question ID
        self.correct_answers = {
            "q1": "Image editing", 
            "q2": "Middle",
            "q3": "Image to File Data", 
            "q4": "Pink & Blue"}
        
        # Ensure the progress CSV and its headers exist  before the app trys to read or write data
        self._initialise_csv()

    def validate_inputs(self, user_answers: dict) -> tuple[bool, str | None]: # Check that all questions have a valid response
        for key, value in user_answers.items(): 
            # Reject empty responses before answers are evaluated
            if not value or value.strip() == "":
                return False, "Please answer all questions before submitting!"
        return True, None

    def evaluate_answers(self, selections): # Compare user selections with the correct answers and calculate the result
        correct_count = 0
        total_questions = len(self.correct_answers)

        results_breakdown = {}  # Dictionary to record whether each individual question was answered correctly

        for key, correct_val in self.correct_answers.items(): # Iterate through each question and compare the user's answer with the stored answer
            user_val = selections.get(key, "")
            is_correct = (user_val == correct_val)
            
            if is_correct:
                correct_count += 1
                
            results_breakdown[key] = is_correct

        # Define the passing status (must get all correct)
        passed = correct_count == total_questions

        return {
            "score": correct_count,
            "total": total_questions,
            "breakdown": results_breakdown,
            "passed": passed
            }
