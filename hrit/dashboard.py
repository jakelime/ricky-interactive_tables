import plotly.graph_objects as go

from hrit.utils import init_logger
from hrit.models import Database

APP_NAME = "hrit"
lg = init_logger(APP_NAME)


class Dashboard:
    def __init__(self, table_name: str = "1_tball"):
        self.fig = go.Figure()
        self.db = Database()
        lg.info("database initialized")
        self.df = self.db[table_name]
        lg.info(f"loaded table '{table_name}' from db")

    def create_plotly_figure(self) -> go.Figure:
        fig = go.Figure()
        df = self.df

        fig.add_trace(
            go.Table(
                header=dict(
                    values=list(df.columns), fill_color="paleturquoise", align="left"
                ),
                cells=dict(
                    values=df.transpose().values.tolist(),
                    fill_color="lavender",
                    align="left",
                ),
            )
        )
        buttons = []
        for i, product in enumerate(df["PRODUCT_NAME"].unique()):
            df_ = df[df["PRODUCT_NAME"] == product]
            buttons.append(
                dict(
                    method="update",
                    label=f"{product}",
                    args=[
                        {
                            "header": dict(
                                values=list(df_.columns),
                                fill_color="paleturquoise",
                                align="left",
                            ),
                            "cells": dict(
                                values=df_.transpose().values.tolist(),
                                fill_color="lavender",
                                align="left",
                            ),
                        }
                    ],
                )
            )

        # Add buttons
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=buttons,
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.1,
                    yanchor="top",
                ),
            ]
        )
        self.fig = fig
        return fig

    def export_html(self, filename: str = "dashboard.html"):
        self.fig.write_html(filename)
        lg.info(f"exported html - {filename}")


def create_dashboard_report():
    d = Dashboard(table_name="1_tball")
    d.create_plotly_figure()
    d.export_html("dashboard.html")
