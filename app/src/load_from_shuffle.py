from PIL import ImageTk, Image
import tkinter as tk
import os
from src import constants, custom_utils, log_utils
from pathlib import Path
from src.execution_variables import current_run

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import ImageSelectorApp

log = log_utils.get_logger()
exception_list = ["Empty", "Coin", "Metal", "Wood", "Fog"]
stages_fixed_list = ['BUG', 'DARK', 'DRAGON', 'ELECTRIC', 'FAIRY', 'FIGHTING', 'FIRE', 'FLYING', 'GHOST', 'GRASS', 'GROUND', 'ICE', 'NORMAL', 'POISON', 'PSYCHIC', 'ROCK', 'STEEL', 'WATER', 'SP_084', 'MEOWTH COIN MANIA', constants.SURVIVAL_MODE, '037', constants.RANDOM]
stages_set = set(stages_fixed_list)

class TeamData():
    
    def __init__(self, stage, icons, stage_added=[]) -> None:
        self.stage = stage
        self.icons = icons
        self.stage_added = stage_added
        

class TeamLoader(tk.Toplevel):
     
    def __init__(self, master = None, root: "ImageSelectorApp" = None, folder = "", forced_team=""): #type: ignore
         
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
            if constants.SURVIVAL_MODE in line:
                log.info("Updating the survival mode team string to the fixed one")
                line = constants.SURVIVAL_TEAM_STRING
            parts = line.strip().split()
            if len(parts) < 3 or parts[0] != "TEAM":
                continue
            team_name = parts[1]
            icons_str = parts[2]
            stage_added = []
            if len(parts) >= 6:
                stage_added_str = parts[5]
                stage_added = stage_added_str.split(",")
            for item in exception_list:
                icons_str = icons_str.replace(item, f"_{item}")
            icons = icons_str.split(",")
            # Append mega:
            if len(parts) > 4 and parts[4] != "-":
                mega_name = f"{constants.MEGA_PREFIX}{parts[4]}"
                icons.append(mega_name)
            self.all_teams.append(TeamData(team_name, icons, stage_added))
            if team_name == "SP_084":
                self.all_teams.append(TeamData(constants.MEOWTH_COIN_MANIA, icons))

        for stage_name in stages_fixed_list:
            if not any(team.stage == stage_name for team in self.all_teams):
                self.all_teams.append(TeamData(stage_name, ["_Wood", "_Metal"], []))

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

        if forced_team:
            search_index_number = 0
            for index in range(self.listbox.size()):
                if self.listbox.get(index) == forced_team:
                    search_index_number = index
                    break
            self.listbox.selection_set(search_index_number)
            self.listbox.activate(search_index_number)
            self.on_double_click(forced_team=forced_team)

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

    def on_double_click(self, event=None, forced_team=None):
        self.withdraw()
        self.root.destroy_selected_pokemons()
        selected_index = self.listbox.curselection()
        if selected_index:
            current_run.current_stage = self.teams[selected_index[0]].stage
            log.info(f"Loading the team: {current_run.current_stage}")
            if current_run.current_stage == constants.SURVIVAL_MODE:
                log.info(f"CURRENT SURVIVAL MODE TEAM: {current_run.survival_mode_current_team}")
                new_pokemon_list = custom_utils.load_file_as_list(constants.SURVIVAL_MODE_TXT)
                self.teams[selected_index[0]].stage_added.extend(new_pokemon_list)
                self.teams[selected_index[0]].icons.extend(new_pokemon_list)
                self.root.disable_switch("check_drop")
                self.root.disable_switch("is_puzzle_stage")
                self.root.disable_switch("pause_survival")
                self.root.disable_switch("debug_mode")
                self.root.disable_switch("coin_stage")
                self.root.disable_switch("escalation_battle")
                self.root.disable_switch("meowth_37")
                self.root.disable_switch("timed_stage")
                self.root.disable_switch("tapper")
                self.root.disable_switch("mega_boosted_score")
                self.root.disable_switch("expand_mega")
                self.root.activate_switch("survival_mode")
                self.root.activate_switch("auto_next_stage")
                self.root.activate_switch("fast_swipe")
            else:
                self.root.disable_switch("survival_mode")
                self.root.disable_switch("mega_boosted_score")
                self.root.disable_switch("fast_swipe")
                self.root.activate_switch("expand_mega")

            if current_run.current_stage == constants.MEOWTH_COIN_MANIA:
                current_run.current_stage = "SP_084"
            if current_run.current_stage == "SP_084":
                current_run.current_strategy = constants.move_strategy.get(constants.GRADING_WEEKEND_MEOWTH, "")
            else:
                current_run.current_strategy = constants.move_strategy.get(constants.GRADING_DISRUPTION_BOOSTED_SCORE, "")
            current_run.has_modifications = True
            selected_team: TeamData = self.teams[selected_index[0]]
            
            if forced_team:
                self.root.master.withdraw()
            #First Append all Stage Added Pokemons
            for pokemon in selected_team.stage_added:
                self.root.insert_image_widget(f"{pokemon}.png", stage_added=True)
            #Then Append the others
            for pokemon in selected_team.icons:
                if not pokemon in selected_team.stage_added and f"{pokemon}.png" not in custom_utils.mega_list:
                    self.root.insert_image_widget(f"{pokemon}.png", stage_added=False)
            for pokemon in selected_team.icons:
                if not pokemon in selected_team.stage_added and f"{pokemon}.png" in custom_utils.mega_list:
                    self.root.insert_image_widget(f"{pokemon}.png", stage_added=False)
            if forced_team:
                self.root.master.deiconify()
                self.root.configure_initial_geometry()
                self.root.master.update()





            self.update_idletasks()

        self.root.stage_combobox.set(current_run.current_stage)
        self.root.strategy_combobox.set(current_run.current_strategy)
        log.info("Loading Finished")
        self.destroy()