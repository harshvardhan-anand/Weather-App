import time

def get_language():
    lang = '''af	Afrikaans
al	Albanian
ar	Arabic
az	Azerbaijani
bg	Bulgarian
ca	Catalan
cz	Czech
da	Danish
de	German
el	Greek
en	English
eu	Basque
fa	Persian (Farsi)
fi	Finnish
fr	French
gl	Galician
he	Hebrew
hi	Hindi
hr	Croatian
hu	Hungarian
id	Indonesian
it	Italian
ja	Japanese
kr	Korean
la	Latvian
lt	Lithuanian
mk	Macedonian
no	Norwegian
nl	Dutch
pl	Polish
pt	Portuguese
pt_br	Português Brasil
ro	Romanian
ru	Russian
sv, se	Swedish
sk	Slovak
sl	Slovenian
sp, es	Spanish
sr	Serbian
th	Thai
tr	Turkish
ua, uk	Ukrainian
vi	Vietnamese
zh_cn	Chinese Simplified
zh_tw	Chinese Traditional
zu	Zul'''

    lang_choice = []
    for i in lang.replace('	',' ').replace(',','').split('\n'):
        if i:
            option = i.split()
            if len(i)>3:
                option = [option[0],' '.join(option[1:])]
            lang_choice.append(option) 
            
        
    return lang_choice

print(get_language())

time.sleep(100)