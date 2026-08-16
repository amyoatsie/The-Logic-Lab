class ChallengeEvaluator: # Handle answer validation, evaluation and progress storage for challenges
    '''
Validates and evaluates answers submitted for a challenge. It determines the user's score and 
whether the challenge has been passed without handling any graphical interface or CSV storage.
    '''
    def __init__(self):
        '''
    Initialises the evaluator with the correct answers used to assess the user's responses.
        '''
        # Dictionary to store each question ID with its correct answer - Using a dictionary allows answers to be retrieved efficiently using the question ID
        self.correct_answers = {
            "q1": "Image editing", 
            "q2": "Middle",
            "q3": "Image to File Data", 
            "q4": "Pink & Blue"}

    #----------------------------------------------------------------------------

    def validate_inputs(self, user_answers: dict) -> tuple[bool, str | None]: # Check that all questions have a valid response before evaluating their responses
        '''
    Args:
        user_selections (dict) is a dictionary containing question IDs as keys and the user's selected answers as values
            - A dictionary is used because each answer needs to be associated with the relevant question.
    ~
    Returns:
        tuple: Contains a boolean indicating whether the inputs are valid and a string containing an error message
            - A tuple is used as it groups the two related results together and a boolean is used as the inputs only 
            need to be existance validated at this point.
        '''
        for key, value in user_answers.items(): 
            # Reject empty responses before answers are evaluated
            if not value or value.strip() == "":
                return False, "Please answer all questions before submitting!"
        return True, None

    #----------------------------------------------------------------------------

    def evaluate_answers(self, user_answers: dict): # Compare user selections with the correct answers and calculate the result
        '''
    Args:
        user_selections (dict) is a dictionary containing question IDs as keys and the user's selected answers as values
            - A dictionary is used because each answer needs to be associated with the relevant question.
    ~
    Returns:
        dict: Contains the calculated score, total number of questions and pass/fail result
            - A dictionary is used so each result can be accessed from a single location using a key.
        '''
        correct_count = 0
        total_questions = len(self.correct_answers)

        results_breakdown = {}  # Dictionary to record whether each individual question was answered correctly

        for key, correct_val in self.correct_answers.items(): # Iterate through each question and compare the user's answer with the stored answer
            user_val = user_answers.get(key, "")
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

    #----------------------------------------------------------------------------