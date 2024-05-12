from google.cloud import functions_v2
from google.oauth2 import service_account
import sys, json

gcp_json = json.loads(sys.argv[1])

credentials = service_account.Credentials.from_service_account_info(gcp_json)

cloud_functions_list = [
    "projects/tfg-twitter/locations/europe-southwest1/functions/heatmap_activity",
    "projects/tfg-twitter/locations/europe-southwest1/functions/advertiser-info-1",
    "projects/tfg-twitter/locations/europe-southwest1/functions/person-criteria",
    "projects/tfg-twitter/locations/europe-southwest1/functions/profile",
    "projects/tfg-twitter/locations/europe-southwest1/functions/user-mentions",
    "projects/tfg-twitter/locations/europe-southwest1/functions/twitter-circle",
    "projects/tfg-twitter/locations/europe-southwest1/functions/sentimientos_lenguajes",
]

client = functions_v2.FunctionServiceClient(credentials=credentials)

for name in cloud_functions_list:
    request = functions_v2.GetFunctionRequest(
        name=name,
    )
    try:
        func = client.get_function(request=request)

        # Si llegamos aquí, significa que la función se obtuvo correctamente
        if str(func.state) != "1":
            raise Exception(f"La función {func.name} no está en un estado activo.")

    except Exception as e:
        # Si ocurre alguna excepción dentro del bloque try, se ejecutará este bloque except
        raise Exception(f"Error al obtener la función: {e}")

print("Todas las funciones están activas.")
