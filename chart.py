import plotly.graph_objects as go

#to render piechart
def renderPiechart(good_eggs, dirty_eggs):
    fig = go.Figure(data=[go.Pie(
        labels=[
            f"Good Eggs: {round(good_eggs * 100 / (good_eggs + dirty_eggs), 3)}%", 
            f"Dirty Eggs: {round(dirty_eggs * 100 / (good_eggs + dirty_eggs), 3)}%"
        ],
        values=[good_eggs, dirty_eggs],
        marker_colors=["#00cc96", "#EF553B"]
    )])

    # Layout adjustments
    fig.update_layout(
        showlegend=True,
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=60),  # Leave space at bottom
        legend=dict(
            orientation="h",       # Horizontal layout
            yanchor="bottom",
            y=-0.2,                # Position legend below chart
            xanchor="center",
            x=0.5,
            font=dict(size=18)
        )
    )
    return fig