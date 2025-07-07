import plotly.graph_objects as go

#to render piechart
def renderPiechart(good_eggs, dirty_eggs):
    # Show placeholder if no data
    if good_eggs + dirty_eggs == 0:
        values = [1, 1]
        labels = ["Good Eggs: 0%", "Dirty Eggs: 0%"]
    else:
        values = [good_eggs, dirty_eggs]
        total = good_eggs + dirty_eggs
        labels = [
            f"Good Eggs: {round(good_eggs * 100 / total, 3)}%",
            f"Dirty Eggs: {round(dirty_eggs * 100 / total, 3)}%"
        ]
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=["#00cc96", "#EF553B"]
    )])

    # Layout adjustments
    fig.update_layout(
        showlegend=True,
        height=420,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=20, b=40),  # Leave space at bottom
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