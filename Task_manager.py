import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import json
import os
from datetime import datetime

STATUS_COLORS = {
    "To Do": "red",
    "In Progress": "yellow",
    "Done": "green"
}

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.users = []
        self.tasks = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        #Główna ramka
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        #Dodanie Przetrzeni pod Do zrobienia status i dodanie scrolbarr
        self.to_do_canvas = tk.Canvas(self.main_frame, borderwidth=0)
        self.to_do_frame = tk.Frame(self.to_do_canvas)
        self.to_do_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.to_do_canvas.yview)
        self.to_do_canvas.configure(yscrollcommand=self.to_do_scrollbar.set)

        self.to_do_scrollbar.pack(side="left", fill="y")
        self.to_do_canvas.pack(side="left", fill="both", expand=True)
        self.to_do_canvas.create_window((0, 0), window=self.to_do_frame, anchor="nw", tags="self.to_do_frame")

        self.to_do_frame.bind("<Configure>", lambda event, canvas=self.to_do_canvas: self.on_frame_configure(canvas))

        #Dodanie Przetrzeni pod Do zrobienia status i dodanie scrolbarr
        self.in_progress_canvas = tk.Canvas(self.main_frame, borderwidth=0)
        self.in_progress_frame = tk.Frame(self.in_progress_canvas)
        self.in_progress_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.in_progress_canvas.yview)
        self.in_progress_canvas.configure(yscrollcommand=self.in_progress_scrollbar.set)

        self.in_progress_scrollbar.pack(side="left", fill="y")
        self.in_progress_canvas.pack(side="left", fill="both", expand=True)
        self.in_progress_canvas.create_window((0, 0), window=self.in_progress_frame, anchor="nw", tags="self.in_progress_frame")

        self.in_progress_frame.bind("<Configure>", lambda event, canvas=self.in_progress_canvas: self.on_frame_configure(canvas))

        #Dodanie Przetrzeni pod zrobione status i dodanie scrolbarr
        self.done_canvas = tk.Canvas(self.main_frame, borderwidth=0)
        self.done_frame = tk.Frame(self.done_canvas)
        self.done_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.done_canvas.yview)
        self.done_canvas.configure(yscrollcommand=self.done_scrollbar.set)

        self.done_scrollbar.pack(side="left", fill="y")
        self.done_canvas.pack(side="left", fill="both", expand=True)
        self.done_canvas.create_window((0, 0), window=self.done_frame, anchor="nw", tags="self.done_frame")

        self.done_frame.bind("<Configure>", lambda event, canvas=self.done_canvas: self.on_frame_configure(canvas))

        #nagłówki dla każdego statusu
        tk.Label(self.to_do_frame, text="Do zrobienia", bg=STATUS_COLORS["To Do"], fg="white").pack(fill=tk.X)
        tk.Label(self.in_progress_frame, text="W trakcie", bg=STATUS_COLORS["In Progress"], fg="black").pack(fill=tk.X)
        tk.Label(self.done_frame, text="Zrobione", bg=STATUS_COLORS["Done"], fg="white").pack(fill=tk.X)

        #przyciski
        #nazwa przycisku opis
        self.add_task_button = tk.Button(self.root, text="Dodaj zadanie", command=self.add_task)
        #położenie przycisku i wygląd
        self.add_task_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_user_button = tk.Button(self.root, text="Dodaj użytkownika", command=self.add_user)
        self.add_user_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.report_button = tk.Button(self.root, text="Wygeneruj raport", command=self.generate_report)
        self.report_button.pack(side=tk.LEFT, padx=5, pady=5)

        #przyciski dodawania i loadowania zadań
        self.save_button = tk.Button(self.root, text="Zapisz zadania do formatu JSON", command=self.save_data)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = tk.Button(self.root, text="Załaduj zadania z pliku tasks.Json", command=self.load_data)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        #przestrzeń listy użytkowników
        self.user_frame = tk.Frame(self.root, borderwidth=2, relief="groove")
        self.user_frame.pack(side=tk.RIGHT, anchor="se", padx=10, pady=10, fill=tk.BOTH)

        #aktualizqacja lsity użytkowniów
        self.update_task_list()
        self.update_user_list()

    def on_frame_configure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def add_task(self):
        #jeżeli chcemy dodać zadanie do użytkownika którego nie ma w liście wystąpi błąd
        #sprawdzane za pomocą if not self.users users to lista naszych użytkowników
        if not self.users:
            messagebox.showwarning("Brak użytkownika w liście użytkowników", "Proszę dodać użytkownika przed dodaniem zadania")
            return

        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Dodaj Zadanie")


        #Tworzy etykietę z tekstem "Nazwa Zadania" i umieszcza ją w oknie
        tk.Label(add_task_window, text="Nazwa Zadania").pack()
        #Tworzy pole tekstowe (entry) w oknie
        task_name_entry = tk.Entry(add_task_window)
        #Umieszcza to pole tekstowe w oknie add_task_window pod etykietą
        task_name_entry.pack()

        tk.Label(add_task_window, text="Opis Zadania").pack()
        task_description_entry = tk.Entry(add_task_window)
        task_description_entry.pack()

        tk.Label(add_task_window, text="Przypisz do").pack()
        assign_to_combobox = ttk.Combobox(add_task_window, values=self.users)
        assign_to_combobox.pack()

        def save_task():
            task_name = task_name_entry.get()
            task_description = task_description_entry.get()
            assigned_to = assign_to_combobox.get()

            if task_name and task_description and assigned_to:
                if assigned_to in self.users:
                    self.tasks.append({
                        "name": task_name,
                        "description": task_description,
                        "status": "To Do",
                        "user": assigned_to,
                        "assigned_at": datetime.now().isoformat(),
                        "completed_at": None
                    })
                    self.update_task_list()
                    add_task_window.destroy()
                else:
                    messagebox.showerror("Nie znaleziono użytkownika", f"użytkownik '{assigned_to}' Nie został znaleziony w liście")
            else:
                messagebox.showwarning("Błąd dodawania zadania", "Wszystkie pola muszą być wypełnione")

        tk.Button(add_task_window, text="Dodaj Zadanie", command=save_task).pack()

    def add_user(self):
        #simpledialog to podstawowa funkcja która tworzy pole do wprowadzania danych
        user_name = simpledialog.askstring("Dodawanie użytkownika", "Podaj nazwę nowego użytkownika")
        if user_name and user_name.strip():
            if user_name.strip() not in self.users:
                self.users.append(user_name.strip())
                self.update_user_list()
            else:
                messagebox.showwarning("Zduplikowany użytkownik", "Użytkownik z podaną nazwą już istnieje")
        else:
            messagebox.showwarning("Błąd dodawanbia", "Nazwa użytkownika nie może być pusta")

    def update_task_list(self):
        #logika tworzenia odśwsieżania listy zadań podczas np przenoszenia zadania na innys tatus czy dodanie zadania
        #tworzymy listę ramek (frames) reprezentujących trzy sekcje zadań
        for frame in [self.to_do_frame, self.in_progress_frame, self.done_frame]:
            #Dla każdej sekcji (ramki), iterujemy przez wszystkie jej dzieci (widżety), które są w niej umieszczone
            #Metoda winfo_children() zwraca listę wszystkich widżetów znajdujących się wewnątrz danej ramki.
            for widget in frame.winfo_children():
                #Sprawdzamy, czy dany widżet jest instancją klasy tk.Frame
                #Jest to konieczne, ponieważ chcemy usuwać tylko te widżety, które są ramkami (czyli nasze karty zadań).
                if isinstance(widget, tk.Frame):
                    widget.destroy()

        for task in self.tasks:
            task_card = tk.Frame(self.to_do_frame, borderwidth=2, relief="groove")
            if task["status"] == "In Progress":
                task_card = tk.Frame(self.in_progress_frame, borderwidth=2, relief="groove")
            elif task["status"] == "Done":
                task_card = tk.Frame(self.done_frame, borderwidth=2, relief="groove")

            task_card.pack(pady=5, padx=20, fill=tk.X, expand=True)

            #kolor statusu
            status_color = STATUS_COLORS.get(task["status"], "white")
            status_bar = tk.Frame(task_card, bg=status_color, height=10)
            status_bar.pack(fill=tk.X)

            #wyświuetlanie informacji na karcie zaddania
            tk.Label(task_card, text=f"Zadanie: {task['name']}").pack(padx=5, pady=2, anchor="w")
            tk.Label(task_card, text=f"Opis Zadania: {task.get('description', '')}",wraplength=200).pack(padx=5, pady=2, anchor="w")
            tk.Label(task_card, text=f"Przypisane Do: {task['user']}").pack(padx=5, pady=2, anchor="w")
            tk.Label(task_card, text=f"Status: {task['status']}").pack(padx=5, pady=2, anchor="w")

            task_card.bind("<Button-1>", lambda e, task=task: self.on_task_click(e, task))

    def update_user_list(self):
        for widget in self.user_frame.winfo_children():
            widget.destroy()

        user_listbox = tk.Listbox(self.user_frame)
        user_listbox.pack(fill=tk.BOTH, expand=True)

        for user in self.users:
            user_listbox.insert(tk.END, user)

        user_listbox.bind("<Button-3>", self.on_user_right_click)

    def on_user_right_click(self, event):
        user_listbox = event.widget
        user_index = user_listbox.nearest(event.y)
        user_name = user_listbox.get(user_index)

        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="usuń użytkownika", command=lambda: self.remove_user(user_name))
        menu.post(event.x_root, event.y_root)

    def remove_user(self, user_name):
        if messagebox.askyesno("Potwierdź usunięcie", f"Jesteś pewny, że chcesz usunąć użytkownika'{user_name}' z zespołu?"):
            self.users.remove(user_name)
            self.update_user_list()
            tasks_to_reassign = [task for task in self.tasks if task["user"] == user_name]
            self.reassign_tasks(tasks_to_reassign)
            self.update_task_list()

    def reassign_tasks(self, tasks):
        if not tasks:
            return

        task = tasks.pop(0)
        reassign_window = tk.Toplevel(self.root)
        reassign_window.title("Przepisz zadanie ")

        tk.Label(reassign_window, text=f"Przepisz zadanie: {task['name']}").pack()

        tk.Label(reassign_window, text="Przypisz do:").pack()
        assign_to_combobox = ttk.Combobox(reassign_window, values=self.users)
        assign_to_combobox.pack()

        def save_reassignment():
            new_user = assign_to_combobox.get()
            if new_user in self.users:
                task["user"] = new_user
                reassign_window.destroy()
                self.update_task_list()
                self.reassign_tasks(tasks)  # Recursively reassign next task
            else:
                messagebox.showerror("nie znaleziono użytkownika", f"użytkownik '{new_user}' nnie został znaleziony w zespole")

        tk.Button(reassign_window, text="Zapisz zmiany", command=save_reassignment).pack()
    def on_task_click(self, event, task):
        #menu po kliknieciu na dane zadanie aby je zmienic
        menu = tk.Menu(self.root, tearoff=0)
        for status in ["To Do", "In Progress", "Done"]:
            menu.add_command(label=status, command=lambda status=status: self.change_task_status(task, status))
        menu.add_command(label="Edytuj zadanie", command=lambda: self.edit_task(task))
        menu.post(event.x_root, event.y_root)

    def change_task_status(self, task, status):
        #zmiana statusu tasku
        if status == "Done" and task["status"] != "Done":
            task["completed_at"] = datetime.now().isoformat()
        task["status"] = status
        self.update_task_list()

    def edit_task(self, task):
        #wywoływanie funkcji do otworzenia okna modyfikacji, padding użyty w celu zwiększenia poczaatkowego stanu wielkosci okna
        edit_task_window = tk.Toplevel(self.root, pady=50,padx=50)
        edit_task_window.title("Modyfikacja zadania")

        tk.Label(edit_task_window, text="Zmień nazwę").pack()
        task_name_entry = tk.Entry(edit_task_window)
        task_name_entry.insert(0, task["name"])
        task_name_entry.pack()

        tk.Label(edit_task_window, text="Zmień opis").pack()
        task_description_entry = tk.Entry(edit_task_window)
        task_description_entry.insert(0, task["description"])
        task_description_entry.pack()

        tk.Label(edit_task_window, text="Zmień przypisanie").pack()
        assign_to_combobox = ttk.Combobox(edit_task_window, values=self.users)
        assign_to_combobox.set(task["user"])
        assign_to_combobox.pack()

        def save_changes():
            task["name"] = task_name_entry.get()
            task["description"] = task_description_entry.get()
            task["user"] = assign_to_combobox.get()
            self.update_task_list()
            edit_task_window.destroy()

        tk.Button(edit_task_window, text="Zapisz Zmiany", command=save_changes).pack()

    def generate_report(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("RAPORT ZADAŃ")

        report_text = tk.Text(report_window)
        report_text.pack(fill=tk.BOTH, expand=True)

        user_task_count = {user: 0 for user in self.users}
        user_task_time = {user: 0 for user in self.users}

        for task in self.tasks:
            user_task_count[task["user"]] += 1
            if task["status"] == "Done" and task.get("completed_at") and task.get("assigned_at"):
                start_time = datetime.fromisoformat(task["assigned_at"])
                end_time = datetime.fromisoformat(task["completed_at"])
                duration = (end_time - start_time).total_seconds()
                user_task_time[task["user"]] += duration

        report_text.insert(tk.END, "Ilość zadań przypisanych do usera:\n")
        for user, count in user_task_count.items():
            report_text.insert(tk.END, f"{user}: {count} tasks\n")

        report_text.insert(tk.END, "\nCzas spędzony przez użytkownika na swoich zadaniach:\n")
        for user, time_spent in user_task_time.items():
            hours, remainder = divmod(time_spent, 3600)
            minutes, seconds = divmod(remainder, 60)
            report_text.insert(tk.END, f"{user}: {int(hours)}h {int(minutes)}m {int(seconds)}s\n")

    def save_data(self):
        data = {
            "users": self.users,
            "tasks": self.tasks
        }
        with open("tasks.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Zapisz dane", "Użytkownicy oraz zadania zostały zapisane")


    #wczytywanie danych z pliku json
    def load_data(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                data = json.load(f)
                self.users = data["users"]
                self.tasks = data["tasks"]
                #sprawdzenie czy w kazdyn wierszu json jest zawarty opis przypisanie oraz kiedy zostało skończone zadanie
                for task in self.tasks:
                    if 'description' not in task:
                        task['description'] = ''
                    if 'assigned_at' not in task:
                        task['assigned_at'] = datetime.now().isoformat()
                    if 'completed_at' not in task:
                        task['completed_at'] = None
                self.update_task_list()
                self.update_user_list()
        else:
            #wyswietlanie warninga kiedy nie udało się znaleźć pliku json
            messagebox.showwarning("Załaduj dane", "Nie znaleziono zapisanego pliku, lub zapisany został w innej nazwie niż tasks.json")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
