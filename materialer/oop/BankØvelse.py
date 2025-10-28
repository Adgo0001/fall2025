class Bank:
    def __init__(self, navn="Min bank"):
        self.navn = navn
        self.naeste_kontonr = 100000
        self.konti = []
        self.konto_pr_kunde = {}

    def opret_konto(self, kunde, start_saldo=0.0, valuta="DKK"):
        if kunde.kunde_id in self.konto_pr_kunde:
            print(f"Kunden {kunde.navn} har allerede en konto "
                  f"({self.konto_pr_kunde[kunde.kunde_id].kontonr}).")
            return self.konto_pr_kunde[kunde.kunde_id]

        konto = Konto(self.naeste_kontonr, kunde, start_saldo, valuta)
        self.naeste_kontonr += 1
        self.konti.append(konto)
        self.konto_pr_kunde[kunde.kunde_id] = konto
        print(f"Konto oprettet til {kunde.navn} med kontonr {konto.kontonr}")
        return konto

    def find_konto(self, kontonr):
        for k in self.konti:
            if k.kontonr == kontonr:
                return k
        return None

    def find_konto_for_kunde(self, kunde):
        return self.konto_pr_kunde.get(kunde.kunde_id)

    def vis_konti(self):
        if not self.konti:
            print("Ingen konti i banken endnu.")
            return
        for k in self.konti:
            print(f"Konto: {k.kontonr}, Kunde: {k.kunde.navn}, Saldo: {k.saldo} {k.valuta}")


class Konto:
    def __init__(self, kontonr, kunde, saldo=0.0, valuta="DKK"):
        self.kontonr = kontonr
        self.kunde = kunde
        self.saldo = float(saldo)
        self.valuta = valuta

    def indsæt(self, beløb):
        self.saldo += beløb
        print(f"{beløb} {self.valuta} indsat. Ny saldo: {self.saldo} {self.valuta}")

    def hæv(self, beløb):
        if beløb <= self.saldo:
            self.saldo -= beløb
            print(f"{beløb} {self.valuta} hævet. Ny saldo: {self.saldo} {self.valuta}")
        else:
            print("Ikke nok penge på kontoen.")


class Kunde:
    def __init__(self, navn, kunde_id, email, telefon):
        self.navn = navn
        self.kunde_id = kunde_id
        self.email = email
        self.telefon = telefon



# ---------- TUI HELPER ----------
import os, shutil, sys

# ANSI farver (virker i nyere Windows PowerShell)
RESET = "\033[0m"; BOLD = "\033[1m"
DIM = "\033[2m"; ITAL = "\033[3m"
FG = {
    "primary": "\033[36m",   # cyan
    "accent":  "\033[35m",   # magenta
    "ok":      "\033[32m",
    "warn":    "\033[33m",
    "err":     "\033[31m",
    "muted":   "\033[90m",
    "title":   "\033[96m",
}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def term_width():
    try:
        return max(60, shutil.get_terminal_size().columns)
    except:
        return 80

def center(text, width=None):
    w = width or term_width()
    return text.center(w)

def hr(char="─", width=None, pad=0):
    w = (width or term_width()) - pad*2
    return " " * pad + char * w

def box(title, lines, width=None, pad=2):
    w = width or term_width()
    inner = w - 2  # borders
    top = f"╔{(' ' + title + ' ').center(inner,'═')}╗"
    bottom = f"╚{'═'*inner}╝"
    out = [top]
    for line in lines:
        # trim / pad
        if len(line) > inner:
            line = line[:inner]
        out.append("║" + line.ljust(inner) + "║")
    out.append(bottom)
    return "\n".join(out)

def prompt(label="➤ "):
    return input(FG["accent"] + BOLD + label + RESET)

def table(headers, rows, width=None):
    w = width or term_width()
    colw = [max(len(str(h)), 10) for h in headers]
    # autosize a bit based on content
    for row in rows:
        for i, cell in enumerate(row):
            colw[i] = max(colw[i], len(str(cell)))
    total = sum(colw) + 3*len(colw) + 1
    if total > w:
        # compact columns if too wide
        scale = (w - (3*len(colw)+1)) / sum(colw)
        colw = [max(8, int(c*scale)) for c in colw]

    def fmt_row(r):
        cells = []
        for i, c in enumerate(r):
            s = str(c)
            if len(s) > colw[i]:
                s = s[:colw[i]-1] + "…"
            cells.append(" " + s.ljust(colw[i]) + " ")
        return "│" + "│".join(cells) + "│"

    line = "├" + "┼".join(("─"*(c+2)) for c in colw) + "┤"
    top  = "┌" + "┬".join(("─"*(c+2)) for c in colw) + "┐"
    bot  = "└" + "┴".join(("─"*(c+2)) for c in colw) + "┘"
    head = fmt_row(headers)
    body = "\n".join(fmt_row(r) for r in rows) if rows else "│ " + "Ingen data".ljust(sum(colw)+2*(len(colw))-1) + " │"
    return "\n".join([top, head, line, body, bot])

def flash(msg, kind="ok"):
    color = FG.get(kind, FG["muted"])
    print(color + BOLD + msg + RESET)

# ---------- NY, PÆN MENU ----------
def start_menu():
    bank = Bank("DTU Bank")
    kunder = []

    # ---------- DUMMY DATA ----------
    dummy_data = [
        ("Zahraa Abdulrihman", 1, "zahraa@dtu.dk", "+45 50665118", 5000.0),
        ("Ali Hassan",         2, "ali@kea.dk",    "+45 50223344", 2500.0),
        ("Fatima Noor",        3, "fatima@stud.kea.dk", "+45 60112233", 10000.0),
    ]

    for navn, kunde_id, email, telefon, saldo in dummy_data:
        kunde = Kunde(navn, kunde_id, email, telefon)
        kunder.append(kunde)
        bank.opret_konto(kunde, saldo)

    # lille info når programmet starter
    clear()
    print(box(" 💾 DUMMY DATA INDLÆST ", [
        f"{len(kunder)} kunder og {len(bank.konti)} konti blev automatisk oprettet.",
        "Tryk Enter for at fortsætte til menuen."
    ]))
    input()
    
    # --------------------------------
    
    while True:
        clear()
        title = FG["title"] + BOLD + f"🏦 {bank.navn}" + RESET
        subtitle = FG["muted"] + "Et simpelt terminal-bankprogram (KEA edition)" + RESET
        print(center(title))
        print(center(subtitle))
        print()

        # INFO BAR
        info = [
            f"{FG['muted']}Konti: {RESET}{len(bank.konti)}",
            f"{FG['muted']}Kunder: {RESET}{len(kunder)}",
        ]
        print(center(" • ".join(info)))
        print()

        # MENU BOX
        options = [
            f"{FG['primary']}1{RESET}. Opret kunde",
            f"{FG['primary']}2{RESET}. Opret konto",
            f"{FG['primary']}3{RESET}. Se alle konti",
            f"{FG['primary']}4{RESET}. Indsæt penge",
            f"{FG['primary']}5{RESET}. Hæv penge",
            f"{FG['primary']}6{RESET}. Afslut",
        ]
        menu_lines = [center(opt) for opt in options]
        print(box(" MENU ", menu_lines))
        print()

        valg = prompt("Vælg (1-6): ").strip()

        # ---- HANDLERS ----
        if valg == "1":
            clear()
            print(box(" Opret kunde ", [""], pad=0))
            print()
            navn = input(f"{BOLD}Navn:{RESET} ")
            kunde_id = len(kunder) + 1
            email = input(f"{BOLD}Email:{RESET} ")
            telefon = input(f"{BOLD}Telefon:{RESET} ")
            ny_kunde = Kunde(navn, kunde_id, email, telefon)
            kunder.append(ny_kunde)
            flash(f"✅ Kunde '{navn}' oprettet!", "ok")
            input("\nTryk Enter for at fortsætte...")

        elif valg == "2":
            clear()
            if not kunder:
                flash("⚠ Der er ingen kunder. Opret en kunde først.", "warn")
                input("\nTryk Enter for at fortsætte...")
                continue

            print(box(" Opret konto ", [""], pad=0))
            print()
            # vælg kunde
            headers = ["#", "Navn", "Email", "Telefon"]
            rows = [[i+1, k.navn, k.email, k.telefon] for i, k in enumerate(kunder)]
            print(table(headers, rows)); print()
            try:
                indeks = int(prompt("Vælg kunde (#): ")) - 1
                if not (0 <= indeks < len(kunder)):
                    raise ValueError
            except ValueError:
                flash("✖ Ugyldigt valg.", "err")
                input("\nTryk Enter for at fortsætte...")
                continue

            valgt = kunder[indeks]
            # tjek om kunden har konto
            eksisterende = bank.find_konto_for_kunde(valgt)
            if eksisterende:
                flash(f"ℹ {valgt.navn} har allerede konto {eksisterende.kontonr} (saldo {eksisterende.saldo} {eksisterende.valuta}).", "warn")
                input("\nTryk Enter for at fortsætte...")
                continue

            try:
                start_saldo = float(prompt("Startsaldo: ").replace(",", "."))
            except ValueError:
                flash("✖ Beløbet skal være et tal.", "err")
                input("\nTryk Enter for at fortsætte...")
                continue

            bank.opret_konto(valgt, start_saldo)
            input("\nTryk Enter for at fortsætte...")

        elif valg == "3":
            clear()
            print(box(" Alle konti ", [""], pad=0)); print()
            if not bank.konti:
                flash("Ingen konti i banken endnu.", "warn")
            else:
                headers = ["Konto", "Kunde", "Saldo", "Valuta"]
                rows = [[k.kontonr, k.kunde.navn, f"{k.saldo:.2f}", k.valuta] for k in bank.konti]
                print(table(headers, rows))
            print()
            input("Tryk Enter for at fortsætte...")

        elif valg == "4":
            clear()
            if not bank.konti:
                flash("⚠ Der er ingen konti i banken endnu ;(", "warn")
                input("\nTryk Enter for at fortsætte...")
                continue
            print(box(" Indsæt penge ", [""], pad=0)); print()
            try:
                kontonr = int(prompt("Kontonummer: "))
                konto = bank.find_konto(kontonr)
                if not konto:
                    flash("✖ Konto ikke fundet.", "err")
                    input("\nTryk Enter for at fortsætte...")
                    continue
                beløb = float(prompt("Beløb at indsætte: ").replace(",", "."))
                konto.indsæt(beløb)
                input("\nTryk Enter for at fortsætte...")
            except ValueError:
                flash("✖ Ugyldigt input.", "err")
                input("\nTryk Enter for at fortsætte...")

        elif valg == "5":
            clear()
            if not bank.konti:
                flash("⚠ Der er ingen konti i banken endnu ;(", "warn")
                input("\nTryk Enter for at fortsætte...")
                continue
            print(box(" Hæv penge ", [""], pad=0)); print()
            try:
                kontonr = int(prompt("Kontonummer: "))
                konto = bank.find_konto(kontonr)
                if not konto:
                    flash("✖ Konto ikke fundet.", "err")
                    input("\nTryk Enter for at fortsætte...")
                    continue
                beløb = float(prompt("Beløb at hæve: ").replace(",", "."))
                konto.hæv(beløb)
                input("\nTryk Enter for at fortsætte...")
            except ValueError:
                flash("✖ Ugyldigt input.", "err")
                input("\nTryk Enter for at fortsætte...")

        elif valg == "6":
            clear()
            print(center(FG["primary"] + BOLD + "Tak fordi du brugte DTU Bank 💙" + RESET))
            print()
            break

        else:
            flash("Ugyldigt valg, prøv igen.", "err")
            input("\nTryk Enter for at fortsætte...")

start_menu()