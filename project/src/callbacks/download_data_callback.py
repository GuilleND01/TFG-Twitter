from dash import Input, Output
from src.utils.cloudfunctionsmanager import CloudFunctionManager

cloud_inst = CloudFunctionManager.get_instance()


def create_download_callback(app):
    @app.callback(
        Output("download-file", "data"),
        Input("download", "n_clicks"),
        prevent_initial_call=True,
    )
    def func(n_clicks):
        return dict(content=str(cloud_inst.get_results()).replace("'", '"'),
                    filename=f"whattheyknow-{cloud_inst.get_id()}.json")