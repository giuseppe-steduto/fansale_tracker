from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import title_contains
from datetime import datetime


def scrivi_log(str):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open("/fansale_tracker/trovati.txt", "a")
    f.write(current_time + " ||| " + str + "\n")
    f.close()


URL = "https://www.fansale.it/fansale/tickets/pop-amp-rock/pinguini-tattici-nucleari/558153/13359444"
opt = Options()
opt.headless = True
browser = webdriver.Firefox(options=opt)
wait = WebDriverWait(browser, 10)
tickets_description = []
parterre = 0 #Numero di posti parterre
browser.get(URL)
wait.until(title_contains("I migliori biglietti per"))
if "Sfortunatamente" not in browser.page_source:
    tickets = browser.find_elements(By.CLASS_NAME, "OfferEntry-Top")
else:
    tickets = []
for t in tickets:
    if t.text == "":
        continue
    if t.text.find("Parterre") == -1:
        posto = t.text[(t.text.find("Posto ") + len("Posto ")):][:2]
        fila = t.text[(t.text.find("Fila ") + len("Fila ")):][:2]
        settore = t.text[(t.text.find("Settore ") + len("Settore ")):][:3]
        tickets_description.append({
            "posto": int(posto),
            "fila": int(fila),
            "settore": settore
        })
    else:
        parterre += 1

# Adesso trova se esistono almeno due posti nello stesso settore
for t1 in tickets_description:
    same_sector = [t1]
    for t2 in tickets_description:
        if t1 != t2:
            if t1["settore"] == t2["settore"]:
                same_sector.append(t2)
    for s in same_sector:
        tickets_description.remove(s)

    # Per tutti quelli nello stesso settore, vedi se ci sono almeno due nella stessa fila:
    for ts in same_sector:
        fila = [ts["posto"]]
        el = [ts]
        for t2 in same_sector:
            if ts != t2:
                if ts["fila"] == t2["fila"]:
                    fila.append(t2["posto"])
                    el.append(t2)
        for e in el:
            same_sector.remove(e)

        # Vedi se esistono due posti contigui
        fila.sort()
        for i in range(0, len(fila) - 1):
            if abs(fila[i] - fila[i + 1]) == 1:
                scrivi_log("Ci sono due posti vicini! Settore " + t1["settore"] +  " | Fila " + str(t1["fila"]) +  " | Posti " + str(fila[i]) +  " e " +  str(fila[i + 1]))

browser.close()

if parterre != 0:
    scrivi_log("Posti parterre: " + str(parterre))
uffi = open("/fansale_tracker/log.txt", "a")
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
uffi.write(current_time + "\n")
uffi.close()