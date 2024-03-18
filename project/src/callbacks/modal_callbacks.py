from dash import Input, Output, State


def create_modal_callback(app):
    @app.callback(
        Output("modal_men", "is_open"),
        [Input("open_modal_men", "n_clicks")],
        [State("modal_men", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open

        return is_open

    @app.callback(
        Output("modal_heatmap", "is_open"),
        [Input("open_modal_heatmap", "n_clicks")],
        [State("modal_heatmap", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open

        return is_open

    @app.callback(
        Output("modal_senti", "is_open"),
        [Input("open_modal_senti", "n_clicks")],
        [State("modal_senti", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @app.callback(
        Output("modal_lang", "is_open"),
        [Input("open_modal_lang", "n_clicks")],
        [State("modal_lang", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @app.callback(
        Output("modal_cir", "is_open"),
        [Input("open_modal_cir", "n_clicks")],
        [State("modal_cir", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open

        return is_open

    @app.callback(
        Output("modal_preg", "is_open"),
        [Input("open_modal_preg", "n_clicks"),
         Input("close_modal_preg", "n_clicks")],
        [State("modal_preg", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output("modal_adv", "is_open"),
        [Input("open_modal_adv", "n_clicks")],
        [State("modal_adv", "is_open")],
    )
    def toggle_modal(n1, is_open):
        if n1:
            return not is_open

        return is_open
