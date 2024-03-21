from deep_translator import GoogleTranslator

def google_translate(text, from_lang, to_lang):
    return GoogleTranslator(source=from_lang, target=to_lang).translate(text)