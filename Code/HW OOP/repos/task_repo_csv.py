import csv
from pathlib import Path

from models.task import Task

#repository aka a place to store stuff
#where all the logic happens, acts like a controller , where all the work happens

class TaskRepoCsv:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"
        self.csv_path = self.data_dir / "tasks.csv"
        self.fields = ["id", "subject", "description", "due_date", "status"]

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_csv_exists(self):
        self._ensure_data_dir()

        if self.csv_path.exists() is True:
            return

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()

    def load_all(self):
        self._ensure_csv_exists()

        tasks = []
        with open(self.csv_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("id", "").isdigit() is False:
                    continue

                tasks.append(
                    Task(
                        id=int(row["id"]),
                        subject=row.get("subject", ""),
                        description=row.get("description", ""),
                        due_date=row.get("due_date", ""),
                        status=row.get("status", "Pending"),
                    )
                )

        tasks.sort(key=lambda t: t.id)
        return tasks

    def save_all(self, tasks):
        self._ensure_csv_exists()

        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()

            for t in tasks:
                writer.writerow(
                    {
                        "id": str(t.id),
                        "subject": t.subject,
                        "description": t.description,
                        "due_date": t.due_date,
                        "status": t.status,
                    }
                )

    def get_next_id(self, tasks):
        if len(tasks) == 0:
            return 1

        max_id = 0
        for t in tasks:
            if t.id > max_id:
                max_id = t.id

        return max_id + 1

    def add(self, tasks, task):
        tasks.append(task)
        tasks.sort(key=lambda t: t.id)
        self.save_all(tasks)

    def update(self, tasks, task):
        index = None

        for i in range(len(tasks)):
            if tasks[i].id == task.id:
                index = i
                break

        if index is None:
            return False

        tasks[index] = task
        tasks.sort(key=lambda t: t.id)
        self.save_all(tasks)
        return True

    def delete(self, tasks, task_id):
        index = None

        for i in range(len(tasks)):
            if tasks[i].id == task_id:
                index = i
                break

        if index is None:
            return False

        del tasks[index]
        self.save_all(tasks)
        return True