import gui
import model
import controller
def main():
    root = gui.tk.Tk()

    data = model.TaskModel()
    view = gui.TaskView(root)
    logic = controller.TaskController(data, view)

    logic.load_tasks()

    root.mainloop()

if __name__ == "__main__":
    main()