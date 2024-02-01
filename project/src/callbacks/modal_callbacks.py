from dash import Input, Output, State


def create_modal_callback(app):
    @app.callback(
        Output("modal_men", "is_open"),
        [Input("open_modal_men", "n_clicks"),
         Input("close_modal_men", "n_clicks")],
        [State("modal_men", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output("modal_lang", "is_open"),
        [Input("open_modal_lang", "n_clicks"),
         Input("close_modal_lang", "n_clicks")],
        [State("modal_lang", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open
