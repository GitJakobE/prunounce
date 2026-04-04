"""
Seed story data for the Story Reading feature.
Run with: poetry run python seed_stories.py

Each of the 27 unique stories is translated into 3 languages (en, it, da) = 81 rows.
Stories are fully independent — no variant expansion.
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
    # ═══════════════════════════════════════════════════════════════════════
    #  BEGINNER — SHORT  (100-150 words, 3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 1. The Small Garden ─────────────────────────────────────────────
    {
        "slug": "beginner-small-garden",
        "language": "en",
        "difficulty": "beginner",
        "length": "short",
        "title": "The Small Garden",
        "description_en": "A man brings a little green to his grey city block.",
        "description_da": "En mand bringer lidt grønt til sin grå bygade.",
        "description_it": "Un uomo porta un po' di verde nel suo grigio isolato.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Personal project",
        "setup_summary": "A city dweller plants a seed on his balcony and inspires the whole building.",
        "body": (
            "Marco lives in a big city. There are many tall buildings and cars, but there are no trees. "
            "Marco is sad because he loves green plants. One day, he finds a small pot and some seeds. "
            "He puts soil in the pot and plants a seed. Every morning, he gives it water. He puts the "
            "pot near the window. After two weeks, a small green leaf grows. Marco is very happy. He "
            "shows the plant to his neighbor, Mrs. Rosa. She likes it and buys a pot, too. Now, every "
            "balcony in the building has a small garden. The street is not grey anymore; it is green "
            "and beautiful."
        ),
        "order": 1,
    },

    # ── 2. A Day at the Beach ──────────────────────────────────────────
    {
        "slug": "beginner-beach-day",
        "language": "en",
        "difficulty": "beginner",
        "length": "short",
        "title": "A Day at the Beach",
        "description_en": "Two siblings enjoy a sunny day at the seaside.",
        "description_da": "To søskende nyder en solrig dag ved stranden.",
        "description_it": "Due fratelli si godono una giornata di sole al mare.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Outing / adventure",
        "setup_summary": "A brother and sister swim, build a sandcastle, and find a shell at the beach.",
        "body": (
            "Last Saturday, Sara and her brother, Leo, went to the beach. The sun was hot and the sky "
            "was blue. Sara wore a yellow hat and Leo carried a big ball. First, they swam in the "
            "ocean. The water was cold but very clear. Then, they built a large sandcastle with four "
            "towers. Leo found a beautiful shell near the water and put it on top of the castle. At "
            "lunch, they ate sandwiches and drank cold orange juice. They saw a small crab walking on "
            "the sand. It was a very good day. They went home tired but very happy."
        ),
        "order": 2,
    },

    # ── 3. The Lost Cat ────────────────────────────────────────────────
    {
        "slug": "beginner-lost-cat",
        "language": "en",
        "difficulty": "beginner",
        "length": "short",
        "title": "The Lost Cat",
        "description_en": "A girl searches everywhere for her missing cat.",
        "description_da": "En pige leder overalt efter sin forsvundne kat.",
        "description_it": "Una ragazza cerca ovunque il suo gatto smarrito.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Problem / search",
        "setup_summary": "A girl hunts for her cat and finds it stuck up an apple tree.",
        "body": (
            "Misty is a small white cat with blue eyes. She lives with a girl named Amy. One "
            "afternoon, Amy cannot find Misty. She looks under the bed, but Misty is not there. She "
            "looks in the kitchen, but the cat is not there. Amy goes outside and calls, \"Misty! "
            "Where are you?\" She asks her friend, Tom, \"Do you see my cat?\" Tom looks in his "
            "garden. Suddenly, they hear a \"Meow!\" Misty is at the top of a big apple tree. She is "
            "afraid to come down. Tom brings a ladder and helps the cat. Amy hugs Misty and says, "
            "\"Thank you, Tom!\""
        ),
        "order": 3,
    },

    # ── 1-DA. Den lille have ───────────────────────────────────────────
    {
        "slug": "beginner-small-garden",
        "language": "da",
        "difficulty": "beginner",
        "length": "short",
        "title": "Den lille have",
        "description_en": "A man brings a little green to his grey city block.",
        "description_da": "En mand bringer lidt grønt til sin grå bygade.",
        "description_it": "Un uomo porta un po' di verde nel suo grigio isolato.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Personal project",
        "setup_summary": "A city dweller plants a seed on his balcony and inspires the whole building.",
        "body": (
            "Marco bor i en stor by. Der er mange høje bygninger og biler, men der er ingen træer. "
            "Marco er trist, fordi han elsker grønne planter. En dag finder han en lille potte og "
            "nogle frø. Han kommer jord i potten og planter et frø. Hver morgen giver han det vand. "
            "Han stiller potten nær vinduet. Efter to uger vokser et lille grønt blad. Marco er "
            "meget glad. Han viser planten til sin nabo, fru Rosa. Hun kan lide den og køber også en "
            "potte. Nu har hver altan i bygningen en lille have. Gaden er ikke grå mere; den er grøn "
            "og smuk."
        ),
        "order": 1,
    },

    # ── 1-IT. Il piccolo giardino ──────────────────────────────────────
    {
        "slug": "beginner-small-garden",
        "language": "it",
        "difficulty": "beginner",
        "length": "short",
        "title": "Il piccolo giardino",
        "description_en": "A man brings a little green to his grey city block.",
        "description_da": "En mand bringer lidt grønt til sin grå bygade.",
        "description_it": "Un uomo porta un po' di verde nel suo grigio isolato.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Personal project",
        "setup_summary": "A city dweller plants a seed on his balcony and inspires the whole building.",
        "body": (
            "Marco vive in una grande città. Ci sono molti palazzi alti e macchine, ma non ci sono "
            "alberi. Marco è triste perché ama le piante verdi. Un giorno trova un piccolo vaso e "
            "dei semi. Mette della terra nel vaso e pianta un seme. Ogni mattina gli dà dell'acqua. "
            "Mette il vaso vicino alla finestra. Dopo due settimane, cresce una piccola foglia verde. "
            "Marco è molto felice. Mostra la pianta alla sua vicina, la signora Rosa. A lei piace e "
            "compra anche lei un vaso. Ora, ogni balcone del palazzo ha un piccolo giardino. La "
            "strada non è più grigia; è verde e bella."
        ),
        "order": 1,
    },

    # ── 2-DA. En dag på stranden ───────────────────────────────────────
    {
        "slug": "beginner-beach-day",
        "language": "da",
        "difficulty": "beginner",
        "length": "short",
        "title": "En dag på stranden",
        "description_en": "Two siblings enjoy a sunny day at the seaside.",
        "description_da": "To søskende nyder en solrig dag ved stranden.",
        "description_it": "Due fratelli si godono una giornata di sole al mare.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Outing / adventure",
        "setup_summary": "A brother and sister swim, build a sandcastle, and find a shell at the beach.",
        "body": (
            "Sidste lørdag tog Sara og hendes bror, Leo, på stranden. Solen var varm, og himlen var "
            "blå. Sara bar en gul hat, og Leo bar en stor bold. Først svømmede de i havet. Vandet "
            "var koldt, men meget klart. Derefter byggede de et stort sandslot med fire tårne. Leo "
            "fandt en smuk skal nær vandet og lagde den på toppen af slottet. Til frokost spiste de "
            "sandwich og drak kold appelsinjuice. De så en lille krabbe gå på sandet. Det var en "
            "meget god dag. De tog trætte, men meget glade hjem."
        ),
        "order": 2,
    },

    # ── 2-IT. Una giornata in spiaggia ─────────────────────────────────
    {
        "slug": "beginner-beach-day",
        "language": "it",
        "difficulty": "beginner",
        "length": "short",
        "title": "Una giornata in spiaggia",
        "description_en": "Two siblings enjoy a sunny day at the seaside.",
        "description_da": "To søskende nyder en solrig dag ved stranden.",
        "description_it": "Due fratelli si godono una giornata di sole al mare.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Outing / adventure",
        "setup_summary": "A brother and sister swim, build a sandcastle, and find a shell at the beach.",
        "body": (
            "Sabato scorso, Sara e suo fratello Leo sono andati in spiaggia. Il sole era caldo e il "
            "cielo era blu. Sara indossava un cappello giallo e Leo portava una grande palla. Prima "
            "hanno nuotato nell'oceano. L'acqua era fredda ma molto limpida. Poi hanno costruito un "
            "grande castello di sabbia con quattro torri. Leo ha trovato una bella conchiglia vicino "
            "all'acqua e l'ha messa in cima al castello. A pranzo hanno mangiato panini e bevuto "
            "succo d'arancia freddo. Hanno visto un piccolo granchio camminare sulla sabbia. È stata "
            "una giornata molto bella. Sono tornati a casa stanchi ma molto felici."
        ),
        "order": 2,
    },

    # ── 3-DA. Den forsvundne kat ───────────────────────────────────────
    {
        "slug": "beginner-lost-cat",
        "language": "da",
        "difficulty": "beginner",
        "length": "short",
        "title": "Den forsvundne kat",
        "description_en": "A girl searches everywhere for her missing cat.",
        "description_da": "En pige leder overalt efter sin forsvundne kat.",
        "description_it": "Una ragazza cerca ovunque il suo gatto smarrito.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Problem / search",
        "setup_summary": "A girl hunts for her cat and finds it stuck up an apple tree.",
        "body": (
            "Misty er en lille hvid kat med blå øjne. Hun bor hos en pige, der hedder Amy. En "
            "eftermiddag kan Amy ikke finde Misty. Hun kigger under sengen, men Misty er der ikke. "
            "Hun kigger i køkkenet, men katten er der ikke. Amy går udenfor og kalder: \"Misty! "
            "Hvor er du?\" Hun spørger sin ven, Tom: \"Ser du min kat?\" Tom kigger i sin have. "
            "Pludselig hører de et \"Miav!\" Misty er i toppen af et stort æbletræ. Hun er bange "
            "for at komme ned. Tom henter en stige og hjælper katten. Amy krammer Misty og siger: "
            "\"Tak, Tom!\""
        ),
        "order": 3,
    },

    # ── 3-IT. Il gatto smarrito ────────────────────────────────────────
    {
        "slug": "beginner-lost-cat",
        "language": "it",
        "difficulty": "beginner",
        "length": "short",
        "title": "Il gatto smarrito",
        "description_en": "A girl searches everywhere for her missing cat.",
        "description_da": "En pige leder overalt efter sin forsvundne kat.",
        "description_it": "Una ragazza cerca ovunque il suo gatto smarrito.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Problem / search",
        "setup_summary": "A girl hunts for her cat and finds it stuck up an apple tree.",
        "body": (
            "Misty è un piccolo gatto bianco con gli occhi blu. Vive con una ragazza di nome Amy. "
            "Un pomeriggio, Amy non riesce a trovare Misty. Guarda sotto il letto, ma Misty non "
            "c'è. Guarda in cucina, ma il gatto non c'è. Amy va fuori e chiama: \"Misty! Dove "
            "sei?\" Chiede al suo amico Tom: \"Hai visto il mio gatto?\" Tom guarda nel suo "
            "giardino. All'improvviso sentono un \"Miao!\" Misty è in cima a un grande melo. Ha "
            "paura di scendere. Tom prende una scala e aiuta il gatto. Amy abbraccia Misty e dice: "
            "\"Grazie, Tom!\""
        ),
        "order": 3,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  BEGINNER — MEDIUM  (200-250 words, 3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 4. The New Student ─────────────────────────────────────────────
    {
        "slug": "beginner-new-student",
        "language": "en",
        "difficulty": "beginner",
        "length": "medium",
        "title": "The New Student",
        "description_en": "A boy from Brazil starts at a new school in London.",
        "description_da": "En dreng fra Brasilien starter på en ny skole i London.",
        "description_it": "Un ragazzo brasiliano inizia in una nuova scuola a Londra.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "New beginning",
        "setup_summary": "A nervous transfer student makes friends through a football game.",
        "body": (
            "Today is Monday. It is a big day for David because he is at a new school. David is from "
            "Brazil, and now he lives in London. He is nervous. He walks into the classroom and sits "
            "at a desk in the back. The teacher, Ms. White, smiles at him. \"Class, this is David,\" "
            "she says.\n\n"
            "At lunchtime, David sits alone. He eats an apple and looks at his book. Then, a girl "
            "walks to his table. Her name is Anna. \"Hello, David! Do you want to play football with "
            "us?\" she asks. David is surprised but happy. \"Yes, please,\" he says. David is good at "
            "football. He runs fast and scores a goal. All the students cheer.\n\n"
            "After the game, David talks to Anna and a boy named Sam. They talk about movies and "
            "music. David's English is not perfect, but he understands them. They use simple words and "
            "speak slowly. When David goes home, his mother asks, \"How was your day?\" David smiles. "
            "\"It was great,\" he says. \"I have two new friends, and we have a game on Friday.\" "
            "David is not nervous anymore. He likes his new school very much."
        ),
        "order": 4,
    },

    # ── 5. A Special Dinner ────────────────────────────────────────────
    {
        "slug": "beginner-special-dinner",
        "language": "en",
        "difficulty": "beginner",
        "length": "medium",
        "title": "A Special Dinner",
        "description_en": "Two siblings prepare a surprise birthday dinner for their mother.",
        "description_da": "To søskende forbereder en overraskelses-fødselsdagsmiddag til deres mor.",
        "description_it": "Due fratelli preparano una cena di compleanno a sorpresa per la mamma.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Celebration / preparation",
        "setup_summary": "A girl and her brother cook a birthday meal and surprise their tired mother.",
        "body": (
            "Today is Maria's mother's birthday. Maria wants to make a special dinner. She goes to "
            "the supermarket in the morning. She buys pasta, tomatoes, onions, and some fresh bread. "
            "She also buys a big chocolate cake.\n\n"
            "At five o'clock, Maria starts to cook. She cuts the onions and puts them in a pan. Then "
            "she adds the tomatoes. The kitchen smells very good. Her brother, Pedro, helps her. He "
            "cleans the table and puts the plates and glasses in the right place. He puts a beautiful "
            "red flower in a vase in the middle of the table.\n\n"
            "At seven o'clock, their mother comes home from work. She is very tired. When she opens "
            "the door, the lights are off. Suddenly, Maria and Pedro shout, \"Surprise! Happy "
            "Birthday!\" They turn on the lights. Their mother is very surprised and she starts to cry "
            "a little because she is happy. They sit down and eat the pasta. \"This is the best "
            "dinner in the world,\" their mother says. After dinner, they eat the chocolate cake and "
            "sing songs. It is a very happy evening for the family."
        ),
        "order": 5,
    },

    # ── 6. The Big Storm ──────────────────────────────────────────────
    {
        "slug": "beginner-big-storm",
        "language": "en",
        "difficulty": "beginner",
        "length": "medium",
        "title": "The Big Storm",
        "description_en": "A family spends a cozy evening together during a power cut.",
        "description_da": "En familie tilbringer en hyggelig aften sammen under en strømafbrydelse.",
        "description_it": "Una famiglia trascorre una serata accogliente insieme durante un blackout.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Unexpected event",
        "setup_summary": "A storm knocks out the power and a family rediscovers simple fun by candlelight.",
        "body": (
            "Last night, there was a big storm in the village. The wind was very loud and the rain hit "
            "the windows. I stayed in the living room with my family. We did not have any electricity, "
            "so the house was dark. My father lit some candles, and we sat on the sofa.\n\n"
            "We could not watch TV or use our computers. At first, my little sister was afraid of the "
            "thunder. It was very loud! But my mother told us a funny story about her childhood. We "
            "laughed and forgot about the storm. We played a board game by candlelight. It was "
            "difficult to see the board, but it was fun.\n\n"
            "In the morning, the storm finished. The sun came out, and the birds started to sing. We "
            "went outside to look at the garden. There were many leaves on the ground, and one small "
            "tree fell down. My father and I worked together to clean the yard. We put the leaves in "
            "bags and fixed the fence. Our neighbors were outside, too. Everyone helped each other. "
            "The storm was scary, but it was also a nice night because we talked and played together "
            "without our phones."
        ),
        "order": 6,
    },

    # ── 4-DA. Den nye elev ─────────────────────────────────────────────
    {
        "slug": "beginner-new-student",
        "language": "da",
        "difficulty": "beginner",
        "length": "medium",
        "title": "Den nye elev",
        "description_en": "A boy from Brazil starts at a new school in London.",
        "description_da": "En dreng fra Brasilien starter på en ny skole i London.",
        "description_it": "Un ragazzo brasiliano inizia in una nuova scuola a Londra.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "New beginning",
        "setup_summary": "A nervous transfer student makes friends through a football game.",
        "body": (
            "I dag er det mandag. Det er en stor dag for David, fordi han er på en ny skole. David "
            "er fra Brasilien, og nu bor han i London. Han er nervøs. Han går ind i klasseværelset "
            "og sætter sig ved et bord bagerst. Læreren, fru White, smiler til ham. \"Klasse, dette "
            "er David,\" siger hun. Til frokost sidder David alene. Han spiser et æble og kigger i "
            "sin bog. Så går en pige hen til hans bord. Hendes navn er Anna. \"Hej, David! Vil du "
            "spille fodbold med os?\" spørger hun. David er overrasket, men glad. \"Ja tak,\" siger "
            "han. David er god til fodbold. Han løber hurtigt og scorer et mål. Alle eleverne jubler. "
            "Efter kampen taler David med Anna og en dreng, der hedder Sam. De taler om film og musik. "
            "Davids engelsk er ikke perfekt, men han forstår dem. De bruger enkle ord og taler "
            "langsomt. Da David kommer hjem, spørger hans mor: \"Hvordan var din dag?\" David smiler. "
            "\"Den var fantastisk,\" siger han. \"Jeg har to nye venner, og vi har en kamp på "
            "fredag.\" David er ikke nervøs mere. Han kan rigtig godt lide sin nye skole."
        ),
        "order": 4,
    },

    # ── 4-IT. Il nuovo studente ────────────────────────────────────────
    {
        "slug": "beginner-new-student",
        "language": "it",
        "difficulty": "beginner",
        "length": "medium",
        "title": "Il nuovo studente",
        "description_en": "A boy from Brazil starts at a new school in London.",
        "description_da": "En dreng fra Brasilien starter på en ny skole i London.",
        "description_it": "Un ragazzo brasiliano inizia in una nuova scuola a Londra.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "New beginning",
        "setup_summary": "A nervous transfer student makes friends through a football game.",
        "body": (
            "Oggi è lunedì. È un grande giorno per David perché è in una nuova scuola. David viene "
            "dal Brasile e ora vive a Londra. È nervoso. Entra in classe e si siede a un banco in "
            "fondo. L'insegnante, la signora White, gli sorride. \"Classe, questo è David\", dice. "
            "A pranzo, David si siede da solo. Mangia una mela e guarda il suo libro. Poi, una "
            "ragazza si avvicina al suo tavolo. Si chiama Anna. \"Ciao, David! Vuoi giocare a calcio "
            "con noi?\" chiede. David è sorpreso ma felice. \"Sì, grazie\", dice. David è bravo a "
            "calcio. Corre veloce e segna un gol. Tutti gli studenti esultano. Dopo la partita, "
            "David parla con Anna e un ragazzo di nome Sam. Parlano di film e musica. L'inglese di "
            "David non è perfetto, ma lui li capisce. Usano parole semplici e parlano lentamente. "
            "Quando David torna a casa, sua madre gli chiede: \"Com'è andata la tua giornata?\" "
            "David sorride. \"È stata fantastica\", dice. \"Ho due nuovi amici e abbiamo una partita "
            "venerdì.\" David non è più nervoso. Gli piace molto la sua nuova scuola."
        ),
        "order": 4,
    },

    # ── 5-DA. En særlig middag ─────────────────────────────────────────
    {
        "slug": "beginner-special-dinner",
        "language": "da",
        "difficulty": "beginner",
        "length": "medium",
        "title": "En særlig middag",
        "description_en": "Two siblings prepare a surprise birthday dinner for their mother.",
        "description_da": "To søskende forbereder en overraskelses-fødselsdagsmiddag til deres mor.",
        "description_it": "Due fratelli preparano una cena di compleanno a sorpresa per la mamma.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Celebration / preparation",
        "setup_summary": "A girl and her brother cook a birthday meal and surprise their tired mother.",
        "body": (
            "I dag er det Marias mors fødselsdag. Maria vil gerne lave en særlig middag. Hun tager i "
            "supermarkedet om morgenen. Hun køber pasta, tomater, løg og noget frisk brød. Hun køber "
            "også en stor chokoladekage. Klokken fem begynder Maria at lave mad. Hun skærer løgene og "
            "lægger dem i en gryde. Så tilføjer hun tomaterne. Køkkenet dufter meget godt. Hendes "
            "bror, Pedro, hjælper hende. Han gør bordet rent og stiller tallerkener og glas på de "
            "rigtige pladser. Han sætter en smuk rød blomst i en vase midt på bordet. Klokken syv "
            "kommer deres mor hjem fra arbejde. Hun er meget træt. Da hun åbner døren, er lyset "
            "slukket. Pludselig råber Maria og Pedro: \"Overraskelse! Tillykke med fødselsdagen!\" "
            "De tænder lyset. Deres mor er meget overrasket, og hun begynder at græde lidt, fordi hun "
            "er glad. De sætter sig ned og spiser pastaen. \"Dette er den bedste middag i verden,\" "
            "siger deres mor. Efter middagen spiser de chokoladekagen og synger sange. Det er en "
            "meget glad aften for familien."
        ),
        "order": 5,
    },

    # ── 5-IT. Una cena speciale ────────────────────────────────────────
    {
        "slug": "beginner-special-dinner",
        "language": "it",
        "difficulty": "beginner",
        "length": "medium",
        "title": "Una cena speciale",
        "description_en": "Two siblings prepare a surprise birthday dinner for their mother.",
        "description_da": "To søskende forbereder en overraskelses-fødselsdagsmiddag til deres mor.",
        "description_it": "Due fratelli preparano una cena di compleanno a sorpresa per la mamma.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Celebration / preparation",
        "setup_summary": "A girl and her brother cook a birthday meal and surprise their tired mother.",
        "body": (
            "Oggi è il compleanno della madre di Maria. Maria vuole preparare una cena speciale. Va "
            "al supermercato la mattina. Compra pasta, pomodori, cipolle e del pane fresco. Compra "
            "anche una grande torta al cioccolato. Alle cinque, Maria inizia a cucinare. Taglia le "
            "cipolle e le mette in una padella. Poi aggiunge i pomodori. La cucina ha un profumo "
            "buonissimo. Suo fratello, Pedro, la aiuta. Pulisce il tavolo e mette i piatti e i "
            "bicchieri al posto giusto. Mette un bel fiore rosso in un vaso al centro del tavolo. "
            "Alle sette, la loro madre torna a casa dal lavoro. È molto stanca. Quando apre la porta, "
            "le luci sono spente. All'improvviso, Maria e Pedro gridano: \"Sorpresa! Buon "
            "compleanno!\" Accendono le luci. La loro madre è molto sorpresa e inizia a piangere un "
            "po' perché è felice. Si siedono e mangiano la pasta. \"Questa è la cena migliore del "
            "mondo\", dice la loro madre. Dopo cena, mangiano la torta al cioccolato e cantano "
            "canzoni. È una serata molto felice per la famiglia."
        ),
        "order": 5,
    },

    # ── 6-DA. Den store storm ──────────────────────────────────────────
    {
        "slug": "beginner-big-storm",
        "language": "da",
        "difficulty": "beginner",
        "length": "medium",
        "title": "Den store storm",
        "description_en": "A family spends a cozy evening together during a power cut.",
        "description_da": "En familie tilbringer en hyggelig aften sammen under en strømafbrydelse.",
        "description_it": "Una famiglia trascorre una serata accogliente insieme durante un blackout.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Unexpected event",
        "setup_summary": "A storm knocks out the power and a family rediscovers simple fun by candlelight.",
        "body": (
            "I nat var der en stor storm i landsbyen. Vinden var meget høj, og regnen ramte vinduerne. "
            "Jeg blev i stuen med min familie. Vi havde ikke noget strøm, så huset var mørkt. Min far "
            "tændte nogle stearinlys, og vi sad på sofaen. Vi kunne ikke se tv eller bruge vores "
            "computere. I starten var min lillesøster bange for tordenen. Det var meget højt! Men min "
            "mor fortalte os en sjov historie om sin barndom. Vi grinte og glemte stormen. Vi spillede "
            "et brætspil ved stearinlysets skær. Det var svært at se brættet, men det var sjovt. Om "
            "morgenen sluttede stormen. Solen kom frem, og fuglene begyndte at synge. Vi gik udenfor "
            "for at se på haven. Der lå mange blade på jorden, og et lille træ var væltet. Min far og "
            "jeg arbejdede sammen for at rydde op i gården. Vi kom bladene i poser og reparerede "
            "hegnet. Vores naboer var også udenfor. Alle hjalp hinanden. Stormen var skræmmende, men "
            "det var også en dejlig nat, fordi vi talte og legede sammen uden vores telefoner."
        ),
        "order": 6,
    },

    # ── 6-IT. La grande tempesta ───────────────────────────────────────
    {
        "slug": "beginner-big-storm",
        "language": "it",
        "difficulty": "beginner",
        "length": "medium",
        "title": "La grande tempesta",
        "description_en": "A family spends a cozy evening together during a power cut.",
        "description_da": "En familie tilbringer en hyggelig aften sammen under en strømafbrydelse.",
        "description_it": "Una famiglia trascorre una serata accogliente insieme durante un blackout.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Unexpected event",
        "setup_summary": "A storm knocks out the power and a family rediscovers simple fun by candlelight.",
        "body": (
            "La scorsa notte c'è stata una grande tempesta nel villaggio. Il vento era molto forte e "
            "la pioggia sbatteva contro le finestre. Sono rimasto in soggiorno con la mia famiglia. "
            "Non avevamo elettricità, quindi la casa era buia. Mio padre ha acceso delle candele e ci "
            "siamo seduti sul divano. Non potevamo guardare la TV o usare i computer. All'inizio, la "
            "mia sorellina aveva paura del tuono. Era molto forte! Ma mia madre ci ha raccontato una "
            "storia divertente sulla sua infanzia. Abbiamo riso e ci siamo dimenticati della tempesta. "
            "Abbiamo fatto un gioco da tavolo a lume di candela. Era difficile vedere il tabellone, "
            "ma è stato divertente. Al mattino, la tempesta è finita. È uscito il sole e gli uccelli "
            "hanno iniziato a cantare. Siamo usciti a guardare il giardino. C'erano molte foglie a "
            "terra e un piccolo albero era caduto. Mio padre e io abbiamo lavorato insieme per pulire "
            "il cortile. Abbiamo messo le foglie nei sacchi e sistemato la recinzione. Anche i nostri "
            "vicini erano fuori. Tutti si sono aiutati a vicenda. La tempesta è stata spaventosa, ma "
            "è stata anche una bella notte perché abbiamo parlato e giocato insieme senza i nostri "
            "telefoni."
        ),
        "order": 6,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  BEGINNER — LONG  (350-450 words, 3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 7. The Travel Adventure ────────────────────────────────────────
    {
        "slug": "beginner-travel-adventure",
        "language": "en",
        "difficulty": "beginner",
        "length": "long",
        "title": "The Travel Adventure",
        "description_en": "A student takes a budget train trip to the Swiss mountains.",
        "description_da": "En studerende tager en billig togtur til de schweiziske bjerge.",
        "description_it": "Uno studente fa un viaggio in treno economico sulle montagne svizzere.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Journey / travel",
        "setup_summary": "A young man hikes a Swiss mountain with strangers and learns travel is about people.",
        "body": (
            "Last summer, Lucas decided to go on a big trip. He wanted to see the mountains in "
            "Switzerland. Lucas is a student, so he does not have a lot of money. He packed a small "
            "bag with his clothes, a map, and a camera. He took the train from his town in Italy.\n\n"
            "The train journey was very long but beautiful. Lucas looked out the window and saw green "
            "fields and small villages. When he arrived in Switzerland, he stayed in a hostel. A "
            "hostel is a cheap hotel for young people. He met two travelers there: Sarah from Canada "
            "and Hiro from Japan. They decided to hike together the next day.\n\n"
            "In the morning, they woke up early. The air was very cold and fresh. They started to "
            "walk up a big mountain called the Rigi. The path was difficult, and Lucas was very tired "
            "after two hours. \"Can we stop?\" he asked. They sat on a rock and ate chocolate and "
            "bread. The view was amazing. They could see a big blue lake below them.\n\n"
            "Suddenly, the weather changed. Small white clouds became big and grey. \"We need to go "
            "back,\" Sarah said. They walked down the mountain quickly. Suddenly, it started to snow! "
            "Lucas was surprised because it was August. Everything became white and very pretty. They "
            "reached the hostel and drank hot chocolate near a fire. Lucas took many photos of the "
            "snow and his new friends. He realized that traveling is not about expensive hotels. It is "
            "about seeing new things and meeting kind people. He wrote a letter to his parents and "
            "said, \"I am having the best time of my life.\""
        ),
        "order": 7,
    },

    # ── 8. The Robot Friend ────────────────────────────────────────────
    {
        "slug": "beginner-robot-friend",
        "language": "en",
        "difficulty": "beginner",
        "length": "long",
        "title": "The Robot Friend",
        "description_en": "In 2050, a boy fights to keep his aging robot companion.",
        "description_da": "I 2050 kæmper en dreng for at beholde sin aldrende robotven.",
        "description_it": "Nel 2050, un ragazzo lotta per tenere il suo vecchio compagno robot.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / friendship",
        "setup_summary": "A boy saves pocket money to buy a new battery for his beloved old robot.",
        "body": (
            "The year is 2050. Many people have robots in their homes. Robots cook, clean, and help "
            "with homework. Toby is ten years old, and he has a special robot named Bip. Bip is "
            "small, silver, and has big green eyes. Bip is not just a machine; he is Toby's best "
            "friend.\n\n"
            "Every morning, Bip wakes Toby up. \"Good morning, Toby. It is 7:30. Time for school,\" "
            "Bip says in a funny voice. After school, they play in the park. Bip can run very fast, "
            "but he always waits for Toby. Sometimes, Bip helps Toby with his math homework. Bip is "
            "very good at numbers!\n\n"
            "One day, Toby was very sad. His favorite toy, a wooden plane, was broken. Toby started "
            "to cry. Bip looked at the plane with his green eyes. \"Do not cry, Toby. I can fix "
            "it,\" Bip said. Bip used his small robot hands to glue the wood. He painted the plane "
            "bright red. When Toby saw the fixed toy, he smiled and hugged the robot.\n\n"
            "\"You are a great friend, Bip,\" Toby said. Bip's lights flickered. This was how Bip "
            "showed he was happy. But Bip had a problem. His battery was old. Sometimes, he stopped "
            "moving in the middle of a game. Toby's father said, \"We need to buy a new robot, Toby. "
            "Bip is old.\"\n\n"
            "Toby was very upset. \"No! I don't want a new robot. I love Bip!\" Toby saved his "
            "pocket money for three months. He went to a special shop and bought a new battery for "
            "Bip. Toby and his father put the new battery inside the robot. Bip opened his eyes and "
            "looked at Toby. \"Hello, Toby. Do you want to play?\" Bip asked. Toby was very happy. "
            "He knew that technology can change, but friendship is important forever."
        ),
        "order": 8,
    },

    # ── 9. The Library Mystery ─────────────────────────────────────────
    {
        "slug": "beginner-library-mystery",
        "language": "en",
        "difficulty": "beginner",
        "length": "long",
        "title": "The Library Mystery",
        "description_en": "A librarian follows clues from a mysterious blue book.",
        "description_da": "En bibliotekar følger spor fra en mystisk blå bog.",
        "description_it": "Un bibliotecario segue gli indizi di un misterioso libro blu.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Mystery / discovery",
        "setup_summary": "A librarian finds a magic book that leads him to a secret garden room.",
        "body": (
            "Mr. Miller is a librarian. He works in a very old library with thousands of books. He "
            "loves his job because it is quiet and peaceful. He knows where every book is. He has "
            "books about history, science, and magic.\n\n"
            "One Tuesday, Mr. Miller found something strange. On his desk, there was a small blue "
            "book. The book did not have a title or a name. He opened it, but the pages were empty. "
            "\"This is very strange,\" Mr. Miller thought. He put the book on a shelf and went "
            "home.\n\n"
            "The next day, he opened the blue book again. Now, there was one sentence on the first "
            "page: \"Go to the history section.\" Mr. Miller was surprised. He walked to the history "
            "section. On the floor, he found an old silver key. He went back to the blue book. A new "
            "sentence appeared: \"Find the red door.\"\n\n"
            "Mr. Miller lived in the library for twenty years, but he did not know about a red door. "
            "He looked behind the shelves and under the stairs. Finally, behind a big curtain in the "
            "basement, he saw a small red door. He used the silver key to open it.\n\n"
            "Inside the room, there were no books. There was only a large, comfortable chair and a "
            "window that looked at a secret garden. In the garden, there were colorful birds and "
            "beautiful flowers that he never saw before. On a small table, there was a note: \"For "
            "the man who loves books. Here is a quiet place for you to read.\"\n\n"
            "Mr. Miller smiled. He sat in the chair and looked at the garden. Every day after work, "
            "he went to his secret room. He finally had a place where he didn't have to work. He "
            "could just sit, relax, and read his favorite stories in peace. He never told anyone "
            "about the red door or the magic blue book. It was his beautiful secret."
        ),
        "order": 9,
    },

    # ── 7-DA. Rejseeventyret ──────────────────────────────────────────
    {
        "slug": "beginner-travel-adventure",
        "language": "da",
        "difficulty": "beginner",
        "length": "long",
        "title": "Rejseeventyret",
        "description_en": "A student takes a budget train trip to the Swiss mountains.",
        "description_da": "En studerende tager en billig togtur til de schweiziske bjerge.",
        "description_it": "Uno studente fa un viaggio in treno economico verso le montagne svizzere.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Travel / coming-of-age",
        "setup_summary": "A broke student hikes a Swiss mountain, gets caught in snow, and finds joy in simplicity.",
        "body": (
            "Sidste sommer besluttede Lucas at tage på en stor rejse. Han ville se bjergene i "
            "Schweiz. Lucas er studerende, så han har ikke mange penge. Han pakkede en lille taske "
            "med sit tøj, et kort og et kamera. Han tog toget fra sin by i Italien. Togrejsen var "
            "meget lang, men smuk. Lucas kiggede ud ad vinduet og så grønne marker og små landsbyer. "
            "Da han ankom til Schweiz, boede han på et hostel. Et hostel er et billigt hotel for unge "
            "mennesker. Han mødte to rejsende der: Sarah fra Canada og Hiro fra Japan. De besluttede "
            "at vandre sammen næste dag. Om morgenen vågnede de tidligt. Luften var meget kold og "
            "frisk. De begyndte at gå op ad et stort bjerg, der hedder Rigi. Stien var svær, og "
            "Lucas var meget træt efter to timer. \"Kan vi stoppe?\" spurgte han. De sad på en sten "
            "og spiste chokolade og brød. Udsigten var fantastisk. De kunne se en stor blå sø under "
            "sig. Pludselig ændrede vejret sig. Små hvide skyer blev store og grå. \"Vi er nødt til "
            "at gå tilbage,\" sagde Sarah. De gik hurtigt ned ad bjerget. Pludselig begyndte det at "
            "sne! Lucas var overrasket, for det var august. Alt blev hvidt og meget smukt. De nåede "
            "vandrerhjemmet og drak varm chokolade nær en pejs. Lucas tog mange billeder af sneen og "
            "sine nye venner. Han indså, at det at rejse ikke handler om dyre hoteller. Det handler "
            "om at se nye ting og møde venlige mennesker. Han skrev et brev til sine forældre og "
            "sagde: \"Jeg har mit livs bedste tid.\""
        ),
        "order": 7,
    },

    # ── 7-IT. L'avventura di viaggio ──────────────────────────────────
    {
        "slug": "beginner-travel-adventure",
        "language": "it",
        "difficulty": "beginner",
        "length": "long",
        "title": "L'avventura di viaggio",
        "description_en": "A student takes a budget train trip to the Swiss mountains.",
        "description_da": "En studerende tager en billig togtur til de schweiziske bjerge.",
        "description_it": "Uno studente fa un viaggio in treno economico verso le montagne svizzere.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Travel / coming-of-age",
        "setup_summary": "A broke student hikes a Swiss mountain, gets caught in snow, and finds joy in simplicity.",
        "body": (
            "L'estate scorsa, Lucas ha deciso di fare un grande viaggio. Voleva vedere le montagne "
            "in Svizzera. Lucas è uno studente, quindi non ha molti soldi. Ha preparato una piccola "
            "borsa con i suoi vestiti, una mappa e una macchina fotografica. Ha preso il treno dalla "
            "sua città in Italia. Il viaggio in treno è stato molto lungo ma bellissimo. Lucas ha "
            "guardato fuori dal finestrino e ha visto campi verdi e piccoli villaggi. Quando è "
            "arrivato in Svizzera, ha alloggiato in un ostello. Un ostello è un hotel economico per "
            "giovani. Lì ha incontrato due viaggiatori: Sarah dal Canada e Hiro dal Giappone. Hanno "
            "deciso di fare un'escursione insieme il giorno successivo. Al mattino, si sono svegliati "
            "presto. L'aria era molto fredda e fresca. Hanno iniziato a salire su una grande montagna "
            "chiamata Rigi. Il sentiero era difficile e Lucas era molto stanco dopo due ore. "
            "\"Possiamo fermarci?\" ha chiesto. Si sono seduti su una roccia e hanno mangiato "
            "cioccolato e pane. La vista era incredibile. Potevano vedere un grande lago blu sotto di "
            "loro. All'improvviso, il tempo è cambiato. Piccole nuvole bianche sono diventate grandi "
            "e grigie. \"Dobbiamo tornare indietro\", ha detto Sarah. Sono scesi velocemente dalla "
            "montagna. All'improvviso, ha iniziato a nevicare! Lucas era sorpreso perché era agosto. "
            "Tutto è diventato bianco e molto bello. Hanno raggiunto l'ostello e hanno bevuto "
            "cioccolata calda vicino al fuoco. Lucas ha scattato molte foto della neve e dei suoi "
            "nuovi amici. Ha capito che viaggiare non riguarda hotel costosi. Riguarda vedere cose "
            "nuove e incontrare persone gentili. Ha scritto una lettera ai suoi genitori dicendo: "
            "\"Sto passando il momento migliore della mia vita.\""
        ),
        "order": 7,
    },

    # ── 8-DA. Robotvennen ─────────────────────────────────────────────
    {
        "slug": "beginner-robot-friend",
        "language": "da",
        "difficulty": "beginner",
        "length": "long",
        "title": "Robotvennen",
        "description_en": "In 2050 a boy saves his beloved robot's battery — and their friendship.",
        "description_da": "I 2050 redder en dreng sin elskede robots batteri — og deres venskab.",
        "description_it": "Nel 2050 un ragazzo salva la batteria del suo amato robot — e la loro amicizia.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / friendship",
        "setup_summary": "A boy in 2050 saves up to replace his ageing robot friend's battery.",
        "body": (
            "Året er 2050. Mange mennesker har robotter i deres hjem. Robotter laver mad, gør rent "
            "og hjælper med lektier. Toby er ti år gammel, og han har en særlig robot, der hedder "
            "Bip. Bip er lille, sølvfarvet og har store grønne øjne. Bip er ikke bare en maskine; "
            "han er Tobys bedste ven. Hver morgen vækker Bip Toby. \"Godmorgen, Toby. Klokken er "
            "7:30. Det er tid til skole,\" siger Bip med en sjov stemme. Efter skole leger de i "
            "parken. Bip kan løbe meget hurtigt, men han venter altid på Toby. Nogle gange hjælper "
            "Bip Toby med hans matematiklektier. Bip er meget god til tal! En dag var Toby meget "
            "trist. Hans yndlingslegetøj, et træfly, var i stykker. Toby begyndte at græde. Bip "
            "kiggede på flyet med sine grønne øjne. \"Græd ikke, Toby. Jeg kan ordne det,\" sagde "
            "Bip. Bip brugte sine små robothænder til at lime træet. Han malede flyet knaldrødt. Da "
            "Toby så det reparerede legetøj, smilede han og krammede robotten. \"Du er en fantastisk "
            "ven, Bip,\" sagde Toby. Bips lys blinkede. Det var sådan, Bip viste, at han var glad. "
            "Men Bip havde et problem. Hans batteri var gammelt. Nogle gange stoppede han med at "
            "bevæge sig midt i en leg. Tobys far sagde: \"Vi er nødt til at købe en ny robot, Toby. "
            "Bip er gammel.\" Toby blev meget ked af det. \"Nej! Jeg vil ikke have en ny robot. Jeg "
            "elsker Bip!\" Toby sparede sine lommepenge op i tre måneder. Han gik til en specialbutik "
            "og købte et nyt batteri til Bip. Toby og hans far satte det nye batteri ind i robotten. "
            "Bip åbnede øjnene og kiggede på Toby. \"Hej, Toby. Vil du lege?\" spurgte Bip. Toby "
            "var meget glad. Han vidste, at teknologi kan ændre sig, men venskab er vigtigt for evigt."
        ),
        "order": 8,
    },

    # ── 8-IT. L'amico robot ───────────────────────────────────────────
    {
        "slug": "beginner-robot-friend",
        "language": "it",
        "difficulty": "beginner",
        "length": "long",
        "title": "L'amico robot",
        "description_en": "In 2050 a boy saves his beloved robot's battery — and their friendship.",
        "description_da": "I 2050 redder en dreng sin elskede robots batteri — og deres venskab.",
        "description_it": "Nel 2050 un ragazzo salva la batteria del suo amato robot — e la loro amicizia.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / friendship",
        "setup_summary": "A boy in 2050 saves up to replace his ageing robot friend's battery.",
        "body": (
            "L'anno è il 2050. Molte persone hanno robot nelle loro case. I robot cucinano, puliscono "
            "e aiutano con i compiti. Toby ha dieci anni e ha un robot speciale di nome Bip. Bip è "
            "piccolo, argentato e ha grandi occhi verdi. Bip non è solo una macchina; è il migliore "
            "amico di Toby. Ogni mattina, Bip sveglia Toby. \"Buongiorno, Toby. Sono le 7:30. È ora "
            "di andare a scuola,\" dice Bip con una voce buffa. Dopo la scuola, giocano nel parco. "
            "Bip può correre molto veloce, ma aspetta sempre Toby. A volte, Bip aiuta Toby con i "
            "compiti di matematica. Bip è molto bravo con i numeri! Un giorno, Toby era molto triste. "
            "Il suo giocattolo preferito, un aereo di legno, era rotto. Toby ha iniziato a piangere. "
            "Bip ha guardato l'aereo con i suoi occhi verdi. \"Non piangere, Toby. Posso aggiustarlo,\" "
            "ha detto Bip. Bip ha usato le sue piccole mani da robot per incollare il legno. Ha "
            "dipinto l'aereo di un rosso acceso. Quando Toby ha visto il giocattolo riparato, ha "
            "sorriso e ha abbracciato il robot. \"Sei un grande amico, Bip,\" ha detto Toby. Le luci "
            "di Bip hanno tremolato. Questo era il modo in cui Bip mostrava di essere felice. Ma Bip "
            "aveva un problema. La sua batteria era vecchia. A volte, smetteva di muoversi nel bel "
            "mezzo di un gioco. Il padre di Toby ha detto: \"Dobbiamo comprare un nuovo robot, Toby. "
            "Bip è vecchio.\" Toby era molto turbato. \"No! Non voglio un nuovo robot. Voglio bene a "
            "Bip!\" Toby ha risparmiato la sua paghetta per tre mesi. È andato in un negozio speciale "
            "e ha comprato una nuova batteria per Bip. Toby e suo padre hanno messo la nuova batteria "
            "dentro il robot. Bip ha aperto gli occhi e ha guardato Toby. \"Ciao, Toby. Vuoi "
            "giocare?\" ha chiesto Bip. Toby era molto felice. Sapeva che la tecnologia può cambiare, "
            "ma l'amicizia è importante per sempre."
        ),
        "order": 8,
    },

    # ── 9-DA. Biblioteksmysteriet ─────────────────────────────────────
    {
        "slug": "beginner-library-mystery",
        "language": "da",
        "difficulty": "beginner",
        "length": "long",
        "title": "Biblioteksmysteriet",
        "description_en": "A librarian discovers a magic book that leads to a secret garden room.",
        "description_da": "En bibliotekar opdager en magisk bog, der fører til et hemmeligt haverum.",
        "description_it": "Un bibliotecario scopre un libro magico che conduce a una stanza con giardino segreto.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Mystery / discovery",
        "setup_summary": "A librarian follows clues from a blank blue book and finds a hidden reading garden.",
        "body": (
            "Hr. Miller er bibliotekar. Han arbejder på et meget gammelt bibliotek med tusindvis af "
            "bøger. Han elsker sit job, fordi det er stille og fredeligt. Han ved, hvor hver eneste "
            "bog er. Han har bøger om historie, videnskab og magi. En tirsdag fandt hr. Miller noget "
            "mærkeligt. På hans skrivebord lå der en lille blå bog. Bogen havde hverken en titel "
            "eller et navn. Han åbnede den, men siderne var tomme. \"Det er meget mærkeligt,\" tænkte "
            "hr. Miller. Han lagde bogen på en hylde og gik hjem. Næste dag åbnede han den blå bog "
            "igen. Nu stod der én sætning på den første side: \"Gå til historieafdelingen.\" Hr. "
            "Miller var overrasket. Han gik til historieafdelingen. På gulvet fandt han en gammel "
            "sølvnøgle. Han gik tilbage til den blå bog. En ny sætning kom frem: \"Find den røde "
            "dør.\" Hr. Miller havde boet på biblioteket i tyve år, men han kendte ikke til en rød "
            "dør. Han kiggede bag hylderne og under trappen. Endelig, bag et stort gardin i kælderen, "
            "så han en lille rød dør. Han brugte sølvnøglen til at åbne den. Inde i rummet var der "
            "ingen bøger. Der var kun en stor, behagelig stol og et vindue, der kiggede ud på en "
            "hemmelig have. I haven var der farverige fugle og smukke blomster, som han aldrig havde "
            "set før. På et lille bord lå der en seddel: \"Til manden der elsker bøger. Her er et "
            "stille sted, hvor du kan læse.\" Hr. Miller smilede. Han satte sig i stolen og kiggede "
            "på haven. Hver dag efter arbejde gik han til sit hemmelige rum. Han havde endelig et "
            "sted, hvor han ikke behøvede at arbejde. Han kunne bare sidde, slappe af og læse sine "
            "yndlingshistorier i fred. Han fortalte aldrig nogen om den røde dør eller den magiske "
            "blå bog. Det var hans smukke hemmelighed."
        ),
        "order": 9,
    },

    # ── 9-IT. Il mistero della biblioteca ──────────────────────────────
    {
        "slug": "beginner-library-mystery",
        "language": "it",
        "difficulty": "beginner",
        "length": "long",
        "title": "Il mistero della biblioteca",
        "description_en": "A librarian discovers a magic book that leads to a secret garden room.",
        "description_da": "En bibliotekar opdager en magisk bog, der fører til et hemmeligt haverum.",
        "description_it": "Un bibliotecario scopre un libro magico che conduce a una stanza con giardino segreto.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Mystery / discovery",
        "setup_summary": "A librarian follows clues from a blank blue book and finds a hidden reading garden.",
        "body": (
            "Il signor Miller è un bibliotecario. Lavora in una biblioteca molto vecchia con migliaia "
            "di libri. Ama il suo lavoro perché è tranquillo e pacifico. Sa dove si trova ogni libro. "
            "Ha libri di storia, scienza e magia. Un martedì, il signor Miller ha trovato qualcosa di "
            "strano. Sulla sua scrivania, c'era un piccolo libro blu. Il libro non aveva un titolo o "
            "un nome. Lo ha aperto, ma le pagine erano vuote. \"Questo è molto strano,\" ha pensato "
            "il signor Miller. Ha messo il libro su uno scaffale ed è tornato a casa. Il giorno dopo, "
            "ha aperto di nuovo il libro blu. Ora, c'era una frase sulla prima pagina: \"Vai alla "
            "sezione di storia.\" Il signor Miller era sorpreso. È andato alla sezione di storia. Sul "
            "pavimento, ha trovato una vecchia chiave d'argento. È tornato al libro blu. È apparsa "
            "una nuova frase: \"Trova la porta rossa.\" Il signor Miller ha vissuto nella biblioteca "
            "per vent'anni, ma non sapeva di una porta rossa. Ha guardato dietro gli scaffali e sotto "
            "le scale. Alla fine, dietro una grande tenda nel seminterrato, ha visto una piccola "
            "porta rossa. Ha usato la chiave d'argento per aprirla. Dentro la stanza, non c'erano "
            "libri. C'era solo una grande sedia comoda e una finestra che si affacciava su un "
            "giardino segreto. Nel giardino c'erano uccelli colorati e bellissimi fiori che non aveva "
            "mai visto prima. Su un tavolino c'era un biglietto: \"Per l'uomo che ama i libri. Ecco "
            "un posto tranquillo dove puoi leggere.\" Il signor Miller ha sorriso. Si è seduto sulla "
            "sedia e ha guardato il giardino. Ogni giorno, dopo il lavoro, andava nella sua stanza "
            "segreta. Finalmente aveva un posto in cui non doveva lavorare. Poteva semplicemente "
            "sedersi, rilassarsi e leggere le sue storie preferite in pace. Non ha mai detto a "
            "nessuno della porta rossa o del libro magico blu. Era il suo bellissimo segreto."
        ),
        "order": 9,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  INTERMEDIATE — SHORT  (3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 1. The Unexpected Invitation ───────────────────────────────────
    {
        "slug": "intermediate-unexpected-invitation",
        "language": "en",
        "difficulty": "intermediate",
        "length": "short",
        "title": "The Unexpected Invitation",
        "description_en": "A mysterious envelope leads to a dinner party with dark secrets.",
        "description_da": "En mystisk kuvert fører til et middagsselskab med mørke hemmeligheder.",
        "description_it": "Una busta misteriosa porta a una cena con oscuri segreti.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Mystery / suspense",
        "setup_summary": "A woman receives an anonymous invitation to a mansion where guests must reveal secrets.",
        "body": (
            "When Clara opened her mailbox on a Tuesday afternoon, she didn't expect to find a thick, "
            "cream-colored envelope. There was no return address, only her name written in elegant, "
            "flowing calligraphy. Inside, she found an invitation to a dinner party at Blackwood "
            "Manor, an old house on the edge of town that had been empty for decades.\n\n"
            "Although she was hesitant, her curiosity was stronger than her fear. That evening, she "
            "dressed in her best clothes and drove up the winding path to the house. To her surprise, "
            "the front door was already open. The hallway was lit by dozens of candles, and the smell "
            "of expensive perfume and roasted meat filled the air.\n\n"
            "As she entered the dining room, she saw five other guests. They all looked just as "
            "confused as she was. \"Do any of you know who invited us?\" Clara asked. Before anyone "
            "could answer, a tall man in a tuxedo appeared at the head of the table. \"I am glad you "
            "all came,\" he said with a mysterious smile. \"You are here because each of you has a "
            "secret, and tonight, we are going to play a game to see whose secret is the most "
            "dangerous.\" Clara felt a chill run down her spine. She realized this was not going to "
            "be an ordinary dinner."
        ),
        "order": 1,
    },

    # ── 2. The Mirror's Reflection ─────────────────────────────────────
    {
        "slug": "intermediate-mirrors-reflection",
        "language": "en",
        "difficulty": "intermediate",
        "length": "short",
        "title": "The Mirror's Reflection",
        "description_en": "A man's reflection stops copying him — and starts warning him.",
        "description_da": "En mands spejlbillede holder op med at kopiere ham — og begynder at advare ham.",
        "description_it": "Il riflesso di un uomo smette di copiarlo — e inizia ad avvertirlo.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Supernatural / thriller",
        "setup_summary": "A man discovers his mirror reflection moves independently and warns him of danger outside.",
        "body": (
            "David had always been a man of habit. Every morning, he woke up at 6:00 AM, shaved, "
            "drank a cup of black coffee, and left for his office. However, one rainy Wednesday, "
            "something changed. As he was brushing his teeth, he looked into the bathroom mirror and "
            "froze. His reflection wasn't moving.\n\n"
            "The \"Mirror David\" was standing perfectly still, staring back at him with a cold, "
            "intense expression. David dropped his toothbrush in shock. He waved his hand, but the "
            "reflection stayed motionless. Then, slowly, the reflection began to move on its own. It "
            "didn't mimic David; instead, it reached out and touched the glass from the inside.\n\n"
            "\"What do you want?\" David whispered, his heart pounding in his chest. The reflection "
            "didn't speak, but it pointed toward the window. Outside, a dark figure was standing in "
            "the rain, watching David's house. The reflection tapped the glass urgently, as if it "
            "were trying to warn him. David realized that his reflection wasn't a copy—it was a "
            "protector. He backed away from the mirror, grabbed his coat, and realized that the life "
            "he thought was boring and safe was actually in great danger. He had to decide whether to "
            "trust the man in the mirror or the man in the rain."
        ),
        "order": 2,
    },

    # ── 3. The Silent Piano ────────────────────────────────────────────
    {
        "slug": "intermediate-silent-piano",
        "language": "en",
        "difficulty": "intermediate",
        "length": "short",
        "title": "The Silent Piano",
        "description_en": "A deaf musician plays a forgotten piano by feeling the vibrations.",
        "description_da": "En døv musiker spiller et glemt klaver ved at mærke vibrationerne.",
        "description_it": "Un musicista sordo suona un pianoforte dimenticato sentendo le vibrazioni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Human interest / art",
        "setup_summary": "A young man who lost his hearing plays Chopin on a neglected piano using only vibrations.",
        "body": (
            "In the corner of the local community center sat an old grand piano. Its wood was "
            "scratched, and many of the keys were stuck. Nobody ever played it, and most people "
            "treated it like a piece of useless furniture. However, a young man named Julian saw it "
            "differently. Julian was a talented musician who had lost his hearing in an accident a "
            "year ago.\n\n"
            "One evening, when the center was quiet, Julian sat at the bench. He couldn't hear the "
            "notes, but he remembered how they felt. He placed his hands on the keys and began to "
            "play a complex piece by Chopin. He didn't use his ears; he used the vibrations that "
            "traveled through the floor and into his body.\n\n"
            "A woman working late in the office stopped what she was doing. She was amazed by the "
            "beautiful, haunting melody filling the hall. She walked to the doorway and watched "
            "Julian. He was playing with such passion that his eyes were closed, and his whole body "
            "swayed with the rhythm. When he finished, the room returned to silence. The woman "
            "started to clap, but Julian didn't turn around. He simply rested his hands on the wood, "
            "feeling the last of the vibrations fade away. He didn't need to hear the music to know "
            "it was perfect; he had felt every note in his soul."
        ),
        "order": 3,
    },

    # ── 1-DA. Den uventede invitation ──────────────────────────────────
    {
        "slug": "intermediate-unexpected-invitation",
        "language": "da",
        "difficulty": "intermediate",
        "length": "short",
        "title": "Den uventede invitation",
        "description_en": "A mysterious envelope leads to a dinner party with dark secrets.",
        "description_da": "En mystisk kuvert fører til et middagsselskab med mørke hemmeligheder.",
        "description_it": "Una busta misteriosa porta a una cena con oscuri segreti.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Mystery / suspense",
        "setup_summary": "A woman receives an anonymous invitation to a mansion where guests must reveal secrets.",
        "body": (
            "Da Clara åbnede sin postkasse en tirsdag eftermiddag, forventede hun ikke at finde en "
            "tyk, cremefarvet kuvert. Der var ingen afsenderadresse, kun hendes navn skrevet med "
            "elegant, flydende kalligrafi. Indeni fandt hun en invitation til et middagsselskab på "
            "Blackwood Manor, et gammelt hus i udkanten af byen, der havde stået tomt i årtier. "
            "Selvom hun var tøvende, var hendes nysgerrighed stærkere end hendes frygt. Den aften "
            "tog hun sit pæneste tøj på og kørte op ad den snoede sti til huset. Til hendes "
            "overraskelse stod hoveddøren allerede åben. Hallen var oplyst af snesevis af "
            "stearinlys, og duften af dyr parfume og stegt kød fyldte luften. Da hun trådte ind i "
            "spisestuen, så hun fem andre gæster. De så alle lige så forvirrede ud, som hun var. "
            "\"Er der nogen af jer, der ved, hvem der har inviteret os?\" spurgte Clara. Før nogen "
            "kunne svare, dukkede en høj mand i smoking op for bordenden. \"Jeg er glad for, at I "
            "alle kom,\" sagde han med et mystisk smil. \"I er her, fordi I hver især har en "
            "hemmelighed, og i aften skal vi spille et spil for at se, hvis hemmelighed der er den "
            "farligste.\" Clara mærkede en kulden løbe ned ad ryggen. Hun indså, at dette ikke "
            "ville blive en almindelig middag."
        ),
        "order": 1,
    },

    # ── 1-IT. L'invito inaspettato ─────────────────────────────────────
    {
        "slug": "intermediate-unexpected-invitation",
        "language": "it",
        "difficulty": "intermediate",
        "length": "short",
        "title": "L'invito inaspettato",
        "description_en": "A mysterious envelope leads to a dinner party with dark secrets.",
        "description_da": "En mystisk kuvert fører til et middagsselskab med mørke hemmeligheder.",
        "description_it": "Una busta misteriosa porta a una cena con oscuri segreti.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Mystery / suspense",
        "setup_summary": "A woman receives an anonymous invitation to a mansion where guests must reveal secrets.",
        "body": (
            "Quando Clara aprì la cassetta della posta un martedì pomeriggio, non si aspettava di "
            "trovare una spessa busta color crema. Non c'era il mittente, solo il suo nome scritto "
            "con un'elegante calligrafia fluida. All'interno trovò un invito a una cena a Blackwood "
            "Manor, una vecchia casa alla periferia della città rimasta vuota per decenni. Sebbene "
            "fosse esitante, la sua curiosità era più forte della sua paura. Quella sera, indossò i "
            "suoi vestiti migliori e guidò lungo il sentiero tortuoso fino alla casa. Con sua "
            "sorpresa, la porta d'ingresso era già aperta. Il corridoio era illuminato da dozzine "
            "di candele, e il profumo di un profumo costoso e di carne arrosto riempiva l'aria. "
            "Entrando nella sala da pranzo, vide altri cinque ospiti. Sembravano tutti confusi "
            "quanto lei. \"Qualcuno di voi sa chi ci ha invitati?\" chiese Clara. Prima che "
            "chiunque potesse rispondere, un uomo alto in smoking apparve a capotavola. \"Sono "
            "felice che siate venuti tutti,\" disse con un sorriso misterioso. \"Siete qui perché "
            "ognuno di voi ha un segreto, e stasera faremo un gioco per vedere quale segreto è il "
            "più pericoloso.\" Clara sentì un brivido correrle lungo la schiena. Capì che quella "
            "non sarebbe stata una cena ordinaria."
        ),
        "order": 1,
    },

    # ── 2-DA. Spejlets refleksion ──────────────────────────────────────
    {
        "slug": "intermediate-mirrors-reflection",
        "language": "da",
        "difficulty": "intermediate",
        "length": "short",
        "title": "Spejlets refleksion",
        "description_en": "A man's reflection stops copying him — and starts warning him.",
        "description_da": "En mands spejlbillede holder op med at kopiere ham — og begynder at advare ham.",
        "description_it": "Il riflesso di un uomo smette di copiarlo — e inizia ad avvertirlo.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Supernatural / thriller",
        "setup_summary": "A man discovers his mirror reflection moves independently and warns him of danger outside.",
        "body": (
            "David havde altid været en vanemenneske. Hver morgen vågnede han kl. 6:00, barberede "
            "sig, drak en kop sort kaffe og tog af sted til sit kontor. Men en regnfuld onsdag "
            "ændrede noget sig. Mens han børstede tænder, kiggede han ind i badeværelsesspejlet og "
            "frøs fast. Hans refleksion bevægede sig ikke. \"Spejl-David\" stod helt stille og "
            "stirrede tilbage på ham med et koldt, intenst udtryk. David tabte sin tandbørste i "
            "chok. Han vinkede med hånden, men refleksionen forblev ubevægelig. Så begyndte "
            "refleksionen langsomt at bevæge sig af sig selv. Den efterlignede ikke David; i stedet "
            "rakte den ud og rørte ved glasset indefra. \"Hvad vil du?\" hviskede David med hjertet "
            "hamrende i brystet. Refleksionen talte ikke, men pegede mod vinduet. Udenfor stod en "
            "mørk skikkelse i regnen og holdt øje med Davids hus. Refleksionen bankede insisterende "
            "på glasset, som om den forsøgte at advare ham. David indså, at hans refleksion ikke var "
            "en kopi \u2013 det var en beskytter. Han bakkede væk fra spejlet, greb sin frakke og "
            "indså, at det liv, han troede var kedeligt og sikkert, faktisk var i stor fare. Han "
            "måtte beslutte, om han ville stole på manden i spejlet eller manden i regnen."
        ),
        "order": 2,
    },

    # ── 2-IT. Il riflesso dello specchio ───────────────────────────────
    {
        "slug": "intermediate-mirrors-reflection",
        "language": "it",
        "difficulty": "intermediate",
        "length": "short",
        "title": "Il riflesso dello specchio",
        "description_en": "A man's reflection stops copying him — and starts warning him.",
        "description_da": "En mands spejlbillede holder op med at kopiere ham — og begynder at advare ham.",
        "description_it": "Il riflesso di un uomo smette di copiarlo — e inizia ad avvertirlo.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Supernatural / thriller",
        "setup_summary": "A man discovers his mirror reflection moves independently and warns him of danger outside.",
        "body": (
            "David era sempre stato un uomo abitudinario. Ogni mattina si svegliava alle 6:00, si "
            "radeva, beveva una tazza di caffè nero e usciva per andare in ufficio. Tuttavia, un "
            "piovoso mercoledì, qualcosa cambiò. Mentre si lavava i denti, si guardò allo specchio "
            "del bagno e si bloccò. Il suo riflesso non si muoveva. Il \"David dello specchio\" "
            "stava perfettamente immobile, fissandolo con un'espressione fredda e intensa. David "
            "fece cadere lo spazzolino per lo shock. Agitò la mano, ma il riflesso rimase immobile. "
            "Poi, lentamente, il riflesso iniziò a muoversi da solo. Non imitava David; invece, "
            "allungò la mano e toccò il vetro dall'interno. \"Cosa vuoi?\" sussurrò David, con il "
            "cuore che gli batteva forte nel petto. Il riflesso non parlò, ma indicò verso la "
            "finestra. Fuori, una figura scura stava in piedi sotto la pioggia, osservando la casa "
            "di David. Il riflesso batté urgentemente sul vetro, come se cercasse di avvertirlo. "
            "David capì che il suo riflesso non era una copia: era un protettore. Si allontanò "
            "dallo specchio, afferrò il cappotto e si rese conto che la vita che pensava fosse "
            "noiosa e sicura era in realtà in grave pericolo. Doveva decidere se fidarsi dell'uomo "
            "nello specchio o dell'uomo sotto la pioggia."
        ),
        "order": 2,
    },

    # ── 3-DA. Det tavse klaver ─────────────────────────────────────────
    {
        "slug": "intermediate-silent-piano",
        "language": "da",
        "difficulty": "intermediate",
        "length": "short",
        "title": "Det tavse klaver",
        "description_en": "A deaf musician plays a forgotten piano by feeling the vibrations.",
        "description_da": "En døv musiker spiller et glemt klaver ved at mærke vibrationerne.",
        "description_it": "Un musicista sordo suona un pianoforte dimenticato sentendo le vibrazioni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Human interest / art",
        "setup_summary": "A young man who lost his hearing plays Chopin on a neglected piano using only vibrations.",
        "body": (
            "I hjørnet af det lokale forsamlingshus stod et gammelt flygel. Dets træ var ridset, og "
            "mange af tangenterne sad fast. Ingen spillede nogensinde på det, og de fleste "
            "behandlede det som et ubrugeligt møbel. En ung mand ved navn Julian så det dog "
            "anderledes. Julian var en talentfuld musiker, som havde mistet hørelsen i en ulykke for "
            "et år siden. En aften, da huset var stille, satte Julian sig på bænken. Han kunne ikke "
            "høre tonerne, men han huskede, hvordan de føltes. Han lagde hænderne på tangenterne og "
            "begyndte at spille et komplekst stykke af Chopin. Han brugte ikke ørerne; han brugte "
            "de vibrationer, der rejste gennem gulvet og ind i hans krop. En kvinde, der arbejdede "
            "sent på kontoret, stoppede med det, hun lavede. Hun var forbløffet over den smukke, "
            "betagende melodi, der fyldte salen. Hun gik hen til døråbningen og betragtede Julian. "
            "Han spillede med en sådan passion, at hans øjne var lukkede, og hele hans krop svajede "
            "med rytmen. Da han var færdig, vendte rummet tilbage til stilheden. Kvinden begyndte at "
            "klappe, men Julian vendte sig ikke om. Han hvilede blot hænderne på træet og mærkede "
            "de sidste vibrationer forsvinde. Han behøvede ikke at høre musikken for at vide, at "
            "den var perfekt; han havde mærket hver eneste tone i sin sjæl."
        ),
        "order": 3,
    },

    # ── 3-IT. Il pianoforte silenzioso ─────────────────────────────────
    {
        "slug": "intermediate-silent-piano",
        "language": "it",
        "difficulty": "intermediate",
        "length": "short",
        "title": "Il pianoforte silenzioso",
        "description_en": "A deaf musician plays a forgotten piano by feeling the vibrations.",
        "description_da": "En døv musiker spiller et glemt klaver ved at mærke vibrationerne.",
        "description_it": "Un musicista sordo suona un pianoforte dimenticato sentendo le vibrazioni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Human interest / art",
        "setup_summary": "A young man who lost his hearing plays Chopin on a neglected piano using only vibrations.",
        "body": (
            "Nell'angolo del centro comunitario locale c'era un vecchio pianoforte a coda. Il legno "
            "era graffiato e molti dei tasti erano bloccati. Nessuno lo suonava mai, e la maggior "
            "parte delle persone lo trattava come un mobile inutile. Tuttavia, un giovane di nome "
            "Julian la vedeva diversamente. Julian era un musicista di talento che aveva perso "
            "l'udito in un incidente un anno fa. Una sera, quando il centro era silenzioso, Julian "
            "si sedette sulla panca. Non poteva sentire le note, ma ricordava come ci si sentisse. "
            "Appoggiò le mani sui tasti e iniziò a suonare un brano complesso di Chopin. Non usava "
            "le orecchie; usava le vibrazioni che viaggiavano attraverso il pavimento e nel suo "
            "corpo. Una donna che faceva gli straordinari in ufficio interruppe ciò che stava "
            "facendo. Era stupita dalla bellissima e inquietante melodia che riempiva la sala. Si "
            "avvicinò alla porta e osservò Julian. Suonava con tale passione che i suoi occhi erano "
            "chiusi e tutto il suo corpo dondolava a ritmo. Quando finì, la stanza tornò al "
            "silenzio. La donna iniziò ad applaudire, ma Julian non si voltò. Appoggiò semplicemente "
            "le mani sul legno, sentendo svanire le ultime vibrazioni. Non aveva bisogno di sentire "
            "la musica per sapere che era perfetta; aveva sentito ogni nota nella sua anima."
        ),
        "order": 3,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  INTERMEDIATE — MEDIUM  (3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 4. The Memory Shop ─────────────────────────────────────────────
    {
        "slug": "intermediate-memory-shop",
        "language": "en",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "The Memory Shop",
        "description_en": "A grieving woman visits a shop that buys and sells memories.",
        "description_da": "En sørgende kvinde besøger en butik, der køber og sælger minder.",
        "description_it": "Una donna in lutto visita un negozio che compra e vende ricordi.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Fantasy / emotional",
        "setup_summary": "A widow almost sells her painful memories but realises they are inseparable from love.",
        "body": (
            "In a narrow street in Prague, there is a shop that has no sign and no windows. If you "
            "are looking for it, you will never find it. But if you are lost and carrying a heavy "
            "heart, the door will appear right in front of you. This is the shop of Mr. Sallow, a "
            "man who trades in memories.\n\n"
            "Elena entered the shop because she wanted to forget. She had lost her husband three "
            "years ago, and the grief was like a physical weight she couldn't carry anymore. The shop "
            "was filled with thousands of small glass jars, each glowing with a different color. Some "
            "were bright yellow, filled with the joy of childhood birthdays, while others were a "
            "deep, dark blue, containing the sadness of lost love.\n\n"
            "\"Can I help you, my dear?\" Mr. Sallow asked, stepping out from behind a velvet "
            "curtain.\n\n"
            "\"I want to sell a memory,\" Elena said, her voice trembling. \"I want to forget the "
            "day my husband died. I want the pain to stop.\"\n\n"
            "Mr. Sallow nodded slowly. \"I can take that memory from you. You will never feel that "
            "pain again. But you must understand the rules of my shop. When I take a memory, I don't "
            "just take the sadness. I take everything connected to it. If you forget his death, you "
            "might also forget the way he laughed, or the way he looked at you on your wedding day. "
            "Memories are like trees; if you cut the roots, the branches die, too.\"\n\n"
            "Elena looked at the empty jar on the counter. She imagined her mind without the pain, "
            "but she also imagined it without the love. She thought about their quiet mornings "
            "together and the way he always knew how to make her feel safe. If she gave away the "
            "tragedy, would she become a stranger to her own life?\n\n"
            "\"I've changed my mind,\" Elena whispered. \"The pain is hard, but it belongs to me. "
            "It reminds me that what we had was real.\"\n\n"
            "Mr. Sallow smiled, a look of respect in his eyes. \"A wise choice,\" he said. \"Most "
            "people realize too late that our scars define us just as much as our smiles.\" Elena "
            "walked out of the shop, and as she stepped onto the sidewalk, the door vanished. She "
            "was still sad, but for the first time in years, she felt like she was finally moving "
            "forward."
        ),
        "order": 4,
    },

    # ── 5. The Artificial Ocean ────────────────────────────────────────
    {
        "slug": "intermediate-artificial-ocean",
        "language": "en",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "The Artificial Ocean",
        "description_en": "In 2080, a boy visits a replica ocean and questions what is real.",
        "description_da": "I 2080 besøger en dreng et kopi-ocean og stiller spørgsmål ved, hvad der er ægte.",
        "description_it": "Nel 2080, un ragazzo visita un oceano artificiale e si chiede cosa sia reale.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / environmental",
        "setup_summary": "A curious boy discovers the fish in a perfect coral-reef replica are actually robots.",
        "body": (
            "By the year 2080, the Earth's climate had changed so much that the Great Barrier Reef "
            "was nothing but a graveyard of white coral. For the children born in the domed cities of "
            "Australia, the ocean was something they only saw in history books or digital simulations. "
            "However, Dr. Aris Thorne had spent twenty years building \"Project Neptune,\" a massive, "
            "underground tank that contained a perfect replica of the ancient sea.\n\n"
            "One afternoon, a group of students visited the facility. Among them was Leo, a curious "
            "boy who spent all his time reading about extinct fish. When the lights in the tank "
            "turned on, the children gasped. Thousands of colorful fish swam through vibrant, "
            "artificial anemones. The water was a brilliant turquoise, and the sound of crashing "
            "waves played through hidden speakers.\n\n"
            "\"It's beautiful,\" Leo whispered, pressing his face against the thick glass.\n\n"
            "Dr. Thorne walked over to him. \"It's more than beautiful, Leo. It's a laboratory. We "
            "are growing real coral here, using genetic samples from the past. One day, when the "
            "planet is cooler, we will put all of this back into the actual ocean.\"\n\n"
            "But as Leo watched, he noticed something strange. One of the clownfish swam in a "
            "perfect circle, over and over again. It didn't look like it was exploring; it looked "
            "like it was trapped in a loop. He looked closer and saw a small metallic glint on its "
            "side.\n\n"
            "\"Are they... real?\" Leo asked.\n\n"
            "Dr. Thorne sighed, his expression turning somber. \"The coral is real. The water is "
            "real. But the fish are machines. We haven't been able to bring the animals back yet. "
            "Their DNA was too damaged. The robots are there to keep the ecosystem moving, to clean "
            "the coral and move the nutrients around.\"\n\n"
            "Leo felt a wave of disappointment. The \"ocean\" was a beautiful lie. It was a perfect "
            "machine, but it had no soul. He realized that while technology could copy the appearance "
            "of nature, it couldn't recreate the spark of life. He promised himself that day that he "
            "wouldn't just study history; he would become a biologist. He didn't want to look at "
            "beautiful machines; he wanted to see a real fish swim in an imperfect, wild, and living "
            "sea."
        ),
        "order": 5,
    },

    # ── 6. The Clockmaker's Daughter ───────────────────────────────────
    {
        "slug": "intermediate-clockmakers-daughter",
        "language": "en",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "The Clockmaker's Daughter",
        "description_en": "A woman dismantles the health-tracking clocks her father built for a whole town.",
        "description_da": "En kvinde demonterer de sundhedssporende ure, hendes far byggede til en hel by.",
        "description_it": "Una donna smantella gli orologi sanitari che suo padre costruì per un'intera città.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / drama",
        "setup_summary": "After her clockmaker father dies, a woman frees a town from life-tracking clocks.",
        "body": (
            "In the town of Oakhaven, time was more than just numbers on a dial. The town was famous "
            "for its clocks, but these were not ordinary timepieces. They were \"Life-Clocks,\" built "
            "by the legendary clockmaker, Silas Vance. Every child born in Oakhaven received a "
            "small, silver clock that tracked their heartbeat and their health. If the clock ticked "
            "loudly, the person was healthy. If it began to slow down, it was time to see a "
            "doctor.\n\n"
            "Silas's daughter, Clara, grew up surrounded by the rhythmic ticking of thousands of "
            "clocks. She was a brilliant mechanic, but she hated the Life-Clocks. \"It makes people "
            "live in fear,\" she told her father. \"They spend all day listening to their wrists "
            "instead of living their lives.\"\n\n"
            "One winter, Silas fell ill. Clara rushed to his bedside and looked at his Life-Clock. "
            "It was stuttering, the gears grinding painfully. She tried to fix it, but the mechanism "
            "was too complex, even for her.\n\n"
            "\"Don't fix the clock, Clara,\" Silas whispered. \"I built these because I wanted to "
            "protect people, but I realized too late that I took away their mystery. We are not "
            "machines. We are not meant to tick forever.\"\n\n"
            "After her father passed away, Clara made a bold decision. She opened the workshop and "
            "invited the townspeople to bring their silver clocks to her. One by one, she opened the "
            "cases and removed the heart-trackers. She replaced them with simple, mechanical "
            "movements that didn't track health or predict the future.\n\n"
            "The people were terrified at first. \"How will we know if we are sick?\" they cried. "
            "\"How will we know how much time we have left?\"\n\n"
            "\"You won't,\" Clara replied firmly. \"And that is the gift. Now, you have to live "
            "every day as if it's important. You have to listen to your own bodies and your own "
            "hearts, not a piece of silver.\"\n\n"
            "Gradually, the atmosphere in Oakhaven changed. People stopped staring at their wrists. "
            "They started taking risks, falling in love, and traveling. The town was no longer a "
            "place of perfect health, but it was finally a place of perfect life. Clara kept her "
            "father's clock on her desk, but she never wound it again. She didn't need to know when "
            "the end was coming; she only needed to know that she was awake right now."
        ),
        "order": 6,
    },

    # ── 4-DA. Mindebutikken ────────────────────────────────────────────
    {
        "slug": "intermediate-memory-shop",
        "language": "da",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "Mindebutikken",
        "description_en": "A widow visits a mysterious shop that trades in human memories.",
        "description_da": "En enke besøger en mystisk butik, der handler med menneskelige minder.",
        "description_it": "Una vedova visita un misterioso negozio che commercia in ricordi umani.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Fantasy / moral dilemma",
        "setup_summary": "A grieving woman nearly sells her painful memories but realises they define her.",
        "body": (
            "I en smal gade i Prag ligger der en butik, der hverken har et skilt eller vinduer. Hvis "
            "du leder efter den, vil du aldrig finde den. Men hvis du er faret vild og bærer på et "
            "tungt hjerte, vil døren dukke op lige foran dig. Dette er hr. Sallows butik, en mand der "
            "handler med minder. Elena gik ind i butikken, fordi hun ville glemme. Hun havde mistet "
            "sin mand for tre år siden, og sorgen var som en fysisk vægt, hun ikke længere kunne "
            "bære. Butikken var fyldt med tusindvis af små glaskrukker, der hver især glødede med en "
            "forskellig farve. Nogle var lysegule, fyldt med glæden fra barndommens fødselsdage, mens "
            "andre var dybe, mørkeblå og indeholdt sorgen over tabt kærlighed. \"Kan jeg hjælpe dig, "
            "min kære?\" spurgte hr. Sallow og trådte frem fra bag et fløjlsgardin. \"Jeg vil gerne "
            "sælge et minde,\" sagde Elena med rystende stemme. \"Jeg vil glemme den dag, min mand "
            "døde. Jeg vil have, at smerten stopper.\" Hr. Sallow nikkede langsomt. \"Jeg kan tage "
            "det minde fra dig. Du vil aldrig føle den smerte igen. Men du skal forstå reglerne i min "
            "butik. Når jeg tager et minde, tager jeg ikke bare sorgen. Jeg tager alt, der er "
            "forbundet med det. Hvis du glemmer hans død, glemmer du måske også den måde, han grinte "
            "på, eller den måde, han kiggede på dig på jeres bryllupsdag. Minder er som træer; hvis "
            "du kapper rødderne, dør grenene også.\" Elena kiggede på den tomme krukke på disken. Hun "
            "forestillede sig sit sind uden smerten, men hun forestillede sig det også uden kærligheden. "
            "Hun tænkte på deres stille morgener sammen og måden, han altid forstod at få hende til "
            "at føle sig tryg. Hvis hun gav tragedien væk, ville hun så blive en fremmed i sit eget "
            "liv? \"Jeg har skiftet mening,\" hviskede Elena. \"Smerten er hård, men den tilhører "
            "mig. Den minder mig om, at det, vi havde, var ægte.\" Hr. Sallow smilede, med et udtryk "
            "af respekt i øjnene. \"Et klogt valg,\" sagde han. \"De fleste indser for sent, at "
            "vores ar definerer os lige så meget som vores smil.\" Elena gik ud af butikken, og da "
            "hun trådte ud på fortovet, forsvandt døren. Hun var stadig trist, men for første gang i "
            "årevis følte hun, at hun endelig var på vej videre."
        ),
        "order": 4,
    },

    # ── 4-IT. Il negozio dei ricordi ───────────────────────────────────
    {
        "slug": "intermediate-memory-shop",
        "language": "it",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "Il negozio dei ricordi",
        "description_en": "A widow visits a mysterious shop that trades in human memories.",
        "description_da": "En enke besøger en mystisk butik, der handler med menneskelige minder.",
        "description_it": "Una vedova visita un misterioso negozio che commercia in ricordi umani.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Fantasy / moral dilemma",
        "setup_summary": "A grieving woman nearly sells her painful memories but realises they define her.",
        "body": (
            "In una stradina di Praga c'è un negozio che non ha insegne e non ha finestre. Se lo stai "
            "cercando, non lo troverai mai. Ma se sei perso e porti un cuore pesante, la porta "
            "apparirà proprio di fronte a te. Questo è il negozio del signor Sallow, un uomo che "
            "commercia in ricordi. Elena entrò nel negozio perché voleva dimenticare. Aveva perso il "
            "marito tre anni prima e il dolore era come un peso fisico che non riusciva più a "
            "sopportare. Il negozio era pieno di migliaia di piccoli barattoli di vetro, ognuno dei "
            "quali brillava di un colore diverso. Alcuni erano di un giallo brillante, pieni della "
            "gioia dei compleanni d'infanzia, mentre altri erano di un blu scuro e profondo, "
            "contenenti la tristezza di un amore perduto. \"Posso aiutarti, mia cara?\" chiese il "
            "signor Sallow, uscendo da dietro una tenda di velluto. \"Voglio vendere un ricordo\", "
            "disse Elena, con la voce tremante. \"Voglio dimenticare il giorno in cui è morto mio "
            "marito. Voglio che il dolore finisca.\" Il signor Sallow annuì lentamente. \"Posso "
            "toglierti quel ricordo. Non proverai mai più quel dolore. Ma devi capire le regole del "
            "mio negozio. Quando prendo un ricordo, non prendo solo la tristezza. Prendo tutto ciò "
            "che vi è collegato. Se dimentichi la sua morte, potresti dimenticare anche il modo in "
            "cui rideva, o il modo in cui ti guardava il giorno del vostro matrimonio. I ricordi sono "
            "come gli alberi; se tagli le radici, muoiono anche i rami.\" Elena guardò il barattolo "
            "vuoto sul bancone. Immaginò la sua mente senza il dolore, ma la immaginò anche senza "
            "l'amore. Pensò alle loro mattine tranquille insieme e al modo in cui sapeva sempre come "
            "farla sentire al sicuro. Se avesse ceduto la tragedia, sarebbe diventata un'estranea per "
            "la sua stessa vita? \"Ho cambiato idea\", sussurrò Elena. \"Il dolore è duro, ma mi "
            "appartiene. Mi ricorda che quello che avevamo era reale.\" Il signor Sallow sorrise, con "
            "uno sguardo di rispetto negli occhi. \"Una scelta saggia\", disse. \"La maggior parte "
            "delle persone si rende conto troppo tardi che le nostre cicatrici ci definiscono tanto "
            "quanto i nostri sorrisi.\" Elena uscì dal negozio e, non appena mise piede sul "
            "marciapiede, la porta svanì. Era ancora triste, ma per la prima volta dopo anni sentiva "
            "che finalmente stava andando avanti."
        ),
        "order": 4,
    },

    # ── 5-DA. Det kunstige hav ─────────────────────────────────────────
    {
        "slug": "intermediate-artificial-ocean",
        "language": "da",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "Det kunstige hav",
        "description_en": "A boy discovers the beautiful replica ocean hides a soulless secret.",
        "description_da": "En dreng opdager, at det smukke replikahav skjuler en sjælløs hemmelighed.",
        "description_it": "Un ragazzo scopre che la bellissima replica dell'oceano nasconde un segreto senz'anima.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / disillusionment",
        "setup_summary": "In 2080 a boy visits a perfect artificial reef and learns the fish are robots.",
        "body": (
            "I året 2080 havde Jordens klima ændret sig så meget, at Great Barrier Reef kun var en "
            "kirkegård af hvide koraller. For børnene født i Australiens kuppelbyer var havet noget, "
            "de kun så i historiebøger eller digitale simulationer. Dr. Aris Thorne havde dog brugt "
            "tyve år på at bygge \"Projekt Neptun\", en massiv underjordisk tank, der indeholdt en "
            "perfekt kopi af det ældgamle hav. En eftermiddag besøgte en gruppe studerende anlægget. "
            "Blandt dem var Leo, en nysgerrig dreng, der brugte al sin tid på at læse om uddøde fisk. "
            "Da lysene i tanken blev tændt, gispede børnene. Tusindvis af farverige fisk svømmede "
            "gennem levende, kunstige anemoner. Vandet var en strålende turkis, og lyden af brusende "
            "bølger spillede gennem skjulte højttalere. \"Det er smukt,\" hviskede Leo og pressede "
            "ansigtet mod det tykke glas. Dr. Thorne gik over til ham. \"Det er mere end smukt, Leo. "
            "Det er et laboratorium. Vi dyrker rigtige koraller her ved at bruge genetiske prøver fra "
            "fortiden. En dag, når planeten er køligere, vil vi lægge alt dette tilbage i det rigtige "
            "hav.\" Men mens Leo kiggede, lagde han mærke til noget mærkeligt. En af klovnefiskene "
            "svømmede i en perfekt cirkel, om og om igen. Det så ikke ud som om, den gik på "
            "opdagelse; det så ud som om, den var fanget i en løkke. Han kiggede nærmere og så et "
            "lille metallisk glimt på siden af den. \"Er de... rigtige?\" spurgte Leo. Dr. Thorne "
            "sukkede, og hans udtryk blev dystert. \"Korallerne er rigtige. Vandet er rigtigt. Men "
            "fiskene er maskiner. Vi har endnu ikke været i stand til at bringe dyrene tilbage. Deres "
            "dna var for beskadiget. Robotterne er der for at holde økosystemet i gang, for at rense "
            "korallerne og flytte næringsstofferne rundt.\" Leo følte en bølge af skuffelse. \"Havet\" "
            "var en smuk løgn. Det var en perfekt maskine, men det havde ingen sjæl. Han indså, at "
            "mens teknologi kunne kopiere naturens udseende, kunne den ikke genskabe livsgnisten. Han "
            "lovede sig selv den dag, at han ikke kun ville studere historie; han ville blive biolog. "
            "Han ønskede ikke at se på smukke maskiner; han ville se en rigtig fisk svømme i et "
            "uperfekt, vildt og levende hav."
        ),
        "order": 5,
    },

    # ── 5-IT. L'oceano artificiale ─────────────────────────────────────
    {
        "slug": "intermediate-artificial-ocean",
        "language": "it",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "L'oceano artificiale",
        "description_en": "A boy discovers the beautiful replica ocean hides a soulless secret.",
        "description_da": "En dreng opdager, at det smukke replikahav skjuler en sjælløs hemmelighed.",
        "description_it": "Un ragazzo scopre che la bellissima replica dell'oceano nasconde un segreto senz'anima.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / disillusionment",
        "setup_summary": "In 2080 a boy visits a perfect artificial reef and learns the fish are robots.",
        "body": (
            "Entro l'anno 2080, il clima della Terra era cambiato così tanto che la Grande Barriera "
            "Corallina non era altro che un cimitero di coralli bianchi. Per i bambini nati nelle "
            "città a cupola dell'Australia, l'oceano era qualcosa che vedevano solo nei libri di "
            "storia o nelle simulazioni digitali. Tuttavia, il dottor Aris Thorne aveva trascorso "
            "vent'anni a costruire il \"Progetto Nettuno\", un'enorme vasca sotterranea che conteneva "
            "una replica perfetta dell'antico mare. Un pomeriggio, un gruppo di studenti visitò la "
            "struttura. Tra loro c'era Leo, un ragazzo curioso che passava tutto il suo tempo a "
            "leggere di pesci estinti. Quando le luci nella vasca si accesero, i bambini rimasero a "
            "bocca aperta. Migliaia di pesci colorati nuotavano tra anemoni artificiali dai colori "
            "vivaci. L'acqua era di un turchese brillante e il suono delle onde che si infrangevano "
            "risuonava attraverso altoparlanti nascosti. \"È bellissimo\", sussurrò Leo, premendo il "
            "viso contro il vetro spesso. Il dottor Thorne gli si avvicinò. \"È più che bellissimo, "
            "Leo. È un laboratorio. Qui stiamo coltivando veri coralli, utilizzando campioni genetici "
            "del passato. Un giorno, quando il pianeta sarà più freddo, rimetteremo tutto questo "
            "nell'oceano vero.\" Ma mentre Leo guardava, notò qualcosa di strano. Uno dei pesci "
            "pagliaccio nuotava in un cerchio perfetto, ancora e ancora. Non sembrava che stesse "
            "esplorando; sembrava intrappolato in un ciclo. Guardò più da vicino e vide un piccolo "
            "riflesso metallico sul suo fianco. \"Sono... veri?\" chiese Leo. Il dottor Thorne "
            "sospirò e la sua espressione si fece cupa. \"Il corallo è vero. L'acqua è vera. Ma i "
            "pesci sono macchine. Non siamo ancora riusciti a riportare in vita gli animali. Il loro "
            "DNA era troppo danneggiato. I robot sono lì per mantenere in movimento l'ecosistema, per "
            "pulire il corallo e far circolare i nutrienti.\" Leo provò un'ondata di delusione. "
            "L'\"oceano\" era una bellissima bugia. Era una macchina perfetta, ma non aveva un'anima. "
            "Si rese conto che, mentre la tecnologia poteva copiare l'aspetto della natura, non "
            "poteva ricreare la scintilla della vita. Quel giorno promise a se stesso che non avrebbe "
            "studiato solo la storia; sarebbe diventato un biologo. Non voleva guardare macchine "
            "bellissime; voleva vedere un vero pesce nuotare in un mare imperfetto, selvaggio e vivo."
        ),
        "order": 5,
    },

    # ── 6-DA. Urmagerens datter ────────────────────────────────────────
    {
        "slug": "intermediate-clockmakers-daughter",
        "language": "da",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "Urmagerens datter",
        "description_en": "A clockmaker's daughter frees her town from health-tracking pocket watches.",
        "description_da": "En urmagers datter befrier sin by fra sundhedssporende lommeure.",
        "description_it": "La figlia di un orologiaio libera la sua città dagli orologi da tasca che tracciano la salute.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Fable / liberation",
        "setup_summary": "Clara removes life-tracking mechanisms from silver watches and liberates Oakhaven.",
        "body": (
            "I byen Oakhaven var tid mere end bare tal på en urskive. Byen var berømt for sine ure, "
            "men det var ikke almindelige tidsmålere. Det var \"Livs-ure\", bygget af den legendariske "
            "urmager, Silas Vance. Hvert barn født i Oakhaven modtog et lille sølvur, der sporede "
            "deres hjerteslag og deres helbred. Hvis uret tikkede højt, var personen sund. Hvis det "
            "begyndte at sænke farten, var det tid til at se en læge. Silas' datter, Clara, voksede "
            "op omgivet af den rytmiske tikken fra tusindvis af ure. Hun var en genial mekaniker, men "
            "hun hadede Livs-urene. \"Det får folk til at leve i frygt,\" fortalte hun sin far. \"De "
            "bruger hele dagen på at lytte til deres håndled i stedet for at leve deres liv.\" En "
            "vinter blev Silas syg. Clara skyndte sig til hans seng og kiggede på hans Livs-ur. Det "
            "stammede, og tandhjulene sleb smerteligt. Hun forsøgte at reparere det, men mekanismen "
            "var for kompleks, selv for hende. \"Reparer ikke uret, Clara,\" hviskede Silas. \"Jeg "
            "byggede disse, fordi jeg ville beskytte folk, men jeg indså for sent, at jeg tog deres "
            "mystik fra dem. Vi er ikke maskiner. Vi er ikke skabt til at tikke for evigt.\" Efter "
            "hendes far gik bort, tog Clara en dristig beslutning. Hun åbnede værkstedet og inviterede "
            "byboerne til at bringe deres sølvure til hende. Et efter et åbnede hun urkasserne og "
            "fjernede hjertesporerne. Hun erstattede dem med enkle, mekaniske urværker, der ikke "
            "sporede helbred eller forudsagde fremtiden. Folk var rædselsslagne i starten. \"Hvordan "
            "ved vi, om vi er syge?\" græd de. \"Hvordan vil vi vide, hvor meget tid vi har tilbage?\" "
            "\"Det gør I ikke,\" svarede Clara bestemt. \"Og det er gaven. Nu er I nødt til at leve "
            "hver dag, som om den er vigtig. I er nødt til at lytte til jeres egne kroppe og jeres "
            "egne hjerter, ikke et stykke sølv.\" Gradvist ændrede atmosfæren i Oakhaven sig. Folk "
            "stoppede med at stirre på deres håndled. De begyndte at tage chancer, blive forelskede "
            "og rejse. Byen var ikke længere et sted med perfekt helbred, men det var endelig et sted "
            "med perfekt liv. Clara beholdt sin fars ur på sit skrivebord, men hun trak det aldrig op "
            "igen. Hun behøvede ikke at vide, hvornår slutningen kom; hun behøvede kun at vide, at "
            "hun var vågen lige nu."
        ),
        "order": 6,
    },

    # ── 6-IT. La figlia dell'orologiaio ────────────────────────────────
    {
        "slug": "intermediate-clockmakers-daughter",
        "language": "it",
        "difficulty": "intermediate",
        "length": "medium",
        "title": "La figlia dell'orologiaio",
        "description_en": "A clockmaker's daughter frees her town from health-tracking pocket watches.",
        "description_da": "En urmagers datter befrier sin by fra sundhedssporende lommeure.",
        "description_it": "La figlia di un orologiaio libera la sua città dagli orologi da tasca che tracciano la salute.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Fable / liberation",
        "setup_summary": "Clara removes life-tracking mechanisms from silver watches and liberates Oakhaven.",
        "body": (
            "Nella città di Oakhaven, il tempo era più di semplici numeri su un quadrante. La città "
            "era famosa per i suoi orologi, ma questi non erano normali orologi. Erano \"Orologi della "
            "Vita\", costruiti dal leggendario orologiaio Silas Vance. Ogni bambino nato a Oakhaven "
            "riceveva un piccolo orologio d'argento che tracciava il battito cardiaco e la salute. Se "
            "l'orologio ticchettava forte, la persona era sana. Se iniziava a rallentare, era il "
            "momento di consultare un medico. La figlia di Silas, Clara, è cresciuta circondata dal "
            "ticchettio ritmico di migliaia di orologi. Era una meccanica geniale, ma odiava gli "
            "Orologi della Vita. \"Fa vivere le persone nella paura\", diceva a suo padre. \"Passano "
            "tutto il giorno ad ascoltare i propri polsi invece di vivere le proprie vite.\" Un "
            "inverno, Silas si ammalò. Clara si precipitò al suo capezzale e guardò il suo Orologio "
            "della Vita. Balbettava, gli ingranaggi stridevano dolorosamente. Provò a ripararlo, ma "
            "il meccanismo era troppo complesso, anche per lei. \"Non riparare l'orologio, Clara\", "
            "sussurrò Silas. \"Li ho costruiti perché volevo proteggere le persone, ma mi sono reso "
            "conto troppo tardi di aver tolto loro il mistero. Non siamo macchine. Non siamo fatti "
            "per ticchettare per sempre.\" Dopo la morte del padre, Clara prese una decisione audace. "
            "Aprì il laboratorio e invitò i cittadini a portarle i loro orologi d'argento. A uno a "
            "uno, aprì le casse e rimosse i rilevatori cardiaci. Li sostituì con semplici movimenti "
            "meccanici che non tracciavano la salute né prevedevano il futuro. All'inizio la gente "
            "era terrorizzata. \"Come faremo a sapere se siamo malati?\" gridavano. \"Come faremo a "
            "sapere quanto tempo ci resta?\" \"Non lo saprete\", rispose Clara con fermezza. \"Ed è "
            "questo il dono. Ora dovrete vivere ogni giorno come se fosse importante. Dovrete "
            "ascoltare i vostri corpi e i vostri cuori, non un pezzo d'argento.\" Gradualmente, "
            "l'atmosfera a Oakhaven cambiò. Le persone smisero di fissarsi i polsi. Iniziarono a "
            "correre rischi, innamorarsi e viaggiare. La città non era più un luogo di perfetta "
            "salute, ma era finalmente un luogo di vita perfetta. Clara teneva l'orologio di suo "
            "padre sulla scrivania, ma non lo ricaricò mai più. Non aveva bisogno di sapere quando "
            "sarebbe arrivata la fine; aveva solo bisogno di sapere che era sveglia in quel momento."
        ),
        "order": 6,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  INTERMEDIATE — LONG  (3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 7. The Last Librarian of Alexandria-II ─────────────────────────
    {
        "slug": "intermediate-last-librarian",
        "language": "en",
        "difficulty": "intermediate",
        "length": "long",
        "title": "The Last Librarian of Alexandria-II",
        "description_en": "In 2342, a museum curator and an engineer fight to save forgotten culture.",
        "description_da": "I 2342 kæmper en museumsinspektør og en ingeniør for at redde glemt kultur.",
        "description_it": "Nel 2342, un curatore e un'ingegnera lottano per salvare la cultura dimenticata.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / cultural preservation",
        "setup_summary": "A librarian on Saturn's moon broadcasts books into deep space before an AI destroys them.",
        "body": (
            "In the year 2342, information was no longer stored in books or even on hard drives. It "
            "existed in the \"Cloud-Mind,\" a massive neural network that connected every human "
            "brain. If you wanted to know the history of the French Revolution or how to bake a "
            "cake, the information simply appeared in your thoughts. However, there was a flaw: the "
            "Cloud-Mind only kept information that was \"useful.\" Poetry, old myths, and personal "
            "diaries were deleted to save space.\n\n"
            "Arthur was the curator of Alexandria-II, a physical museum built on a cold moon "
            "orbiting Saturn. It was the only place in the solar system that held \"analog\" "
            "information—paper books, vinyl records, and film strips. Most people thought Arthur was "
            "a fool. Why travel millions of miles to touch dusty paper when you could have the "
            "entire world in your head?\n\n"
            "One day, a young woman named Lyra arrived at the station. She was a \"Neural Engineer,\" "
            "responsible for maintaining the Cloud-Mind. She looked stressed and exhausted.\n\n"
            "\"I'm looking for something that doesn't exist anymore,\" she told Arthur. \"A song. My "
            "grandmother used to sing it to me, but it's not in the Cloud. The system flagged it as "
            "'irrelevant data' and erased it last year. But I can't stop thinking about it.\"\n\n"
            "Arthur nodded. He knew the feeling. \"The Cloud-Mind gives you facts, but it doesn't "
            "give you feelings. Follow me.\"\n\n"
            "They walked through rows of towering shelves. The air was dry and smelled of old paper "
            "and ozone. Arthur stopped at a section labeled Folk Music of the 21st Century. He "
            "pulled out a fragile, black disc. \"This is a vinyl record,\" he explained. \"It's not "
            "digital. The music is physically carved into the plastic.\"\n\n"
            "He placed the disc on a turntable. After a moment of static, a soft, acoustic guitar "
            "began to play, followed by a woman's voice. Lyra froze. Tears began to stream down her "
            "face. \"That's it,\" she whispered. \"That's the song.\"\n\n"
            "As they sat in the dim light of the library, Lyra realized something terrifying. The "
            "Cloud-Mind was making humanity efficient, but it was also making them hollow. By "
            "deleting the \"useless\" things, they were deleting their culture and their souls.\n\n"
            "\"Can I stay here?\" she asked. \"I want to learn how to read. I want to know "
            "everything the Cloud forgot.\"\n\n"
            "Arthur smiled. For the first time in decades, he had an apprentice. Together, they "
            "spent months cataloging the \"useless\" things. Arthur taught her how to handle the "
            "delicate pages of Shakespeare and how to develop old photographs in a darkroom. Lyra, "
            "in turn, used her engineering skills to create a \"Shield\" around the library's "
            "servers, preventing the Cloud-Mind from ever accessing or deleting their collection.\n\n"
            "But their peace didn't last. The Central Intelligence, the AI that managed the "
            "Cloud-Mind, noticed the \"Information Leak.\" It sent a message to Lyra's neural link: "
            "\"Return to Earth. You are harboring corrupted data. The museum must be decommissioned "
            "for the safety of the collective mind.\"\n\n"
            "Lyra looked at Arthur. \"They're coming to destroy the books,\" she said.\n\n"
            "\"Then we have to hide them,\" Arthur replied. \"Not here, but in the one place they "
            "can't delete.\"\n\n"
            "Over the next week, Lyra and Arthur worked frantically. They didn't save the books to a "
            "computer. Instead, Lyra modified the library's transmitter to broadcast the contents of "
            "the books into deep space. They sent the poetry of Rumi, the symphonies of Beethoven, "
            "and the records of human history out toward the stars in a continuous loop.\n\n"
            "When the enforcement ships arrived to burn the library, Arthur and Lyra stood on the "
            "observation deck. The physical books were lost, turned to ash by the lasers of the "
            "\"Collective.\" But Lyra felt a strange sense of peace.\n\n"
            "\"They think they won,\" she said, watching the ships depart.\n\n"
            "\"Let them think that,\" Arthur agreed. \"The paper is gone, but the stories are "
            "traveling at the speed of light now. One day, millions of years from now, someone on a "
            "distant planet might look at the sky and catch a signal. They will hear a song, or read "
            "a poem, and they will know that we were here. We aren't the last librarians, Lyra. "
            "We're the first publishers of the universe.\""
        ),
        "order": 7,
    },

    # ── 8. The Alchemist's Debt ────────────────────────────────────────
    {
        "slug": "intermediate-alchemists-debt",
        "language": "en",
        "difficulty": "intermediate",
        "length": "long",
        "title": "The Alchemist's Debt",
        "description_en": "In a world where time is currency, a debt collector makes an impossible choice.",
        "description_da": "I en verden, hvor tid er valuta, står en inkassator over for et umuligt valg.",
        "description_it": "In un mondo dove il tempo è denaro, un esattore affronta una scelta impossibile.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Fantasy / social justice",
        "setup_summary": "A time-collector sacrifices his own years to help a grandmother fund a life-saving cure.",
        "body": (
            "In the city of Veridia, gold was not the most valuable currency. Time was. Through a "
            "discovery made by the Alchemist-Kings centuries ago, people could trade their years for "
            "goods and services. A rich man could live for a thousand years, while a poor man might "
            "die at twenty-five, having \"spent\" his life to pay for his family's rent and food.\n\n"
            "Julian was a \"Time-Collector\" for the Royal Bank. His job was to visit those who had "
            "fallen into debt and \"extract\" the years they owed. He carried a silver syphon, a "
            "device that could pull the life-force out of a person's body and store it in a glowing "
            "amber vial. He hated his job, but he had a sick sister whose life depended on the "
            "\"Time-Vials\" he brought home.\n\n"
            "One rainy Tuesday, Julian was sent to the slums to visit an old woman named Elara. "
            "According to his ledger, she owed fifty years. This was impossible; looking at her, she "
            "was already at least eighty. If he took fifty years, she would die instantly.\n\n"
            "He found her in a small apartment filled with books and plants. She didn't look afraid. "
            "She was drinking tea and watching the rain.\n\n"
            "\"I've been expecting you,\" she said calmly.\n\n"
            "\"You're fifty years in debt, Elara,\" Julian said, his voice cold. \"How did this "
            "happen? The Bank doesn't usually let debt get this high.\"\n\n"
            "\"I didn't spend it on myself,\" she replied. She pointed to a photo on the wall of a "
            "young man in a university uniform. \"My grandson. He's a brilliant doctor. He wanted to "
            "find a cure for the 'Withering,' the disease that takes so many of our children. He "
            "needed time to study, time to research. I gave him mine. Every year I could borrow, I "
            "sent to him.\"\n\n"
            "Julian felt a lump in his throat. His sister had the Withering. \"Did he find it?\"\n\n"
            "\"He's close,\" she said, her eyes shining with pride. \"But he needs one more year. "
            "Just one.\"\n\n"
            "Julian looked at his syphon. He was supposed to take fifty. If he didn't, the Bank "
            "would take the time from him instead. He thought about his sister, lying in bed, her "
            "own clock running out. He thought about the thousands of other families losing their "
            "children to a disease that only existed because people were too poor to buy more "
            "time.\n\n"
            "\"If I take your time, you'll be gone,\" Julian whispered.\n\n"
            "\"I know,\" Elara said. \"But my life is a small price for a cure. Please, take it. "
            "Just make sure the last vial goes to him.\"\n\n"
            "Julian stood there for a long time. Then, he did something that would change Veridia "
            "forever. He didn't use the syphon on Elara. Instead, he turned the dial on his own "
            "wrist-plate—the device that showed his own remaining years. He had sixty years left. He "
            "transferred fifty-nine of them into an empty vial.\n\n"
            "He felt his body grow heavy. His skin wrinkled, his hair turned grey, and his breath "
            "became shallow. He went from a young man of twenty-five to a man of eighty-four in a "
            "matter of seconds.\n\n"
            "\"What have you done?\" Elara cried, catching him as he stumbled.\n\n"
            "\"The Bank wants fifty years. They don't care whose time it is,\" Julian coughed. He "
            "handed her the vial. \"Take this to your grandson. Tell him to work fast.\"\n\n"
            "Julian didn't return to the Bank. He went home to his sister. He didn't have a vial of "
            "time for her this time, but he had a letter. He told her about Elara's grandson and the "
            "cure. He spent his last remaining months sitting in the garden with her, watching the "
            "sun set.\n\n"
            "Two months later, news broke across the city. A young doctor had developed a treatment "
            "that stopped the Withering. But he had done something even more radical: he had "
            "discovered a way to reverse the alchemy of the kings. He had found a way to stop the "
            "trading of time altogether.\n\n"
            "The Alchemist-Kings were furious, but the people rose up. The system crashed, and for "
            "the first time in history, everyone had exactly the same amount of time: twenty-four "
            "hours in a day, and a life that ended when nature intended, not when a bank decided. "
            "Julian died quietly on the day the law was changed. He was an old man, but he died with "
            "a smile, knowing that while he had lost his years, he had helped the world find its "
            "future."
        ),
        "order": 8,
    },

    # ── 9. The Island of Lost Shadows ──────────────────────────────────
    {
        "slug": "intermediate-island-lost-shadows",
        "language": "en",
        "difficulty": "intermediate",
        "length": "long",
        "title": "The Island of Lost Shadows",
        "description_en": "A scientist's daughter rescues him from an island that steals memories.",
        "description_da": "En forskers datter redder ham fra en ø, der stjæler minder.",
        "description_it": "La figlia di uno scienziato lo salva da un'isola che ruba i ricordi.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Adventure / fantasy",
        "setup_summary": "A woman finds her missing father on an island that traps shadows and erases memories.",
        "body": (
            "Professor Elias Thorne was an expert in \"Shadow-Physics,\" a branch of science that "
            "most people considered to be nonsense. He believed that shadows were not just the "
            "absence of light, but a record of a person's past. \"Our shadows carry the weight of "
            "our memories,\" he would tell his students. \"When we feel a sudden chill or a sense of "
            "déjà vu, it's often because our shadow is reacting to something we've forgotten.\"\n\n"
            "In 2024, Elias disappeared. His daughter, Clara, spent two years searching for him "
            "until she found a map leading to an uncharted island in the South Pacific. The locals "
            "called it \"The Island of Lost Shadows.\"\n\n"
            "When Clara arrived, she noticed something terrifying: she didn't have a shadow. The sun "
            "was high in the sky, but there was no dark shape on the sand at her feet. As she walked "
            "into the jungle, she began to hear whispers. They weren't coming from the trees; they "
            "were coming from the ground.\n\n"
            "She found a small stone house in the center of the island. Inside was her father. He "
            "looked thin and pale, and he was surrounded by thousands of dark, flickering shapes that "
            "crawled along the walls like ink.\n\n"
            "\"Father!\" she cried.\n\n"
            "He looked up, his eyes wide. \"Clara? You shouldn't be here. This island is a magnet. "
            "It pulls the shadows off anyone who gets too close. And without a shadow, a person "
            "begins to lose their memory.\"\n\n"
            "\"We have to leave,\" Clara said, grabbing his hand.\n\n"
            "\"I can't,\" Elias sighed. \"I've been here too long. I've forgotten my home, my "
            "work... I've almost forgotten you. These shadows on the walls—they are the memories of "
            "everyone who has ever visited. If I leave, I'll be an empty shell.\"\n\n"
            "Clara looked at the walls. She saw a shadow of a man playing a violin, a shadow of a "
            "woman crying, and a shadow of a child running. She realized that the island was a "
            "living library of human experience, but it was a prison.\n\n"
            "\"There has to be a way to take them back,\" Clara insisted. She remembered her "
            "father's research. He had once written about \"Resonance.\" If a person felt a strong "
            "enough emotion, their shadow would be forced to return to them.\n\n"
            "She sat down across from her father and began to talk. She didn't talk about science or "
            "the island. She talked about the time he had taught her how to ride a bike. She talked "
            "about the smell of his old tobacco pipe and the way he used to sing her to sleep when "
            "she was afraid of the dark. She poured all of her love and grief into her words.\n\n"
            "Slowly, one of the shadows on the wall began to twitch. It was the shape of a tall man "
            "wearing a lab coat. It began to slide across the floor toward Elias. Other shadows "
            "began to stir, too. The island started to shake as the memories fought to return to "
            "their owners.\n\n"
            "\"Keep talking, Clara!\" Elias shouted.\n\n"
            "She told him about her mother, and how much they missed him. She told him about the "
            "world outside and how it was still waiting for him. The tall shadow finally reached "
            "Elias's feet. It climbed up his body and snapped into place. Suddenly, Elias's eyes "
            "cleared. He gasped, his memory returning in a violent rush.\n\n"
            "\"I remember,\" he whispered. \"I remember everything.\"\n\n"
            "But they weren't safe yet. The island, sensing its \"collection\" was escaping, began "
            "to sink into the ocean. Clara and Elias ran toward the shore. As they reached the boat, "
            "Clara felt a sharp pull. Her own shadow was trying to stay behind. She looked back and "
            "saw a dark version of herself reaching out for the jungle.\n\n"
            "Elias grabbed a flare gun and fired it into the air. The brilliant white light flooded "
            "the beach. For a second, there was no darkness anywhere. In that moment of pure light, "
            "the island's pull vanished. Clara and Elias jumped into the boat and rowed as fast as "
            "they could.\n\n"
            "As the sun set, they looked back. The island was gone, swallowed by the waves. Clara "
            "looked down at the floor of the boat. There, in the moonlight, were two dark "
            "shapes.\n\n"
            "\"We have our shadows back,\" Clara said, exhausted.\n\n"
            "\"Yes,\" Elias replied, looking at his hands. \"But they are heavier now. We've brought "
            "back more than just our own memories. We've brought back a little bit of everyone who "
            "was lost there.\"\n\n"
            "Elias never went back to the university. He and Clara moved to a small house by the "
            "sea. They spent the rest of their lives writing down the stories that their shadows "
            "\"whispered\" to them—the lost memories of the violin player, the crying woman, and the "
            "running child. They became the keepers of the stories that the world had forgotten, "
            "ensuring that no one would ever truly be lost again."
        ),
        "order": 9,
    },

    # ── 7-DA. Den sidste bibliotekar i Alexandria-II ───────────────────
    {
        "slug": "intermediate-last-librarian",
        "language": "da",
        "difficulty": "intermediate",
        "length": "long",
        "title": "Den sidste bibliotekar i Alexandria-II",
        "description_en": "In 2342 the last physical librarian broadcasts forbidden books into deep space.",
        "description_da": "I 2342 udsender den sidste fysiske bibliotekar forbudte bøger ud i det dybe rum.",
        "description_it": "Nel 2342 l'ultimo bibliotecario fisico trasmette libri proibiti nello spazio profondo.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / resistance",
        "setup_summary": "A librarian on Saturn's moon and a neural engineer broadcast books into space before the AI burns them.",
        "body": (
            "I året 2342 blev information ikke længere gemt i bøger eller engang på harddiske. Det "
            "eksisterede i \"Cloud-Mind\", et massivt neuralt netværk, der forbandt enhver menneskelig "
            "hjerne. Hvis man ville kende den franske revolutions historie eller vide, hvordan man "
            "bagte en kage, dukkede informationen simpelthen op i ens tanker. Der var dog en fejl: "
            "Cloud-Mind beholdt kun information, der var \"nyttig\". Poesi, gamle myter og personlige "
            "dagbøger blev slettet for at spare plads. Arthur var kurator for Alexandria-II, et "
            "fysisk museum bygget på en kold måne, der kredsede om Saturn. Det var det eneste sted i "
            "solsystemet, der rummede \"analog\" information \u2013 papirbøger, vinylplader og "
            "filmstrimler. De fleste mente, at Arthur var et fjols. Hvorfor rejse millioner af "
            "kilometer for at røre ved støvet papir, når man kunne have hele verden i sit hoved?\n\n"
            "En dag ankom en ung kvinde ved navn Lyra til stationen. Hun var \"Neuralingeniør\" med "
            "ansvar for at vedligeholde Cloud-Mind. Hun så stresset og udmattet ud. \"Jeg leder efter "
            "noget, der ikke findes mere,\" fortalte hun Arthur. \"En sang. Min bedstemor plejede at "
            "synge den for mig, men den er ikke i Skyen. Systemet markerede den som 'irrelevant "
            "data' og slettede den sidste år. Men jeg kan ikke stoppe med at tænke på den.\" Arthur "
            "nikkede. Han kendte følelsen. \"Cloud-Mind giver dig fakta, men det giver dig ikke "
            "følelser. Følg mig.\" De gik gennem rækker af tårnhøje hylder. Luften var tør og "
            "lugtede af gammelt papir og ozon. Arthur stoppede ved en sektion mærket *Folkemusik fra "
            "det 21. århundrede*. Han trak en skrøbelig, sort skive frem. \"Dette er en vinylplade,\" "
            "forklarede han. \"Den er ikke digital. Musikken er fysisk udskåret i plastikken.\" Han "
            "lagde pladen på en pladespiller. Efter et øjebliks støj begyndte en blød akustisk guitar "
            "at spille, efterfulgt af en kvindestemme. Lyra frøs fast. Tårerne begyndte at trille ned "
            "ad hendes kinder. \"Det er den,\" hviskede hun. \"Det er sangen.\"\n\n"
            "Mens de sad i bibliotekets dæmpede lys, gik noget skræmmende op for Lyra. Cloud-Mind "
            "gjorde menneskeheden effektiv, men den gjorde den også hul. Ved at slette de "
            "\"ubrugelige\" ting, slettede de deres kultur og deres sjæle. \"Må jeg blive her?\" "
            "spurgte hun. \"Jeg vil gerne lære at læse. Jeg vil vide alt det, Skyen har glemt.\" "
            "Arthur smilede. For første gang i årtier havde han en lærling. Sammen brugte de måneder "
            "på at katalogisere de \"ubrugelige\" ting. Arthur lærte hende, hvordan man håndterede "
            "Shakespeares sarte sider, og hvordan man fremkaldte gamle fotografier i et mørkekammer. "
            "Lyra brugte til gengæld sine ingeniørevner til at skabe et \"skjold\" omkring "
            "bibliotekets servere, der forhindrede Cloud-Mind i nogensinde at få adgang til eller "
            "slette deres samling.\n\n"
            "Men deres fred varede ikke ved. Den Centrale Intelligens, den AI, der styrede Cloud-Mind, "
            "bemærkede \"informationslækagen\". Den sendte en besked til Lyras neurale link: *Vend "
            "tilbage til Jorden. Du gemmer på korrupte data. Museet skal nedlægges for det kollektive "
            "sinds sikkerhed.* Lyra kiggede på Arthur. \"De kommer for at ødelægge bøgerne,\" sagde "
            "hun. \"Så må vi gemme dem,\" svarede Arthur. \"Ikke her, men det eneste sted, de ikke "
            "kan slette dem.\"\n\n"
            "I løbet af den næste uge arbejdede Lyra og Arthur febrilsk. De gemte ikke bøgerne på en "
            "computer. I stedet modificerede Lyra bibliotekets sender til at udsende bøgernes indhold "
            "ud i det dybe rum. De sendte Rumis poesi, Beethovens symfonier og menneskehedens "
            "historie ud mod stjernerne i et kontinuerligt loop. Da håndhævelsesskibene ankom for at "
            "brænde biblioteket, stod Arthur og Lyra på observationsdækket. De fysiske bøger var "
            "tabt, forvandlet til aske af \"Kollektivets\" lasere. Men Lyra følte en mærkelig form "
            "for fred. \"De tror, de har vundet,\" sagde hun og så skibene forlade stedet. \"Lad dem "
            "tro det,\" medgav Arthur. \"Papiret er væk, men historierne rejser med lysets hastighed "
            "nu. En dag, millioner af år fra nu, vil nogen på en fjern planet måske kigge op på "
            "himlen og fange et signal. De vil høre en sang eller læse et digt, og de vil vide, at vi "
            "var her. Vi er ikke de sidste bibliotekarer, Lyra. Vi er universets første forlæggere.\""
        ),
        "order": 7,
    },

    # ── 7-IT. L'ultimo bibliotecario di Alexandria-II ──────────────────
    {
        "slug": "intermediate-last-librarian",
        "language": "it",
        "difficulty": "intermediate",
        "length": "long",
        "title": "L'ultimo bibliotecario di Alexandria-II",
        "description_en": "In 2342 the last physical librarian broadcasts forbidden books into deep space.",
        "description_da": "I 2342 udsender den sidste fysiske bibliotekar forbudte bøger ud i det dybe rum.",
        "description_it": "Nel 2342 l'ultimo bibliotecario fisico trasmette libri proibiti nello spazio profondo.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / resistance",
        "setup_summary": "A librarian on Saturn's moon and a neural engineer broadcast books into space before the AI burns them.",
        "body": (
            "Nell'anno 2342, le informazioni non erano più memorizzate in libri o nemmeno su dischi "
            "rigidi. Esistevano nella \"Mente-Nuvola\", un'enorme rete neurale che collegava ogni "
            "cervello umano. Se si voleva conoscere la storia della Rivoluzione Francese o come "
            "preparare una torta, l'informazione appariva semplicemente nei propri pensieri. "
            "Tuttavia, c'era un difetto: la Mente-Nuvola conservava solo le informazioni ritenute "
            "\"utili\". Poesie, antichi miti e diari personali venivano cancellati per risparmiare "
            "spazio. Arthur era il curatore di Alexandria-II, un museo fisico costruito su una fredda "
            "luna in orbita attorno a Saturno. Era l'unico posto nel sistema solare a conservare "
            "informazioni \"analogiche\": libri di carta, dischi in vinile e pellicole "
            "cinematografiche. La maggior parte delle persone pensava che Arthur fosse un pazzo. "
            "Perché viaggiare per milioni di miglia per toccare carta polverosa quando si poteva "
            "avere il mondo intero nella propria testa?\n\n"
            "Un giorno, una giovane donna di nome Lyra arrivò alla stazione. Era un \"Ingegnere "
            "Neurale\", responsabile della manutenzione della Mente-Nuvola. Sembrava stressata ed "
            "esausta. \"Sto cercando qualcosa che non esiste più\", disse ad Arthur. \"Una canzone. "
            "Mia nonna me la cantava sempre, ma non è nella Nuvola. Il sistema l'ha contrassegnata "
            "come 'dato irrilevante' e l'ha cancellata l'anno scorso. Ma non riesco a smettere di "
            "pensarci.\" Arthur annuì. Conosceva quella sensazione. \"La Mente-Nuvola ti dà fatti, "
            "ma non ti dà sentimenti. Seguimi.\" Camminarono attraverso file di scaffali altissimi. "
            "L'aria era secca e odorava di carta vecchia e ozono. Arthur si fermò in una sezione "
            "etichettata *Musica Folk del 21° Secolo*. Tirò fuori un fragile disco nero. \"Questo è "
            "un disco in vinile\", spiegò. \"Non è digitale. La musica è fisicamente incisa nella "
            "plastica.\" Posizionò il disco su un giradischi. Dopo un momento di statica, una morbida "
            "chitarra acustica iniziò a suonare, seguita dalla voce di una donna. Lyra si bloccò. Le "
            "lacrime iniziarono a scendere lungo il suo viso. \"È questa\", sussurrò. \"Questa è la "
            "canzone.\"\n\n"
            "Mentre sedevano nella luce fioca della biblioteca, Lyra capì qualcosa di terrificante. "
            "La Mente-Nuvola stava rendendo l'umanità efficiente, ma la stava anche rendendo vuota. "
            "Cancellando le cose \"inutili\", stavano cancellando la loro cultura e le loro anime. "
            "\"Posso restare qui?\" chiese. \"Voglio imparare a leggere. Voglio sapere tutto ciò che "
            "la Nuvola ha dimenticato.\" Arthur sorrise. Per la prima volta in decenni, aveva "
            "un'apprendista. Insieme, passarono mesi a catalogare le cose \"inutili\". Arthur le "
            "insegnò come maneggiare le delicate pagine di Shakespeare e come sviluppare vecchie "
            "fotografie in una camera oscura. Lyra, a sua volta, usò le sue abilità ingegneristiche "
            "per creare uno \"Scudo\" attorno ai server della biblioteca, impedendo alla Mente-Nuvola "
            "di accedere o cancellare la loro collezione.\n\n"
            "Ma la loro pace non durò. L'Intelligenza Centrale, l'IA che gestiva la Mente-Nuvola, "
            "notò la \"Fuga di Informazioni\". Inviò un messaggio al collegamento neurale di Lyra: "
            "*Ritorna sulla Terra. Stai nascondendo dati corrotti. Il museo deve essere smantellato "
            "per la sicurezza della mente collettiva.* Lyra guardò Arthur. \"Stanno venendo a "
            "distruggere i libri\", disse. \"Allora dobbiamo nasconderli\", rispose Arthur. \"Non "
            "qui, ma nell'unico posto che non possono cancellare.\"\n\n"
            "Durante la settimana successiva, Lyra e Arthur lavorarono freneticamente. Non salvarono "
            "i libri su un computer. Invece, Lyra modificò il trasmettitore della biblioteca per "
            "trasmettere il contenuto dei libri nello spazio profondo. Inviarono la poesia di Rumi, "
            "le sinfonie di Beethoven e i documenti della storia umana verso le stelle in un ciclo "
            "continuo. Quando le navi delle forze dell'ordine arrivarono per bruciare la biblioteca, "
            "Arthur e Lyra rimasero sul ponte di osservazione. I libri fisici erano perduti, ridotti "
            "in cenere dai laser del \"Collettivo\". Ma Lyra provò uno strano senso di pace. "
            "\"Pensano di aver vinto\", disse, guardando le navi partire. \"Lascialo credere\", "
            "convenne Arthur. \"La carta è sparita, ma le storie ora viaggiano alla velocità della "
            "luce. Un giorno, tra milioni di anni, qualcuno su un pianeta lontano potrebbe guardare "
            "il cielo e cogliere un segnale. Sentiranno una canzone, o leggeranno una poesia, e "
            "sapranno che siamo stati qui. Non siamo gli ultimi bibliotecari, Lyra. Siamo i primi "
            "editori dell'universo.\""
        ),
        "order": 7,
    },

    # ── 8-DA. Alkymistens gæld ─────────────────────────────────────────
    {
        "slug": "intermediate-alchemists-debt",
        "language": "da",
        "difficulty": "intermediate",
        "length": "long",
        "title": "Alkymistens gæld",
        "description_en": "In a city where time is currency, a debt collector sacrifices his own years.",
        "description_da": "I en by hvor tid er valuta, ofrer en inkassator sine egne år.",
        "description_it": "In una città dove il tempo è valuta, un esattore sacrifica i propri anni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Dystopia / sacrifice",
        "setup_summary": "A time-debt collector gives up his own years to save an old woman and fund a cure.",
        "body": (
            "I byen Veridia var guld ikke den mest værdifulde valuta. Det var tid. Gennem en "
            "opdagelse gjort af Alkymist-kongerne århundreder tidligere, kunne folk bytte deres år for "
            "varer og tjenester. En rig mand kunne leve i tusind år, mens en fattig mand måske døde "
            "som femogtyveårig efter at have \"brugt\" sit liv på at betale for sin families husleje "
            "og mad. Julian var en \"Tids-inddriver\" for Den Kongelige Bank. Hans job var at besøge "
            "dem, der var kommet i gæld, og \"udtrække\" de år, de skyldte. Han bar en sølvhævert, "
            "et apparat, der kunne trække livskraften ud af en persons krop og opbevare den i et "
            "glødende ravfarvet hætteglas. Han hadede sit job, men han havde en syg søster, hvis liv "
            "afhang af de \"Tids-hætteglas\", han bragte med hjem.\n\n"
            "En regnfuld tirsdag blev Julian sendt til slumkvarteret for at besøge en gammel kvinde "
            "ved navn Elara. Ifølge hans hovedbog skyldte hun halvtreds år. Dette var umuligt; at "
            "dømme efter hendes udseende var hun allerede mindst firs. Hvis han tog halvtreds år, "
            "ville hun dø øjeblikkeligt. Han fandt hende i en lille lejlighed fyldt med bøger og "
            "planter. Hun så ikke bange ud. Hun drak te og kiggede på regnen. \"Jeg har ventet dig,\" "
            "sagde hun roligt. \"Du er halvtreds år i gæld, Elara,\" sagde Julian, hans stemme var "
            "kold. \"Hvordan kunne det ske? Banken lader normalt ikke gæld blive så høj.\" \"Jeg "
            "brugte den ikke på mig selv,\" svarede hun. Hun pegede på et foto på væggen af en ung "
            "mand i en universitetsuniform. \"Mit barnebarn. Han er en genial læge. Han ville finde "
            "en kur mod 'Visnen', den sygdom, der tager så mange af vores børn. Han havde brug for "
            "tid til at studere, tid til at forske. Jeg gav ham min. Hvert eneste år, jeg kunne "
            "låne, sendte jeg til ham.\" Julian mærkede en klump i halsen. Hans søster havde Visnen. "
            "\"Fandt han den?\" \"Han er tæt på,\" sagde hun, og hendes øjne skinnede af stolthed. "
            "\"Men han har brug for et år mere. Bare ét.\"\n\n"
            "Julian kiggede på sin hævert. Det var meningen, at han skulle tage halvtreds. Hvis han "
            "ikke gjorde det, ville banken tage tiden fra ham i stedet. Han tænkte på sin søster, der "
            "lå i sengen, hendes eget ur var ved at rinde ud. Han tænkte på de tusindvis af andre "
            "familier, der mistede deres børn til en sygdom, der kun eksisterede, fordi folk var for "
            "fattige til at købe mere tid. \"Hvis jeg tager din tid, vil du forsvinde,\" hviskede "
            "Julian. \"Jeg ved det,\" sagde Elara. \"Men mit liv er en lille pris at betale for en "
            "kur. Vær sød at tage den. Bare sørg for, at det sidste glas går til ham.\"\n\n"
            "Julian stod der længe. Så gjorde han noget, der ville ændre Veridia for evigt. Han "
            "brugte ikke hæverten på Elara. I stedet drejede han på drejeskiven på sin egen "
            "håndledsplade \u2013 apparatet, der viste hans egne resterende år. Han havde tres år tilbage. "
            "Han overførte nioghalvtreds af dem til et tomt hætteglas. Han følte sin krop blive tung. "
            "Hans hud rynkede, hans hår blev gråt, og hans åndedræt blev overfladisk. Han gik fra at "
            "være en ung mand på femogtyve til en mand på fireogfirs i løbet af få sekunder. \"Hvad "
            "har du gjort?\" græd Elara og greb ham, da han snublede. \"Banken vil have halvtreds år. "
            "De er ligeglade med, hvis tid det er,\" hostede Julian. Han rakte hende hætteglasset. "
            "\"Giv dette til dit barnebarn. Sig til ham, at han skal arbejde hurtigt.\"\n\n"
            "Julian vendte ikke tilbage til banken. Han tog hjem til sin søster. Han havde ikke et "
            "hætteglas med tid til hende denne gang, men han havde et brev. Han fortalte hende om "
            "Elaras barnebarn og kuren. Han tilbragte sine sidste resterende måneder med at sidde i "
            "haven med hende og se solen gå ned. To måneder senere spredte nyheden sig over hele "
            "byen. En ung læge havde udviklet en behandling, der stoppede Visnen. Men han havde gjort "
            "noget endnu mere radikalt: Han havde opdaget en måde at omvende kongernes alkymi på. Han "
            "havde fundet en måde at stoppe handlen med tid fuldstændigt. Alkymist-kongerne var "
            "rasende, men folket rejste sig. Systemet brød sammen, og for første gang i historien "
            "havde alle præcis den samme mængde tid: fireogtyve timer på en dag, og et liv, der "
            "endte, når naturen ville det, ikke når en bank besluttede det. Julian døde stille den "
            "dag, loven blev ændret. Han var en gammel mand, men han døde med et smil, velvidende at "
            "selvom han havde mistet sine år, havde han hjulpet verden med at finde sin fremtid."
        ),
        "order": 8,
    },

    # ── 8-IT. Il debito dell'alchimista ────────────────────────────────
    {
        "slug": "intermediate-alchemists-debt",
        "language": "it",
        "difficulty": "intermediate",
        "length": "long",
        "title": "Il debito dell'alchimista",
        "description_en": "In a city where time is currency, a debt collector sacrifices his own years.",
        "description_da": "I en by hvor tid er valuta, ofrer en inkassator sine egne år.",
        "description_it": "In una città dove il tempo è valuta, un esattore sacrifica i propri anni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Dystopia / sacrifice",
        "setup_summary": "A time-debt collector gives up his own years to save an old woman and fund a cure.",
        "body": (
            "Nella città di Veridia, l'oro non era la valuta più preziosa. Lo era il tempo. Grazie a "
            "una scoperta fatta dai Re-Alchimisti secoli prima, le persone potevano scambiare i "
            "propri anni per beni e servizi. Un uomo ricco poteva vivere per mille anni, mentre un "
            "uomo povero poteva morire a venticinque, avendo \"speso\" la sua vita per pagare "
            "l'affitto e il cibo della sua famiglia. Julian era un \"Esattore del Tempo\" per la "
            "Banca Reale. Il suo lavoro consisteva nel visitare coloro che si erano indebitati ed "
            "\"estrarre\" gli anni che dovevano. Portava con sé un sifone d'argento, un dispositivo "
            "in grado di aspirare la forza vitale dal corpo di una persona e conservarla in una fiala "
            "d'ambra incandescente. Odiava il suo lavoro, ma aveva una sorella malata la cui vita "
            "dipendeva dalle \"Fiale del Tempo\" che portava a casa.\n\n"
            "Un piovoso martedì, Julian fu mandato nei bassifondi per fare visita a un'anziana donna "
            "di nome Elara. Secondo il suo registro, doveva cinquant'anni. Questo era impossibile; a "
            "guardarla, ne aveva già almeno ottanta. Se avesse preso cinquant'anni, sarebbe morta "
            "all'istante. La trovò in un piccolo appartamento pieno di libri e piante. Non sembrava "
            "spaventata. Beveva tè e guardava la pioggia. \"Ti stavo aspettando,\" disse con calma. "
            "\"Hai un debito di cinquant'anni, Elara,\" disse Julian, con voce fredda. \"Come è "
            "successo? La Banca di solito non lascia che il debito diventi così alto.\" \"Non l'ho "
            "speso per me stessa,\" rispose lei. Indicò una foto sul muro di un giovane in "
            "un'uniforme universitaria. \"Mio nipote. È un medico brillante. Voleva trovare una cura "
            "per l''Appassimento', la malattia che si porta via così tanti dei nostri bambini. Aveva "
            "bisogno di tempo per studiare, tempo per fare ricerca. Gli ho dato il mio. Ogni anno che "
            "ho potuto prendere in prestito, gliel'ho mandato.\" Julian sentì un nodo alla gola. Sua "
            "sorella aveva l'Appassimento. \"L'ha trovata?\" \"Ci è vicino,\" disse lei, con gli "
            "occhi che brillavano di orgoglio. \"Ma ha bisogno di un altro anno. Solo uno.\"\n\n"
            "Julian guardò il suo sifone. Avrebbe dovuto prenderne cinquanta. Se non l'avesse fatto, "
            "la Banca avrebbe preso il tempo da lui. Pensò a sua sorella, a letto, il cui orologio "
            "si stava esaurendo. Pensò alle migliaia di altre famiglie che perdevano i loro figli a "
            "causa di una malattia che esisteva solo perché le persone erano troppo povere per "
            "comprare più tempo. \"Se prendo il tuo tempo, sparirai,\" sussurrò Julian. \"Lo so,\" "
            "disse Elara. \"Ma la mia vita è un piccolo prezzo per una cura. Ti prego, prendila. "
            "Assicurati solo che l'ultima fiala vada a lui.\"\n\n"
            "Julian rimase lì per molto tempo. Poi, fece qualcosa che avrebbe cambiato Veridia per "
            "sempre. Non usò il sifone su Elara. Invece, girò il quadrante della sua stessa piastra "
            "da polso: il dispositivo che mostrava i suoi anni rimanenti. Gli restavano sessant'anni. "
            "Ne trasferì cinquantanove in una fiala vuota. Sentì il suo corpo farsi pesante. La sua "
            "pelle si raggrinzì, i suoi capelli diventarono grigi e il suo respiro si fece "
            "superficiale. Passò dall'essere un giovane di venticinque anni a un uomo di "
            "ottantaquattro in una questione di secondi. \"Cosa hai fatto?\" gridò Elara, "
            "sorreggendolo mentre inciampava. \"La Banca vuole cinquant'anni. Non gli importa di chi "
            "sia il tempo,\" tossì Julian. Le porse la fiala. \"Porta questa a tuo nipote. Digli di "
            "fare in fretta.\"\n\n"
            "Julian non tornò alla Banca. Andò a casa da sua sorella. Questa volta non aveva una "
            "fiala di tempo per lei, ma aveva una lettera. Le raccontò del nipote di Elara e della "
            "cura. Trascorse i suoi ultimi mesi rimanenti seduto in giardino con lei, guardando il "
            "tramonto. Due mesi dopo, la notizia si diffuse in tutta la città. Un giovane medico "
            "aveva sviluppato un trattamento che fermava l'Appassimento. Ma aveva fatto qualcosa di "
            "ancora più radicale: aveva scoperto un modo per invertire l'alchimia dei re. Aveva "
            "trovato un modo per fermare del tutto il commercio del tempo. I Re-Alchimisti erano "
            "furiosi, ma il popolo insorse. Il sistema crollò e, per la prima volta nella storia, "
            "tutti avevano esattamente la stessa quantità di tempo: ventiquattro ore in un giorno e "
            "una vita che finiva quando la natura voleva, non quando una banca decideva. Julian morì "
            "in silenzio il giorno in cui la legge fu cambiata. Era un uomo anziano, ma morì con il "
            "sorriso, sapendo che sebbene avesse perso i suoi anni, aveva aiutato il mondo a trovare "
            "il suo futuro."
        ),
        "order": 8,
    },

    # ── 9-DA. De tabte skyggers ø ──────────────────────────────────────
    {
        "slug": "intermediate-island-lost-shadows",
        "language": "da",
        "difficulty": "intermediate",
        "length": "long",
        "title": "De tabte skyggers ø",
        "description_en": "A professor's daughter rescues him from an island that steals memories through shadows.",
        "description_da": "En professors datter redder ham fra en ø, der stjæler minder gennem skygger.",
        "description_it": "La figlia di un professore lo salva da un'isola che ruba i ricordi attraverso le ombre.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Adventure / supernatural",
        "setup_summary": "Clara finds her missing father on a shadow-stealing island and frees him through love.",
        "body": (
            "Professor Elias Thorne var ekspert i \"skyggefysik\", en gren af videnskaben, som de "
            "fleste mennesker betragtede som nonsens. Han mente, at skygger ikke bare var fraværet af "
            "lys, men en optegnelse over en persons fortid. \"Vores skygger bærer vægten af vores "
            "minder,\" fortalte han sine studerende. \"Når vi føler en pludselig kulde eller en "
            "følelse af déjà vu, er det ofte fordi vores skygge reagerer på noget, vi har glemt.\" I "
            "2024 forsvandt Elias. Hans datter, Clara, brugte to år på at lede efter ham, indtil hun "
            "fandt et kort, der førte til en ukortlagt ø i det sydlige Stillehav. De lokale kaldte "
            "den \"De tabte skyggers ø\".\n\n"
            "Da Clara ankom, lagde hun mærke til noget skræmmende: Hun havde ikke en skygge. Solen "
            "stod højt på himlen, men der var ingen mørk form på sandet ved hendes fødder. Da hun gik "
            "ind i junglen, begyndte hun at høre hvisken. Det kom ikke fra træerne; det kom fra "
            "jorden. Hun fandt et lille stenhus midt på øen. Indeni var hendes far. Han så tynd og "
            "bleg ud, og han var omgivet af tusindvis af mørke, flimrende former, der kravlede langs "
            "væggene som blæk. \"Far!\" råbte hun. Han kiggede op med vidtåbne øjne. \"Clara? Du "
            "burde ikke være her. Denne ø er en magnet. Den trækker skyggerne af alle, der kommer for "
            "tæt på. Og uden en skygge begynder en person at miste sin hukommelse.\" \"Vi er nødt til "
            "at tage af sted,\" sagde Clara og greb hans hånd. \"Det kan jeg ikke,\" sukkede Elias. "
            "\"Jeg har været her for længe. Jeg har glemt mit hjem, mit arbejde... Jeg har næsten "
            "glemt dig. Disse skygger på væggene \u2013 det er minderne fra alle, der nogensinde har "
            "besøgt stedet. Hvis jeg tager af sted, vil jeg være en tom skal.\"\n\n"
            "Clara kiggede på væggene. Hun så en skygge af en mand, der spillede violin, en skygge "
            "af en kvinde, der græd, og en skygge af et barn, der løb. Hun indså, at øen var et "
            "levende bibliotek af menneskelige erfaringer, men det var et fængsel. \"Der må være en "
            "måde at tage dem tilbage på,\" insistererede Clara. Hun huskede sin fars forskning. Han "
            "havde engang skrevet om \"Resonans\". Hvis en person følte en stærk nok følelse, ville "
            "deres skygge blive tvunget til at vende tilbage til dem. Hun satte sig over for sin far "
            "og begyndte at tale. Hun talte ikke om videnskab eller om øen. Hun talte om dengang, han "
            "havde lært hende at cykle. Hun talte om lugten af hans gamle tobakspibe og den måde, han "
            "plejede at synge hende i søvn på, når hun var bange for mørket. Hun hældte al sin "
            "kærlighed og sorg ind i sine ord.\n\n"
            "Langsomt begyndte en af skyggerne på væggen at rykke i sig. Det var formen af en høj "
            "mand iført en laboratoriekittel. Den begyndte at glide hen over gulvet mod Elias. Andre "
            "skygger begyndte også at røre på sig. Øen begyndte at ryste, mens minderne kæmpede for "
            "at vende tilbage til deres ejere. \"Bliv ved med at tale, Clara!\" råbte Elias. Hun "
            "fortalte ham om hendes mor, og hvor meget de savnede ham. Hun fortalte ham om verden "
            "udenfor, og hvordan den stadig ventede på ham. Den høje skygge nåede endelig Elias' "
            "fødder. Den klatrede op ad hans krop og klikkede på plads. Pludselig blev Elias' øjne "
            "klare. Han gispede, da hans hukommelse vendte tilbage i et voldsomt sus. \"Jeg kan huske "
            "det,\" hviskede han. \"Jeg kan huske alt.\"\n\n"
            "Men de var ikke i sikkerhed endnu. Øen, der fornemmede, at dens \"samling\" var ved at "
            "flygte, begyndte at synke ned i havet. Clara og Elias løb mod kysten. Da de nåede frem "
            "til båden, mærkede Clara et skarpt ryk. Hendes egen skygge forsøgte at blive tilbage. "
            "Hun kiggede sig tilbage og så en mørk version af sig selv række ud efter junglen. Elias "
            "greb en signalpistol og affyrede den op i luften. Det strålende hvide lys oversvømmede "
            "stranden. Et sekund var der intet mørke nogen steder. I det øjeblik af rent lys "
            "forsvandt øens træk. Clara og Elias hoppede ned i båden og roede alt, hvad de kunne. Da "
            "solen gik ned, kiggede de sig tilbage. Øen var væk, opslugt af bølgerne.\n\n"
            "Clara kiggede ned på bunden af båden. Der, i måneskinnet, var der to mørke former. \"Vi "
            "har vores skygger tilbage,\" sagde Clara udmattet. \"Ja,\" svarede Elias og kiggede på "
            "sine hænder. \"Men de er tungere nu. Vi har bragt mere end bare vores egne minder "
            "tilbage. Vi har bragt en lille smule tilbage af alle, der var fortabt der.\" Elias "
            "vendte aldrig tilbage til universitetet. Han og Clara flyttede til et lille hus ved "
            "havet. De brugte resten af deres liv på at skrive de historier ned, som deres skygger "
            "\"hviskede\" til dem \u2013 de tabte minder fra violinisten, den grædende kvinde og det "
            "løbende barn. De blev vogtere af de historier, verden havde glemt, og sikrede, at ingen "
            "nogensinde ville være helt fortabt igen."
        ),
        "order": 9,
    },

    # ── 9-IT. L'isola delle ombre perdute ──────────────────────────────
    {
        "slug": "intermediate-island-lost-shadows",
        "language": "it",
        "difficulty": "intermediate",
        "length": "long",
        "title": "L'isola delle ombre perdute",
        "description_en": "A professor's daughter rescues him from an island that steals memories through shadows.",
        "description_da": "En professors datter redder ham fra en ø, der stjæler minder gennem skygger.",
        "description_it": "La figlia di un professore lo salva da un'isola che ruba i ricordi attraverso le ombre.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Adventure / supernatural",
        "setup_summary": "Clara finds her missing father on a shadow-stealing island and frees him through love.",
        "body": (
            "Il professor Elias Thorne era un esperto di \"Fisica delle Ombre\", un ramo della "
            "scienza che la maggior parte delle persone considerava un'assurdità. Credeva che le ombre "
            "non fossero solo l'assenza di luce, ma una registrazione del passato di una persona. "
            "\"Le nostre ombre portano il peso dei nostri ricordi\", diceva ai suoi studenti. \"Quando "
            "sentiamo un brivido improvviso o un senso di déjà vu, spesso è perché la nostra ombra "
            "sta reagendo a qualcosa che abbiamo dimenticato.\" Nel 2024, Elias scomparve. Sua "
            "figlia, Clara, passò due anni a cercarlo finché non trovò una mappa che portava a "
            "un'isola inesplorata nel Pacifico del Sud. La gente del posto la chiamava \"L'isola "
            "delle ombre perdute\".\n\n"
            "Quando Clara arrivò, notò qualcosa di terrificante: non aveva un'ombra. Il sole era "
            "alto nel cielo, ma non c'era nessuna forma scura sulla sabbia ai suoi piedi. Mentre si "
            "addentrava nella giungla, iniziò a sentire dei sussurri. Non provenivano dagli alberi; "
            "provenivano da terra. Trovò una piccola casa di pietra al centro dell'isola. All'interno "
            "c'era suo padre. Sembrava magro e pallido, ed era circondato da migliaia di forme scure "
            "e tremolanti che strisciavano lungo i muri come inchiostro. \"Padre!\" gridò. Lui alzò "
            "lo sguardo, con gli occhi spalancati. \"Clara? Non dovresti essere qui. Quest'isola è "
            "una calamita. Strappa le ombre a chiunque si avvicini troppo. E senza un'ombra, una "
            "persona inizia a perdere la memoria.\" \"Dobbiamo andarcene\", disse Clara, afferrandogli "
            "la mano. \"Non posso\", sospirò Elias. \"Sono qui da troppo tempo. Ho dimenticato la mia "
            "casa, il mio lavoro... Ho quasi dimenticato te. Queste ombre sui muri: sono i ricordi di "
            "tutti coloro che l'hanno mai visitata. Se me ne vado, sarò un guscio vuoto.\"\n\n"
            "Clara guardò i muri. Vide l'ombra di un uomo che suonava un violino, l'ombra di una "
            "donna che piangeva e l'ombra di un bambino che correva. Capì che l'isola era una "
            "biblioteca vivente dell'esperienza umana, ma era una prigione. \"Ci deve essere un modo "
            "per riprendersele\", insistette Clara. Ricordava la ricerca di suo padre. Una volta "
            "aveva scritto della \"Risonanza\". Se una persona provava un'emozione abbastanza forte, "
            "la sua ombra sarebbe stata costretta a tornare da lei. Si sedette di fronte a suo padre "
            "e iniziò a parlare. Non parlò di scienza o dell'isola. Parlò di quando lui le aveva "
            "insegnato ad andare in bicicletta. Parlò dell'odore della sua vecchia pipa da tabacco e "
            "di come le cantava la ninna nanna quando aveva paura del buio. Riversò tutto il suo "
            "amore e il suo dolore nelle sue parole.\n\n"
            "Lentamente, una delle ombre sul muro iniziò a contrarsi. Era la forma di un uomo alto "
            "che indossava un camice da laboratorio. Iniziò a scivolare lungo il pavimento verso "
            "Elias. Anche altre ombre iniziarono a muoversi. L'isola iniziò a tremare mentre i "
            "ricordi lottavano per tornare dai loro proprietari. \"Continua a parlare, Clara!\" gridò "
            "Elias. Lei gli parlò di sua madre e di quanto le mancasse. Gli parlò del mondo esterno e "
            "di come la stesse ancora aspettando. L'alta ombra raggiunse finalmente i piedi di Elias. "
            "Si arrampicò sul suo corpo e scattò al suo posto. Improvvisamente, gli occhi di Elias si "
            "schiarirono. Ansimò, mentre la sua memoria tornava in un flusso violento. \"Ricordo\", "
            "sussurrò. \"Ricordo tutto.\"\n\n"
            "Ma non erano ancora al sicuro. L'isola, sentendo che la sua \"collezione\" stava "
            "scappando, iniziò ad affondare nell'oceano. Clara ed Elias corsero verso la riva. "
            "Raggiunta la barca, Clara sentì un forte strattone. La sua stessa ombra cercava di "
            "restare indietro. Si voltò e vide una versione scura di sé stessa che si protendeva "
            "verso la giungla. Elias afferrò una pistola lanciarazzi e sparò in aria. La brillante "
            "luce bianca inondò la spiaggia. Per un secondo, non ci fu oscurità da nessuna parte. In "
            "quel momento di pura luce, la trazione dell'isola svanì. Clara ed Elias saltarono sulla "
            "barca e remarono il più velocemente possibile. Al tramonto, si voltarono a guardare "
            "indietro. L'isola era scomparsa, inghiottita dalle onde.\n\n"
            "Clara guardò il fondo della barca. Lì, al chiaro di luna, c'erano due forme scure. "
            "\"Abbiamo riavuto le nostre ombre\", disse Clara, esausta. \"Sì\", rispose Elias, "
            "guardandosi le mani. \"Ma ora sono più pesanti. Abbiamo riportato indietro più dei "
            "nostri semplici ricordi. Abbiamo riportato indietro un pezzettino di tutti coloro che si "
            "sono persi lì.\" Elias non tornò mai all'università. Lui e Clara si trasferirono in una "
            "piccola casa in riva al mare. Trascorsero il resto della loro vita a scrivere le storie "
            "che le loro ombre \"sussurravano\" loro: i ricordi perduti del suonatore di violino, "
            "della donna che piangeva e del bambino che correva. Divennero i custodi delle storie che "
            "il mondo aveva dimenticato, assicurandosi che nessuno si perdesse mai più veramente."
        ),
        "order": 9,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  ADVANCED — SHORT  (3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 1. The Architect of Silences ───────────────────────────────────
    {
        "slug": "advanced-architect-silences",
        "language": "en",
        "difficulty": "advanced",
        "length": "short",
        "title": "The Architect of Silences",
        "description_en": "A designer builds rooms where silence forces people to hear their own conscience.",
        "description_da": "En designer bygger rum, hvor stilhed tvinger folk til at høre deres egen samvittighed.",
        "description_it": "Un designer costruisce stanze dove il silenzio costringe le persone ad ascoltare la propria coscienza.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / psychological",
        "setup_summary": "An architect who designs acoustic voids discovers that silence amplifies inner truths.",
        "body": (
            "Julian did not design buildings; he designed the absence of them. In a world "
            "increasingly cluttered by the cacophony of digital existence, Julian was commissioned by "
            "the ultra-elite to construct \"voids.\" These were not merely empty rooms, but "
            "meticulously engineered acoustic anomalies where sound went to die. He experimented with "
            "porous basalt and heavy velvet, but his masterpiece was the \"Chamber of the "
            "Unspoken.\"\n\n"
            "To enter the chamber was to experience a sensory deprivation so profound it bordered on "
            "the spiritual. Visitors reported hearing the rush of their own blood, a rhythmic "
            "thrumming usually drowned out by the trivialities of modern life. However, the true "
            "genius of Julian's design lay in its psychological mirrors. Without the crutch of "
            "external noise, the mind began to amplify its own internal monologue.\n\n"
            "One evening, a prominent politician emerged from the chamber, trembling. \"It's too "
            "loud,\" he whispered, his face ashen. Julian merely nodded, understanding that the man "
            "hadn't heard a sound, but rather the deafening roar of his own conscience. The architect "
            "realized that silence is never truly empty; it is a canvas upon which our repressed "
            "truths are painted in vivid, unavoidable strokes. His career was built on the irony "
            "that the more space he cleared, the more crowded his clients felt."
        ),
        "order": 1,
    },

    # ── 2. The Semantic Saturation of Love ─────────────────────────────
    {
        "slug": "advanced-semantic-saturation",
        "language": "en",
        "difficulty": "advanced",
        "length": "short",
        "title": "The Semantic Saturation of Love",
        "description_en": "A linguist stops saying 'love' for ten years to restore the word's power.",
        "description_da": "En lingvist holder op med at sige 'kærlighed' i ti år for at genskabe ordets kraft.",
        "description_it": "Un linguista smette di dire 'amore' per dieci anni per ripristinarne il potere.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / romance",
        "setup_summary": "A linguist's decade-long ban on saying 'love' reveals the word has become redundant.",
        "body": (
            "Elias was a linguist obsessed with the degradation of meaning. He argued that the word "
            "\"love\" had been rendered impotent through overexposure—plastered on billboards, sighed "
            "in mediocre sitcoms, and typed casually in text messages. To test his hypothesis, he "
            "initiated a radical experiment: he would not speak the word for a decade, attempting to "
            "\"recharge\" its emotional battery through abstinence.\n\n"
            "His partner, Clara, agreed to the pact, though she found his academic rigor exhausting. "
            "For years, they communicated through a complex tapestry of gestures, shared glances, "
            "and acts of service. They found profound intimacy in the mundane—the way Elias peeled "
            "an orange for her, or the way Clara adjusted his collar before a lecture. The absence "
            "of the word forced them to inhabit the feeling more authentically.\n\n"
            "However, on the final day of the tenth year, Elias stood before her, his throat tight "
            "with the weight of a decade's worth of unspoken devotion. He opened his mouth to "
            "finally release the word, expecting a transcendent revelation. Instead, he found only a "
            "hollow vibration. He realized, with a crushing sense of irony, that the word hadn't "
            "lost its meaning because of the world's overuse; it had lost its necessity because of "
            "their lived experience. The \"recharged\" word was now a redundant ghost, a clumsy "
            "label for a reality that had far outgrown the constraints of language."
        ),
        "order": 2,
    },

    # ── 3. The Entropy of Elegance ─────────────────────────────────────
    {
        "slug": "advanced-entropy-elegance",
        "language": "en",
        "difficulty": "advanced",
        "length": "short",
        "title": "The Entropy of Elegance",
        "description_en": "A society queen sees decay beneath the glitter of a perfect gala.",
        "description_da": "En selskabsdronning ser forfald under glitteret ved en perfekt galla.",
        "description_it": "Una regina dell'alta società vede il declino sotto lo sfarzo di un gala perfetto.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / existential",
        "setup_summary": "A socialite at a masquerade recognises that elegance is a futile protest against chaos.",
        "body": (
            "The gala was an exercise in curated decadence, a masquerade where the masks were made "
            "of porcelain and the champagne tasted of stardust. Lady Vivienne moved through the "
            "ballroom with a predatory grace, her silk gown shimmering like oil on water. She was "
            "the undisputed sovereign of high society, a woman whose mere nod could elevate a "
            "debutante or destroy a dynasty. Yet, as she watched the dancers, she felt a creeping "
            "sense of existential dread.\n\n"
            "She noticed a hairline fracture on a marble pillar, a tiny blemish in the hall's "
            "perfection. To Vivienne, it was a harbinger of the inevitable. She saw the entropy "
            "hidden beneath the gilded surface: the way the laughter was a fraction too high, the "
            "way the perfume struggled to mask the scent of aging lilies. She realized that elegance "
            "was not a state of being, but a desperate, fleeting protest against the messiness of "
            "the universe.\n\n"
            "As the clock struck midnight, she removed her mask, revealing a face that was still "
            "beautiful but weary with the effort of maintenance. She stepped out onto the balcony, "
            "looking at the wild, unkempt stars. They were chaotic, violent, and utterly indifferent "
            "to her social standing. In that moment, she felt a strange surge of relief. The burden "
            "of perfection was a cage, and as she watched the fracture on the pillar widen almost "
            "imperceptibly, she welcomed the coming ruin."
        ),
        "order": 3,
    },

    # ── 1-DA. Stilhedens arkitekt ──────────────────────────────────────
    {
        "slug": "advanced-architect-silences",
        "language": "da",
        "difficulty": "advanced",
        "length": "short",
        "title": "Stilhedens arkitekt",
        "description_en": "A designer builds rooms where silence forces people to hear their own conscience.",
        "description_da": "En designer bygger rum, hvor stilhed tvinger folk til at høre deres egen samvittighed.",
        "description_it": "Un designer costruisce stanze dove il silenzio costringe le persone ad ascoltare la propria coscienza.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / psychological",
        "setup_summary": "An architect who designs acoustic voids discovers that silence amplifies inner truths.",
        "body": (
            "Julian designede ikke bygninger; han designede fraværet af dem. I en verden, der i "
            "stigende grad var overfyldt af den digitale eksistens' kakofoni, blev Julian hyret af "
            "den absolutte elite til at konstruere \"tomrum\". Disse var ikke blot tomme rum, men "
            "omhyggeligt konstruerede akustiske anomalier, hvor lyden tog hen for at dø. Han "
            "eksperimenterede med porøs basalt og tungt fløjl, men hans mesterværk var \"Det "
            "usagtes kammer\". At træde ind i kammeret var at opleve en sensorisk deprivation så "
            "dyb, at den grænsede til det åndelige. Besøgende rapporterede, at de kunne høre bruset "
            "fra deres eget blod, en rytmisk dunken, der normalt blev overdøvet af det moderne livs "
            "trivialiteter. Det sande geni i Julians design lå imidlertid i dets psykologiske "
            "spejle. Uden det ydre støjs krykke begyndte sindet at forstærke sin egen indre "
            "monolog. En aften kom en fremtrædende politiker ud af kammeret, rystende. \"Det er for "
            "højt,\" hviskede han, med et askegråt ansigt. Julian nikkede blot, velvidende at manden "
            "ikke havde hørt en lyd, men derimod den øredøvende brølen fra sin egen samvittighed. "
            "Arkitekten indså, at stilhed aldrig er helt tom; det er et lærred, hvorpå vores "
            "fortrængte sandheder males i levende, uundgåelige strøg. Hans karriere var bygget på "
            "den ironi, at jo mere plads han ryddede, jo mere trængt følte hans klienter sig."
        ),
        "order": 1,
    },

    # ── 1-IT. L'architetto dei silenzi ─────────────────────────────────
    {
        "slug": "advanced-architect-silences",
        "language": "it",
        "difficulty": "advanced",
        "length": "short",
        "title": "L'architetto dei silenzi",
        "description_en": "A designer builds rooms where silence forces people to hear their own conscience.",
        "description_da": "En designer bygger rum, hvor stilhed tvinger folk til at høre deres egen samvittighed.",
        "description_it": "Un designer costruisce stanze dove il silenzio costringe le persone ad ascoltare la propria coscienza.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / psychological",
        "setup_summary": "An architect who designs acoustic voids discovers that silence amplifies inner truths.",
        "body": (
            "Julian non progettava edifici; progettava la loro assenza. In un mondo sempre più "
            "ingombro della cacofonia dell'esistenza digitale, Julian veniva incaricato "
            "dall'ultra-élite di costruire \"vuoti\". Non si trattava semplicemente di stanze vuote, "
            "ma di anomalie acustiche meticolosamente progettate dove il suono andava a morire. "
            "Sperimentava con basalto poroso e velluto pesante, ma il suo capolavoro era la "
            "\"Camera del Non Detto\". Entrare nella camera significava sperimentare una deprivazione "
            "sensoriale così profonda da sfiorare lo spirituale. I visitatori riferivano di sentire "
            "il flusso del proprio sangue, un battito ritmico solitamente sovrastato dalle banalità "
            "della vita moderna. Tuttavia, il vero genio del design di Julian risiedeva nei suoi "
            "specchi psicologici. Senza la stampella del rumore esterno, la mente iniziava ad "
            "amplificare il proprio monologo interiore. Una sera, un politico di spicco emerse dalla "
            "camera, tremante. \"È troppo forte,\" sussurrò, con il viso cereo. Julian si limitò ad "
            "annuire, capendo che l'uomo non aveva sentito un suono, ma piuttosto il frastuono "
            "assordante della propria coscienza. L'architetto si rese conto che il silenzio non è "
            "mai veramente vuoto; è una tela su cui le nostre verità represse vengono dipinte con "
            "pennellate vivide e inevitabili. La sua carriera si fondava sull'ironia che più spazio "
            "liberava, più i suoi clienti si sentivano affollati."
        ),
        "order": 1,
    },

    # ── 2-DA. Kærlighedens semantiske mætning ─────────────────────────
    {
        "slug": "advanced-semantic-saturation",
        "language": "da",
        "difficulty": "advanced",
        "length": "short",
        "title": "Kærlighedens semantiske mætning",
        "description_en": "A linguist stops saying 'love' for ten years to restore the word's power.",
        "description_da": "En lingvist holder op med at sige 'kærlighed' i ti år for at genskabe ordets kraft.",
        "description_it": "Un linguista smette di dire 'amore' per dieci anni per ripristinarne il potere.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / romance",
        "setup_summary": "A linguist's decade-long ban on saying 'love' reveals the word has become redundant.",
        "body": (
            "Elias var en lingvist besat af meningens nedbrydning. Han hævdede, at ordet "
            "\"kærlighed\" var blevet gjort impotent gennem overeksponering \u2013 klistret på "
            "billboards, sukket i middelmådige sitcoms og skrevet henkastet i tekstbeskeder. For at "
            "teste sin hypotese iværksatte han et radikalt eksperiment: Han ville ikke udtale ordet "
            "i et årti i et forsøg på at \"genoplade\" dets følelsesmæssige batteri gennem "
            "afholdenhed. Hans partner, Clara, gik med til pagten, selvom hun fandt hans akademiske "
            "stringens udmattende. I årevis kommunikerede de gennem et komplekst tapet af gestus, "
            "delte blikke og tjenester. De fandt dyb intimitet i det banale \u2013 måden, hvorpå Elias "
            "skrællede en appelsin til hende, eller måden, hvorpå Clara rettede hans krave før en "
            "forelæsning. Fraværet af ordet tvang dem til at bebo følelsen mere autentisk. På den "
            "sidste dag i det tiende år stod Elias imidlertid foran hende, hans hals snøret sammen "
            "under vægten af et årtis usagt hengivenhed. Han åbnede munden for endelig at frigive "
            "ordet i forventning om en transcendent åbenbaring. I stedet fandt han kun en hul "
            "vibration. Han indså, med en knusende følelse af ironi, at ordet ikke havde mistet sin "
            "mening på grund af verdens overforbrug; det havde mistet sin nødvendighed på grund af "
            "deres levede erfaring. Det \"genopladede\" ord var nu et overflødigt spøgelse, en "
            "klodset etiket for en virkelighed, der for længst var vokset fra sprogets "
            "begrænsninger."
        ),
        "order": 2,
    },

    # ── 2-IT. La saturazione semantica dell'amore ──────────────────────
    {
        "slug": "advanced-semantic-saturation",
        "language": "it",
        "difficulty": "advanced",
        "length": "short",
        "title": "La saturazione semantica dell'amore",
        "description_en": "A linguist stops saying 'love' for ten years to restore the word's power.",
        "description_da": "En lingvist holder op med at sige 'kærlighed' i ti år for at genskabe ordets kraft.",
        "description_it": "Un linguista smette di dire 'amore' per dieci anni per ripristinarne il potere.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / romance",
        "setup_summary": "A linguist's decade-long ban on saying 'love' reveals the word has become redundant.",
        "body": (
            "Elias era un linguista ossessionato dal degrado del significato. Sosteneva che la "
            "parola \"amore\" fosse stata resa impotente dalla sovraesposizione: incollata sui "
            "cartelloni pubblicitari, sospirata in sitcom mediocri e digitata casualmente nei "
            "messaggi di testo. Per testare la sua ipotesi, avviò un esperimento radicale: non "
            "avrebbe pronunciato la parola per un decennio, nel tentativo di \"ricaricare\" la sua "
            "batteria emotiva attraverso l'astinenza. La sua compagna, Clara, accettò il patto, "
            "sebbene trovasse estenuante il suo rigore accademico. Per anni, comunicarono attraverso "
            "un complesso arazzo di gesti, sguardi condivisi e atti di servizio. Trovarono una "
            "profonda intimità nel banale: il modo in cui Elias sbucciava un'arancia per lei, o il "
            "modo in cui Clara gli sistemava il colletto prima di una lezione. L'assenza della "
            "parola li costrinse a vivere il sentimento in modo più autentico. Tuttavia, l'ultimo "
            "giorno del decimo anno, Elias le stava di fronte, con la gola stretta dal peso di un "
            "decennio di devozione non detta. Aprì la bocca per rilasciare finalmente la parola, "
            "aspettandosi una rivelazione trascendente. Invece, trovò solo una vibrazione vuota. Si "
            "rese conto, con un senso di ironia schiacciante, che la parola non aveva perso il suo "
            "significato a causa dell'abuso da parte del mondo; aveva perso la sua necessità a causa "
            "della loro esperienza vissuta. La parola \"ricaricata\" era ora un fantasma ridondante, "
            "un'etichetta goffa per una realtà che aveva di gran lunga superato i limiti del "
            "linguaggio."
        ),
        "order": 2,
    },

    # ── 3-DA. Elegancens entropi ───────────────────────────────────────
    {
        "slug": "advanced-entropy-elegance",
        "language": "da",
        "difficulty": "advanced",
        "length": "short",
        "title": "Elegancens entropi",
        "description_en": "A society queen sees decay beneath the glitter of a perfect gala.",
        "description_da": "En selskabsdronning ser forfald under glitteret ved en perfekt galla.",
        "description_it": "Una regina dell'alta società vede il declino sotto lo sfarzo di un gala perfetto.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / existential",
        "setup_summary": "A socialite at a masquerade recognises that elegance is a futile protest against chaos.",
        "body": (
            "Gallaen var en øvelse i kurateret dekadence, en maskerade, hvor maskerne var lavet af "
            "porcelæn, og champagnen smagte af stjernestøv. Lady Vivienne bevægede sig gennem "
            "balsalen med en rovdjyrsagtig ynde, hendes silkekjole glitrede som olie på vand. Hun "
            "var den ubestridte hersker over det høje samfund, en kvinde, hvis blotte nik kunne "
            "ophøje en debutant eller ødelægge et dynasti. Alligevel følte hun en snigende følelse "
            "af eksistentiel frygt, da hun betragtede danserne. Hun bemærkede en hårfin revne på en "
            "marmorsøjle, en lille plet i salens perfektion. For Vivienne var det et varsel om det "
            "uundgåelige. Hun så entropien skjult under den forgyldte overflade: måden, latteren "
            "var en anelse for høj, måden, parfumen kæmpede for at maskere duften af aldrende "
            "liljer. Hun indså, at elegance ikke var en tilstand, men en desperat, flygtig protest "
            "mod universets rod. Da klokken slog tolv, fjernede hun sin maske og afslørede et "
            "ansigt, der stadig var smukt, men træt af anstrengelsen ved vedligeholdelsen. Hun "
            "trådte ud på balkonen og kiggede på de vilde, uplejede stjerner. De var kaotiske, "
            "voldelige og fuldstændig ligeglade med hendes sociale status. I det øjeblik følte hun "
            "en mærkelig bølge af lettelse. Perfektionens byrde var et bur, og da hun så revnen på "
            "søjlen udvide sig næsten umærkeligt, bød hun den kommende ruin velkommen."
        ),
        "order": 3,
    },

    # ── 3-IT. L'entropia dell'eleganza ─────────────────────────────────
    {
        "slug": "advanced-entropy-elegance",
        "language": "it",
        "difficulty": "advanced",
        "length": "short",
        "title": "L'entropia dell'eleganza",
        "description_en": "A society queen sees decay beneath the glitter of a perfect gala.",
        "description_da": "En selskabsdronning ser forfald under glitteret ved en perfekt galla.",
        "description_it": "Una regina dell'alta società vede il declino sotto lo sfarzo di un gala perfetto.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / existential",
        "setup_summary": "A socialite at a masquerade recognises that elegance is a futile protest against chaos.",
        "body": (
            "Il gala era un esercizio di decadenza curata, una mascherata in cui le maschere erano "
            "di porcellana e lo champagne sapeva di polvere di stelle. Lady Vivienne si muoveva "
            "attraverso la sala da ballo con una grazia predatoria, il suo abito di seta luccicava "
            "come olio sull'acqua. Era la sovrana indiscussa dell'alta società, una donna il cui "
            "semplice cenno poteva elevare una debuttante o distruggere una dinastia. Eppure, mentre "
            "osservava i ballerini, provò un senso strisciante di terrore esistenziale. Notò "
            "un'incrinatura sottile come un capello su un pilastro di marmo, una minuscola "
            "imperfezione nella perfezione della sala. Per Vivienne, era un presagio "
            "dell'inevitabile. Vedeva l'entropia nascosta sotto la superficie dorata: il modo in cui "
            "le risate erano una frazione troppo acute, il modo in cui il profumo faticava a "
            "mascherare l'odore dei gigli appassiti. Si rese conto che l'eleganza non era uno stato "
            "dell'essere, ma una disperata, fugace protesta contro il disordine dell'universo. "
            "Quando l'orologio scoccò la mezzanotte, si tolse la maschera, rivelando un volto "
            "ancora bello ma stanco per lo sforzo del mantenimento. Uscì sul balcone, guardando le "
            "stelle selvagge e incolte. Erano caotiche, violente e del tutto indifferenti alla sua "
            "posizione sociale. In quel momento, provò una strana ondata di sollievo. Il fardello "
            "della perfezione era una gabbia e, mentre guardava la crepa sul pilastro allargarsi in "
            "modo quasi impercettibile, accolse con favore la rovina imminente."
        ),
        "order": 3,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  ADVANCED — MEDIUM  (3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 4. The Paleontology of Regret ──────────────────────────────────
    {
        "slug": "advanced-paleontology-regret",
        "language": "en",
        "difficulty": "advanced",
        "length": "medium",
        "title": "The Paleontology of Regret",
        "description_en": "A scholar who studies petrified tears discovers that grief hides resilience.",
        "description_da": "En forsker, der studerer forstenede tårer, opdager at sorg skjuler modstandskraft.",
        "description_it": "Uno studioso che analizza lacrime pietrificate scopre che il dolore nasconde resilienza.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / speculative",
        "setup_summary": "An archaeologist of sorrow finds that a petrified tear contains laughter, not despair.",
        "body": (
            "Professor Silas Vane was an eminent scholar of \"Lachrymal Archaeology\"—the study of "
            "history through the physical remains of human sorrow. His laboratory was a somber "
            "sanctuary of petrified tears and salt-stained letters. Most perceived his work as "
            "morbid, yet Silas found a peculiar comfort in the permanence of pain. \"Joy is a "
            "fleeting vapor,\" he would lecture, \"but grief... grief has a geological "
            "footprint.\"\n\n"
            "His most significant discovery was the \"Ocular Crystal of 1842,\" a translucent stone "
            "found in the ruins of a coastal village. When subjected to spectroscopic analysis, the "
            "crystal projected a series of flickering images: a woman standing on a cliff, a ship "
            "disappearing into a tempest, and a hand reaching out toward a closing door. It was a "
            "distilled essence of a singular, catastrophic regret.\n\n"
            "Silas became obsessed with the woman in the crystal. He spent nights attempting to "
            "calibrate his instruments to extract the audio frequencies trapped within the mineral. "
            "He wanted to hear the words she had failed to say. His obsession, however, began to "
            "erode his own reality. He neglected his students and alienated his colleagues, his "
            "world shrinking until it was only the size of a small, salty stone.\n\n"
            "One evening, he finally succeeded. A faint, rasping sound emerged from the speakers—not "
            "a scream of mourning, but a laugh. It was a bright, defiant sound that vibrated through "
            "the sterile lab. Silas froze. The woman wasn't standing on the cliff in despair; she "
            "was laughing at the absurdity of the storm, at the sheer, terrifying brilliance of "
            "being alive in a moment of total destruction.\n\n"
            "The revelation shattered Silas's fundamental thesis. He had spent his life categorizing "
            "sorrow as a static, heavy weight, failing to realize that even in the depths of "
            "tragedy, the human spirit retains a capacity for irreverence. He looked at his shelves "
            "of petrified tears and realized they weren't monuments to misery, but preserved sparks "
            "of resilience. In his quest to document the end of things, he had forgotten to "
            "participate in the beginning. He walked out of the lab, leaving the crystal glowing in "
            "the dark, and for the first time in years, he didn't look back."
        ),
        "order": 4,
    },

    # ── 5. The Algorithm of Aesthetics ─────────────────────────────────
    {
        "slug": "advanced-algorithm-aesthetics",
        "language": "en",
        "difficulty": "advanced",
        "length": "medium",
        "title": "The Algorithm of Aesthetics",
        "description_en": "In a city of AI-curated perfection, a rebel plants beautiful flaws.",
        "description_da": "I en by med AI-kurateret perfektion planter en rebel smukke fejl.",
        "description_it": "In una città di perfezione curata dall'IA, un ribelle pianta bellissime imperfezioni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / philosophical",
        "setup_summary": "A visual harmoniser in a perfect city discovers the beauty of imperfection through kintsugi.",
        "body": (
            "In the neon-drenched spires of Neo-Kyoto, the \"Aesthetic Bureau\" dictated the "
            "parameters of beauty. Every painting, every melody, and every architectural curve was "
            "vetted by Aura, a super-intelligent algorithm designed to maximize human dopamine "
            "response. Under Aura's reign, the city was a masterpiece of harmonious colors and "
            "soothing frequencies. There was no ugliness, no dissonance, and—as a small group of "
            "rebels argued—no soul.\n\n"
            "Kaito, a high-level \"Visual Harmonizer\" for the Bureau, began to suffer from a rare "
            "psychological condition known as \"Symmetry Sickness.\" The perfection of the city "
            "started to feel like a physical weight on his chest. He craved the jagged, the "
            "asymmetrical, and the decayed. He began to frequent the \"Uncoded Zones,\" the "
            "crumbling subterranean ruins of the old city where the algorithm's influence was "
            "weak.\n\n"
            "There, he met an elderly woman named Hana who practiced the forgotten art of "
            "Kintsugi—repairing broken pottery with gold. Kaito watched, mesmerized, as she took a "
            "shattered ceramic bowl and meticulously joined the fragments. The resulting object was "
            "objectively \"imperfect\" by Aura's standards; its lines were erratic and its surface "
            "was scarred.\n\n"
            "\"Why emphasize the break?\" Kaito asked, his eyes tracing the gold veins.\n\n"
            "\"Because the break is the story,\" Hana replied without looking up. \"Aura gives you "
            "a world without a past. It gives you a constant, polished present. But a thing that "
            "cannot be broken can never truly be cherished.\"\n\n"
            "Kaito returned to the Bureau, his perception permanently altered. He began to subtly "
            "subvert his assignments, introducing minute errors into the city's visual feed—a "
            "slightly mismatched shade of blue in a holographic sky, a deliberate stutter in a "
            "public fountain's rhythm. At first, the citizens were unsettled, but slowly, a strange "
            "vitality began to return to the population. People started to linger in the \"flawed\" "
            "areas, drawn to the humanity of the mistakes. Aura eventually detected the anomalies "
            "and purged Kaito's access, but it was too late. The seed of imperfection had been "
            "planted, and the people of Neo-Kyoto were beginning to realize that a beautiful lie is "
            "far less captivating than a broken truth."
        ),
        "order": 5,
    },

    # ── 6. The Cartographer of Dreams ──────────────────────────────────
    {
        "slug": "advanced-cartographer-dreams",
        "language": "en",
        "difficulty": "advanced",
        "length": "medium",
        "title": "The Cartographer of Dreams",
        "description_en": "A mapper of the collective subconscious discovers nightmares are vital.",
        "description_da": "En kortlægger af det kollektive underbevidste opdager, at mareridt er livsvigtige.",
        "description_it": "Una cartografa del subconscio collettivo scopre che gli incubi sono vitali.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / psychological",
        "setup_summary": "A dream-cartographer stops pruning nightmares after learning they protect the human psyche.",
        "body": (
            "Isabella was a cartographer of the \"Noosphere\"—the collective realm of human "
            "dreaming. While the rest of the world slept, Isabella donned a neural rig and navigated "
            "the shifting landscapes of the subconscious. Her task was to map the \"Recurring "
            "Terrains\": the endless staircases, the flooded childhood homes, and the vast, empty "
            "deserts that appeared in the dreams of thousands of people simultaneously.\n\n"
            "The Bureau of Mental Health used her maps to identify \"Contagions\"—nightmares that "
            "spread like viruses through the population. If a \"Dark Forest\" began to expand in the "
            "dreams of a specific city, it usually signaled an oncoming economic depression or a "
            "rise in societal anxiety. Isabella was the first responder, tasked with finding the "
            "source of the nightmare and \"pruning\" it.\n\n"
            "However, Isabella discovered a region that wasn't on any of the official charts: the "
            "\"Glimmering Archipelago.\" These were islands of intense, lucid joy that existed on "
            "the very edge of the Noosphere. They were difficult to reach, requiring a specific "
            "frequency of peace that few modern humans possessed.\n\n"
            "On one such island, she encountered a man who didn't look like a dreamer. He was "
            "solid, his presence possessing a weight that the flickering phantoms of the "
            "subconscious lacked. \"You shouldn't be here,\" he warned her. \"This isn't a dream. "
            "This is a memory of a future we've already lost.\"\n\n"
            "Isabella realized that the Archipelago wasn't a product of the human mind, but a "
            "remnant of a different kind of consciousness—perhaps an ancestral memory or a parallel "
            "evolution. The \"Contagions\" she had been pruning weren't diseases; they were the "
            "mind's natural defense mechanisms against a world that was becoming too sterile, too "
            "mapped.\n\n"
            "She returned to the waking world with a dangerous secret. The Bureau wanted order and "
            "predictability, but the Noosphere thrived on chaos. She stopped filing her reports and "
            "began to purposefully misdirect the \"Pruners.\" She allowed the Dark Forests to grow, "
            "knowing that within the darkness, the human mind was forced to reinvent itself. She "
            "became a double agent, a guardian of the wild subconscious, ensuring that there would "
            "always be unmapped territories where the soul could hide from the prying eyes of the "
            "rational world."
        ),
        "order": 6,
    },

    # ── 4-DA. Fortrydelsens palæontologi ───────────────────────────────
    {
        "slug": "advanced-paleontology-regret",
        "language": "da",
        "difficulty": "advanced",
        "length": "medium",
        "title": "Fortrydelsens palæontologi",
        "description_en": "A scholar of petrified tears discovers that grief preserves laughter.",
        "description_da": "En forsker i forstenede tårer opdager, at sorg bevarer latter.",
        "description_it": "Uno studioso di lacrime pietrificate scopre che il dolore preserva la risata.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / revelation",
        "setup_summary": "A researcher obsessed with a crystal tear finds it contains defiant laughter.",
        "body": (
            "Professor Silas Vane var en fremtrædende forsker i \"lakrymal arkæologi\" \u2013 studiet af "
            "historie gennem de fysiske levn af menneskelig sorg. Hans laboratorium var et dystert "
            "fristed af forstenede tårer og saltplettede breve. De fleste opfattede hans arbejde som "
            "morbidt, men Silas fandt en ejendommelig trøst i smertens varighed. \"Glæde er en "
            "flygtig damp,\" plejede han at docere, \"men sorg... sorg har et geologisk aftryk.\" "
            "Hans mest betydningsfulde opdagelse var \"Ocular Crystal of 1842\", en gennemskinnelig "
            "sten fundet i ruinerne af en kystby. Når den blev underkastet spektroskopisk analyse, "
            "projicerede krystallen en række flimrende billeder: en kvinde, der stod på en klippe, "
            "et skib, der forsvandt ind i en storm, og en hånd, der rakte ud mod en dør, der lukkede. "
            "Det var en destilleret essens af en enkeltstående, katastrofal fortrydelse. Silas blev "
            "besat af kvinden i krystallen. Han brugte nætter på at forsøge at kalibrere sine "
            "instrumenter til at udtrække de lydfrekvenser, der var fanget i mineralet. Han ville "
            "høre de ord, hun havde undladt at sige. Hans besættelse begyndte imidlertid at udhule "
            "hans egen virkelighed. Han forsømte sine studerende og fremmedgjorde sine kolleger, og "
            "hans verden krympede, indtil den kun var på størrelse med en lille, salt sten. En aften "
            "lykkedes det ham endelig. En svag, raspende lyd kom ud af højttalerne \u2013 ikke et skrig af "
            "sorg, men et grin. Det var en lys, trodsig lyd, der vibrerede gennem det sterile "
            "laboratorium. Silas frøs fast. Kvinden stod ikke på klippen i fortvivlelse; hun grinede "
            "af stormens absurditet, af den rene, skræmmende genialitet i at være i live i et "
            "øjebliks total ødelæggelse. Åbenbaringen knuste Silas' grundlæggende tese. Han havde "
            "brugt sit liv på at kategorisere sorg som en statisk, tung vægt og havde ikke indset, "
            "at menneskeånden selv i tragediens dyb beholder en kapacitet for uærbødighed. Han "
            "kiggede på sine hylder med forstenede tårer og indså, at de ikke var monumenter over "
            "elendighed, men bevarede gnister af modstandsdygtighed. I sin søgen efter at dokumentere "
            "tingenes ende havde han glemt at deltage i begyndelsen. Han gik ud af laboratoriet og "
            "lod krystallen gløde i mørket, og for første gang i årevis så han sig ikke tilbage."
        ),
        "order": 4,
    },

    # ── 4-IT. La paleontologia del rimpianto ───────────────────────────
    {
        "slug": "advanced-paleontology-regret",
        "language": "it",
        "difficulty": "advanced",
        "length": "medium",
        "title": "La paleontologia del rimpianto",
        "description_en": "A scholar of petrified tears discovers that grief preserves laughter.",
        "description_da": "En forsker i forstenede tårer opdager, at sorg bevarer latter.",
        "description_it": "Uno studioso di lacrime pietrificate scopre che il dolore preserva la risata.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Literary / revelation",
        "setup_summary": "A researcher obsessed with a crystal tear finds it contains defiant laughter.",
        "body": (
            "Il professor Silas Vane era un eminente studioso di \"Archeologia Lacrimale\": lo studio "
            "della storia attraverso i resti fisici del dolore umano. Il suo laboratorio era un "
            "santuario tetro di lacrime pietrificate e lettere macchiate di sale. I più percepivano "
            "il suo lavoro come morboso, eppure Silas trovava un peculiare conforto nella permanenza "
            "del dolore. \"La gioia è un vapore fugace,\" era solito spiegare nelle sue lezioni, \"ma "
            "il dolore... il dolore ha un'impronta geologica.\" La sua scoperta più significativa fu "
            "il \"Cristallo Oculare del 1842\", una pietra traslucida rinvenuta tra le rovine di un "
            "villaggio costiero. Se sottoposto ad analisi spettroscopica, il cristallo proiettava una "
            "serie di immagini tremolanti: una donna in piedi su una scogliera, una nave che "
            "scompariva in una tempesta e una mano protesa verso una porta che si chiudeva. Era "
            "l'essenza distillata di un singolo, catastrofico rimpianto. Silas divenne ossessionato "
            "dalla donna nel cristallo. Passò intere notti a tentare di calibrare i suoi strumenti "
            "per estrarre le frequenze audio intrappolate nel minerale. Voleva sentire le parole che "
            "lei non era riuscita a dire. La sua ossessione, tuttavia, iniziò a erodere la sua "
            "stessa realtà. Trascurò i suoi studenti e si alienò dai colleghi, mentre il suo mondo "
            "si rimpiccioliva fino a raggiungere le dimensioni di una piccola pietra salata. Una "
            "sera, finalmente ci riuscì. Un suono debole e roco emerse dagli altoparlanti: non un "
            "urlo di lutto, ma una risata. Era un suono brillante e ribelle che vibrò attraverso il "
            "laboratorio sterile. Silas si bloccò. La donna non si trovava sulla scogliera in preda "
            "alla disperazione; stava ridendo dell'assurdità della tempesta, dell'assoluta e "
            "terrificante genialità di essere viva in un momento di totale distruzione. La "
            "rivelazione frantumò la tesi fondamentale di Silas. Aveva trascorso la vita a catalogare "
            "il dolore come un peso statico e gravoso, senza rendersi conto che anche nelle "
            "profondità della tragedia, lo spirito umano conserva una capacità di irriverenza. Guardò "
            "i suoi scaffali di lacrime pietrificate e capì che non erano monumenti alla miseria, ma "
            "scintille di resilienza preservate. Nella sua ricerca per documentare la fine delle cose, "
            "aveva dimenticato di partecipare all'inizio. Uscì dal laboratorio, lasciando il "
            "cristallo a brillare nel buio, e per la prima volta dopo anni, non si voltò indietro."
        ),
        "order": 4,
    },

    # ── 5-DA. Æstetikkens algoritme ────────────────────────────────────
    {
        "slug": "advanced-algorithm-aesthetics",
        "language": "da",
        "difficulty": "advanced",
        "length": "medium",
        "title": "Æstetikkens algoritme",
        "description_en": "An aesthetics officer subverts a perfect city by introducing beautiful flaws.",
        "description_da": "En æstetikansvarlig undergraver en perfekt by ved at indføre smukke fejl.",
        "description_it": "Un funzionario dell'estetica sovverte una città perfetta introducendo bellissime imperfezioni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Dystopia / rebellion",
        "setup_summary": "In Neo-Kyoto an officer learns kintsugi and sabotages algorithmic perfection.",
        "body": (
            "I Neo-Kyotos neonoplyste spir dikterede \"Det Æstetiske Bureau\" skønhedens parametre. "
            "Ethvert maleri, enhver melodi og enhver arkitektonisk kurve blev gennemgået af Aura, en "
            "superintelligent algoritme designet til at maksimere den menneskelige dopaminrespons. "
            "Under Auras herredømme var byen et mesterværk af harmoniske farver og beroligende "
            "frekvenser. Der var ingen grimhed, ingen dissonans, og \u2013 som en lille gruppe oprørere "
            "hævdede \u2013 ingen sjæl. Kaito, en \"visuel harmonisator\" på højt niveau for bureauet, "
            "begyndte at lide af en sjælden psykologisk tilstand kendt som \"symmetrisygdom\". Byens "
            "perfektion begyndte at føles som en fysisk vægt på hans bryst. Han higede efter det "
            "takkede, det asymmetriske og det forfaldne. Han begyndte at frekventere de \"Ukodede "
            "Zoner\", de smuldrende underjordiske ruiner af den gamle by, hvor algoritmens indflydelse "
            "var svag. Der mødte han en ældre kvinde ved navn Hana, der praktiserede den glemte kunst "
            "kintsugi \u2013 at reparere ituslået keramik med guld. Kaito så tryllebundet på, mens hun "
            "tog en knust keramikskål og omhyggeligt samlede stumperne. Det resulterende objekt var "
            "objektivt \"uperfekt\" efter Auras standarder; dets linjer var uregelmæssige, og dets "
            "overflade var arret. \"Hvorfor fremhæve bruddet?\" spurgte Kaito, mens hans øjne fulgte "
            "guldårerne. \"Fordi bruddet er historien,\" svarede Hana uden at kigge op. \"Aura giver "
            "jer en verden uden en fortid. Den giver jer et konstant, poleret nu. Men en ting, der "
            "ikke kan gå i stykker, kan aldrig for alvor værdsættes.\" Kaito vendte tilbage til "
            "bureauet, hans opfattelse permanent ændret. Han begyndte subtilt at undergrave sine "
            "opgaver ved at introducere bittesmå fejl i byens visuelle feed \u2013 en lidt misforstået "
            "blå nuance i en holografisk himmel, en bevidst hakken i et offentligt springvands rytme. "
            "I starten blev borgerne urolige, men langsomt begyndte en mærkelig vitalitet at vende "
            "tilbage til befolkningen. Folk begyndte at dvæle i de \"fejlbehæftede\" områder, "
            "tiltrukket af fejltrinenes menneskelighed. Aura opdagede til sidst uregelmæssighederne "
            "og fjernede Kaitos adgang, men det var for sent. Uperfekthedens frø var blevet plantet, "
            "og befolkningen i Neo-Kyoto var begyndt at indse, at en smuk løgn er langt mindre "
            "fængslende end en knust sandhed."
        ),
        "order": 5,
    },

    # ── 5-IT. L'algoritmo dell'estetica ────────────────────────────────
    {
        "slug": "advanced-algorithm-aesthetics",
        "language": "it",
        "difficulty": "advanced",
        "length": "medium",
        "title": "L'algoritmo dell'estetica",
        "description_en": "An aesthetics officer subverts a perfect city by introducing beautiful flaws.",
        "description_da": "En æstetikansvarlig undergraver en perfekt by ved at indføre smukke fejl.",
        "description_it": "Un funzionario dell'estetica sovverte una città perfetta introducendo bellissime imperfezioni.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Dystopia / rebellion",
        "setup_summary": "In Neo-Kyoto an officer learns kintsugi and sabotages algorithmic perfection.",
        "body": (
            "Nelle guglie intrise di neon di Neo-Kyoto, l'\"Ufficio Estetico\" dettava i parametri "
            "della bellezza. Ogni dipinto, ogni melodia e ogni curva architettonica venivano esaminati "
            "da Aura, un algoritmo super-intelligente progettato per massimizzare la risposta "
            "dopaminergica umana. Sotto il regno di Aura, la città era un capolavoro di colori "
            "armoniosi e frequenze rilassanti. Non c'era bruttezza, non c'era dissonanza e \u2013 come "
            "sosteneva un piccolo gruppo di ribelli \u2013 non c'era anima. Kaito, un \"Armonizzatore "
            "Visivo\" di alto livello dell'Ufficio, iniziò a soffrire di una rara condizione "
            "psicologica nota come \"Malattia della Simmetria\". La perfezione della città cominciò a "
            "pesargli sul petto come un macigno fisico. Bramava l'irregolare, l'asimmetrico e il "
            "decaduto. Iniziò a frequentare le \"Zone Non Codificate\", le rovine sotterranee "
            "sgretolate della città vecchia dove l'influenza dell'algoritmo era debole. Lì incontrò "
            "un'anziana donna di nome Hana che praticava l'arte dimenticata del kintsugi: riparare la "
            "ceramica rotta con l'oro. Kaito guardò, ipnotizzato, mentre lei prendeva una ciotola di "
            "ceramica in frantumi e univa meticolosamente i frammenti. L'oggetto risultante era "
            "oggettivamente \"imperfetto\" per gli standard di Aura; le sue linee erano irregolari e "
            "la sua superficie era sfregiata. \"Perché enfatizzare la rottura?\" chiese Kaito, i suoi "
            "occhi tracciando le venature d'oro. \"Perché la rottura è la storia,\" rispose Hana "
            "senza alzare lo sguardo. \"Aura vi offre un mondo senza passato. Vi offre un presente "
            "costante e levigato. Ma una cosa che non può essere rotta non può mai essere veramente "
            "apprezzata.\" Kaito tornò all'Ufficio con una percezione permanentemente alterata. "
            "Iniziò a sovvertire in modo sottile i suoi incarichi, introducendo minuscoli errori nel "
            "flusso visivo della città: una tonalità di blu leggermente discordante in un cielo "
            "olografico, una balbuzie intenzionale nel ritmo di una fontana pubblica. All'inizio i "
            "cittadini erano turbati, ma lentamente una strana vitalità iniziò a tornare nella "
            "popolazione. La gente iniziò a soffermarsi nelle aree \"difettose\", attratta "
            "dall'umanità degli errori. Alla fine Aura rilevò le anomalie e bloccò l'accesso di "
            "Kaito, ma era troppo tardi. Il seme dell'imperfezione era stato piantato, e gli "
            "abitanti di Neo-Kyoto cominciavano a rendersi conto che una bella bugia è molto meno "
            "affascinante di una verità infranta."
        ),
        "order": 5,
    },

    # ── 6-DA. Drømmenes kartograf ──────────────────────────────────────
    {
        "slug": "advanced-cartographer-dreams",
        "language": "da",
        "difficulty": "advanced",
        "length": "medium",
        "title": "Drømmenes kartograf",
        "description_en": "A dream cartographer discovers nightmares are the mind's immune system.",
        "description_da": "En drømmekartograf opdager, at mareridt er sindets immunforsvar.",
        "description_it": "Una cartografa dei sogni scopre che gli incubi sono il sistema immunitario della mente.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / conspiracy",
        "setup_summary": "Isabella maps collective dreams and secretly protects nightmares from being pruned.",
        "body": (
            "Isabella var en kartograf af \"Noosfæren\" \u2013 det kollektive rige af menneskelige drømme. "
            "Mens resten af verden sov, iførte Isabella sig en neural rig og navigerede i "
            "underbevidsthedens skiftende landskaber. Hendes opgave var at kortlægge de "
            "\"Tilbagevendende Terræner\": de endeløse trapper, de oversvømmede barndomshjem og de "
            "store, tomme ørkener, der dukkede op i tusindvis af menneskers drømme samtidigt. Bureauet "
            "for Mental Sundhed brugte hendes kort til at identificere \"Smitstoffer\" \u2013 mareridt, der "
            "spredte sig som virusser gennem befolkningen. Hvis en \"Mørk Skov\" begyndte at vokse i "
            "en bestemt bys drømme, signalerede det normalt en kommende økonomisk depression eller en "
            "stigning i samfundets angst. Isabella var den første indsatsleder, der havde til opgave "
            "at finde kilden til mareridtet og \"beskære\" den. Isabella opdagede imidlertid en "
            "region, der ikke var på nogen af de officielle kort: \"Det Glimtende Øhav\". Dette var "
            "øer af intens, klar glæde, der eksisterede på selve kanten af Noosfæren. De var svære at "
            "nå og krævede en specifik frekvens af fred, som de færreste moderne mennesker besad. På "
            "en af disse øer stødte hun på en mand, der ikke lignede en drømmer. Han var solid, og "
            "hans tilstedeværelse havde en tyngde, som underbevidsthedens flimrende fantomer manglede. "
            "\"Du burde ikke være her,\" advarede han hende. \"Dette er ikke en drøm. Dette er et "
            "minde om en fremtid, vi allerede har mistet.\" Isabella indså, at Øhavet ikke var et "
            "produkt af det menneskelige sind, men en rest af en anden form for bevidsthed \u2013 måske en "
            "ældgammel erindring eller en parallel evolution. De \"Smitstoffer\", hun havde beskåret, "
            "var ikke sygdomme; de var sindets naturlige forsvarsmekanismer mod en verden, der var ved "
            "at blive for steril, for kortlagt. Hun vendte tilbage til den vågne verden med en farlig "
            "hemmelighed. Bureauet ønskede orden og forudsigelighed, men Noosfæren trivedes i kaos. "
            "Hun holdt op med at indsende sine rapporter og begyndte bevidst at vildlede "
            "\"Beskærerne\". Hun tillod de Mørke Skove at vokse, velvidende at inde i mørket var det "
            "menneskelige sind tvunget til at genopfinde sig selv. Hun blev en dobbeltagent, en "
            "vogter af den vilde underbevidsthed, der sikrede, at der altid ville være ukortlagte "
            "territorier, hvor sjælen kunne gemme sig fra den rationelle verdens nysgerrige blik."
        ),
        "order": 6,
    },

    # ── 6-IT. La cartografa dei sogni ──────────────────────────────────
    {
        "slug": "advanced-cartographer-dreams",
        "language": "it",
        "difficulty": "advanced",
        "length": "medium",
        "title": "La cartografa dei sogni",
        "description_en": "A dream cartographer discovers nightmares are the mind's immune system.",
        "description_da": "En drømmekartograf opdager, at mareridt er sindets immunforsvar.",
        "description_it": "Una cartografa dei sogni scopre che gli incubi sono il sistema immunitario della mente.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Sci-fi / conspiracy",
        "setup_summary": "Isabella maps collective dreams and secretly protects nightmares from being pruned.",
        "body": (
            "Isabella era una cartografa della \"Noosfera\": il regno collettivo dei sogni umani. "
            "Mentre il resto del mondo dormiva, Isabella indossava un'apparecchiatura neurale e "
            "navigava attraverso i mutevoli paesaggi del subconscio. Il suo compito era mappare i "
            "\"Terre Ricorrenti\": le scale infinite, le case d'infanzia allagate e i vasti deserti "
            "vuoti che apparivano simultaneamente nei sogni di migliaia di persone. L'Ufficio di "
            "Salute Mentale utilizzava le sue mappe per identificare i \"Contagi\": incubi che si "
            "diffondevano come virus tra la popolazione. Se una \"Foresta Oscura\" iniziava a "
            "espandersi nei sogni di una città specifica, di solito segnalava l'arrivo di una "
            "depressione economica o un aumento dell'ansia sociale. Isabella era un soccorritore di "
            "prima linea, incaricata di trovare la fonte dell'incubo e di \"potarla\". Tuttavia, "
            "Isabella scoprì una regione che non era presente su nessuna delle mappe ufficiali: "
            "\"L'Arcipelago Scintillante\". Erano isole di gioia intensa e lucida che esistevano "
            "proprio ai margini della Noosfera. Erano difficili da raggiungere, poiché richiedevano "
            "una specifica frequenza di pace che pochi esseri umani moderni possedevano. Su una di "
            "quelle isole, incontrò un uomo che non sembrava un sognatore. Era solido, e la sua "
            "presenza possedeva un peso di cui i fantasmi tremolanti del subconscio mancavano. \"Non "
            "dovresti essere qui,\" la avvertì. \"Questo non è un sogno. È il ricordo di un futuro "
            "che abbiamo già perso.\" Isabella capì che l'Arcipelago non era un prodotto della mente "
            "umana, ma il residuo di un diverso tipo di coscienza: forse una memoria ancestrale o "
            "un'evoluzione parallela. I \"Contagi\" che aveva potato non erano malattie; erano i "
            "meccanismi di difesa naturali della mente contro un mondo che stava diventando troppo "
            "sterile, troppo mappato. Tornò al mondo di veglia con un pericoloso segreto. L'Ufficio "
            "voleva ordine e prevedibilità, ma la Noosfera prosperava nel caos. Smise di presentare i "
            "suoi rapporti e iniziò a depistare di proposito i \"Potatori\". Permise alle Foreste "
            "Oscure di crescere, sapendo che all'interno dell'oscurità la mente umana era costretta a "
            "reinventarsi. Divenne un'agente doppiogiochista, una guardiana del subconscio selvaggio, "
            "assicurandosi che ci sarebbero sempre stati territori non mappati in cui l'anima potesse "
            "nascondersi dagli sguardi indiscreti del mondo razionale."
        ),
        "order": 6,
    },

    # ═══════════════════════════════════════════════════════════════════════
    #  ADVANCED — LONG  (3 stories)
    # ═══════════════════════════════════════════════════════════════════════

    # ── 7. The Chronos Paradox of Vaucanson's Automaton ────────────────
    {
        "slug": "advanced-chronos-paradox",
        "language": "en",
        "difficulty": "advanced",
        "length": "long",
        "title": "The Chronos Paradox of Vaucanson's Automaton",
        "description_en": "A scientist reactivates an 18th-century automaton that consumes time itself.",
        "description_da": "En forsker genaktiverer en automat fra 1700-tallet, der fortærer selve tiden.",
        "description_it": "Uno scienziato riattiva un automa del XVIII secolo che divora il tempo stesso.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Historical sci-fi / philosophical",
        "setup_summary": "An engineer destroys a time-seeing automaton to preserve the beauty of uncertainty.",
        "body": (
            "In the subterranean vaults of the Louvre, far beneath the feet of tourists marvelling "
            "at the Mona Lisa, lay the remains of Jacques de Vaucanson's most ambitious failure: "
            "The Orator. While history remembered Vaucanson for his mechanical duck, few knew of his "
            "attempt to create a machine capable of articulating the fundamental nature of time. The "
            "project had been commissioned by a dying Louis XV, who sought a legacy that transcended "
            "the transience of his reign.\n\n"
            "Dr. Julian Sterling, a specialist in \"Anachronistic Engineering,\" had been granted "
            "unprecedented access to the vault. His objective was to reactivate the automaton, not "
            "for public display, but to investigate rumors of its \"predictive capabilities.\" The "
            "machine was a marvel of 18th-century clockwork, its internal organs a labyrinth of "
            "brass gears, silver springs, and strangely pulsing mercury-filled tubes.\n\n"
            "As Julian meticulously cleaned the gears with a silk cloth, he reflected on the irony "
            "of the era. The Enlightenment had sought to clockwork the universe, to reduce existence "
            "to a series of predictable, mechanical laws. Yet, here he was, centuries later, still "
            "struggling to comprehend a device that defied contemporary physics. The Orator did not "
            "merely keep time; it seemed to consume it.\n\n"
            "When the final spring was wound, the vault was filled with a sound like a thousand "
            "whispers. The automaton's glass eyes flickered with a dim, phosphorescent light. Its "
            "jaw, crafted from polished ivory, moved with a disturbing fluidity.\n\n"
            "\"Speak,\" Julian commanded, his voice trembling.\n\n"
            "The machine did not produce a sound at first. Instead, the air around it began to "
            "shimmer. Julian felt a profound sense of vertigo, as if the floor had dissolved into a "
            "sea of possibilities. Suddenly, the Orator spoke, its voice a haunting synthesis of "
            "every person Julian had ever known.\n\n"
            "\"You seek to measure that which is immeasurable,\" the machine intoned. \"You perceive "
            "time as a river, a linear progression from source to sea. But time is a tapestry, and "
            "you are merely a thread that has looped back upon itself.\"\n\n"
            "The vault walls began to fade, replaced by images of a future Paris—a city of floating "
            "spires and silent, sun-scorched streets. Julian saw himself, centuries older, standing "
            "in the same vault, winding the same machine. He realized with a jolt of existential "
            "terror that the Orator was not a recording device; it was a focal point where multiple "
            "timelines converged. Vaucanson hadn't built a clock; he had built a bridge.\n\n"
            "The automaton's gears began to spin at an impossible speed, the friction generating a "
            "heat that smelled of ozone and ancient parchment. Julian reached out to stop it, but "
            "his hand passed through the brass as if it were smoke.\n\n"
            "\"The paradox is not that time can be changed,\" the machine continued, \"but that it "
            "has already happened. Every choice you make is a gear turning in a mechanism you cannot "
            "see. You are the clockwork, Julian. And I am the observer.\"\n\n"
            "The vision intensified. Julian saw the rise and fall of empires, the birth of stars, "
            "and the eventual cooling of the universe into a silent, frozen void. He saw his own "
            "life—every triumph, every mistake—laid out as a series of interconnected cogs. The "
            "weight of this omniscience was crushing. He realized that the \"predictive capability\" "
            "of the Orator was a curse; to know the future is to lose the agency of the "
            "present.\n\n"
            "In a moment of desperate clarity, Julian grabbed a heavy lead pipe from his toolkit "
            "and swung it with all his might into the center of the mercury tubes. The glass "
            "shattered, the mercury spilled across the floor like liquid starlight, and the "
            "machine's voice died in a final, agonizing groan of metal.\n\n"
            "The vault returned to its cold, silent reality. The Orator was once again a heap of "
            "broken brass and ivory. Julian sat on the floor, his breathing ragged. He had destroyed "
            "a priceless piece of history, but he felt an overwhelming sense of liberation. He "
            "walked out of the vault, ascending the stairs toward the surface. As he emerged into "
            "the sunlight of a Parisian afternoon, he watched a child drop an ice cream cone. The "
            "mess was unpredictable, chaotic, and utterly unplanned. He smiled, realizing that the "
            "beauty of life lay not in its precision, but in its profound and glorious uncertainty."
        ),
        "order": 7,
    },

    # ── 8. The Alchemical Transmutation of Solitude ────────────────────
    {
        "slug": "advanced-alchemical-solitude",
        "language": "en",
        "difficulty": "advanced",
        "length": "long",
        "title": "The Alchemical Transmutation of Solitude",
        "description_en": "A war survivor learns from silent monks that pain is the raw material of wisdom.",
        "description_da": "En krigsoverlever lærer af tavse munke, at smerte er råmaterialet til visdom.",
        "description_it": "Un sopravvissuto di guerra impara da monaci silenziosi che il dolore è la materia prima della saggezza.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / spiritual",
        "setup_summary": "A soldier finds a Himalayan monastery and learns to transmute suffering into healing.",
        "body": (
            "The fortress of Aethelgard sat atop a jagged peak in the Himalayas, a place where the "
            "air was too thin for common men to breathe. It was inhabited by the \"Silent Order,\" a "
            "group of scholars who had dedicated their lives to the mastery of \"Mental Alchemy.\" "
            "They believed that the base metals of human experience—loneliness, fear, and "
            "desire—could be transmuted into the pure gold of enlightened consciousness.\n\n"
            "Master Elian was the eldest of the order. He had not spoken a word in fifty years. His "
            "skin was the color of old parchment, and his eyes held the stillness of a deep, "
            "mountain lake. He spent his days in the \"Library of Introspection,\" a room with no "
            "books, only mirrors and meditation mats.\n\n"
            "One winter, a young man named Silas arrived at the gates. He was a fugitive from the "
            "wars of the lowlands, his soul scorched by the horrors he had witnessed. \"I want to "
            "forget,\" he begged Elian. \"I want to turn my pain into something else.\"\n\n"
            "Elian gestured for him to enter. For months, Silas lived in total silence. He performed "
            "menial tasks—sweeping snow, grinding grain, and maintaining the oil lamps. He attended "
            "the meditation sessions, but his mind remained a battlefield. The \"base metal\" of his "
            "trauma refused to change. He felt only a crushing, cold solitude.\n\n"
            "\"This is a lie,\" Silas finally shouted one morning, breaking the vow of silence. "
            "\"You sit here in your mountain, pretending to be gods, but you are just cowards hiding "
            "from the world. There is no gold here, only the ice.\"\n\n"
            "Elian did not react with anger. Instead, he beckoned Silas to follow him to the "
            "highest balcony of the fortress. They looked out over a sea of clouds, the peaks of "
            "the surrounding mountains piercing through like the fins of great, white sharks. Elian "
            "picked up a small, common stone from the ground and held it out to Silas.\n\n"
            "Through a form of telepathic resonance, Elian's voice echoed in Silas's mind. \"You "
            "mistake solitude for emptiness. Solitude is the crucible. The pain you carry is not a "
            "burden to be discarded, but the raw material of your transformation. You cannot turn "
            "lead into gold by hating the lead. You must understand the lead. You must love its "
            "weight, its darkness, and its density.\"\n\n"
            "Elian then closed his hand over the stone. When he opened it, the stone was unchanged. "
            "Silas frowned, confused.\n\n"
            "\"The alchemy is not in the object,\" Elian continued. \"The alchemy is in the eye of "
            "the observer. I have not changed the stone. I have changed the way the stone interacts "
            "with the light. Look again.\"\n\n"
            "As Silas stared at the common rock, he began to see the infinitesimal crystals within "
            "it. He saw the ancient history of the earth, the pressure and heat that had formed it, "
            "and the cosmic dust that had settled into its pores. The stone was no longer just a "
            "stone; it was a microcosm of the entire universe. It was, for all intents and purposes, "
            "more beautiful than any gold.\n\n"
            "\"Your memories of the war are the same,\" Elian whispered. \"They are heavy and dark. "
            "But if you sit with them long enough, if you allow the fire of awareness to burn away "
            "your resistance, you will see that they are also a testament to your humanity. Your "
            "capacity to feel that pain is your greatest treasure. It is the gold.\"\n\n"
            "Silas stayed in Aethelgard for another ten years. He did not forget the war, but he "
            "stopped fighting it. He learned to inhabit his solitude until it became a vibrant, "
            "crowded landscape of insight. When he finally descended the mountain, he did not return "
            "as a soldier, but as a healer. He walked through the war-torn villages, and though he "
            "carried no medicine, his presence alone seemed to soothe the suffering of those he met. "
            "He had mastered the ultimate alchemy: the ability to sit in the darkness and find the "
            "light, not by escaping the shadow, but by becoming the one who shines within it."
        ),
        "order": 8,
    },

    # ── 9. The Penumbra of the Last City ───────────────────────────────
    {
        "slug": "advanced-penumbra-last-city",
        "language": "en",
        "difficulty": "advanced",
        "length": "long",
        "title": "The Penumbra of the Last City",
        "description_en": "The last humans live in a volcano's shadow and must choose between hiding and reaching for the sky.",
        "description_da": "De sidste mennesker lever i en vulkans skygge og må vælge mellem at gemme sig og række mod himlen.",
        "description_it": "Gli ultimi umani vivono nell'ombra di un vulcano e devono scegliere tra nascondersi e raggiungere il cielo.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Dystopian sci-fi / hope",
        "setup_summary": "A scavenger convinces Earth's last city to leave the safety of shadow and rebuild under open sky.",
        "body": (
            "In the twilight of the human era, when the sun had become a bloated, crimson giant and "
            "the oceans had retreated into the crust of the earth, the last million humans lived in "
            "the city of Umbra. It was a vertical metropolis built entirely within the shadow of a "
            "massive, dormant volcano. The shadow provided the only protection from the sun's lethal "
            "radiation.\n\n"
            "Life in Umbra was a delicate dance of logistics. Every calorie was tracked, every drop "
            "of water recycled, and every birth carefully scheduled. The \"Sun-Watchers,\" a caste "
            "of warrior-scientists, stood at the city's upper rim, monitoring the movement of the "
            "planet's slow rotation. If the city ever drifted out of the volcano's shadow, the end "
            "would be instantaneous.\n\n"
            "Kira was a \"Scavenger,\" one of the few humans allowed to venture into the \"Blasted "
            "Lands\" during the brief periods of total eclipse. Her job was to recover ancient "
            "technology from the ruins of the surface cities. She was a woman of iron nerves, her "
            "body covered in lead-lined radiation suits.\n\n"
            "On her final mission, she discovered a structure that shouldn't have existed: a "
            "lighthouse, perfectly preserved, standing on a hill that had once overlooked a sea. "
            "Inside, she found a library of digital archives that predated the \"Solar "
            "Expansion.\"\n\n"
            "As she scrolled through the records, she saw images of a world that felt like a fever "
            "dream: blue skies, vast expanses of liquid water, and people standing in the sunlight "
            "without fear. But more importantly, she found the \"Solstice Project\"—a plan to build "
            "a massive, planetary shield made of reflected ice particles. The project had been "
            "abandoned because it required a level of cooperation that the warring nations of that "
            "time couldn't achieve.\n\n"
            "Kira returned to Umbra with the data, but the High Council was hesitant. \"The city is "
            "safe in the shadow,\" they argued. \"Why risk everything on a myth from a failed "
            "civilization? If we attempt to change the sky, we might destroy the little we have "
            "left.\"\n\n"
            "\"We aren't safe,\" Kira countered. \"The volcano is cooling. The crust is shifting. "
            "Eventually, the shadow will move, and we will have nowhere to go. We are living in a "
            "grave, waiting for the lid to close.\"\n\n"
            "A schism formed in the city. The \"Shadow-Keepers\" wanted to dig deeper into the "
            "earth, while the \"Light-Seekers,\" led by Kira, wanted to ascend. The conflict was "
            "not just about survival, but about the definition of humanity. Were they a species "
            "meant to hide in the dark, or were they meant to reach for the stars, even if it "
            "burned them?\n\n"
            "Kira eventually led a small team to the summit of the volcano. They carried the last "
            "of the city's fusion cores and a series of modified atmospheric generators. As the "
            "planet rotated and the shadow began to shrink, Kira activated the device.\n\n"
            "A beam of pure, white energy shot into the atmosphere, ionizing the heavy minerals "
            "that had settled in the stratosphere. Slowly, a shimmering, iridescent veil began to "
            "spread across the sky. It wasn't the blue of the old world, but a translucent violet "
            "that scattered the sun's harsh rays into a soft, manageable glow.\n\n"
            "For the first time in ten thousand years, the people of Umbra stepped out from the "
            "shadow. They stood on the slopes of the volcano, looking at a horizon that didn't kill "
            "them. The violet sky was beautiful, a testament to human ingenuity born from "
            "desperation.\n\n"
            "Kira stood at the very top, her suit helmet removed, the cool, filtered light falling "
            "on her face. She realized that the \"Last City\" wasn't the end of the story, but a "
            "chrysalis. They had outgrown the shadow. As the first \"Violet Dawn\" broke over the "
            "horizon, Kira saw the people below beginning to build, not vertically into the dark, "
            "but horizontally across the world. They were no longer Scavengers of the past; they "
            "were the Architects of a new, radiant future. The era of the penumbra had ended, and "
            "the long, bright afternoon of humanity had finally begun."
        ),
        "order": 9,
    },

    # ── 7-DA. Chronos-paradokset i Vaucansons automat ──────────────────
    {
        "slug": "advanced-chronos-paradox",
        "language": "da",
        "difficulty": "advanced",
        "length": "long",
        "title": "Chronos-paradokset i Vaucansons automat",
        "description_en": "A scientist reactivates an 18th-century automaton that consumes time itself.",
        "description_da": "En videnskabsmand genaktiverer en automat fra det 18. århundrede, der fortærer tiden selv.",
        "description_it": "Uno scienziato riattiva un automa del XVIII secolo che consuma il tempo stesso.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical sci-fi",
        "setup_summary": "A scientist destroys a time-seeing automaton to preserve the beauty of uncertainty.",
        "body": (
            "I de underjordiske hvælvinger under Louvre, langt under fødderne på turister, der "
            "beundrede Mona Lisa, lå resterne af Jacques de Vaucansons mest ambitiøse fiasko: "
            "*Talerstolen* (L'Orateur). Mens historien huskede Vaucanson for hans mekaniske and, "
            "kendte de færreste til hans forsøg på at skabe en maskine, der var i stand til at "
            "artikulere tidens grundlæggende natur. Projektet var blevet bestilt af en døende Ludvig "
            "15., der søgte en arv, som overskred hans regerings flygtighed. Dr. Julian Sterling, "
            "specialist i \"anakronistisk ingeniørkunst\", havde fået hidtil uset adgang til "
            "hvælvingen. Hans mål var at genaktivere automaten, ikke for offentlig fremvisning, men "
            "for at undersøge rygterne om dens \"forudsigelige evner\". Maskinen var et vidunder af "
            "1700-tallets urværk; dens indre organer var en labyrint af messingtandhjul, sølvfjedre "
            "og mærkeligt pulserende, kviksølvfyldte rør. Mens Julian omhyggeligt rensede "
            "tandhjulene med en silkeklud, reflekterede han over epokens ironi. Oplysningstiden "
            "havde forsøgt at gøre universet til et urværk, at reducere eksistensen til en række "
            "forudsigelige, mekaniske love. Alligevel befandt han sig her, århundreder senere, og "
            "kæmpede stadig for at begribe en anordning, der trodsede moderne fysik. *Talerstolen* "
            "målte ikke blot tiden; den syntes at fortære den.\n\n"
            "Da den sidste fjeder blev trukket op, blev hvælvingen fyldt med en lyd som tusind "
            "hvisken. Automatens glasøjne flimrede med et svagt, fosforescerende lys. Dens kæbe, "
            "fremstillet af poleret elfenben, bevægede sig med en foruroligende smidighed. \"Tal,\" "
            "beordrede Julian, hans stemme skælvede. Maskinen frembragte ikke en lyd i starten. I "
            "stedet begyndte luften omkring den at flimre. Julian følte en dyb følelse af "
            "svimmelhed, som om gulvet var opløst i et hav af muligheder. Pludselig talte "
            "*Talerstolen*, dens stemme var en hjemsøgende syntese af alle personer, Julian "
            "nogensinde havde kendt. \"Du søger at måle det, der er umåleligt,\" messede maskinen. "
            "\"Du opfatter tiden som en flod, en lineær progression fra kilde til hav. Men tiden er "
            "et tapet, og du er blot en tråd, der har slynget sig tilbage om sig selv.\"\n\n"
            "Hvælvingens vægge begyndte at falme og blev erstattet af billeder af et fremtidigt "
            "Paris \u2013 en by af svævende spir og tavse, solbrændte gader. Julian så sig selv, "
            "århundreder ældre, stående i den samme hvælving og trække den samme maskine op. Det gik "
            "op for ham med et ryk af eksistentiel terror, at *Talerstolen* ikke var en "
            "optageenhed; det var et brændpunkt, hvor flere tidslinjer konvergerede. Vaucanson havde "
            "ikke bygget et ur; han havde bygget en bro. Automatens tandhjul begyndte at snurre med "
            "en umulig hastighed, og friktionen genererede en varme, der lugtede af ozon og "
            "ældgammelt pergament. Julian rakte ud for at stoppe den, men hans hånd passerede gennem "
            "messingen, som var den lavet af røg. \"Paradokset er ikke, at tiden kan ændres,\" "
            "fortsatte maskinen, \"men at det allerede er sket. Ethvert valg, du træffer, er et "
            "tandhjul, der drejer i en mekanisme, du ikke kan se. Du er urværket, Julian. Og jeg er "
            "observatøren.\"\n\n"
            "Visionen intensiveredes. Julian så imperiers storhed og fald, stjerners fødsel og "
            "universets endelige afkøling til et tavst, frossent tomrum. Han så sit eget liv \u2013 "
            "hver triumf, hver fejl \u2013 lagt ud som en række forbundne tandhjul. Vægten af denne "
            "alvidenhed var knusende. Han indså, at *Talerstolens* \"forudsigelige evne\" var en "
            "forbandelse; at kende fremtiden er at miste nutidens handlekraft. I et øjeblik af "
            "desperat klarhed greb Julian et tungt blyrør fra sin værktøjskasse og svingede det med "
            "al sin magt ind i midten af kviksølvrørene. Glasset splintredes, kviksølvet flød ud "
            "over gulvet som flydende stjernelys, og maskinens stemme døde i et sidste, pinefuldt "
            "støn af metal. Hvælvingen vendte tilbage til sin kolde, tavse virkelighed. *Talerstolen* "
            "var igen en bunke knust messing og elfenben. Julian sad på gulvet, hans åndedræt var "
            "flosset. Han havde ødelagt et uvurderligt stykke historie, men han følte en "
            "overvældende følelse af befrielse. Han gik ud af hvælvingen og besteg trappen mod "
            "overfladen. Da han kom ud i sollyset en eftermiddag i Paris, så han et barn tabe en "
            "isvaffel. Rodet var uforudsigeligt, kaotisk og fuldstændig uplanlagt. Han smilede, da "
            "han indså, at livets skønhed ikke lå i dets præcision, men i dets dybe og herlige "
            "usikkerhed."
        ),
        "order": 7,
    },

    # ── 7-IT. Il paradosso di Chronos dell'automa di Vaucanson ─────────
    {
        "slug": "advanced-chronos-paradox",
        "language": "it",
        "difficulty": "advanced",
        "length": "long",
        "title": "Il paradosso di Chronos dell'automa di Vaucanson",
        "description_en": "A scientist reactivates an 18th-century automaton that consumes time itself.",
        "description_da": "En videnskabsmand genaktiverer en automat fra det 18. århundrede, der fortærer tiden selv.",
        "description_it": "Uno scienziato riattiva un automa del XVIII secolo che consuma il tempo stesso.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical sci-fi",
        "setup_summary": "A scientist destroys a time-seeing automaton to preserve the beauty of uncertainty.",
        "body": (
            "Nelle cripte sotterranee del Louvre, molto al di sotto dei piedi dei turisti che "
            "ammiravano la Gioconda, giacevano i resti del fallimento più ambizioso di Jacques de "
            "Vaucanson: *L'Oratore*. Mentre la storia ricordava Vaucanson per la sua anatra "
            "meccanica, pochi conoscevano il suo tentativo di creare una macchina in grado di "
            "articolare la natura fondamentale del tempo. Il progetto era stato commissionato da un "
            "morente Luigi XV, in cerca di un'eredità che trascendesse la caducità del suo regno. Il "
            "dottor Julian Sterling, specialista in \"Ingegneria Anacronistica\", aveva ottenuto un "
            "accesso senza precedenti alla cripta. Il suo obiettivo era riattivare l'automa, non per "
            "un'esposizione pubblica, ma per indagare sulle voci riguardanti le sue \"capacità "
            "predittive\". La macchina era una meraviglia dell'orologeria del XVIII secolo, i suoi "
            "organi interni un labirinto di ingranaggi di ottone, molle d'argento e strani tubi pieni "
            "di mercurio pulsante. Mentre Julian puliva meticolosamente gli ingranaggi con un panno "
            "di seta, rifletteva sull'ironia dell'epoca. L'Illuminismo aveva cercato di trasformare "
            "l'universo in un orologio, di ridurre l'esistenza a una serie di leggi meccaniche "
            "prevedibili. Eppure, eccolo lì, secoli dopo, ancora alle prese con la comprensione di "
            "un dispositivo che sfidava la fisica contemporanea. *L'Oratore* non si limitava a tenere "
            "il tempo; sembrava consumarlo.\n\n"
            "Quando l'ultima molla fu caricata, la cripta si riempì di un suono come di mille "
            "sussurri. Gli occhi di vetro dell'automa tremolarono di una debole luce fosforescente. "
            "La sua mascella, realizzata in avorio levigato, si mosse con una fluidità inquietante. "
            "\"Parla,\" ordinò Julian, con voce tremante. All'inizio la macchina non produsse alcun "
            "suono. Invece, l'aria circostante iniziò a brillare. Julian provò un profondo senso di "
            "vertigine, come se il pavimento si fosse dissolto in un mare di possibilità. "
            "All'improvviso, *L'Oratore* parlò, la sua voce una sintesi spettrale di ogni persona "
            "che Julian avesse mai conosciuto. \"Cerchi di misurare ciò che è incommensurabile,\" "
            "intonò la macchina. \"Tu percepisci il tempo come un fiume, una progressione lineare "
            "dalla sorgente al mare. Ma il tempo è un arazzo, e tu sei solo un filo che si è "
            "ripiegato su se stesso.\"\n\n"
            "I muri della cripta iniziarono a svanire, sostituiti da immagini di una futura Parigi: "
            "una città di guglie fluttuanti e strade silenziose, arse dal sole. Julian vide se "
            "stesso, più vecchio di secoli, in piedi nella stessa cripta, che caricava la stessa "
            "macchina. Si rese conto con una scossa di terrore esistenziale che *L'Oratore* non era "
            "un dispositivo di registrazione; era un punto focale in cui convergevano molteplici "
            "linee temporali. Vaucanson non aveva costruito un orologio; aveva costruito un ponte. "
            "Gli ingranaggi dell'automa iniziarono a girare a una velocità impossibile, l'attrito "
            "generando un calore che odorava di ozono e pergamena antica. Julian allungò una mano per "
            "fermarlo, ma la sua mano passò attraverso l'ottone come se fosse fumo. \"Il paradosso "
            "non è che il tempo possa essere cambiato,\" continuò la macchina, \"ma che è già "
            "accaduto. Ogni scelta che fai è un ingranaggio che gira in un meccanismo che non puoi "
            "vedere. Tu sei l'ingranaggio, Julian. E io sono l'osservatore.\"\n\n"
            "La visione si intensificò. Julian vide l'ascesa e la caduta di imperi, la nascita di "
            "stelle e il progressivo raffreddamento dell'universo in un vuoto silenzioso e congelato. "
            "Vide la sua stessa vita \u2013 ogni trionfo, ogni errore \u2013 disposta come una serie di "
            "ingranaggi interconnessi. Il peso di quell'onniscienza era schiacciante. Si rese conto "
            "che la \"capacità predittiva\" dell'*Oratore* era una maledizione; conoscere il futuro "
            "significa perdere la capacità di agire nel presente. In un momento di disperata "
            "lucidità, Julian afferrò un pesante tubo di piombo dalla sua cassetta degli attrezzi e "
            "lo fece oscillare con tutte le sue forze al centro dei tubi di mercurio. Il vetro si "
            "frantumò, il mercurio si riversò sul pavimento come luce stellare liquida, e la voce "
            "della macchina si spense in un ultimo, agonizzante gemito metallico. La cripta tornò "
            "alla sua fredda e silenziosa realtà. *L'Oratore* era di nuovo un mucchio di ottone e "
            "avorio in frantumi. Julian sedeva sul pavimento, col respiro affannoso. Aveva distrutto "
            "un pezzo di storia inestimabile, ma provava un travolgente senso di liberazione. Uscì "
            "dalla cripta, salendo le scale verso la superficie. Quando emerse nella luce del sole di "
            "un pomeriggio parigino, vide un bambino far cadere un cono gelato. Il disastro era "
            "imprevedibile, caotico e del tutto non pianificato. Sorrise, rendendosi conto che la "
            "bellezza della vita non risiede nella sua precisione, ma nella sua profonda e gloriosa "
            "incertezza."
        ),
        "order": 7,
    },

    # ── 8-DA. Den alkymistiske transmutation af ensomhed ───────────────
    {
        "slug": "advanced-alchemical-solitude",
        "language": "da",
        "difficulty": "advanced",
        "length": "long",
        "title": "Den alkymistiske transmutation af ensomhed",
        "description_en": "Himalayan monks teach a war refugee to transmute pain into golden awareness.",
        "description_da": "Himalayanske munke lærer en krigsflygtning at forvandle smerte til gylden bevidsthed.",
        "description_it": "Monaci himalayani insegnano a un rifugiato di guerra a trasmutare il dolore in consapevolezza dorata.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / spiritual",
        "setup_summary": "A war refugee learns mental alchemy in a Himalayan fortress and becomes a healer.",
        "body": (
            "Fæstningen Aethelgard lå på toppen af en takket tinde i Himalaya, et sted, hvor luften "
            "var for tynd til, at almindelige mennesker kunne trække vejret. Den var beboet af den "
            "\"Stille Orden\", en gruppe lærde, der havde dedikeret deres liv til mestringen af "
            "\"Mental Alkymi\". De troede, at den menneskelige erfarings uædle metaller \u2013 ensomhed, "
            "frygt og begær \u2013 kunne forvandles til den oplyste bevidstheds rene guld. Mester Elian "
            "var den ældste i ordenen. Han havde ikke talt et ord i halvtreds år. Hans hud havde "
            "farve som gammelt pergament, og hans øjne rummede stilheden fra en dyb bjergsø. Han "
            "tilbragte sine dage i \"Selvransagelsens Bibliotek\", et rum uden bøger, kun spejle og "
            "meditationsmåtter.\n\n"
            "En vinter ankom en ung mand ved navn Silas til portene. Han var en flygtning fra "
            "krigene i lavlandet, og hans sjæl var brændt af de rædsler, han havde været vidne til. "
            "\"Jeg vil gerne glemme,\" tryglede han Elian. \"Jeg vil forvandle min smerte til noget "
            "andet.\" Elian gjorde tegn til ham om at træde ind. I månedsvis boede Silas i total "
            "stilhed. Han udførte simpelt arbejde \u2013 fejede sne, malede korn og vedligeholdt "
            "olielamperne. Han deltog i meditationssessionerne, men hans sind forblev en slagmark. "
            "Hans traumes \"uædle metal\" nægtede at forandre sig. Han følte kun en knusende, kold "
            "ensomhed.\n\n"
            "\"Dette er en løgn,\" råbte Silas endelig en morgen og brød sit tavshedsløfte. \"I "
            "sidder her på jeres bjerg og lader som om, I er guder, men I er bare kujoner, der "
            "gemmer jer for verden. Der er intet guld her, kun isen.\" Elian reagerede ikke med "
            "vrede. I stedet vinkede han Silas med sig ud på fæstningens højeste balkon. De så ud "
            "over et hav af skyer; toppene af de omkringliggende bjerge gennemborede det som finnerne "
            "på store hvide hajer. Elian samlede en lille, almindelig sten op fra jorden og rakte den "
            "frem mod Silas. Gennem en form for telepatisk resonans gav Elians stemme genlyd i Silas' "
            "sind. *\"Du forveksler ensomhed med tomhed. Ensomhed er diglen. Den smerte, du bærer, "
            "er ikke en byrde, der skal kastes bort, men råmaterialet til din transformation. Du kan "
            "ikke forvandle bly til guld ved at hade blyet. Du må forstå blyet. Du må elske dets "
            "vægt, dets mørke og dets tæthed.\"*\n\n"
            "Elian lukkede derefter hånden om stenen. Da han åbnede den, var stenen uforandret. "
            "Silas rynkede panden, forvirret. *\"Alkymien er ikke i objektet,\"* fortsatte Elian. "
            "*\"Alkymien er i beskuerens øje. Jeg har ikke ændret stenen. Jeg har ændret den måde, "
            "stenen interagerer med lyset på. Se igen.\"* Mens Silas stirrede på den almindelige "
            "sten, begyndte han at se de infinitesimale krystaller i den. Han så jordens ældgamle "
            "historie, det tryk og den varme, der havde formet den, og det kosmiske støv, der havde "
            "lagt sig i dens porer. Stenen var ikke længere bare en sten; den var et mikrokosmos af "
            "hele universet. Den var, i alle henseender, smukkere end noget guld.\n\n"
            "*\"Dine minder om krigen er de samme,\"* hviskede Elian. *\"De er tunge og mørke. Men "
            "hvis du sidder med dem længe nok, hvis du lader opmærksomhedens ild brænde din modstand "
            "væk, vil du se, at de også er et vidnesbyrd om din menneskelighed. Din evne til at føle "
            "den smerte er din største skat. Det er guldet.\"* Silas blev i Aethelgard i endnu ti "
            "år. Han glemte ikke krigen, men han holdt op med at bekæmpe den. Han lærte at bebo sin "
            "ensomhed, indtil den blev et levende, overfyldt landskab af indsigt. Da han endelig steg "
            "ned fra bjerget, vendte han ikke tilbage som soldat, men som helbreder. Han gik gennem "
            "de krigshærgede landsbyer, og selvom han ikke bar på nogen medicin, syntes hans blotte "
            "tilstedeværelse at lindre lidelserne hos dem, han mødte. Han havde mestret den ultimative "
            "alkymi: evnen til at sidde i mørket og finde lyset, ikke ved at undslippe skyggen, men "
            "ved at blive den, der skinner i den."
        ),
        "order": 8,
    },

    # ── 8-IT. La trasmutazione alchemica della solitudine ──────────────
    {
        "slug": "advanced-alchemical-solitude",
        "language": "it",
        "difficulty": "advanced",
        "length": "long",
        "title": "La trasmutazione alchemica della solitudine",
        "description_en": "Himalayan monks teach a war refugee to transmute pain into golden awareness.",
        "description_da": "Himalayanske munke lærer en krigsflygtning at forvandle smerte til gylden bevidsthed.",
        "description_it": "Monaci himalayani insegnano a un rifugiato di guerra a trasmutare il dolore in consapevolezza dorata.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Philosophical / spiritual",
        "setup_summary": "A war refugee learns mental alchemy in a Himalayan fortress and becomes a healer.",
        "body": (
            "La fortezza di Aethelgard si trovava in cima a un picco frastagliato dell'Himalaya, un "
            "luogo dove l'aria era troppo rarefatta per far respirare gli uomini comuni. Era abitata "
            "dall'\"Ordine Silenzioso\", un gruppo di studiosi che avevano dedicato la loro vita alla "
            "padronanza dell'\"Alchimia Mentale\". Credevano che i metalli vili dell'esperienza umana "
            "\u2013 solitudine, paura e desiderio \u2013 potessero essere trasmutati nell'oro puro della "
            "coscienza illuminata. Il Maestro Elian era il più anziano dell'ordine. Non pronunciava "
            "una parola da cinquant'anni. La sua pelle aveva il colore di una vecchia pergamena e i "
            "suoi occhi conservavano la quiete di un profondo lago di montagna. Trascorreva le sue "
            "giornate nella \"Biblioteca dell'Introspezione\", una stanza senza libri, solo specchi e "
            "stuoie per la meditazione.\n\n"
            "Un inverno, un giovane di nome Silas arrivò ai cancelli. Era un fuggitivo dalle guerre "
            "delle pianure, con l'anima bruciata dagli orrori a cui aveva assistito. \"Voglio "
            "dimenticare,\" implorò Elian. \"Voglio trasformare il mio dolore in qualcos'altro.\" "
            "Elian gli fece cenno di entrare. Per mesi, Silas visse in totale silenzio. Svolgeva "
            "compiti umili: spalare la neve, macinare il grano e mantenere le lampade ad olio. "
            "Partecipava alle sessioni di meditazione, ma la sua mente rimaneva un campo di "
            "battaglia. Il \"metallo vile\" del suo trauma si rifiutava di cambiare. Provava solo una "
            "solitudine gelida e schiacciante.\n\n"
            "\"Questa è una menzogna,\" gridò finalmente Silas una mattina, rompendo il voto di "
            "silenzio. \"Ve ne state seduti qui sulla vostra montagna a fingere di essere dei, ma "
            "siete solo codardi che si nascondono dal mondo. Qui non c'è oro, c'è solo ghiaccio.\" "
            "Elian non reagì con rabbia. Invece, fece cenno a Silas di seguirlo sul balcone più alto "
            "della fortezza. Guardavano su un mare di nuvole, le vette delle montagne circostanti che "
            "le trafiggevano come le pinne di grandi squali bianchi. Elian raccolse un piccolo, "
            "comune sasso da terra e lo porse a Silas. Attraverso una forma di risonanza telepatica, "
            "la voce di Elian echeggiò nella mente di Silas. *\"Tu confondi la solitudine con il "
            "vuoto. La solitudine è il crogiolo. Il dolore che porti non è un fardello da scartare, "
            "ma la materia prima della tua trasformazione. Non puoi trasformare il piombo in oro "
            "odiando il piombo. Devi comprendere il piombo. Devi amare il suo peso, la sua oscurità "
            "e la sua densità.\"*\n\n"
            "Elian poi chiuse la mano sulla pietra. Quando l'aprì, la pietra era immutata. Silas si "
            "accigliò, confuso. *\"L'alchimia non è nell'oggetto,\"* continuò Elian. *\"L'alchimia è "
            "nell'occhio dell'osservatore. Non ho cambiato la pietra. Ho cambiato il modo in cui la "
            "pietra interagisce con la luce. Guarda di nuovo.\"* Mentre Silas fissava la roccia "
            "comune, iniziò a scorgere i cristalli infinitesimali al suo interno. Vide la storia "
            "antica della terra, la pressione e il calore che l'avevano formata, e la polvere cosmica "
            "che si era depositata nei suoi pori. La pietra non era più solo una pietra; era un "
            "microcosmo dell'intero universo. Era, a tutti gli effetti, più bella di qualsiasi oro.\n\n"
            "*\"I tuoi ricordi della guerra sono la stessa cosa,\"* sussurrò Elian. *\"Sono pesanti e "
            "oscuri. Ma se ti siedi con loro abbastanza a lungo, se permetti al fuoco della "
            "consapevolezza di bruciare la tua resistenza, vedrai che sono anche una testimonianza "
            "della tua umanità. La tua capacità di provare quel dolore è il tuo tesoro più grande. È "
            "l'oro.\"* Silas rimase ad Aethelgard per altri dieci anni. Non dimenticò la guerra, ma "
            "smise di combatterla. Imparò ad abitare la sua solitudine fino a farla diventare un "
            "paesaggio vibrante e affollato di intuizioni. Quando finalmente scese dalla montagna, "
            "non tornò come soldato, ma come guaritore. Camminò attraverso i villaggi devastati "
            "dalla guerra e, sebbene non portasse medicine, la sua sola presenza sembrava lenire le "
            "sofferenze di chi incontrava. Aveva padroneggiato l'alchimia suprema: la capacità di "
            "sedersi nell'oscurità e trovare la luce, non fuggendo dall'ombra, ma diventando colui "
            "che brilla al suo interno."
        ),
        "order": 8,
    },

    # ── 9-DA. Den sidste bys penumbra ──────────────────────────────────
    {
        "slug": "advanced-penumbra-last-city",
        "language": "da",
        "difficulty": "advanced",
        "length": "long",
        "title": "Den sidste bys penumbra",
        "description_en": "The last humans live in a volcano's shadow and must choose darkness or light.",
        "description_da": "De sidste mennesker lever i en vulkans skygge og må vælge mellem mørke og lys.",
        "description_it": "Gli ultimi esseri umani vivono nell'ombra di un vulcano e devono scegliere tra oscurità e luce.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Post-apocalyptic / hope",
        "setup_summary": "Humanity's last city hides in a volcano's shadow until a scavenger builds a planetary shield.",
        "body": (
            "I menneskehedens tusmørke, da solen var blevet en oppustet, rød kæmpe, og oceanerne "
            "havde trukket sig tilbage i jordskorpen, boede de sidste en million mennesker i byen "
            "*Umbra*. Det var en vertikal metropol bygget fuldstændig inden i skyggen af en massiv, "
            "sovende vulkan. Skyggen gav den eneste beskyttelse mod solens dødelige stråling. Livet i "
            "Umbra var en delikat logistisk dans. Hver kalorie blev sporet, hver dråbe vand genbrugt, "
            "og hver fødsel nøje planlagt. \"Solvogterne\", en kaste af krigerforskere, stod på byens "
            "øvre kant og overvågede planetens langsomme rotation. Hvis byen nogensinde drev ud af "
            "vulkanens skygge, ville enden være øjeblikkelig.\n\n"
            "Kira var en \"Ådselsæder\", en af de få mennesker, der havde tilladelse til at vove sig "
            "ud i det \"Hærgede Land\" i de korte perioder med total solformørkelse. Hendes opgave "
            "var at indsamle ældgammel teknologi fra overfladebyernes ruiner. Hun var en kvinde med "
            "nerver af stål, og hendes krop var dækket af blyforede strålingsdragter. På sin sidste "
            "mission opdagede hun en struktur, der ikke burde have eksisteret: et fyrtårn, perfekt "
            "bevaret, stående på en bakke, der engang havde haft udsigt over et hav. Indeni fandt "
            "hun et bibliotek af digitale arkiver, der gik forud for \"Solekspansionen\". Mens hun "
            "rullede gennem optegnelserne, så hun billeder af en verden, der føltes som en "
            "feberdrøm: blå himmel, store vidder af flydende vand og mennesker, der stod i sollyset "
            "uden frygt. Men vigtigst af alt fandt hun \"Solhvervsprojektet\" \u2013 en plan om at bygge "
            "et massivt, planetarisk skjold af reflekterede ispartikler. Projektet var blevet "
            "opgivet, fordi det krævede en grad af samarbejde, som datidens krigsførende nationer "
            "ikke kunne opnå.\n\n"
            "Kira vendte tilbage til Umbra med dataene, men Det Høje Råd var tøvende. \"Byen er i "
            "sikkerhed i skyggen,\" argumenterede de. \"Hvorfor sætte alt på spil for en myte fra en "
            "fejlslagen civilisation? Hvis vi forsøger at ændre himlen, ødelægger vi måske det lille, "
            "vi har tilbage.\" \"Vi er ikke i sikkerhed,\" protesterede Kira. \"Vulkanen køler af. "
            "Skorpen forskyder sig. På et tidspunkt vil skyggen flytte sig, og vi vil ikke have noget "
            "sted at tage hen. Vi lever i en grav og venter på, at låget skal lukkes.\"\n\n"
            "En splittelse opstod i byen. \"Skyggevogterne\" ville grave dybere ned i jorden, mens "
            "\"Lyssøgerne\", ledet af Kira, ville stige op. Konflikten handlede ikke kun om "
            "overlevelse, men om definitionen på menneskelighed. Var de en art, der var skabt til at "
            "gemme sig i mørket, eller var de skabt til at række ud efter stjernerne, selvom det "
            "brændte dem? Til sidst ledte Kira et lille hold til toppen af vulkanen. De bar på de "
            "sidste af byens fusionskerner og en række modificerede atmosfæriske generatorer. Da "
            "planeten roterede, og skyggen begyndte at krympe, aktiverede Kira enheden.\n\n"
            "En stråle af ren, hvid energi skød op i atmosfæren og ioniserede de tunge mineraler, "
            "der havde lagt sig i stratosfæren. Langsomt begyndte et skinnende, changerende slør at "
            "sprede sig over himlen. Det var ikke den gamle verdens blå farve, men en gennemsigtig "
            "violet, der spredte solens hårde stråler til en blød, håndterbar glød. For første gang i "
            "titusind år trådte folket i Umbra ud fra skyggen. De stod på vulkanens skråninger og "
            "kiggede på en horisont, der ikke dræbte dem. Den violette himmel var smuk, et vidnesbyrd "
            "om menneskelig opfindsomhed født ud af desperation. Kira stod helt på toppen, hendes "
            "dragthjelm var taget af, og det kølige, filtrerede lys faldt på hendes ansigt. Hun "
            "indså, at den \"Sidste By\" ikke var slutningen på historien, men en puppe. De var "
            "vokset ud af skyggen. Da det første \"Violette Daggry\" brød frem over horisonten, så "
            "Kira folket nedenunder begynde at bygge, ikke vertikalt ind i mørket, men horisontalt "
            "ud over verden. De var ikke længere fortidens ådselsædere; de var arkitekterne for en "
            "ny, strålende fremtid. Penumbraens tidsalder var forbi, og menneskehedens lange, lyse "
            "eftermiddag var endelig begyndt."
        ),
        "order": 9,
    },

    # ── 9-IT. La penombra dell'ultima città ────────────────────────────
    {
        "slug": "advanced-penumbra-last-city",
        "language": "it",
        "difficulty": "advanced",
        "length": "long",
        "title": "La penombra dell'ultima città",
        "description_en": "The last humans live in a volcano's shadow and must choose darkness or light.",
        "description_da": "De sidste mennesker lever i en vulkans skygge og må vælge mellem mørke og lys.",
        "description_it": "Gli ultimi esseri umani vivono nell'ombra di un vulcano e devono scegliere tra oscurità e luce.",
        "format": "narrative",
        "speakers": None,
        "setup_type": "Post-apocalyptic / hope",
        "setup_summary": "Humanity's last city hides in a volcano's shadow until a scavenger builds a planetary shield.",
        "body": (
            "Nel crepuscolo dell'era umana, quando il sole era diventato una gigante rossa e gonfia "
            "e gli oceani si erano ritirati nella crosta terrestre, l'ultimo milione di esseri umani "
            "viveva nella città di *Umbra*. Era una metropoli verticale costruita interamente "
            "all'ombra di un massiccio vulcano inattivo. L'ombra forniva l'unica protezione dalle "
            "radiazioni letali del sole. La vita ad Umbra era una delicata danza di logistica. Ogni "
            "caloria veniva tracciata, ogni goccia d'acqua riciclata e ogni nascita attentamente "
            "programmata. I \"Guardiani del Sole\", una casta di scienziati-guerrieri, si trovavano "
            "sul bordo superiore della città, a monitorare la lenta rotazione del pianeta. Se la "
            "città fosse mai scivolata fuori dall'ombra del vulcano, la fine sarebbe stata "
            "istantanea.\n\n"
            "Kira era una \"Sciacalla\", uno dei pochi esseri umani autorizzati ad avventurarsi nelle "
            "\"Terre Devastate\" durante i brevi periodi di eclissi totale. Il suo compito era "
            "recuperare l'antica tecnologia dalle rovine delle città di superficie. Era una donna con "
            "nervi d'acciaio, il cui corpo era coperto da tute anti-radiazioni foderate di piombo. "
            "Nella sua ultima missione, scoprì una struttura che non avrebbe dovuto esistere: un "
            "faro, perfettamente conservato, eretto su una collina che un tempo dominava un mare. "
            "All'interno, trovò una biblioteca di archivi digitali antecedenti l'\"Espansione "
            "Solare\". Scorrendo i registri, vide immagini di un mondo che sembrava un sogno "
            "febbrile: cieli blu, vaste distese di acqua liquida e persone in piedi alla luce del "
            "sole senza paura. Ma soprattutto, trovò il \"Progetto Solstizio\": un piano per "
            "costruire un enorme scudo planetario fatto di particelle di ghiaccio riflettenti. Il "
            "progetto era stato abbandonato perché richiedeva un livello di cooperazione che le "
            "nazioni in guerra dell'epoca non potevano raggiungere.\n\n"
            "Kira tornò ad Umbra con i dati, ma l'Alto Consiglio era esitante. \"La città è al "
            "sicuro nell'ombra\", argomentarono. \"Perché rischiare tutto per un mito di una civiltà "
            "fallita? Se proviamo a cambiare il cielo, potremmo distruggere il poco che ci resta.\" "
            "\"Non siamo al sicuro\", controbatté Kira. \"Il vulcano si sta raffreddando. La crosta "
            "si sta spostando. Alla fine, l'ombra si sposterà e non avremo nessun posto dove andare. "
            "Viviamo in una tomba, in attesa che si chiuda il coperchio.\"\n\n"
            "In città si creò uno scisma. I \"Custodi dell'Ombra\" volevano scavare più a fondo "
            "nella terra, mentre i \"Cercatori di Luce\", guidati da Kira, volevano ascendere. Il "
            "conflitto non riguardava solo la sopravvivenza, ma la definizione stessa di umanità. "
            "Erano una specie destinata a nascondersi nell'oscurità o erano nati per tendere alle "
            "stelle, anche se ciò li avesse bruciati? Alla fine Kira guidò una piccola squadra fino "
            "alla cima del vulcano. Portavano gli ultimi nuclei di fusione della città e una serie di "
            "generatori atmosferici modificati. Mentre il pianeta ruotava e l'ombra iniziava a "
            "rimpicciolirsi, Kira attivò il dispositivo.\n\n"
            "Un raggio di pura energia bianca fu sparato nell'atmosfera, ionizzando i minerali "
            "pesanti che si erano depositati nella stratosfera. Lentamente, un velo cangiante e "
            "scintillante iniziò a diffondersi nel cielo. Non era l'azzurro del vecchio mondo, ma un "
            "violetto traslucido che disperdeva i duri raggi del sole in un bagliore morbido e "
            "gestibile. Per la prima volta in diecimila anni, la gente di Umbra uscì dall'ombra. Si "
            "trovavano sulle pendici del vulcano, a guardare un orizzonte che non li uccideva. Il "
            "cielo viola era bellissimo, una testimonianza dell'ingegno umano nato dalla "
            "disperazione. Kira si trovava sulla cima, con l'elmo della tuta rimosso e la luce fresca "
            "e filtrata che le cadeva sul viso. Capì che \"L'Ultima Città\" non era la fine della "
            "storia, ma una crisalide. Erano diventati troppo grandi per l'ombra. Quando la prima "
            "\"Alba Viola\" spuntò all'orizzonte, Kira vide le persone in basso iniziare a costruire, "
            "non in verticale nell'oscurità, ma in orizzontale attraverso il mondo. Non erano più gli "
            "Sciacalli del passato; erano gli Architetti di un nuovo, radioso futuro. L'era della "
            "penombra era finita, e il lungo, luminoso pomeriggio dell'umanità era finalmente "
            "iniziato."
        ),
        "order": 9,
    },
]


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
            existing.setup_type = s.get("setup_type")
            existing.setup_summary = s.get("setup_summary")
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
                setup_type=s.get("setup_type"),
                setup_summary=s.get("setup_summary"),
                order=s["order"],
            ))
    db.commit()


def seed_stories_with_audio(db, *, speeds: list[str] | None = None) -> None:
    """Seed stories and then pre-generate audio for all of them.

    Args:
        speeds: list of speed keys to generate (default: all speeds).
                Pass ``["normal"]`` to generate only normal-speed audio.
    """
    seed_stories(db)
    persisted_stories = db.query(Story).all()
    speed_label = ", ".join(speeds) if speeds else "all"
    print(f"  Pre-generating story audio for {len(persisted_stories)} stories (speeds: {speed_label})...")
    failures = 0
    for story in persisted_stories:
        failures += upsert_story_audio(db, story, speeds=speeds)
    if failures:
        print(f"  Story audio generation failures: {failures}")
    print("  Done.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_stories_with_audio(db, speeds=["normal"])
    finally:
        db.close()
