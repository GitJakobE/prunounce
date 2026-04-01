"""
Seed story data for the Story Reading feature.
Run with: poetry run python seed_stories.py
"""
import json
import sys
import uuid

sys.path.insert(0, ".")

from app.database import SessionLocal, engine, Base, ensure_sqlite_schema
from app.models import Story
from app.services.story_audio import STORY_SPEED_TO_RATE, upsert_story_audio

Base.metadata.create_all(bind=engine)
ensure_sqlite_schema()

STORIES = [
    # ── ITALIAN BEGINNER ────────────────────────────────────────────────────
    # ── short ──
    {
        "slug": "it-beginner-cafe",
        "language": "it",
        "difficulty": "beginner",
        "length": "short",
        "title": "Al caffè",
        "description_en": "Order a coffee and a pastry in a typical Italian café.",
        "description_da": "Bestil en kaffe og en kage på en typisk italiensk café.",
        "description_it": "Ordina un caffè e un pasticcino in un tipico bar italiano.",
        "format": "dialogue",
        "speakers": json.dumps(["Cliente", "Barista"]),
        "body": (
            "Cliente: Buongiorno! Vorrei un caffè, per favore.\n"
            "Barista: Certo, subito. Vuole anche qualcosa da mangiare?\n"
            "Cliente: Sì, un cornetto, grazie.\n"
            "Barista: Benissimo. Desidera zucchero nel caffè?\n"
            "Cliente: No, grazie, lo prendo amaro.\n"
            "Barista: Va bene. Ecco il suo caffè e il cornetto.\n"
            "Cliente: Quanto costa?\n"
            "Barista: Un euro e cinquanta, per favore.\n"
            "Cliente: Ecco a lei. Arrivederci!\n"
            "Barista: Arrivederci e buona giornata!"
        ),
        "order": 1,
    },
    {
        "slug": "it-beginner-mercato",
        "language": "it",
        "difficulty": "beginner",
        "length": "short",        "title": "Al mercato",
        "description_en": "Buy fruit and vegetables at the local market.",
        "description_da": "Køb frugt og grønt på det lokale marked.",
        "description_it": "Compra frutta e verdura al mercato locale.",
        "format": "dialogue",
        "speakers": json.dumps(["Cliente", "Venditore"]),
        "body": (
            "Venditore: Buongiorno, signora. Cosa desidera oggi?\n"
            "Cliente: Vorrei un chilo di pomodori, per favore.\n"
            "Venditore: Certo. Sono freschi di stamattina. Altro?\n"
            "Cliente: Sì, due mele e qualche banana.\n"
            "Venditore: Quante banane vuole?\n"
            "Cliente: Quattro vanno bene, grazie.\n"
            "Venditore: Benissimo. Vuole anche delle zucchine? Sono belle oggi.\n"
            "Cliente: Sì, mezzo chilo di zucchine, grazie.\n"
            "Venditore: Sono in tutto quattro euro e venti.\n"
            "Cliente: Ecco cinque euro.\n"
            "Venditore: Grazie. Ottanta centesimi di resto. Buona giornata!"
        ),
        "order": 2,
    },
    {
        "slug": "it-beginner-presentazione",
        "language": "it",
        "difficulty": "beginner",
        "length": "short",        "title": "Mi presento",
        "description_en": "Introduce yourself to a new neighbour.",
        "description_da": "Præsenter dig for en ny nabo.",
        "description_it": "Presentati a un nuovo vicino di casa.",
        "format": "dialogue",
        "speakers": json.dumps(["Sofia", "Marco"]),
        "body": (
            "Sofia: Ciao! Sei nuovo nel palazzo?\n"
            "Marco: Sì, mi chiamo Marco. Sono arrivato ieri.\n"
            "Sofia: Piacere, io sono Sofia. Abito al secondo piano.\n"
            "Marco: Piacere mio, Sofia. Io abito al terzo.\n"
            "Sofia: Di dove sei, Marco?\n"
            "Marco: Sono di Roma, ma lavoro qui a Milano da un mese.\n"
            "Sofia: Che bello! Lavori vicino?\n"
            "Marco: Sì, in centro. Prendo la metro ogni mattina.\n"
            "Sofia: Ottimo. Se hai bisogno di qualcosa, suona pure.\n"
            "Marco: Grazie mille, Sofia. Sei molto gentile.\n"
            "Sofia: Prego! A presto, Marco."
        ),
        "order": 3,
    },
    # ── ITALIAN INTERMEDIATE ─────────────────────────────────────────────────
    {
        "slug": "it-intermediate-ristorante",
        "language": "it",
        "difficulty": "intermediate",
        "length": "short",        "title": "A cena fuori",
        "description_en": "An evening out at an Italian restaurant with friends.",
        "description_da": "En aften ude på en italiensk restaurant med venner.",
        "description_it": "Una serata in un ristorante italiano con gli amici.",
        "format": "dialogue",
        "speakers": json.dumps(["Cameriere", "Luca", "Giulia"]),
        "body": (
            "Cameriere: Buonasera. Avete prenotato?\n"
            "Luca: Sì, abbiamo una prenotazione a nome Rossi per quattro persone.\n"
            "Cameriere: Perfetto. Prego, accomodatevi. Ecco il menu.\n"
            "Giulia: Grazie. Cosa ci consiglia stasera?\n"
            "Cameriere: La specialità della casa è il risotto ai funghi porcini. Lo abbiamo preparato fresco.\n"
            "Luca: Perfetto, lo prendo io.\n"
            "Giulia: Per me, invece, la pasta al pomodoro. Sono vegetariana.\n"
            "Cameriere: Certo, nessun problema. E da bere?\n"
            "Luca: Una bottiglia di vino rosso della casa, grazie.\n"
            "Cameriere: Un momento. Volete anche dell'acqua naturale o frizzante?\n"
            "Giulia: Naturale, per favore.\n"
            "Cameriere: Benissimo. Vi porto tutto subito."
        ),
        "order": 1,
    },
    {
        "slug": "it-intermediate-medico",
        "language": "it",
        "difficulty": "intermediate",
        "length": "short",        "title": "Dal medico",
        "description_en": "A visit to the doctor for a routine check-up.",
        "description_da": "Et besøg hos lægen til en rutinekontrol.",
        "description_it": "Una visita dal medico per un controllo di routine.",
        "format": "dialogue",
        "speakers": json.dumps(["Paziente", "Dottoressa"]),
        "body": (
            "Paziente: Buongiorno, dottoressa.\n"
            "Dottoressa: Buongiorno. Si accomodi. Come sta?\n"
            "Paziente: Non benissimo. Ho mal di testa da tre giorni e mi sento stanco.\n"
            "Dottoressa: Capisco. Ha anche la febbre?\n"
            "Paziente: Ieri sera avevo trentasette e otto, ma stamattina è scesa.\n"
            "Dottoressa: Ha tosse o difficoltà respiratorie?\n"
            "Paziente: Una leggera tosse, ma non grave.\n"
            "Dottoressa: Ha preso qualcosa per il dolore?\n"
            "Paziente: Solo paracetamolo. Ha aiutato un po'.\n"
            "Dottoressa: Bene. Le misuro la pressione.\n"
            "Paziente: Va bene?\n"
            "Dottoressa: Sì, è nella norma. Probabilmente è un'influenza lieve. Le prescrivo tre giorni di riposo e un antinfiammatorio.\n"
            "Paziente: Grazie, dottoressa."
        ),
        "order": 2,
    },
    {
        "slug": "it-intermediate-treno",
        "language": "it",
        "difficulty": "intermediate",
        "length": "short",        "title": "In viaggio in treno",
        "description_en": "Buying a train ticket and boarding the right coach.",
        "description_da": "Køb en togbillet og find den rigtige vogn.",
        "description_it": "Comprare un biglietto del treno e salire sulla carrozza giusta.",
        "format": "dialogue",
        "speakers": json.dumps(["Viaggiatore", "Bigliettaio"]),
        "body": (
            "Viaggiatore: Buongiorno. Vorrei un biglietto per Firenze, per oggi pomeriggio.\n"
            "Bigliettaio: A che ora preferisce partire?\n"
            "Viaggiatore: Attorno alle quindici, se possibile.\n"
            "Bigliettaio: C'è un Intercity alle quindici e venti. Arriva a Firenze alle diciassette e quarantacinque.\n"
            "Viaggiatore: Va bene. Quanto costa il biglietto?\n"
            "Bigliettaio: In seconda classe, ventidue euro.\n"
            "Viaggiatore: Lo prendo. Posso scegliere il posto?\n"
            "Bigliettaio: Sì. Preferisce finestrino o corridoio?\n"
            "Viaggiatore: Finestrino, per favore. Senso di marcia.\n"
            "Bigliettaio: Ecco il suo biglietto. La carrozza è la quattro, posto diciassette.\n"
            "Bigliettaio: Il treno parte dal binario sei.\n"
            "Viaggiatore: Grazie mille. Sono in anticipo, ho tempo per un caffè.\n"
            "Bigliettaio: Ce n'è uno proprio all'interno della stazione. Buon viaggio!"
        ),
        "order": 3,
    },
    # ── ITALIAN ADVANCED ─────────────────────────────────────────────────────
    {
        "slug": "it-advanced-banca",
        "language": "it",
        "difficulty": "advanced",
        "length": "short",        "title": "In banca",
        "description_en": "Opening a bank account and setting up online banking.",
        "description_da": "Åbn en bankkonto og opsæt netbank.",
        "description_it": "Aprire un conto corrente e attivare l'home banking.",
        "format": "dialogue",
        "speakers": json.dumps(["Cliente", "Impiegato"]),
        "body": (
            "Cliente: Buongiorno. Vorrei aprire un conto corrente.\n"
            "Impiegato: Benvenuto. Si accomodi. Ha già un rapporto con la nostra banca?\n"
            "Cliente: No, è la prima volta. Ho bisogno di un conto per accredito stipendio e pagamenti online.\n"
            "Impiegato: Ottimo. Le illustro le nostre opzioni. Abbiamo tre tipi di conto: base, standard e premium.\n"
            "Impiegato: Il conto base prevede canone zero se accredita lo stipendio e ha un limite di tre prelievi gratuiti al mese.\n"
            "Impiegato: Il conto standard costa cinque euro al mese e include prelievi illimitati e una carta di credito.\n"
            "Cliente: Qual è la differenza principale tra standard e premium?\n"
            "Impiegato: Il premium offre anche gestione degli investimenti e assistenza dedicata ventiquattr'ore su ventiquattro.\n"
            "Cliente: Per il momento il conto standard va benissimo.\n"
            "Impiegato: Perfetto. Avrò bisogno del suo documento d'identità, codice fiscale e una bolletta recente per la residenza.\n"
            "Cliente: Eccoli. Ho tutto con me.\n"
            "Impiegato: Ottimo. Compilo io il modulo. Firmi qui e qui.\n"
            "Impiegato: L'accesso all'home banking sarà attivo entro ventiquattr'ore.\n"
            "Impiegato: Riceverà la carta entro cinque giorni lavorativi.\n"
            "Cliente: Grazie. Ha un numero a cui posso rivolgermi in caso di problemi?\n"
            "Impiegato: Certo. Questo è il mio biglietto da visita con il mio numero diretto.\n"
            "Cliente: Perfetto. Grazie per la disponibilità."
        ),
        "order": 1,
    },
    {
        "slug": "it-advanced-affitto",
        "language": "it",
        "difficulty": "advanced",
        "length": "short",        "title": "Cercare casa in affitto",
        "description_en": "Negotiating a rental contract with a landlord.",
        "description_da": "Forhandle en lejekontrakt med en udlejer.",
        "description_it": "Trattare un contratto d'affitto con un proprietario.",
        "format": "dialogue",
        "speakers": json.dumps(["Inquilino", "Proprietario"]),
        "body": (
            "Inquilino: Ho visto l'annuncio online per l'appartamento in Via Roma.\n"
            "Proprietario: Sì, è ancora disponibile. Quando vuole venire a vederlo?\n"
            "Inquilino: Sarei libero domani mattina, se possibile.\n"
            "Proprietario: Domani alle dieci va bene.\n"
            "Inquilino: Perfetto. Quanto è la superficie?\n"
            "Proprietario: Settanta metri quadri: due camere, un bagno, cucina abitabile e balcone.\n"
            "Inquilino: Che piano è?\n"
            "Proprietario: Terzo, con ascensore. L'esposizione è a sud, molto luminoso.\n"
            "Proprietario: L'affitto mensile è di ottocentocinquanta euro, più spese condominiali di circa ottanta euro.\n"
            "Inquilino: Include il riscaldamento?\n"
            "Proprietario: No, il riscaldamento è autonomo. I consumi dipendono dall'uso.\n"
            "Inquilino: È trattabile il canone?\n"
            "Proprietario: Di poco. Se firma un contratto triennale, posso scendere a ottocentoventi.\n"
            "Inquilino: La caparra a quanto ammonta?\n"
            "Proprietario: Due mesi d'affitto, restituiti alla fine se l'immobile è in buone condizioni.\n"
            "Inquilino: Devo pensarci. Le faccio sapere domani dopo la visita.\n"
            "Proprietario: Certo, nessuna fretta. A domani."
        ),
        "order": 2,
    },
    {
        "slug": "it-advanced-colloquio",
        "language": "it",
        "difficulty": "advanced",
        "length": "short",        "title": "Il colloquio di lavoro",
        "description_en": "A job interview at an Italian company.",
        "description_da": "En jobsamtale hos et italiensk firma.",
        "description_it": "Un colloquio di lavoro in un'azienda italiana.",
        "format": "dialogue",
        "speakers": json.dumps(["Intervistatrice", "Candidato"]),
        "body": (
            "Intervistatrice: Buongiorno. Prego, si accomodi. Sono la direttrice delle risorse umane, Elena Ferretti.\n"
            "Candidato: Buongiorno, dottoressa Ferretti. Piacere, sono Lorenzo Mancini.\n"
            "Intervistatrice: Ho letto il suo curriculum con attenzione. Ha un percorso interessante.\n"
            "Candidato: Grazie. Ho lavorato cinque anni nel settore del marketing digitale, prima a Milano e poi a Barcellona.\n"
            "Intervistatrice: Cosa l'ha portata a candidarsi da noi?\n"
            "Candidato: Ho seguito la vostra crescita nell'e-commerce negli ultimi due anni. Il progetto di espansione europea mi interessava molto.\n"
            "Intervistatrice: Bene. Ci descriva la sua esperienza nella gestione di campagne internazionali.\n"
            "Candidato: Ho coordinato campagne su quattro mercati europei con budget superiori a trecentomila euro. I risultati in termini di conversioni sono stati superiori agli obiettivi del trenta per cento.\n"
            "Intervistatrice: Lavora bene in team o preferisce l'autonomia?\n"
            "Candidato: Apprezzo entrambe le modalità. Nei ruoli di leadership è fondamentale saper motivare il gruppo, ma so anche lavorare in modo indipendente quando necessario.\n"
            "Intervistatrice: Quali sarebbero le sue aspettative salariali?\n"
            "Candidato: In base al ruolo e alle responsabilità descritte, mi aspetto qualcosa tra i quarantadue e i quarantacinquemila euro lordi annui.\n"
            "Intervistatrice: Rientra nel nostro range. Le faremo sapere entro la settimana prossima.\n"
            "Candidato: Grazie per l'opportunità, dottoressa Ferretti."
        ),
        "order": 3,
    },

    # ── DANISH BEGINNER ──────────────────────────────────────────────────────
    {
        "slug": "da-beginner-kaffe",
        "language": "da",
        "difficulty": "beginner",
        "length": "short",        "title": "På caféen",
        "description_en": "Order coffee and cake at a Danish café.",
        "description_da": "Bestil kaffe og kage på en dansk café.",
        "description_it": "Ordina caffè e dolce in un bar danese.",
        "format": "dialogue",
        "speakers": json.dumps(["Kunde", "Barista"]),
        "body": (
            "Barista: Goddag! Hvad må det være?\n"
            "Kunde: Jeg vil gerne have en kop kaffe, tak.\n"
            "Barista: Med mælk?\n"
            "Kunde: Ja tak, lidt mælk.\n"
            "Barista: Ønsker du noget at spise?\n"
            "Kunde: Ja, et stykke chokoladekage.\n"
            "Barista: Det er tres kroner i alt.\n"
            "Kunde: Værsgo. Her er tres kroner.\n"
            "Barista: Tak! Vi råber op, når din ordre er klar.\n"
            "Kunde: Mange tak. Ses!"
        ),
        "order": 1,
    },
    {
        "slug": "da-beginner-supermarked",
        "language": "da",
        "difficulty": "beginner",
        "length": "short",        "title": "I supermarkedet",
        "description_en": "Shopping for groceries in a Danish supermarket.",
        "description_da": "Handle dagligvarer i et dansk supermarked.",
        "description_it": "Fare la spesa in un supermercato danese.",
        "format": "dialogue",
        "speakers": json.dumps(["Kunde", "Medarbejder"]),
        "body": (
            "Kunde: Undskyld, kan du hjælpe mig? Jeg leder efter mælk.\n"
            "Medarbejder: Ja, mejerivarerne er derovre til venstre.\n"
            "Kunde: Tak. Har I også fuldkornsbrød?\n"
            "Medarbejder: Ja, brødet er i midtergangen, hylde tre.\n"
            "Kunde: Perfekt. Og hvor er æblerne?\n"
            "Medarbejder: Frugt og grønt er ved indgangen.\n"
            "Kunde: Mange tak for hjælpen.\n"
            "Medarbejder: Selv tak. God handel!"
        ),
        "order": 2,
    },
    {
        "slug": "da-beginner-vejret",
        "language": "da",
        "difficulty": "beginner",
        "length": "short",        "title": "Hvad er vejret?",
        "description_en": "Talk about the weather with a colleague.",
        "description_da": "Snak om vejret med en kollega.",
        "description_it": "Parlare del tempo con un collega.",
        "format": "dialogue",
        "speakers": json.dumps(["Anna", "Lars"]),
        "body": (
            "Anna: God morgen! Hvordan har du det?\n"
            "Lars: Godt, tak. Men det er koldt i dag!\n"
            "Anna: Ja, det er kun fem grader.\n"
            "Lars: Det er ikke sjovt at cykle i det vejr.\n"
            "Anna: Nej, jeg tog bussen i dag.\n"
            "Lars: Det var klogt. Er der regn i udsigt?\n"
            "Anna: Vejr-appen siger, at det regner til middag.\n"
            "Lars: Åh nej. Jeg glemte min paraply derhjemme!\n"
            "Anna: Tag min. Jeg har en ekstra.\n"
            "Lars: Det er meget venligt af dig. Tak!"
        ),
        "order": 3,
    },
    # ── DANISH INTERMEDIATE ──────────────────────────────────────────────────
    {
        "slug": "da-intermediate-laege",
        "language": "da",
        "difficulty": "intermediate",
        "length": "short",        "title": "Hos lægen",
        "description_en": "A visit to the doctor about a cold.",
        "description_da": "Et besøg hos lægen på grund af en forkølelse.",
        "description_it": "Una visita dal medico per un raffreddore.",
        "format": "dialogue",
        "speakers": json.dumps(["Patient", "Læge"]),
        "body": (
            "Læge: Goddag. Hvad kan jeg hjælpe dig med?\n"
            "Patient: Jeg har været forkølet i en uge. Jeg hoster meget og har ondt i halsen.\n"
            "Læge: Har du også feber?\n"
            "Patient: Ja, i går havde jeg otteogtredive grader.\n"
            "Læge: Har du taget noget imod feberen?\n"
            "Patient: Ja, paracetamol. Det hjælper lidt.\n"
            "Læge: Lad mig kigge i din hals. Sig aah.\n"
            "Patient: Aah.\n"
            "Læge: Halsen er lidt rød, men det ligner ikke en halsbetændelse. Det er sandsynligvis en viral infektion.\n"
            "Patient: Hvad skal jeg gøre?\n"
            "Læge: Hvil dig, drik masser af vand og tag paracetamol efter behov.\n"
            "Læge: Hvis du har det bedre om tre dage, behøver du ikke komme igen.\n"
            "Patient: Hvornår skal jeg være bekymret?\n"
            "Læge: Hvis feberen stiger over niogtredive en halv, eller du får svært ved at trække vejret, skal du ringe til os.\n"
            "Patient: Mange tak, doktor."
        ),
        "order": 1,
    },
    {
        "slug": "da-intermediate-rejse",
        "language": "da",
        "difficulty": "intermediate",
        "length": "short",        "title": "Planlæg en rejse",
        "description_en": "Planning a holiday trip with a travel agent.",
        "description_da": "Planlæg en ferietur med et rejsebureau.",
        "description_it": "Pianificare una vacanza con un agente di viaggio.",
        "format": "dialogue",
        "speakers": json.dumps(["Kunde", "Rejsekonsulent"]),
        "body": (
            "Kunde: Goddag. Jeg vil gerne bestille en ferie til Italien.\n"
            "Rejsekonsulent: Hvad slags ferie søger du? Strandhotel, bytur eller noget tredje?\n"
            "Kunde: Vi er to voksne og en teenager. Vi vil gerne se lidt kultur, men også slappe af.\n"
            "Rejsekonsulent: Toscana er oplagt. I kan kombinere kulturelle oplevelser i Firenze med afslapning på landet.\n"
            "Kunde: Lyder fantastisk. Hvornår rejser vi?\n"
            "Rejsekonsulent: Vi har to uger i juli til rådighed.\n"
            "Kunde: Juli er højsæson. Er det dyrt?\n"
            "Rejsekonsulent: Jeg vil anbefale at booke tidligt. For tre personer, med fly fra København og en agriturismo i syv nætter, plus hoteller i Firenze og Siena, regner vi cirka femogtyvtusinde til otteogtyvetusinde kroner.\n"
            "Kunde: Det er inden for budgettet. Inkluderer det morgenmad?\n"
            "Rejsekonsulent: Morgenmad er inkluderet på agriturismoen. Hotellerne tilbyder det som tilkøb.\n"
            "Kunde: Vi tager det med. Hvad er næste skridt?\n"
            "Rejsekonsulent: Jeg laver et konkret tilbud og sender det til dig inden fredag.\n"
            "Kunde: Perfekt. Tak for hjælpen!"
        ),
        "order": 2,
    },
    {
        "slug": "da-intermediate-job",
        "language": "da",
        "difficulty": "intermediate",
        "length": "short",        "title": "En ny stilling",
        "description_en": "Discussing a new job offer with a friend.",
        "description_da": "Diskuter et nyt jobtilbud med en ven.",
        "description_it": "Discutere una nuova offerta di lavoro con un amico.",
        "format": "dialogue",
        "speakers": json.dumps(["Mikkel", "Sofie"]),
        "body": (
            "Mikkel: Jeg har fået et jobtilbud!\n"
            "Sofie: Det er fantastisk! Hvad er det for et job?\n"
            "Mikkel: En stilling som projektleder i en ny tech-virksomhed.\n"
            "Sofie: Lyder godt! Hvad med lønnen?\n"
            "Mikkel: De tilbyder ti procent mere, end jeg tjener nu.\n"
            "Sofie: Det er da fedt. Er der nogen ulemper?\n"
            "Mikkel: Det er lidt længere transport. Og der er prøvetid på seks måneder.\n"
            "Sofie: Prøvetid er jo normalt. Hvad siger din kæreste?\n"
            "Mikkel: Hun synes, jeg skal tage det.\n"
            "Sofie: Og hvad siger din mavefornemmelse?\n"
            "Mikkel: Positiv! Teamet virkede engageret, og opgaverne er spændende.\n"
            "Sofie: Så tag det! Hvornår skal du give svar?\n"
            "Mikkel: Inden på fredag.\n"
            "Sofie: Skrid til, og held og lykke!"
        ),
        "order": 3,
    },
    # ── DANISH ADVANCED ──────────────────────────────────────────────────────
    {
        "slug": "da-advanced-bank",
        "language": "da",
        "difficulty": "advanced",
        "length": "short",        "title": "I banken",
        "description_en": "Opening a bank account and setting up digital services.",
        "description_da": "Åbn en bankkonto og opsæt digitale tjenester.",
        "description_it": "Aprire un conto in banca e attivare servizi digitali.",
        "format": "dialogue",
        "speakers": json.dumps(["Kunde", "Rådgiver"]),
        "body": (
            "Kunde: Goddag. Jeg vil gerne oprette en konto.\n"
            "Rådgiver: Selvfølgelig. Er du kunde hos os i forvejen?\n"
            "Kunde: Nej, dette er min første konto her.\n"
            "Rådgiver: Fint nok. Vi har tre typer konti: basiskonto, standardkonto og premiumpakke.\n"
            "Rådgiver: Basiskontoen er gebyrfri, hvis du har din løn stående hos os.\n"
            "Rådgiver: Standardkontoen koster fyrre kroner om måneden og inkluderer gratis hævninger og et Visa-kreditkort.\n"
            "Kunde: Hvad er forskellen til premium?\n"
            "Rådgiver: Premiumpakken giver adgang til investeringsrådgivning og prioriteret kundeservice.\n"
            "Kunde: Standardkontoen passer bedst til mig.\n"
            "Rådgiver: Perfekt. Jeg har brug for dit kørekort eller pas, dit NemID og et nyligt brev, der bekræfter din adresse.\n"
            "Kunde: Her er mit pas og mit sundhedskort. Hvad med NemID?\n"
            "Rådgiver: Du skal aktivere det her på stedet via vores system. Det tager fem minutter.\n"
            "Kunde: Kan jeg allerede bruge MobilePay i dag?\n"
            "Rådgiver: Ja, du kan tilknytte kortet til MobilePay, så snart du har fået det. Kortet ankommer inden for tre hverdage.\n"
            "Kunde: Fremragende. Og netbanken?\n"
            "Rådgiver: Den aktiveres automatisk. Du modtager en velkomstsms med en kode i dag.\n"
            "Kunde: Mange tak. Det var nemmere end forventet!"
        ),
        "order": 1,
    },
    {
        "slug": "da-advanced-lejekontrakt",
        "language": "da",
        "difficulty": "advanced",
        "length": "short",        "title": "Lejekontrakt",
        "description_en": "Reviewing and signing a rental agreement.",
        "description_da": "Gennemgå og underskriv en lejekontrakt.",
        "description_it": "Esaminare e firmare un contratto d'affitto.",
        "format": "dialogue",
        "speakers": json.dumps(["Lejer", "Udlejer"]),
        "body": (
            "Lejer: Jeg har kigget kontrakten igennem, og jeg har et par spørgsmål.\n"
            "Udlejer: Selvfølgelig. Hvad drejer det sig om?\n"
            "Lejer: I paragraf tre står der, at jeg ikke må holde husdyr. Men vi har en lille kat.\n"
            "Udlejer: Det er et restriktivt vilkår. Vi kan tilføje en undtagelse for små stuegående kæledyr, hvis ejerforeningen accepterer det. Jeg undersøger det.\n"
            "Lejer: Godt. Og vedrørende depositum: kontrakten angiver tre måneders husleje. Er det til forhandling?\n"
            "Udlejer: Standardvilkåret er tre måneder ifølge lejeloven. Vi kan ikke gå under, men du kan betale i rater over tre måneder, hvis det letter det.\n"
            "Lejer: Det hjælper. Hvad med vedligeholdelse? Hvem betaler hvad?\n"
            "Udlejer: Indvendig vedligeholdelse er lejers ansvar, det vil sige maling og småreparationer. Større reparationer af rør og elinstallationer dækkes af udlejer.\n"
            "Lejer: Hvad sker der, hvis jeg ønsker at opsige kontrakten før tid?\n"
            "Udlejer: Opsigelsesvarslet er tre måneder. Fraflytter du inden kontraktens udløb, skal du betale leje i opsigelsesperioden, medmindre vi finder en ny lejer hurtigere.\n"
            "Lejer: Alt i alt synes jeg, vilkårene er rimelige. Kan vi underskrive i dag?\n"
            "Udlejer: Ja. Jeg printer to eksemplarer. Vi underskriver begge, og du får dit eksemplar med det samme.\n"
            "Lejer: Perfekt."
        ),
        "order": 2,
    },
    {
        "slug": "da-advanced-interview",
        "language": "da",
        "difficulty": "advanced",
        "length": "short",        "title": "Jobinterview",
        "description_en": "A professional job interview in Danish.",
        "description_da": "Et professionelt jobinterview på dansk.",
        "description_it": "Un colloquio di lavoro professionale in danese.",
        "format": "dialogue",
        "speakers": json.dumps(["Interviewer", "Mette"]),
        "body": (
            "Interviewer: Goddag og velkommen. Sæt dig ned. Kan vi tilbyde dig kaffe eller vand?\n"
            "Mette: Vand, tak.\n"
            "Interviewer: Du søger stillingen som marketingchef. Kan du starte med at præsentere dig?\n"
            "Mette: Selvfølgelig. Jeg hedder Mette Kjær. Jeg har otte års erfaring inden for digital markedsføring, de seneste tre år som seniorkonsulent i et internationalt bureau.\n"
            "Interviewer: Hvad tiltrækker dig ved netop vores virksomhed?\n"
            "Mette: Jeres bæredygtighedsprofil og jeres ekspansion på det nordiske marked er det, der skiller jer ud. Jeg tror på, at stærk markedsføring og ansvarlig vækst kan gå hånd i hånd.\n"
            "Interviewer: Hvilke kompetencer mener du er afgørende for rollen?\n"
            "Mette: Dataanalyse, evnen til at fortælle overbevisende historier om brandet og stærk interessentkommunikation. Og selvfølgelig evnen til at lede og motivere et team.\n"
            "Interviewer: Beskriv en situation, hvor du vendte et underpræsterende kampagneresultat.\n"
            "Mette: Vi lancerede en kampagne med fladt engagement de første to uger. Jeg analyserede målgruppedataene og identificerede, at vi ramte en for bred aldersgruppe. Vi tilpassede budskabet til femogtyvefyrreårige urbane professionelle, og konverteringsraten steg med femogfyrre procent inden for to uger.\n"
            "Interviewer: Imponerende. Hvad er dine lønforventninger?\n"
            "Mette: Baseret på rollens ansvar og branchens niveau forventer jeg en årsløn på sekshundrede og firs tusinde til syvhundrede og tyve tusinde kroner.\n"
            "Interviewer: Det er inden for vores ramme. Vi vender tilbage inden for to uger.\n"
            "Mette: Mange tak for en god samtale."
        ),
        "order": 3,
    },

    # ── ENGLISH BEGINNER ─────────────────────────────────────────────────────
    {
        "slug": "en-beginner-coffee-shop",
        "language": "en",
        "difficulty": "beginner",
        "length": "short",        "title": "At the coffee shop",
        "description_en": "Order a drink and a snack at a coffee shop.",
        "description_da": "Bestil en drink og en snack på en kaffebar.",
        "description_it": "Ordinare una bevanda e uno spuntino in una caffetteria.",
        "format": "dialogue",
        "speakers": json.dumps(["Barista", "Sarah"]),
        "body": (
            "Barista: Hello! What can I get for you today?\n"
            "Sarah: Hi! Can I have a medium latte, please?\n"
            "Barista: Of course. Would you like any syrup in that?\n"
            "Sarah: Yes, vanilla, please.\n"
            "Barista: Sure. Anything to eat?\n"
            "Sarah: Yes, a blueberry muffin, please.\n"
            "Barista: Great choice. What's your name?\n"
            "Sarah: Sarah.\n"
            "Barista: That will be six dollars and fifty cents, please.\n"
            "Sarah: Here you go.\n"
            "Barista: Thanks! We'll call your name when it's ready.\n"
            "Sarah: Thank you!"
        ),
        "order": 1,
    },
    {
        "slug": "en-beginner-grocery",
        "language": "en",
        "difficulty": "beginner",
        "length": "short",        "title": "At the grocery store",
        "description_en": "Find items and pay at the grocery store.",
        "description_da": "Find varer og betal i supermarkedet.",
        "description_it": "Trovare articoli e pagare al supermercato.",
        "format": "dialogue",
        "speakers": json.dumps(["Customer", "Employee"]),
        "body": (
            "Customer: Excuse me, where can I find the bread?\n"
            "Employee: It's in aisle four, on the left side.\n"
            "Customer: Thank you. And do you have almond milk?\n"
            "Employee: Yes, it's with the dairy alternatives, in aisle two.\n"
            "Customer: Great. I also need some apples.\n"
            "Employee: Fresh fruit is at the back of the store.\n"
            "Customer: Perfect. That's everything I need.\n"
            "Employee: Are you ready to check out?\n"
            "Customer: Yes, please. Do you take card?\n"
            "Employee: Of course. Tap or insert?\n"
            "Customer: Tap, please.\n"
            "Employee: All done. Have a great day!"
        ),
        "order": 2,
    },
    {
        "slug": "en-beginner-directions",
        "language": "en",
        "difficulty": "beginner",
        "length": "short",        "title": "Asking for directions",
        "description_en": "Ask a local how to get to the train station.",
        "description_da": "Spørg en lokal om vej til togstationen.",
        "description_it": "Chiedere indicazioni per la stazione ferroviaria.",
        "format": "dialogue",
        "speakers": json.dumps(["Visitor", "Local"]),
        "body": (
            "Visitor: Excuse me! Can you help me?\n"
            "Local: Sure, what do you need?\n"
            "Visitor: I'm looking for the train station. Am I going the right way?\n"
            "Local: Actually, no. You're going the wrong direction.\n"
            "Visitor: Oh no. How do I get there?\n"
            "Local: Go back to the traffic lights and turn left.\n"
            "Local: Then walk straight for about five minutes.\n"
            "Local: You'll see a big clock tower. The station entrance is right next to it.\n"
            "Visitor: Got it. Left at the lights, then straight.\n"
            "Local: Yes, exactly. You can't miss it.\n"
            "Visitor: Thank you so much!\n"
            "Local: No problem. Have a good trip!"
        ),
        "order": 3,
    },
    # ── ENGLISH INTERMEDIATE ─────────────────────────────────────────────────
    {
        "slug": "en-intermediate-doctor",
        "language": "en",
        "difficulty": "intermediate",
        "length": "short",        "title": "At the doctor",
        "description_en": "Describe symptoms and get advice from a doctor.",
        "description_da": "Beskriv symptomer og få råd fra en læge.",
        "description_it": "Descrivere sintomi e ricevere consigli dal medico.",
        "format": "dialogue",
        "speakers": json.dumps(["Doctor", "Patient"]),
        "body": (
            "Doctor: Good morning. What brings you in today?\n"
            "Patient: I've had a sore throat and a headache for the past four days.\n"
            "Doctor: Do you have a fever?\n"
            "Patient: I did yesterday, about thirty-eight point five. It seems to have gone down overnight.\n"
            "Doctor: Any other symptoms? Cough, runny nose, body aches?\n"
            "Patient: A bit of a runny nose, and I feel quite tired.\n"
            "Doctor: Have you taken anything for the fever?\n"
            "Patient: Just ibuprofen. It helped for a few hours.\n"
            "Doctor: Let me take a look at your throat. Open wide and say ahh.\n"
            "Patient: Ahh.\n"
            "Doctor: Your throat is a little red, but I don't see signs of a bacterial infection.\n"
            "Doctor: This looks like a viral illness.\n"
            "Patient: Should I take antibiotics?\n"
            "Doctor: No, antibiotics don't work against viruses.\n"
            "Doctor: Rest, stay hydrated, and keep taking ibuprofen as needed.\n"
            "Doctor: If you're not improving in five days, or if your fever spikes again, come back.\n"
            "Patient: Thank you, doctor."
        ),
        "order": 1,
    },
    {
        "slug": "en-intermediate-apartment",
        "language": "en",
        "difficulty": "intermediate",
        "length": "short",        "title": "Renting an apartment",
        "description_en": "Enquire about an apartment listing on the phone.",
        "description_da": "Forhør dig om en lejlighedsannonce per telefon.",
        "description_it": "Informarsi su un annuncio di appartamento per telefono.",
        "format": "dialogue",
        "speakers": json.dumps(["Caller", "Agent"]),
        "body": (
            "Caller: Hi, I'm calling about the two-bedroom apartment you have listed.\n"
            "Agent: Oh, yes. Are you interested in viewing it?\n"
            "Caller: Definitely. Can you tell me a bit more about it first?\n"
            "Agent: Of course. It's on the third floor, about seventy square metres.\n"
            "Agent: It has a modern kitchen, a balcony, and great natural light.\n"
            "Caller: Is parking included?\n"
            "Agent: There's one parking space in the garage, yes.\n"
            "Caller: What's the monthly rent?\n"
            "Agent: It's fifteen hundred a month, plus utilities.\n"
            "Caller: Are utilities usually another hundred or two?\n"
            "Agent: About that, yes, depending on usage.\n"
            "Caller: Is the landlord open to a long-term lease?\n"
            "Agent: Yes, he prefers at least twelve months.\n"
            "Caller: That works for me. When can I come to see it?\n"
            "Agent: How about Saturday at eleven?\n"
            "Caller: Saturday at eleven is perfect. What's the address?\n"
            "Agent: It's forty-two Maple Street, apartment three B.\n"
            "Caller: Great. See you then. Thanks!"
        ),
        "order": 2,
    },
    {
        "slug": "en-intermediate-meeting",
        "language": "en",
        "difficulty": "intermediate",
        "length": "short",        "title": "A work meeting",
        "description_en": "Discuss a project update in a team meeting.",
        "description_da": "Diskuter en projektstatus i et teammøde.",
        "description_it": "Discutere un aggiornamento di progetto in una riunione.",
        "format": "dialogue",
        "speakers": json.dumps(["Manager", "Tom", "Lisa"]),
        "body": (
            "Manager: Thanks everyone for joining. Let's get started.\n"
            "Manager: Can you give us a quick update on the project, Tom?\n"
            "Tom: Sure. We're on track with phase one. The design mockups are done.\n"
            "Tom: We're waiting on client approval before we move to development.\n"
            "Manager: When do you expect to hear back from them?\n"
            "Tom: By the end of this week, hopefully.\n"
            "Manager: What's the risk if they delay?\n"
            "Tom: We'd lose about four working days. We could absorb that without slipping the deadline.\n"
            "Manager: Good. Any blockers right now?\n"
            "Tom: We need access to their content management system.\n"
            "Lisa: IT is setting that up. It should be ready by Thursday.\n"
            "Manager: Okay, I'll chase that up after this meeting.\n"
            "Manager: Anything else from the team?\n"
            "Lisa: I'd like to schedule a quick call with the client to clarify the brand guidelines.\n"
            "Manager: Go ahead and set that up. Copy me in.\n"
            "Lisa: Will do.\n"
            "Manager: Great. Let's touch base again on Thursday. Thanks, everyone."
        ),
        "order": 3,
    },
    # ── ENGLISH ADVANCED ─────────────────────────────────────────────────────
    {
        "slug": "en-advanced-negotiation",
        "language": "en",
        "difficulty": "advanced",
        "length": "short",        "title": "Salary negotiation",
        "description_en": "Negotiate your salary in a job offer conversation.",
        "description_da": "Forhandl løn i forbindelse med et jobtilbud.",
        "description_it": "Negoziare il proprio stipendio in una trattativa di lavoro.",
        "format": "dialogue",
        "speakers": json.dumps(["Recruiter", "Candidate"]),
        "body": (
            "Recruiter: We're pleased to offer you the position. Before we proceed, I'd like to discuss compensation.\n"
            "Candidate: Thank you. I'm genuinely excited about the role.\n"
            "Recruiter: Based on your experience, we're proposing a base salary of sixty-two thousand.\n"
            "Candidate: I appreciate the offer. I was hoping we could discuss something closer to sixty-eight thousand.\n"
            "Candidate: That's based on my seven years of industry experience and the results I've driven, particularly the thirty per cent revenue increase in my last role.\n"
            "Recruiter: I understand your reasoning. Sixty-eight is above our current band for this level.\n"
            "Candidate: Could we meet somewhere in the middle? Perhaps sixty-five thousand, with a review at six months?\n"
            "Recruiter: I could see sixty-five working, especially with the six-month review.\n"
            "Candidate: What does the bonus structure look like?\n"
            "Recruiter: There's an annual performance bonus of up to fifteen per cent of base salary.\n"
            "Candidate: And the benefits package?\n"
            "Recruiter: Private healthcare, twenty-five days' holiday, pension contributions, and a hybrid working policy.\n"
            "Candidate: That's a strong package. I'd like to accept at sixty-five thousand with the conditions we've discussed.\n"
            "Recruiter: Wonderful. We'll get the formal offer letter to you by end of day.\n"
            "Candidate: Thank you. I look forward to joining the team."
        ),
        "order": 1,
    },
    {
        "slug": "en-advanced-complaint",
        "language": "en",
        "difficulty": "advanced",
        "length": "short",        "title": "Making a formal complaint",
        "description_en": "Lodge a formal complaint about a faulty product.",
        "description_da": "Indgiv en formel klage over et fejlbehæftet produkt.",
        "description_it": "Presentare un reclamo formale su un prodotto difettoso.",
        "format": "dialogue",
        "speakers": json.dumps(["Customer", "Manager"]),
        "body": (
            "Customer: Good afternoon. I'd like to speak with the customer service manager, please.\n"
            "Manager: I am the duty manager. How can I assist you?\n"
            "Customer: I purchased a laptop from your store three weeks ago, and it's already malfunctioning.\n"
            "Manager: I'm sorry to hear that. Can you describe the issue?\n"
            "Customer: The battery won't hold a charge for more than thirty minutes, and the keyboard intermittently stops responding.\n"
            "Customer: For a fifteen-hundred-pound device, this is entirely unacceptable.\n"
            "Manager: I completely understand your frustration. Do you have the receipt with you?\n"
            "Customer: Yes, here it is. I also have the original packaging.\n"
            "Manager: Thank you. You're within your statutory thirty-day return window.\n"
            "Manager: We have two options: a full refund, or a replacement unit.\n"
            "Customer: I'd prefer a refund, please. I've lost confidence in this particular model.\n"
            "Manager: Of course. I'll process that now. The funds will appear within three to five business days.\n"
            "Customer: In writing, if possible. I'd like a confirmation email.\n"
            "Manager: Absolutely. Can I take your email address?\n"
            "Customer: It's johnson at email dot com.\n"
            "Manager: Done. I sincerely apologise for the inconvenience.\n"
            "Customer: Thank you for handling this so professionally."
        ),
        "order": 2,
    },
    {
        "slug": "en-advanced-conference",
        "language": "en",
        "difficulty": "advanced",
        "length": "short",        "title": "At a professional conference",
        "description_en": "Network and discuss ideas at an industry conference.",
        "description_da": "Netværk og diskuter idéer på en branchekonference.",
        "description_it": "Fare networking e discutere idee a una conferenza di settore.",
        "format": "dialogue",
        "speakers": json.dumps(["Alex", "Jordan"]),
        "body": (
            "Alex: Excuse me, I loved your talk on sustainable supply chains.\n"
            "Jordan: Thank you so much! Are you in the logistics sector?\n"
            "Alex: I'm in procurement, actually. We're grappling with the same challenges.\n"
            "Alex: The pressure to decarbonise while keeping costs competitive is enormous.\n"
            "Jordan: Absolutely. We've been trialling carbon-offset partnerships with our key suppliers.\n"
            "Jordan: The results have been mixed, but directionally positive.\n"
            "Alex: That's interesting. We've been exploring supplier incentive programmes.\n"
            "Alex: We reward partners who meet sustainability targets with preferential payment terms.\n"
            "Jordan: That's a smart lever. Does it scale across a large supplier base?\n"
            "Alex: It's a challenge. We piloted it with the top twenty suppliers first.\n"
            "Alex: The plan is to roll it out to the next tier next quarter.\n"
            "Jordan: Would you be open to connecting further on this?\n"
            "Jordan: We have a working group on sustainable procurement, and your insights could be valuable.\n"
            "Alex: I'd be delighted. Here's my card.\n"
            "Jordan: Brilliant. I'll reach out next week. There's a lot we could learn from each other.\n"
            "Alex: Looking forward to it. Enjoy the rest of the conference!"
        ),
        "order": 3,
    },
]


_TITLE_SUFFIXES = {
    "en": {"medium": "Extended", "long": "Complete"},
    "da": {"medium": "Udvidet", "long": "Komplet"},
    "it": {"medium": "Versione estesa", "long": "Versione completa"},
}

_DESCRIPTION_SUFFIXES = {
    "en": {
        "medium": " Longer practice version.",
        "long": " Full-length practice version.",
    },
    "da": {
        "medium": " Længere øveversion.",
        "long": " Fuld øveversion.",
    },
    "it": {
        "medium": " Versione di pratica più lunga.",
        "long": " Versione completa per esercitarsi.",
    },
}

_UNIQUE_BEATS = {
    "en": [
        {"focus": "timing", "obstacle": "a small delay", "action": "the final check", "result": "a smoother plan"},
        {"focus": "budget", "obstacle": "extra fees", "action": "a clearer estimate", "result": "fewer surprises"},
        {"focus": "quality", "obstacle": "limited options", "action": "a practical alternative", "result": "a better fit"},
        {"focus": "communication", "obstacle": "mixed information", "action": "a written summary", "result": "fewer misunderstandings"},
        {"focus": "availability", "obstacle": "a busy schedule", "action": "a confirmed slot", "result": "a reliable next step"},
        {"focus": "preparation", "obstacle": "missing details", "action": "a checklist", "result": "faster progress"},
        {"focus": "coordination", "obstacle": "different priorities", "action": "a shared plan", "result": "better alignment"},
        {"focus": "follow-up", "obstacle": "unclear ownership", "action": "clear responsibilities", "result": "better execution"},
        {"focus": "consistency", "obstacle": "last-minute changes", "action": "a simple routine", "result": "steady improvement"},
    ],
    "da": [
        {"focus": "timing", "obstacle": "en lille forsinkelse", "action": "det sidste tjek", "result": "en mere rolig plan"},
        {"focus": "budget", "obstacle": "ekstra gebyrer", "action": "et klarere overslag", "result": "færre overraskelser"},
        {"focus": "kvalitet", "obstacle": "få valgmuligheder", "action": "et praktisk alternativ", "result": "en bedre løsning"},
        {"focus": "kommunikation", "obstacle": "blandet information", "action": "et skriftligt overblik", "result": "færre misforståelser"},
        {"focus": "tilgængelighed", "obstacle": "en travl kalender", "action": "en bekræftet tid", "result": "et sikkert næste skridt"},
        {"focus": "forberedelse", "obstacle": "manglende detaljer", "action": "en tjekliste", "result": "hurtigere fremdrift"},
        {"focus": "koordinering", "obstacle": "forskellige prioriteter", "action": "en fælles plan", "result": "bedre samspil"},
        {"focus": "opfølgning", "obstacle": "uklart ansvar", "action": "tydelige roller", "result": "bedre udførelse"},
        {"focus": "stabilitet", "obstacle": "sidste-øjebliks ændringer", "action": "en enkel rutine", "result": "jævn forbedring"},
    ],
    "it": [
        {"focus": "tempistiche", "obstacle": "un piccolo ritardo", "action": "la verifica finale", "result": "un piano più fluido"},
        {"focus": "budget", "obstacle": "costi extra", "action": "una stima più chiara", "result": "meno sorprese"},
        {"focus": "qualità", "obstacle": "poche opzioni", "action": "un'alternativa pratica", "result": "una scelta migliore"},
        {"focus": "comunicazione", "obstacle": "informazioni confuse", "action": "un riepilogo scritto", "result": "meno malintesi"},
        {"focus": "disponibilità", "obstacle": "un'agenda piena", "action": "uno slot confermato", "result": "un prossimo passo sicuro"},
        {"focus": "preparazione", "obstacle": "dettagli mancanti", "action": "una checklist", "result": "avanzamento più rapido"},
        {"focus": "coordinamento", "obstacle": "priorità diverse", "action": "un piano condiviso", "result": "maggiore allineamento"},
        {"focus": "follow-up", "obstacle": "responsabilità poco chiare", "action": "ruoli definiti", "result": "esecuzione migliore"},
        {"focus": "continuità", "obstacle": "cambi all'ultimo minuto", "action": "una routine semplice", "result": "miglioramento costante"},
    ],
}


def _speaker_name(speakers: list[str], index: int) -> str:
    if not speakers:
        return f"Speaker {index + 1}"
    if index < len(speakers):
        return speakers[index]
    return speakers[-1]


def _slug_seed(slug: str) -> int:
    return sum(ord(char) for char in slug)


def _build_unique_block(story: dict, block_index: int, speakers: list[str]) -> list[str]:
    language = story["language"]
    topic = story["title"].lower()
    beats = _UNIQUE_BEATS[language]
    beat = beats[(_slug_seed(story["slug"]) + block_index) % len(beats)]
    s1 = _speaker_name(speakers, 0)
    s2 = _speaker_name(speakers, 1)
    s3 = _speaker_name(speakers, 2)

    if language == "da":
        return [
            f"{s1}: Når vi taler om {topic}, er der én ting mere, vi bør afklare.",
            f"{s2}: Enig. Den største udfordring lige nu er {beat['obstacle']}.",
            f"{s1}: Så lad os fokusere på {beat['focus']} først.",
            f"{s2}: God idé. Jeg tager mig af {beat['action']} i dag.",
            f"{s3}: Imens gennemgår jeg detaljer og tidsplan.",
            f"{s1}: Perfekt, så kan vi tage næste trin bagefter.",
            f"{s2}: Målet er {beat['result']}.",
            f"{s1}: Super. Lad os følge op senere og bekræfte alt.",
        ]

    if language == "it":
        return [
            f"{s1}: Restando su {topic}, c'è ancora un punto da chiarire.",
            f"{s2}: D'accordo. Il problema principale adesso è {beat['obstacle']}.",
            f"{s1}: Allora concentriamoci prima su {beat['focus']}.",
            f"{s2}: Perfetto. Oggi mi occupo io di {beat['action']}.",
            f"{s3}: Intanto controllo bene dettagli e tempistiche.",
            f"{s1}: Ottimo, così possiamo passare allo step successivo.",
            f"{s2}: L'obiettivo è {beat['result']}.",
            f"{s1}: Benissimo. Più tardi facciamo un rapido follow-up.",
        ]

    return [
        f"{s1}: Since we're still talking about {topic}, there is one more point to settle.",
        f"{s2}: Agreed. The main obstacle right now is {beat['obstacle']}.",
        f"{s1}: Then let's focus on {beat['focus']} first.",
        f"{s2}: Good call. I'll handle {beat['action']} today.",
        f"{s3}: Meanwhile I'll review the details and timeline.",
        f"{s1}: Great, then we can move to the next step.",
        f"{s2}: The target outcome is {beat['result']}.",
        f"{s1}: Perfect. Let's follow up later and confirm everything.",
    ]


def _variant_title(title: str, language: str, length: str) -> str:
    return f"{title} - {_TITLE_SUFFIXES[language][length]}"


def _variant_description(description: str, language: str, length: str) -> str:
    return f"{description}{_DESCRIPTION_SUFFIXES[language][length]}"


def _extend_dialogue_body(story: dict, blocks_to_add: int) -> str:
    speakers = json.loads(story.get("speakers") or "[]")
    language = story["language"]
    topic = story["title"].lower()
    s1 = _speaker_name(speakers, 0)
    s2 = _speaker_name(speakers, 1)

    if language == "da":
        opener = [
            f"{s1}: Skal vi tage en ny snak om {topic}?",
            f"{s2}: Ja, lad os starte fra begyndelsen og lægge en klar plan.",
        ]
        closer = [
            f"{s1}: Perfekt. Nu føles beslutningen mere gennemarbejdet.",
            f"{s2}: Enig. Vi følger op i morgen og justerer om nødvendigt.",
        ]
    elif language == "it":
        opener = [
            f"{s1}: Possiamo riprendere il tema di {topic} da un nuovo punto di vista?",
            f"{s2}: Certo, ricominciamo con un piano più chiaro e dettagliato.",
        ]
        closer = [
            f"{s1}: Perfetto, adesso la decisione è molto più solida.",
            f"{s2}: D'accordo. Facciamo un follow-up domani e rifiniamo i dettagli.",
        ]
    else:
        opener = [
            f"{s1}: Can we revisit {topic} with a fresh plan?",
            f"{s2}: Absolutely. Let's rebuild the conversation step by step.",
        ]
        closer = [
            f"{s1}: Great, this feels much clearer than before.",
            f"{s2}: Agreed. We'll follow up tomorrow and lock the final details.",
        ]

    body_lines: list[str] = []
    body_lines.extend(opener)
    for block_index in range(blocks_to_add):
        body_lines.extend(_build_unique_block(story, block_index, speakers))
    body_lines.extend(closer)
    return "\n".join(body_lines)


def _build_variant_story(story: dict, *, length: str, order_offset: int, blocks_to_add: int) -> dict:
    variant = dict(story)
    variant["slug"] = f"{story['slug']}-{length}"
    variant["length"] = length
    variant["title"] = _variant_title(story["title"], story["language"], length)
    variant["description_en"] = _variant_description(story["description_en"], "en", length)
    variant["description_da"] = _variant_description(story["description_da"], "da", length)
    variant["description_it"] = _variant_description(story["description_it"], "it", length)
    variant["body"] = _extend_dialogue_body(story, blocks_to_add)
    variant["order"] = story["order"] + order_offset
    return variant


def _build_story_variants(base_stories: list[dict]) -> list[dict]:
    expanded: list[dict] = []
    for story in base_stories:
        short_story = dict(story)
        short_story["length"] = "short"
        expanded.append(short_story)
        expanded.append(
            _build_variant_story(short_story, length="medium", order_offset=3, blocks_to_add=2)
        )
        expanded.append(
            _build_variant_story(short_story, length="long", order_offset=6, blocks_to_add=4)
        )
    return expanded


STORIES = _build_story_variants(STORIES)


def seed_stories(db) -> None:
    print(f"  Seeding {len(STORIES)} stories...")
    for s in STORIES:
        existing = (
            db.query(Story)
            .filter(Story.slug == s["slug"], Story.language == s["language"])
            .first()
        )
        if existing:
            existing.difficulty = s["difficulty"]
            existing.length = s.get("length", "short")
            existing.title = s["title"]
            existing.description_en = s["description_en"]
            existing.description_da = s["description_da"]
            existing.description_it = s["description_it"]
            existing.body = s["body"]
            existing.format = s.get("format", "narrative")
            existing.speakers = s.get("speakers")
            existing.order = s["order"]
        else:
            db.add(Story(
                id=str(uuid.uuid4()),
                slug=s["slug"],
                language=s["language"],
                difficulty=s["difficulty"],
                length=s.get("length", "short"),
                title=s["title"],
                description_en=s["description_en"],
                description_da=s["description_da"],
                description_it=s["description_it"],
                body=s["body"],
                format=s.get("format", "narrative"),
                speakers=s.get("speakers"),
                order=s["order"],
            ))
    db.commit()
    persisted_stories = db.query(Story).all()
    print(f"  Pre-generating story audio for {len(persisted_stories)} stories and {len(STORY_SPEED_TO_RATE)} speeds...")
    failures = 0
    for story in persisted_stories:
        failures += upsert_story_audio(db, story)
    if failures:
        print(f"  Story audio generation failures: {failures}")
    print("  Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_stories(db)
    finally:
        db.close()
