from expro import *

main = MainPage()
settings = {
    'general-progress': main.von.get()
}

with open('settings.json', 'w') as s:
    json.dump(settings, s)
    s.close()

