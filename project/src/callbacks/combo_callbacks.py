from dash.dependencies import Input, Output
from dash import dcc, html
from pandas import json_normalize
import plotly.express as px
import dash_bootstrap_components as dbc
from utils.cloudfunctionsmanager import CloudFunctionManager

'''
return html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.H1(f" {res['advertisements']}", className="m-1"),
                                html.H6('anuncios recibidos', className="m-1")
                            ],
                            className='m-2'
                        ),
                        dbc.Row(
                            children=[
                                dbc.Col(
                                    children=[
                                        html.Iframe(srcDoc=res['recent'], style={'margin': '0', 'padding': '0',
                                                                                 'height': '100%',
                                                                                 'width': '100%',
                                                                                 'border': 'none'
                                                                                 })
                                    ],
                                    className='col-6 d-flex justify-content-center align-items-center'
                                ),
                                dbc.Col(
                                    children=[
                                        dcc.Graph(figure=fig, className='h-100 w-100')
                                    ],
                                    className='col-6'
                                ),
                            ]
                        )
                    ]
            )
'''

def create_combo_clicks(app):
    @app.callback(
        Output('graph-criteria', 'children'),
        [Input('pombo-box', 'value')]
    )
    def actualizar_resultado_combo(valor_seleccionado):
        cloud_inst_res = CloudFunctionManager.get_instance().get_results()
        df_json = cloud_inst_res['person-criteria']
        if valor_seleccionado is not None:
            print(cloud_inst_res)
            df = json_normalize(eval(df_json[valor_seleccionado]))
            fig = px.bar(df, x="TargetingValue", y="Count",
                         labels={'TargetingValue': 'Criterio', 'Count': 'Anuncios en los que figura'})
            fig.update_traces(
                hovertemplate=
                "El criterio <b>%{x}</b> se ha"
                "<br>"
                "empleado en <b>%{y}</b> anuncios"
            )
            return dcc.Graph(
                figure=fig
            )

        return None

    @app.callback(
        Output('graph-advertiser', 'children'),
        [Input('pombo-bo', 'value')]
    )
    def actualizar_resultado_combo(valor_seleccionado):
        cloud_inst_res = CloudFunctionManager.get_instance().get_results()
        if valor_seleccionado is not None:
            print(cloud_inst_res)
            df_json = cloud_inst_res['advertiser-info-1']
            res = df_json[valor_seleccionado]

            df = json_normalize(eval(res['criteria']))
            fig = px.pie(df, values='Count', names='TargetingValue')
            # fig.update_layout(showlegend=False)
            fig.update_traces(
                hovertemplate=
                "El criterio <b>%{label}</b> se ha"
                "<br>"
                "empleado en <b>%{value}</b> anuncios"
            )

            return dbc.Row(
                children=[
                    dbc.Col(
                        html.Iframe(srcDoc=res['recent'], style={'margin': '0', 'padding': '0',
                                                                 'height': '150%',
                                                                 'width': '100%',
                                                                 'border': 'none'
                                                                 }),
                        className='col-5'
                    ),
                    dbc.Col(
                        dcc.Graph(figure=fig, className='h-100 w-100'),
                        className='col-7'
                    )
                ], className='d-flex justify-content-center align-items-center'
            )

        return None
