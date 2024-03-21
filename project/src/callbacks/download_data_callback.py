from dash import Input, Output
from src.utils.cloudfunctionsmanager import CloudFunctionManager

cloud_inst = CloudFunctionManager.get_instance()

'''
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout del formulario
app.layout = html.Div([
    dbc.FormGroup(
        [
            dbc.Label("Ingrese su nombre:"),
            dbc.Input(id='input_nombre', placeholder="Nombre", type="text"),
        ]
    ),
    html.Br(),
    dbc.Button("Enviar", id='submit_button', color="primary", className="mr-2"),
    html.Div(id='output_div')
])

# Callback para leer el valor del campo de entrada al hacer clic en el botón de enviar
@app.callback(
    Output('output_div', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('input_nombre', 'value')]
)
def update_output(n_clicks, input_value):
    if n_clicks is not None:
        if input_value is not None:
            return html.Div([
                html.Label('Nombre ingresado:'),
                html.Div(input_value)
            ])
        else:
            return html.Div([
                html.Label('Por favor, ingrese un nombre válido.')
            ])

if __name__ == '__main__':
    app.run_server(debug=True)

'''
def create_download_callback(app):
    @app.callback(
        Output("download-file", "data"),
        Input("download", "n_clicks"),
        prevent_initial_call=True,
    )
    def func(n_clicks):
        return dict(content=str(cloud_inst.get_results()),
                    filename=f"whattheyknow-{cloud_inst.get_id()}.json")