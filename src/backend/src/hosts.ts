export interface HostVoice {
  /** Microsoft Edge TTS neural voice name */
  voiceName: string;
}

export interface Host {
  id: string;
  name: string;
  language: string; // "it" | "da" | "en"
  emoji: string;
  imageUrl: string;
  descriptionEn: string;
  descriptionDa: string;
  descriptionIt: string;
  greetingEn: string;
  greetingDa: string;
  greetingIt: string;
  color: string; // tailwind color key
  voice: HostVoice;
}

export const HOSTS: Host[] = [
  // ── Italian hosts ──
  {
    id: "marco",
    name: "Marco",
    language: "it",
    emoji: "👨‍🍳",
    imageUrl: "/hosts/marco.jpg",
    descriptionEn: "A passionate Roman chef who brings Italian to life through the kitchen.",
    descriptionDa: "En passioneret romersk kok, der bringer italiensk til live gennem køkkenet.",
    descriptionIt: "Uno chef romano appassionato che dà vita all'italiano attraverso la cucina.",
    greetingEn: "Ciao! Let's cook up some beautiful Italian words together!",
    greetingDa: "Ciao! Lad os lave nogle smukke italienske ord sammen!",
    greetingIt: "Ciao! Cuciniamo insieme delle belle parole italiane!",
    color: "red",
    voice: { voiceName: "it-IT-DiegoNeural" },
  },
  {
    id: "giulia",
    name: "Giulia",
    language: "it",
    emoji: "👩‍🏫",
    imageUrl: "/hosts/giulia.jpg",
    descriptionEn: "An elegant Florentine professor with a love for precise pronunciation.",
    descriptionDa: "En elegant florentinsk professor med kærlighed til præcis udtale.",
    descriptionIt: "Un'elegante professoressa fiorentina con la passione per la pronuncia perfetta.",
    greetingEn: "Buongiorno! Let's perfect your Italian pronunciation today.",
    greetingDa: "Buongiorno! Lad os perfektionere din italienske udtale i dag.",
    greetingIt: "Buongiorno! Perfezzioniamo insieme la tua pronuncia italiana oggi.",
    color: "blue",
    voice: { voiceName: "it-IT-IsabellaNeural" },
  },
  {
    id: "luca",
    name: "Luca",
    language: "it",
    emoji: "🧑‍🎤",
    imageUrl: "/hosts/luca.jpg",
    descriptionEn: "An energetic Milanese student who makes learning Italian fun and casual.",
    descriptionDa: "En energisk milanesisk studerende, der gør det sjovt at lære italiensk.",
    descriptionIt: "Uno studente milanese pieno di energia che rende l'italiano divertente e informale.",
    greetingEn: "Ehi! Ready to sound like a true Italian? Let's go!",
    greetingDa: "Ehi! Klar til at lyde som en ægte italiener? Lad os komme i gang!",
    greetingIt: "Ehi! Pronto a parlare come un vero italiano? Andiamo!",
    color: "purple",
    voice: { voiceName: "it-IT-BenignoNeural" },
  },
  {
    id: "sofia",
    name: "Sofia",
    language: "it",
    emoji: "👵",
    imageUrl: "/hosts/sofia.jpg",
    descriptionEn: "A warm Neapolitan nonna who teaches through stories and tradition.",
    descriptionDa: "En varm napolitansk bedstemor, der underviser gennem historier og tradition.",
    descriptionIt: "Una calda nonna napoletana che insegna attraverso storie e tradizioni.",
    greetingEn: "Benvenuto, tesoro! Let me share the beauty of our language with you.",
    greetingDa: "Benvenuto, tesoro! Lad mig dele skønheden ved vores sprog med dig.",
    greetingIt: "Benvenuto, tesoro! Lascia che ti mostri la bellezza della nostra lingua.",
    color: "amber",
    voice: { voiceName: "it-IT-ElsaNeural" },
  },
  // ── Danish hosts ──
  {
    id: "anders",
    name: "Anders",
    language: "da",
    emoji: "☕",
    imageUrl: "/hosts/anders.jpg",
    descriptionEn: "A Copenhagen barista who teaches Danish through hygge culture and coffee.",
    descriptionDa: "En københavnsk barista, der underviser i dansk gennem hyggekultur og kaffe.",
    descriptionIt: "Un barista di Copenaghen che insegna il danese attraverso la cultura hygge e il caffè.",
    greetingEn: "Hej! Grab a coffee and let's learn some Danish together!",
    greetingDa: "Hej! Tag en kop kaffe, og lad os lære noget dansk sammen!",
    greetingIt: "Hej! Prendi un caffè e impariamo un po' di danese insieme!",
    color: "teal",
    voice: { voiceName: "da-DK-JeppeNeural" },
  },
  {
    id: "freja",
    name: "Freja",
    language: "da",
    emoji: "📚",
    imageUrl: "/hosts/freja.jpg",
    descriptionEn: "An Aarhus librarian with a passion for Nordic literature and clear speech.",
    descriptionDa: "En bibliotekar fra Aarhus med passion for nordisk litteratur og tydelig tale.",
    descriptionIt: "Una bibliotecaria di Aarhus appassionata di letteratura nordica e dizione chiara.",
    greetingEn: "Velkommen! Let me guide you through the beauty of Danish words.",
    greetingDa: "Velkommen! Lad mig guide dig gennem de smukke danske ord.",
    greetingIt: "Velkommen! Lascia che ti guidi attraverso la bellezza delle parole danesi.",
    color: "indigo",
    voice: { voiceName: "da-DK-ChristelNeural" },
  },
  {
    id: "mikkel",
    name: "Mikkel",
    language: "da",
    emoji: "🎨",
    imageUrl: "/hosts/mikkel.jpg",
    descriptionEn: "An Odense student fascinated by Danish design and modern culture.",
    descriptionDa: "En studerende fra Odense, fascineret af dansk design og moderne kultur.",
    descriptionIt: "Uno studente di Odense affascinato dal design danese e dalla cultura moderna.",
    greetingEn: "Hej hej! Ready to discover Danish? It's easier than you think!",
    greetingDa: "Hej hej! Klar til at opdage dansk? Det er nemmere end du tror!",
    greetingIt: "Hej hej! Pronto a scoprire il danese? È più facile di quanto pensi!",
    color: "cyan",
    voice: { voiceName: "da-DK-JeppeNeural" },
  },
  {
    id: "ingrid",
    name: "Ingrid",
    language: "da",
    emoji: "🧶",
    imageUrl: "/hosts/ingrid.jpg",
    descriptionEn: "A Jutland grandmother who teaches through Danish traditions and warmth.",
    descriptionDa: "En jysk bedstemor, der underviser gennem danske traditioner og varme.",
    descriptionIt: "Una nonna dello Jutland che insegna attraverso le tradizioni e il calore danese.",
    greetingEn: "Goddag, dear! Let me share the warmth of Danish with you.",
    greetingDa: "Goddag, kære! Lad mig dele det danske sprogs varme med dig.",
    greetingIt: "Goddag, caro! Lascia che condivida con te il calore della lingua danese.",
    color: "rose",
    voice: { voiceName: "da-DK-ChristelNeural" },
  },
  // ── English hosts ──
  {
    id: "james",
    name: "James",
    language: "en",
    emoji: "🎩",
    imageUrl: "/hosts/james.jpg",
    descriptionEn: "A London tour guide who brings English to life through British culture.",
    descriptionDa: "En London-turistguide, der bringer engelsk til live gennem britisk kultur.",
    descriptionIt: "Una guida turistica londinese che dà vita all'inglese attraverso la cultura britannica.",
    greetingEn: "Good day! Shall we explore the English language together?",
    greetingDa: "God dag! Skal vi udforske det engelske sprog sammen?",
    greetingIt: "Buongiorno! Esploriamo insieme la lingua inglese?",
    color: "slate",
    voice: { voiceName: "en-GB-ThomasNeural" },
  },
  {
    id: "emma",
    name: "Emma",
    language: "en",
    emoji: "🎓",
    imageUrl: "/hosts/emma.jpg",
    descriptionEn: "An Oxford professor with a love for literature and etymology.",
    descriptionDa: "En Oxford-professor med kærlighed til litteratur og etymologi.",
    descriptionIt: "Una professoressa di Oxford appassionata di letteratura ed etimologia.",
    greetingEn: "Welcome! Let's delve into the nuances of English pronunciation.",
    greetingDa: "Velkommen! Lad os dykke ned i nuancerne i engelsk udtale.",
    greetingIt: "Benvenuto! Approfondiamo le sfumature della pronuncia inglese.",
    color: "emerald",
    voice: { voiceName: "en-GB-SoniaNeural" },
  },
  {
    id: "ryan",
    name: "Ryan",
    language: "en",
    emoji: "🏄",
    imageUrl: "/hosts/ryan.jpg",
    descriptionEn: "An Australian surfer who makes learning English fun and laid-back.",
    descriptionDa: "En australsk surfer, der gør det sjovt og afslappet at lære engelsk.",
    descriptionIt: "Un surfista australiano che rende l'apprendimento dell'inglese divertente e rilassato.",
    greetingEn: "G'day mate! Let's have a crack at some English words!",
    greetingDa: "G'day mate! Lad os prøve kræfter med nogle engelske ord!",
    greetingIt: "G'day mate! Proviamo qualche parola inglese insieme!",
    color: "orange",
    voice: { voiceName: "en-AU-WilliamMultilingualNeural" },
  },
  {
    id: "margaret",
    name: "Margaret",
    language: "en",
    emoji: "🏔️",
    imageUrl: "/hosts/margaret.jpg",
    descriptionEn: "A Scottish grandmother who teaches through stories and wisdom.",
    descriptionDa: "En skotsk bedstemor, der underviser gennem historier og visdom.",
    descriptionIt: "Una nonna scozzese che insegna attraverso storie e saggezza.",
    greetingEn: "Hello, dear! Come sit down and let's practise some lovely English words.",
    greetingDa: "Hej, kære! Kom og sæt dig, og lad os øve nogle dejlige engelske ord.",
    greetingIt: "Ciao, caro! Siediti e esercitiamoci con qualche bella parola inglese.",
    color: "violet",
    voice: { voiceName: "en-GB-LibbyNeural" },
  },
];

export function getHost(id: string): Host {
  return HOSTS.find((h) => h.id === id) || HOSTS[0];
}

export const HOST_IDS = HOSTS.map((h) => h.id);
