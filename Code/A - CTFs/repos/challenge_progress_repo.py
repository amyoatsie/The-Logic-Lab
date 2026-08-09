import csv # CSV is used because the progress data can be easily read, updated and referenced in the app
from datetime import datetime
from pathlib import Path

class ChallengeProgressRepo: # Manage reading and writing challenge progress in the CSV file
    HEADERS = [
        "username",
        "timestamp",
        "currentChallenge",
        "numberCorrect",
        "totalQuestions",
        "result"
        ]

    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)

        # Create the CSV and its parent directory if they do not exist.
        self._initialise_csv()

# ----------------------------------------------------------------

    def _initialise_csv(self): # Create the progress CSV with headers if it does not exist
            # Ensure the parent data directory exists
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)

            if not self.csv_path.exists():
                with open(self.csv_path, mode="w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([
                            "username", 
                            "timestamp", 
                            "currentChallenge", 
                            "numberCorrect", 
                            "questionNumber", 
                            "result"]
                            )

# ----------------------------------------------------------------

    def get_completed_cases_from_csv(self, path, username): # Read the progress CSV file to find successful cases
        completed = set()

        if username:
            username = username.strip().lower()
    
        if not path.exists():
            return completed
        try:
            with open(path, "r", newline="") as f:
                reader = csv.DictReader(f)
            
                for row in reader:
                    if row["username"] != username:
                        continue
                
                    if row["result"].strip().lower() == "pass":
                        case_str = row["currentChallenge"]
                        num = int(''.join(filter(str.isdigit, case_str)
                            ))
                        completed.add(num)

        except Exception as e:
            print(f"Error reading progress: {e}")
    
        return completed

# ----------------------------------------------------------------

    def save_progress(self, username: str, challenge_name: str, score: int, total: int, passed: bool): # Update or create the user's progress record for a challenge
        self._initialise_csv()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Pass" if passed else "Fail"
        
        updated_rows = []
        record_found = False
        headers = []

        # Read existing records so the matching user's challenge can be updated without removing other users progress
        with open(self.csv_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            headers = next(reader) # Store the CSV column headings for the rewritten file
            clean_username = username.strip().lower()
            
            for row in reader:
                if not row:  # Ignore blank rows in the CSV
                    continue
                
                # Normalise usernames so comparisons are not affected by capitalisation
                existing_user = row[0].strip().lower() # maybe redundant
                
                # Replace the existing record when the user and challenge match
                if existing_user == clean_username and row[2] == challenge_name:
                    updated_rows.append([
                                clean_username, 
                                timestamp, 
                                challenge_name, 
                                score, 
                                total, 
                                status]
                                )
                    record_found = True
                else:
                    updated_rows.append(row)

        # Append a new record if the user has not previously attempted this challenge
        if not record_found:
            updated_rows.append([username, timestamp, challenge_name, score, total, status])

        # Rewrite the CSV  with the updated records
        with open(self.csv_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_rows) # Save full updated data set

# ----------------------------------------------------------------

    

    #