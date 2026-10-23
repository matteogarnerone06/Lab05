import dataclasses
import flet as ft
from flet import value

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"


def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)
    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    tipo = ft.TextField(label="Tipo", value="")
    marca = ft.TextField(label="Marca", value="")
    anno = ft.TextField(label="Anno", value="2026")
    def year(anno):
        try:
            anno_1 = int(anno.value)
            if anno_1<=2026:
                return True
            else:
                alert.show_alert("L'anno inserito non esiste")
                return False
        except ValueError:
            alert.show_alert("L'anno inserito non esiste")
            return False


    valore = ft.TextField(value="0", label="Prezzo €")
    def valore_f(valore):
        try:
            valore = float(valore.value)
            if valore >=0:
                return True
            else:
                alert.show_alert("Prezzo inserito non è accettabile")
                return False
        except ValueError:
            alert.show_alert("Il prezzo inserito non è accettabile")
            return False

    aggiungi_strumento = ft.Text("Aggiungi strumento",size=30,weight=ft.FontWeight.BOLD)
    def incremento():
        try:
            valore_attuale = float(valore.value)
            valore.value = str(valore_attuale + 1)
            page.update()
        except ValueError:
            pass
    def decremento():
        try:
            valore_attuale = float(valore.value)
            if valore_attuale > 0:
                valore.value = str(valore_attuale - 1)
                page.update()
        except ValueError:
            pass




    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    def conferma_aggiunta():
        if str(valore_f(valore)) and str(year(anno)):
            deposito.aggiungi_strumento(tipo.value,marca.value,anno.value,valore.value)
            aggiorna_lista_strumenti()
        tipo.value = ''
        marca.value = ''
        anno.value = "2026"
        valore.value = '0'


    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento",on_click=conferma_aggiunta)
    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE, on_click=decremento)
    btn_piu = ft.IconButton(icon=ft.Icons.ADD, on_click=incremento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        aggiungi_strumento,
        ft.Row([tipo,marca,anno,btn_meno,valore,btn_piu]),
        pulsante_aggiungi_strumento,
        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti)
    aggiorna_lista_strumenti()

ft.run(main)