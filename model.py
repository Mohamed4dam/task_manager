import csv
from typing import List, Union, Dict

class TaskModel:
    """
    Model class for managing tasks in the Task Reminder application.

    Attributes:
        file_path (str): The file path to the CSV file storing tasks.
    """

    def __init__(self, file_path: str = 'tasks.csv'):
        """
        Initialize the TaskModel.

        Parameters:
            file_path (str): The file path to the CSV file storing tasks.
        """
        self.file_path = file_path

    def get_tasks(self) -> List[Dict[str, Union[str, bool]]]:
        """
        Retrieve tasks from the CSV file.

        Returns:
            List[Dict[str, Union[str, bool]]]: A list of tasks as dictionaries.
        """
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []

    def add_task(self, task: Dict[str, Union[str, bool]]):
        """
        Add a new task to the CSV file.

        Parameters:
            task (Dict[str, Union[str, bool]]): A dictionary representing the task to be added.
        """
        tasks = self.get_tasks()
        tasks.append(task)
        self._save_tasks(tasks)

    def mark_task_as_done(self, task_id: int):
        """
        Mark a task as done in the CSV file.

        Parameters:
            task_id (int): The ID of the task to be marked as done.
        """
        tasks = self.get_tasks()
        if 0 < task_id <= len(tasks):
            tasks[task_id - 1]['Done'] = True
            self._save_tasks(tasks)

    def clear_all_tasks(self):
        """
        Clear all tasks from the CSV file.
        """
        self._save_tasks([])  # Clears all tasks by writing an empty list to the CSV file

    def _save_tasks(self, tasks: List[Dict[str, Union[str, bool]]]):
        """
        Save tasks to the CSV file.

        Parameters:
            tasks (List[Dict[str, Union[str, bool]]]): A list of tasks to be saved.
        """
        with open(self.file_path, 'w', newline='') as file:
            fieldnames = ['Task', 'Due Date', 'Done']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(tasks)
