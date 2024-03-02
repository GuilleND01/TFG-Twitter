from dash.dependencies import Input, Output

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


def create_heatmap_callback(app):

    @app.callback(
        Output("graph-heatmap", "figure"),
        Input("opciones", "value"))
    def filter_heatmap(cols):

        data = []

        for dia in range(len(dias)):
            lista = []
            for franja in range(0, 24):
                clave = f"('{str(franja).zfill(2)}', '{dias[dia]}')"  # Construir la clave
                suma = 0

                #En función de las columnas que se tengan seleccionadas en la checklist, se calcula la suma
                for col in cols:
                    checklist_opt = json_resultado["opciones_checklist"][col]
                    suma += json_data.get(clave)[checklist_opt] if json_data.get(clave) else 0

                lista.append(suma)
            data.append(lista)

        fig = px.imshow(data, y=dias, x=[f"{str(i).zfill(2)}" for i in range(24)],
                        labels=dict(x="Hora", y="Día", color="Actividad"),
        

        )
        return fig
