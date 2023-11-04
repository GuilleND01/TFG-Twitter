# This file is meant for common functions run throughout the application
import html
import re


def clean_text(text):
    """ Cleansing tweets by using regular expressions """
    text = re.sub(r'@\w+:', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'RT', '', text)
    text = re.sub(r'http\S+', '', text)
    text = text.strip().replace('\n', ' ')
    text = html.unescape(text)
    return text


def prueba():
    print(clean_text("RT @carlos_cataruz: my grandmother fighting in the Spanish Civil War (1938) https://t.co/KhndpEeKaF"))
    print(clean_text("RT @Alvaro_vgar97: @elenacanizares_ -Selectividad 2021:\n¿Cual de las 3 compañeras de Elena "
                     "Cañizares quería que se fuese del piso?\n\nA)Lucía…"))
    print(clean_text("RT @ModernoNoSoy: Biden - 264\nTrump - 214\nZoey - 101 https://t.co/zHpbxt4CKw"))
    print(clean_text("RT @supporteva1: ✨✨✨✨HSM2 AS OT2020 ✨✨✨\n\n#EvaOT15M #DirectoAcademia15M #OTDirecto15M "
                     "https://t.co/2FyknU4BDh"))

    print(clean_text(("esta persona es la mejor persona del &amp; mundo es que &gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt; "
                      "https://t.co/amyqUmgnCk")))
    print(clean_text("RT @paulacdrs: va a empezar el bucle d \"bueno mañana m tiene q cundir si o si\""))