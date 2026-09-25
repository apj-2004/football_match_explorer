#this is for the pitch panel on the left hand side of the application.
import customtkinter as ctk
from mplsoccer import Pitch
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PitchPanel:

    def __init__(self, parent):

        self.parent = parent

        self.main_frame = ctk.CTkFrame(
            self.parent
        )

        self.main_frame.pack(
             fill="both",
             expand=True
        )

        self.figure= Figure(
            figsize=(8,6),
            dpi=100,
            facecolor="#2B2B2B"
        )

        self.ax = self.figure.add_subplot(111)

        self.pitch = Pitch(
            pitch_type="statsbomb",
            pitch_color="#f2f2f0",
            line_color="#0d0d0d"
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self.main_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.update_pitch()


    def update_pitch(self):
        self.ax.clear()

        self.pitch.draw(ax=self.ax)

        self.canvas.draw()

    def plot_starting_lineup(self, lineup_data):

        self.update_pitch()

        #home_team

        self.ax.text(
                    25, 78,
                    lineup_data.get("home_team")+"-"+lineup_data.get("home_formation"),
                    ha= "center", va="center",
                    fontsize=14
        )

        self.pitch.formation(
                            lineup_data.get("home_formation"),
                            kind = "scatter",
                            positions=lineup_data.get("home_lineup")["position.id"],
                            color='#053e7a',
                            half=True,
                            s=500,
                            alpha=0.1,
                            ax=self.ax
                        )

        self.pitch.formation(
                            lineup_data.get("home_formation"),
                            kind = "text",
                            text = lineup_data.get("home_lineup")["jersey_number"],
                            positions=lineup_data.get("home_lineup")["position.id"],
                            color='#053e7a',
                            half=True,
                            va='center', ha='center',
                            ax=self.ax
                        )

        #away_team

        self.pitch.formation(
                            lineup_data.get("away_formation"),
                            kind = "scatter",
                            positions=lineup_data.get("away_lineup")["position.id"],
                            color='#7a0505',
                            half=True, flip=True,
                            s=500,
                            alpha=0.1,
                            ax=self.ax
                        )

        self.pitch.formation(
                            lineup_data.get("away_formation"),
                            kind = "text",
                            text = lineup_data.get("away_lineup")["jersey_number"],
                            positions=lineup_data.get("away_lineup")["position.id"],
                            color='#7a0505',
                            half=True, flip=True,
                            va='center', ha='center',
                            ax=self.ax
                        )

        self.ax.text(
        75, 78,
        lineup_data.get("away_team")+"-"+lineup_data.get("away_formation"),
        ha="center",va="center",
        fontsize=14
        )

        self.canvas.draw()

    def plot_player_heat_map(self, player_location_data):

        self.update_pitch()

        player_location_data = np.array(player_location_data.tolist())

        player_x = player_location_data[:,0]
        player_y = player_location_data[:,1]

        self.pitch.kdeplot(
            player_x,
            player_y,
            ax = self.ax,
            fill =True,
            levels=100,
            cmap="coolwarm",
            alpha=0.3
        )

        self.canvas.draw()
