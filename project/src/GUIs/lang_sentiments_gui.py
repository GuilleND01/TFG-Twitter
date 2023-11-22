from src.GUIs.languages_gui import create_gui_languages
from src.GUIs.sentiments_gui import create_gui_sentiments
from src.scripts.lenguajes_sentimientos import lenguajes_and_sentimientos


def return_gui_langu_senti(info_decoded):
    language_rts, language_without_rts, polarity_rts, polarity_without_rts, tweets_rts, tweets_no_rts = lenguajes_and_sentimientos(info_decoded)
    return create_gui_languages(language_rts, language_without_rts), create_gui_sentiments(polarity_rts, polarity_without_rts, tweets_rts, tweets_no_rts)

