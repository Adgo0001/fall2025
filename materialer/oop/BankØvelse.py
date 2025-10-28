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



def start_menu():
    bank = Bank("DTU Bank")
    kunder = []

    while True:
        print("\n=== DTU BANK MENU ===")
        print("1. Opret kunde")
        print("2. Opret konto")
        print("3. Se alle konti")
        print("4. Indsæt penge")
        print("5. Hæv penge")
        print("6. Afslut")
        valg = input("Vælg en funktion (1-6): ")

        if valg == "1":
            navn = input("Navn: ")
            kunde_id = len(kunder) + 1
            email = input("Email: ")
            telefon = input("Telefon: ")
            ny_kunde = Kunde(navn, kunde_id, email, telefon)
            kunder.append(ny_kunde)
            print(f"Kunde '{navn}' oprettet!")

        elif valg == "2":
            if not kunder:
                print("Der er ingen kunder. Opret en kunde først.")
                continue
            print("Vælg kunde:")
            for i, kunde in enumerate(kunder):
                print(f"{i+1}. {kunde.navn}")
            indeks = int(input("Indtast kundens nummer: ")) - 1
            start_saldo = float(input("Startsaldo: "))
            bank.opret_konto(kunder[indeks], start_saldo)

        elif valg == "3":
            bank.vis_konti()

        elif valg == "4":
            if not bank.konti:
                print("Der er ingen konti i banken endnu ;(")
                continue
            kontonr = int(input("Indtast kontonummer: "))
            konto = bank.find_konto(kontonr)
            if konto:
                beløb = float(input("Beløb at indsætte: "))
                konto.indsæt(beløb)
            else:
                print("Konto ikke fundet.")

        elif valg == "5":
            if not bank.konti:
                print("Der er ingen konti i banken endnu ;(")
                continue
            kontonr = int(input("Indtast kontonummer: "))
            konto = bank.find_konto(kontonr)
            if konto:
                beløb = float(input("Beløb at hæve: "))
                konto.hæv(beløb)
            else:
                print("Konto ikke fundet.")

        elif valg == "6":
            print("Programmet afsluttes. Tak fordi du brugte KEA Bank!")
            break

        else:
            print("Ugyldigt valg, prøv igen.")

            
start_menu()