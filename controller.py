class TaskController:
    """
    Controller class for managing tasks in the Task Reminder application.

    Attributes:
        model (TaskModel): The model responsible for handling task data.
        view (TaskView): The view responsible for displaying the user interface.
    """

    def __init__(self, model, view):
        """
        Initialize the TaskController.

        Parameters:
            model (TaskModel): The model responsible for handling task data.
            view (TaskView): The view responsible for displaying the user interface.
        """
        self.model = model
        self.view = view
        self.view.controller = self

    def add_task(self, task):
        """
        Add a new task to the model and update the view.

        Parameters:
            task (dict): A dictionary representing the task to be added.
        """
        self.model.add_task(task)
        self.view.tree.delete(*self.view.tree.get_children())
        self.load_tasks()

    def edit_task(self, task_id):
        """
        Mark a task as done in the model and update the view.

        Parameters:
            task_id (int): The ID of the task to be marked as done.
        """
        self.model.mark_task_as_done(task_id)
        self.view.tree.delete(*self.view.tree.get_children())
        self.load_tasks()

    def clear_all_tasks(self):
        """
        Clear all tasks from the model and update the view.
        """
        self.model.clear_all_tasks()
        self.view.tree.delete(*self.view.tree.get_children())

    def load_tasks(self):
        """
        Load tasks from the model and update the view.
        """
        tasks = self.model.get_tasks()
        for i, task in enumerate(tasks, 1):
            done_status = task.get('Done', False)
            self.view.tree.insert('', 'end', text=i, values=(task['Task'], task['Due Date'], done_status))
