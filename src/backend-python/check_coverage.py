"""Quick diagnostic: which story words are missing from the dictionary?"""
import sys, re
sys.path.insert(0, ".")
from app.database import SessionLocal
from app.models import Story, Word

db = SessionLocal()

def normalize(v):
    base = v.lower()
    mapping = str.maketrans({
        "à":"a","á":"a","â":"a","ã":"a","ä":"a","å":"a",
        "è":"e","é":"e","ê":"e","ë":"e",
        "ì":"i","í":"i","î":"i","ï":"i",
        "ò":"o","ó":"o","ô":"o","õ":"o","ö":"o",
        "ù":"u","ú":"u","û":"u","ü":"u",
        "ç":"c","ñ":"n",
    })
    return base.translate(mapping)

TOKEN_RE = re.compile(r"[a-zA-ZÀ-ÿæøåÆØÅ']+")
STOPWORDS_EN = {
    "a","an","the","and","or","of","in","to","is","are","was","were","it","i",
    "you","he","she","we","they","this","that","with","for","on","at","be",
    "have","has","had","do","did","will","would","can","could","should","not",
    "no","so","if","but","as","from","by","my","your","his","her","our","their",
    "me","him","us","them","what","which","who","when","where","how","yes","oh",
    "ok","its","am","been","then","than","there","here","about","up","out",
    "all","just","also","very","more","some","any","too","now","get","got","let",
    "say","said","one","two","three","four","five","six","seven","eight","nine",
    "ten","go","going","come","like","take","see","know","make","look","want",
    "back","new","old","first","last","long","great","little","good","right",
    "well","still","few","much","call","may","next","down","way","over","about",
    "need","same","did","each","she","him","his","had","its",
}
STOPWORDS_IT = {
    "il","la","lo","le","gli","un","una","uno","dei","del","della","delle",
    "dei","degli","che","con","non","per","nel","nella","nelle","nei","negli",
    "sul","sulla","sulle","sui","sugli","dal","dalla","dalle","dai","dagli",
    "al","alla","alle","ai","agli","tra","fra","ma","poi","anche","come","se",
    "sua","suo","suoi","sue","mia","mio","miei","mie","tua","tuo","tuoi","tue",
    "era","sono","siamo","sei","avete","avevo","aveva","loro","questa","questo",
    "questi","queste","lui","lei","noi","voi","qui","qua","mi","ti","vi","ci",
    "ho","hai","ha","abbiamo","avete","hanno","sia","gia","piu","meno","molto",
    "poco","tutti","tutte","tutto","tutta","ad","ed","od","nel","si","gli",
    "sta","stai","stanno","siano","avrei","avrebbe","sarei","sarebbe","fare",
    "fai","fa","facciamo","fate","fanno","due","tre","uno","una","due","tre",
    "poi","gia","cosi","puo","piu","ne","li","le","lo","cio","cui","sua",
}
STOPWORDS_DA = {
    "en","et","er","jeg","du","han","hun","vi","de","det","den","at","og","med",
    "til","fra","for","men","om","har","ikke","kan","vil","skal","var","sig",
    "alle","ham","hende","dem","som","da","naar","nar","men","alle","hvad",
    "samt","ind","ud","man","her","der","alt","sin","sit","sine","min","mit",
    "mine","din","dit","dine","enten","eller","hvert","efter","under","over",
    "ved","mod","mellem","gennem","ned","op","gerne","mig","dig","os","jer",
    "have","har","tage","give","see","godt","meget","noget","nogen","jo","nok",
    "ogs","hen","dog","men","vel","bare","blot","disse","dette","disse","denne",
    "saa","sa","nu","ja","nej","jo","tak","bede","kan","skal","vil","maa","ma",
    "var","kom","kom","tag","kom","bor","god","god","got","good",
}

for lang in ["it", "da", "en"]:
    stories = db.query(Story).filter(Story.language == lang).all()
    words_in_db = {normalize(w.word) for w in db.query(Word).filter(Word.language == lang).all()}
    stopwords = STOPWORDS_IT if lang == "it" else (STOPWORDS_DA if lang == "da" else STOPWORDS_EN)
    
    story_words = set()
    for s in stories:
        for tok in TOKEN_RE.findall(s.body):
            w = normalize(tok)
            if len(w) > 2 and w not in stopwords:
                story_words.add(w)
    
    missing = sorted(story_words - words_in_db)
    found = story_words & words_in_db
    print(f"\n[{lang.upper()}] Stories: {len(stories)}, Unique content tokens: {len(story_words)}, In DB: {len(found)}, Missing: {len(missing)}")
    if missing:
        print(f"  Missing words: {missing}")

db.close()
