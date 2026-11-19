from PIL import ImageTk, Image
import tkinter as tk
import os
from src import constants, custom_utils
from pathlib import Path
from src.execution_variables import execution_variables
exception_list = ["Empty", "Coin", "Metal", "Wood"]
stages_fixed_list = ['BUG', 'DARK', 'DRAGON', 'ELECTRIC', 'FAIRY', 'FIGHTING', 'FIRE', 'FLYING', 'GHOST', 'GRASS', 'GROUND', 'ICE', 'MEOWTH COIN MANIA', 'NONE', 'NORMAL', 'POISON', 'PSYCHIC', 'ROCK', 'STEEL', 'WATER', 'SP_084', 'MEOWTH COIN MANIA']
stages_set = set(stages_fixed_list)

class TeamData():
    
    def __init__(self, stage, icons) -> None:
        self.stage = stage
        self.icons = icons
        

class TeamLoader(tk.Toplevel):
     
    def __init__(self, master = None, root = None, folder = ""):
         
        super().__init__(master = master)
        self.title(f"Select a Team")
        self.root = root
        # self.geometry('500x500')        
        # self.create_widgets()



        # Read the file and parse each line into a TeamData
        with open(Path.joinpath(Path.home(), "Shuffle-Move", "config", "teamsData.txt"), "r") as file:
            lines = file.readlines()

        self.all_teams: list[TeamData] = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 3 or parts[0] != "TEAM":
                continue
            team_name = parts[1]
            icons_str = parts[2]
            for item in exception_list:
                icons_str = icons_str.replace(item, f"_{item}")
            icons = icons_str.split(",")
            # Append mega:
            if len(parts) > 4 and parts[4] != "-":
                mega_name = f"Mega_{parts[4]}"
                icons.append(mega_name)
            self.all_teams.append(TeamData(team_name, icons))
            if team_name == "SP_084":
                self.all_teams.append(TeamData("MEOWTH COIN MANIA", icons))

        self.teams: list[TeamData] = []

        self.filter_var = tk.BooleanVar(value=False)
        self.filter_checkbox = tk.Checkbutton(
            self,
            text="Filter to default stages only",
            variable=self.filter_var,
            command=self.populate_listbox,
        )
        self.filter_checkbox.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=(10, 5))

        # Create a Tkinter list with the second element of each tuple
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.populate_listbox()

        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.grid(row=1, column=2, sticky='ns', padx=(0, 10), pady=(10,10))

        self.listbox.config(yscrollcommand=scrollbar.set)

        self.image_preview = tk.Label(self)
        self.image_preview.grid(row=1, column=3, padx=5, pady=5)

        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.listbox.grid(row=1, column=1, sticky='ns')
        self.rowconfigure(1, weight=1)
        
        
        self.configure_initial_geometry()

    def populate_listbox(self):
        """Populate the team listbox, optionally filtering to stages_fixed_list."""
        if self.filter_var.get():
            self.teams = [t for t in self.all_teams if t.stage in stages_set]
            self.teams.sort(key=lambda x: stages_fixed_list.index(x.stage))
        else:
            self.teams = list(self.all_teams)
            self.teams.sort(
                key=lambda x: (0, stages_fixed_list.index(x.stage), "")
                if x.stage in stages_set
                else (1, 0, x.stage.lower())
            )
        self.listbox.delete(0, tk.END)
        for team in self.teams:
            self.listbox.insert(tk.END, team.stage)

    def configure_initial_geometry(self):
        self.update()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() - ( 2 * custom_utils.get_taskbar_size())

        x = int(screen_width / 2)
        y = 0

        app_width = self.winfo_width()
        
        # Set window geometry
        self.geometry(f"{app_width}x{screen_height}+{x}+{y}")

    def on_double_click(self, event):
        self.withdraw()
        self.root.destroy_selected_pokemons()
        selected_index = self.listbox.curselection()
        if selected_index:
            execution_variables.current_stage = self.teams[selected_index[0]].stage
            if execution_variables.current_stage == "MEOWTH COIN MANIA":
                execution_variables.current_stage = "SP_084"
            if execution_variables.current_stage == "SP_084":
                execution_variables.current_strategy = constants.move_strategy.get(constants.GRADING_WEEKEND_MEOWTH, "")
            else:
                execution_variables.current_strategy = constants.move_strategy.get(constants.GRADING_TOTAL_SCORE, "")
            execution_variables.has_modifications = True
            selected_team: TeamData = self.teams[selected_index[0]]
            for pokemon in selected_team.icons:
                self.root.insert_image_widget(f"{pokemon}.png")
                self.update_idletasks()
        
        self.root.stage_combobox.set(execution_variables.current_stage)
        self.root.strategy_combobox.set(execution_variables.current_strategy)
        self.destroy()