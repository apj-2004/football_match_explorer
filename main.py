#this is the main python code file for the football match explorer  project
# Author:   APJ
#StartDate: 24-06-2026

#import
import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from data.statsbomb_manager import StatsBombManager
from ui.match_panel import MatchPanel
from ui.navigation_panel import NavigationPanel
from ui.pitch_panel import PitchPanel
from ui.player_panel import PlayerPanel

## App Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

## Main Window

root = ctk.CTk()

root.title("Football Match Explorer")
root.geometry("1400x800")

#main frame
main_frame = ctk.CTkFrame(root)

main_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

##Loading the matches

#StatsBombManager
manager = StatsBombManager()



#competitions_df
competitions_df = manager.get_competitions()
competition_names = sorted(
    competitions_df["competition_name"]
    .unique()
    .tolist()
)

#create a function for the popup
def open_load_match_window():

    load_window = ctk.CTkToplevel(root)

    load_window.title("Load Match")
    load_window.geometry("500x400")

    navigation_panel = NavigationPanel(load_window, competition_names)

    #competition selected
    def competition_selected(choice):
        season_names = manager.get_seasons(choice)

        navigation_panel.update_seasons(season_names)

    def season_selected(choice):
        manager.get_season_details(choice)

        manager.load_matches_df()

        matches_name = manager.get_matches_list()

        navigation_panel.update_matches(matches_name)

    def match_selected(choice):
        manager.update_match_id(choice)

    def load_match_button_action(load_window):
        manager.load_match()

        if manager.check_events_lineups_df() is True:
            CTkMessagebox(
                title="Match Load Info",
                message="Match events and lineups loaded ok!",
                icon="info"
            )
        else:
            CTkMessagebox(
                title="Match Load Info",
                message="Match events and lineups not loaded!",
                icon="error"
            )

            return

        match_info = manager.get_match_info()

        match_panel.update_match_info(match_info)

        team_statistics = manager.get_team_statistics()
        match_panel.update_team_statistics(team_statistics)

        lineup_details = manager.get_starting_lineups()
        pitch_panel.plot_starting_lineup(lineup_details)

        player_panel.update_players(lineup_details)

        load_window.grab_release()

        load_window.destroy()

    navigation_panel.set_competition_callback(competition_selected)

    navigation_panel.set_season_callback(season_selected)

    navigation_panel.set_match_callback(match_selected)

    navigation_panel.set_load_match_button_callback(
        lambda: load_match_button_action(load_window)
    )

    load_window.transient(root)
    load_window.grab_set()

menu_bar = tk.Menu(root)

file_menu = tk.Menu(
    menu_bar,
    tearoff=0
)

file_menu.add_command(
    label="Load Match",
    command=open_load_match_window
)

menu_bar.add_cascade(
    label="File",
    menu=file_menu
)

root.config(menu=menu_bar)



#content frame
content_frame= ctk.CTkFrame(main_frame)
content_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

content_frame.grid_columnconfigure(0, weight=2)

content_frame.grid_columnconfigure(1, weight=2)
content_frame.grid_columnconfigure(2, weight=4)

content_frame.grid_rowconfigure(
    0,
    weight=1
)

#creating subframes within the content frame.
pitch_container=ctk.CTkFrame(content_frame)
pitch_container.grid(
    row=0,
    column=2,
    sticky="nsew",
    padx=5,
    pady=5
)

pitch_panel = PitchPanel(pitch_container)

match_container=ctk.CTkFrame(content_frame)
match_container.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=5, pady=5
)

match_panel = MatchPanel(match_container)

#player_panel

def player_selected(player_id):

    player_heatmap_Data = manager.get_player_heatmap_data(player_id)

    pitch_panel.plot_player_heat_map(player_heatmap_Data)

players_container = ctk.CTkFrame(content_frame)

players_container.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=5,
    pady=5
)

player_panel = PlayerPanel(players_container, player_selected_callback= player_selected)

root.mainloop()
