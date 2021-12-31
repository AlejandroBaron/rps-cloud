import sys
sys.path.insert(1,'../')

import numpy as np
import pandas as pd 

import plotly.express as px 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.io import to_html
from src.utils.game import rules


class StatsChecker:


    def __init__(self, cursor):
        
        self.cursor = cursor

    def move_counts(self):
        """
        Returns the past move outcomes
        """

        query = f"""SELECT SUM(R), SUM(P), SUM(S) FROM transitionmatrix1"""

        self.cursor.execute(query)

        R, P, S = self.cursor.fetchall()[0]

        return {"Rock":R, "Paper":P, "Scissors":S}
    
    def win_loss_counts(self):
        """
        Returns the win/loss outcomes
        """

        oc = self.outcome_counts()
        oc.pop("Ties")
        return oc

    def outcome_counts(self):
        """
        Returns the win/ties/loss outcomes
        """

        query = f"""SELECT SUM(W), SUM(T), SUM(L) FROM statistics"""

        self.cursor.execute(query)

        W, T, L = self.cursor.fetchall()[0]

        return {"User Wins":W, "Ties":T, "Bot Wins":L}
    
    def wins_by_depth(self):
        """
        Returns the statistics for each depth setting
        """

        query = f"""SELECT * FROM statistics"""

        self.cursor.execute(query)

        rows =  self.cursor.fetchall()

        return [{"Depth":D, "User Wins":W, "Ties":T, "Bot Wins":L} for D,W,T,L in rows]

    def get_transition_matrix(self, depth=2, as_pandas=True, as_probs=True):
        """
        Gets the transition matrix for the specified depth
        """

        query = f"""SELECT Hist, R, P, S FROM transitionmatrix{depth}"""

        self.cursor.execute(query)
        
        tm = self.cursor.fetchall()

        tm_pd = pd.DataFrame.from_records(tm, columns=["History","Rock","Paper","Scissors"])
        tm_pd = tm_pd.sort_values("History").set_index("History")
        if as_probs:
            RSP = tm_pd[["Rock","Paper","Scissors"]]
            tm_pd[["Rock","Paper","Scissors"]] = RSP.div(RSP.sum(axis=1),axis=0)
    
        return tm_pd if as_pandas else tm

    def get_stats_matrix(self, depth=2, as_pandas=True):
        """
        Gets the stats matrix (depth as rows, outcomes as columns)
        """

        query = f"""SELECT Depth, W, T, L FROM statistics"""

        self.cursor.execute(query)
        
        tm = self.cursor.fetchall()

        tm_pd = pd.DataFrame.from_records(tm, columns=["Depth","User Win","Tie","Bot Win"])
        tm_pd = tm_pd.sort_values("Depth").set_index("Depth")
        
        return tm_pd if as_pandas else tm
    

    def __piechart_plot(self, names: list[str], values: list[int], **kwargs):
        """Generates a plotly piechart

        Args:
            names (list[str]): labels
            values (list[int]): count for each label

        Returns:
            plotly go.Pie trace
        """

        fig = go.Pie(labels=list(names), values=list(values), **kwargs)
        
        return fig

    
    def get_piechart(self, plot_name: str, as_html=False, **kwargs):
        """Returns the specified chart under plot_name

        Args:
            plot_name (str): one of outcomes, winrate or moves
            as_html (bool, optional): returns the plot as an html figure. Defaults to False.

        Returns:
            plotly piechart
        """

        
        data = {"outcomes": self.outcome_counts,
                "winrate": self.win_loss_counts,
                "moves": self.move_counts}
        
        plot_data = data[plot_name]()

        plot = self.__piechart_plot(plot_data.keys(), plot_data.values(), **kwargs)
        return to_html(plot) if as_html else plot

    def transition_matrix_plot(self):
        """
        Plotly px.imshow heatmap for the transition matrix of depth 2
        """

        df = self.get_transition_matrix()

        fig = px.imshow(df, 
                        color_continuous_scale='Reds')

        html = to_html(fig, include_plotlyjs="require", full_html=False)
        
        return html

    def stats_matrix_plot(self):
        """
        Plotly px.imshow heatmap for the statistics for each depth
        """

        df = self.get_stats_matrix()

        fig = px.imshow(df, color_continuous_scale='algae')
        fig.update_traces(name="",hovertemplate=" Outcome: %{x} <br> Depth: %{y} <br> Count: %{z}")

        html = to_html(fig, include_plotlyjs="require", full_html=False)
        
        return html

    def report_plots(self):
        """
        Get report plots for 'Game outcomes',  'User moves','Winrate (exc. Ties)'
        """

        fig = make_subplots(rows=1, cols=3, 
                            specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
                            subplot_titles=('Game outcomes',  'User moves','Winrate (exc. Ties)'))

        fig.add_trace(self.get_piechart("outcomes", legendgroup='1', name="Outcomes", textinfo='value'), row=1, col=1)

        fig.add_trace(self.get_piechart("moves", legendgroup='2', name="Moves", textinfo='value'), row=1, col=2)

        fig.add_trace(self.get_piechart("winrate", legendgroup='3', name="Win vs Losses"), row=1, col=3)

        html = to_html(fig, include_plotlyjs="require", full_html=False)
        return html
    
    