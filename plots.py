import numpy as np
from scipy.stats import exponweib

import plotly.graph_objects as go

linewidth_pt = 240
linewidth_px = linewidth_pt*1.25

font_size_pt = 12
font_size_px = font_size_pt#/0.75

# ============================

base_layout = dict(
    
    # sizing
    width = linewidth_px,
    height = 0.6*linewidth_px,

    # fonts
    font = {
        "family": 'Serif',
        "size": font_size_px,
    },

    # legend
    legend = {
        "font_size" : font_size_px-2
    }

)

utilization_layout =  dict(

    # X axis    
    xaxis_title='Utilization',
    xaxis_range=[-0.05, 1.05],
    xaxis_tickvals=[0,1],
    xaxis_ticktext=[0,1],

    # margins
    margin = dict(
        t=10,
        r=0,
        b=20,
        l=20
    ),
)


# ============================

def failure_rate_plot(
    ):

    # Get the figure data
    figure_data = __prep_failure_rate__(
        )

    if figure_data is None:
        return

    # Generate the figure
    figure = go.Figure()
    for trace in figure_data:
        figure.add_traces(trace)
    
    # Apply default layouts
    figure.update_layout(base_layout)

    # Customize the layout
    figure.update_layout(dict(
        
        # resize
        height = 0.75*linewidth_px,

        # X axis    
        xaxis_title='Time',
        xaxis_range=[-0.5, 14.5],
        xaxis_tickvals=[0],

        # Y axis    
        yaxis_title='Failure rate',
        yaxis_tickvals=[0],

        # margins 
        margin = dict(
            t=0,
            r=0,
            b=0,
            l=0
        ),

        # legend
        legend = dict(
            orientation='h',
            # x = 0.95,
            # xanchor = 'right',
            y = 1.02,
            yanchor = 'bottom'
        ),

    ))

    return figure

def __prep_failure_rate__(

    ):

    # constants
    a = 1
    x = np.linspace(0,30,100)

    # Burn-in phase
    c = 0.2
    scale = 1
    loc = 0
    y_burnin = exponweib.pdf(x, a, c, loc, scale)

    # Random failures
    rate = 0.05
    y_random = [rate]*np.size(x)

    # Wearing phase
    c = 10
    scale = 20
    loc = -5
    y_wearout = exponweib.pdf(x, a, c, loc, scale)

    # Observed failure rate
    y_total = y_burnin + y_random + y_wearout

    traces = []
    traces.append(go.Scatter(
        x=x,
        y=y_total,
        mode='lines',
        name='Observed failure rate',
        line=dict(
                color='black',
                width=3,
        )))
    traces.append(go.Scatter(
        x=x,
        y=y_burnin,
        mode='lines',
        name='Burn-in failures',
        line=dict(
                color='red',
                width=3,
                dash='dash',
        )))
    traces.append(go.Scatter(
        x=x,
        y=y_random,
        mode='lines',
        name='Random failures',
        line=dict(
                color='lightgrey',
                width=3,
                dash='dot',
        )))
    traces.append(go.Scatter(
        x=x,
        y=y_wearout,
        mode='lines',
        name='Wear-out failures',
        line=dict(
                color='lightgreen',
                width=3,
                dash='longdash',
        )))

    return traces

# ============================

def power_model_plot(
    P0,P1=1
    ):

    # Get the figure data
    figure_data = __prep_power_model__(
        P0,P1
        )

    if figure_data is None:
        return

    # Generate the figure
    figure = go.Figure()
    for trace in figure_data:
        figure.add_traces(trace)
    
    # Apply default layouts
    figure.update_layout(base_layout)
    figure.update_layout(utilization_layout)

    # Customize the layout
    figure.update_layout(
        # Y axis
        yaxis_title='Power draw',
        yaxis_tickvals=[0,P0,P1],
        yaxis_ticktext=[0,r'$P_0$',r'$P_1$'],


        # legend
        legend = dict(
            orientation='v',
            x = 0.95,
            xanchor = 'right',
            y = 0.05,
            yanchor = 'bottom'
        ),
    )

    return figure


def __prep_power_model__(
    P0,P1
    ):

    U_model = [0,0,1]
    P_model = [0,P0,P1]

    traces = []

    traces.append(go.Scatter(
                        x=U_model, 
                        y=P_model,
                        mode='lines',
                        name='Model',
                        line=dict(
                            color='red',
                            width=3,
                        )))
    traces.append(go.Scatter(
                        x=[U_model[0],U_model[-1]], 
                        y=[P_model[0],P_model[-1]],
                        mode='lines',
                        name='Proportional',
                        line=dict(
                            color='grey',
                            width=1,
                        )))
    traces.append(go.Scatter(
                        x=[U_model[0],U_model[-1]], 
                        y=[P_model[-1],P_model[-1]],
                        mode='lines',
                        name='Agnostic',
                        line=dict(
                            color='grey',
                            width=1,
                            dash='dash',
                        )))


    return traces

# ============================

def energy_savings_plot(
    P0,P1=1
    ):

    # Get the figure data
    figure_data = __prep_energy_savings__(
        P0,P1
        )

    if figure_data is None:
        return

    # Generate the figure
    figure = go.Figure()
    for trace in figure_data:
        figure.add_traces(trace)
    
    # Apply default layouts
    figure.update_layout(base_layout)
    figure.update_layout(utilization_layout)

    # Customize the layout
    u=0.3
    p=0.5
    saving = int(100 * p*(1-u) / (p + u*(1-p)))
    figure.update_layout(

        # X axis
        xaxis_tickvals=[0,u,1],
        xaxis_ticktext=[0,0.3,1],
        xaxis_title='Baseline utilization',

        # Y axis
        yaxis_title='Energy savings (%)',
        yaxis_range=[-5, 105],
        yaxis_tickvals=[0,saving,100],

        # legend
        legend = dict(
            title=r'$\;\;P_0 = $',
            orientation='v',
            x = 0.95,
            xanchor = 'right',
            y = 0.95,
            yanchor = 'top'
        ),
    )

    return figure


def __prep_energy_savings__(
    P0,P1=1
    ):
    
    # Initialization
    step = 0.01
    U = np.arange(0,1+step,step)
    traces = []

    # Generate the traces
    for p in P0:
        eps = P1 - p
        savings = [ 100 * p*(1-u) / (p + u*eps) for u in U ]

        traces.append(go.Scatter(x=U, y=savings,
                        mode='lines',
                        name=p))

    # Generate layout
    layout = utilization_layout.copy()

    return traces

# ============================
