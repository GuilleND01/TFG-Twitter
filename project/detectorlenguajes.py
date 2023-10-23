from langdetect import detect
import pandas as pd
import json
from pandas import json_normalize
def convertir_codigo_lenguaje(cod):
    codigo_lenguaje = {'af':'Africano', 'ar': 'Árabe', 'bg':'Búlgaro', 'bn':'Bengalí', 'ca':'Catalán', 'cs':'Checo', 'cy':'Galés',
                       'da':'Danés', 'de':'Alemán', 'el':'Griego', 'en':'Inglés', 'es':'Español', 'et':'Estonio', 'fa':'Persa',
                       'fi':'Finés', 'fr':'Francés', 'gu':'Gujarati', 'he':'Hebreo', 'hr':'Croata', 'hu':'Húngaro', 'id':'Indonedsio',
                       'it':'Italiano', 'ja':'Japonés', 'kn':'Kannada', 'ko':'Coreano', 'lt':'Lituano', 'lv':'Letón', 'mk':'Macedonio',
                       'ml':'Malasio', 'mr':'Marathi', 'ne':'Nepalí', 'no':'Noruego', 'pl':'Polaco', 'pt':'Portugués', 'ro':'Rumano',
                       'sk':'Eslovaco', 'sl':'Esloveno', 'so':'Somalí', 'sq':'Albanés', 'sv':'Sueco', 'sw':'Suajili', 'ta':'Tamil',
                       'te':'Telugu', 'th':'Tailandés', 'tl':'Tagalo', 'tr':'Turco', 'vi':'Vietnamita'}

    return codigo_lenguaje[cod]

def retornar_df():
    # Contenido del archivo JSON con un nombre asignado
    with open("tweets.js", "r", encoding="UTF-8") as js_file:
        js_code = js_file.read()

    # Quita los saltos de línea
    js_code = js_code.replace('\n', '')
    js_code = js_code.replace('window.YTD.tweets.part0 = ', '')

    json_dat = json.loads(js_code)
    data = json_normalize(json_dat)

    lang_aux = {}
    lang = {'Idioma': [], 'Cantidad': []}
    for i in range(len(data)):
        leng = convertir_codigo_lenguaje(detect(data.iloc[i]['tweet.full_text']))
        if leng in lang_aux:
            lang_aux[leng] += 1
        else:
            lang_aux[leng] = 1

    res = [(key,value) for key, value in lang_aux.items()]
    for i in range(0, len(res)):
        lang['Idioma'].append(res[i][0])
        lang['Cantidad'].append(res[i][1])

    return pd.DataFrame(lang).sort_values(by=['Cantidad'], ascending=False)

'''
labels = []
for i in range(0, len(df)):
    labels.append(df.iloc[i]['idioma'] + ' (' + str(round((df.iloc[i]['cantidad']/sum(df['cantidad']))*100, 2)) + '%)')

fig, ax = plt.subplots()
plt.pie(df['cantidad'])
plt.axis('equal')
plt.title('Idiomas utilizados en los Tweets')
plt.legend(labels, loc="best")

plt.show()
'''