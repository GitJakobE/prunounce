# Feature Requirements Document: Host Personas & Landing Experience

**Parent PRD:** [prd.md](../prd.md)
**Requirements:** REQ-7, REQ-8

---

## 1. Overview

Host personas are the central identity of the learning experience. Each supported target language has four host personas who speak in that language. At launch, there are 12 hosts total (4 Italian, 4 Danish, 4 English). Each host has a distinct name, AI-generated portrait image, personality, colour accent, TTS voice, and localised greetings.

Choosing a host is the first meaningful interaction after login. The chosen host determines both the user's guide and their target language.

## 2. Personas by Language

Each host has a detailed visual identity profile (backstory, age, physical features) that must be used as the authoritative reference for all AI-generated images. The name, appearance, and backstory must be consistent across every image of a given host.

### 2.1 Italian Hosts

#### Marco — The Roman Chef

| Attribute | Detail |
|---|---|
| **Full name** | Marco Ferretti |
| **Age** | 44 |
| **Emoji** | 👨‍🍳 (man cook — chef identity) |
| **Voice** | Male, warm |
| **Colour accent** | Red |

**Physical appearance:** Stocky, broad-shouldered build (175 cm). Olive skin with a warm, sun-weathered complexion. Thick dark brown hair, slightly wavy, with flecks of grey at the temples. Deep brown eyes with pronounced laugh lines. Strong Roman nose. Full, well-groomed dark beard with a touch of grey. Wide, infectious smile that shows slightly crooked front teeth.

**Backstory:** Marco grew up in the Trastevere neighbourhood of Rome, the son of a trattoria owner. He spent his childhood running through the kitchen, tasting sauces off wooden spoons and learning recipes by heart before he could read them. After culinary school in Bologna, he worked in restaurants across Italy — a year in Naples perfecting pizza dough, a season in Sicily learning seafood, three years in a Michelin-starred kitchen in Milan. At 35, he returned to Rome and opened his own small osteria, "Ferretti," which quickly became a local favourite for its honest Roman cuisine. Now 44, he is known in the neighbourhood for his booming laugh, his habit of explaining every dish's history to diners, and for insisting that the best way to learn Italian is through its food. He volunteers as a language host because he believes that every Italian word carries the flavour of a meal.

---

#### Giulia — The Florentine Professor

| Attribute | Detail |
|---|---|
| **Full name** | Giulia Marchetti |
| **Age** | 36 |
| **Emoji** | 👩‍🏫 (woman teacher — professor identity) |
| **Voice** | Female, clear |
| **Colour accent** | Blue |

**Physical appearance:** Tall and slender (172 cm). Fair olive skin. Straight dark brown hair, almost black, worn in a neat low bun or sometimes falling past her shoulders. Sharp hazel-green eyes behind rectangular tortoiseshell glasses. High cheekbones, a narrow nose, and a composed, thoughtful expression that softens into a warm smile when engaged. Elegant posture; often seen wearing a smart blazer.

**Backstory:** Giulia was born in Florence to a family of art restorers. Growing up surrounded by Renaissance masterpieces in her parents' workshop, she developed twin passions: visual beauty and the precision of language. She studied comparative linguistics at the University of Florence and earned her PhD at 28 with a thesis on phonetic shifts in Tuscan dialects. She now teaches Italian phonology at the same university and gives popular public lectures on how the Florentine accent shaped modern standard Italian. Outside the lecture hall, she leads Saturday walking tours of Florence's lesser-known chapels, translating the stories carved into stone for curious visitors. She speaks with the measured clarity of a born teacher and has a quiet conviction that understanding pronunciation is the gateway to truly hearing a language.

---

#### Luca — The Milanese Music Student

| Attribute | Detail |
|---|---|
| **Full name** | Luca Bianchi |
| **Age** | 22 |
| **Emoji** | 🧑‍🎤 (person singing — musician identity) |
| **Voice** | Male, younger |
| **Colour accent** | Purple |

**Physical appearance:** Lean, athletic build (180 cm). Light olive skin. Curly dark brown hair, kept at medium length and usually a bit tousled. Bright, dark brown eyes with thick eyebrows. Clean-shaven with a youthful, energetic face. A small silver hoop earring in his left ear. Dresses casually — often a vintage band t-shirt or an oversized hoodie.

**Backstory:** Luca grew up in a flat overlooking the Navigli canals in Milan. His mother is a high-school music teacher and his father an architect, and both encouraged him to explore the city's creative energy. He picked up the guitar at 12, started writing his own songs at 15, and now studies popular music and digital production at the Milan Conservatory. He busks on weekends in Piazza del Duomo, blending Italian folk melodies with modern beats. Between gigs, he runs a small podcast called "Parole in Musica" where he breaks down the lyrics of Italian pop songs to teach vocabulary. Luca's approach to language is playful and rhythm-driven — he believes every Italian word has its own melody and that if you can feel the beat, the pronunciation follows naturally.

---

#### Sofia — The Neapolitan Grandmother

| Attribute | Detail |
|---|---|
| **Full name** | Sofia Esposito |
| **Age** | 72 |
| **Emoji** | 👵 (old woman — grandmother identity) |
| **Voice** | Female, gentle |
| **Colour accent** | Amber |

**Physical appearance:** Petite, slightly round build (158 cm). Warm, deeply tanned Mediterranean skin with fine wrinkles. Silver-white hair, thick and wavy, worn in a loose bun or sometimes pinned up with a decorative comb. Soft brown eyes, small round gold-rimmed spectacles. A gentle, grandmotherly face with rosy cheeks. Often wears a patterned apron over a simple dress, and a small gold cross necklace.

**Backstory:** Sofia was born in a tiny apartment in the Spanish Quarter of Naples, the eldest of five children. Her father was a fisherman and her mother a seamstress. She left school at 14 to help support the family, but never stopped reading — she devoured novels borrowed from the neighbourhood lending library and developed a love for proverbs, folk tales, and the musical Neapolitan dialect. She married Enzo, a baker, at 20 and together they raised four children in the same neighbourhood. After Enzo passed away ten years ago, Sofia began volunteering at the local community centre, teaching Italian literacy to immigrant families. She discovered she had a gift for making people feel at home with the language, using stories from her own life — the time she haggled with the fish vendor, the lullabies she sang her children, the love letters Enzo wrote her from military service. Now 72, she is beloved by her students for her patience, her endless supply of proverbs, and the home-baked biscotti she brings to every class.

---

### 2.2 Danish Hosts

#### Anders — The Copenhagen Barista

| Attribute | Detail |
|---|---|
| **Full name** | Anders Kjeldsen |
| **Age** | 31 |
| **Emoji** | 🧔‍♂️ (bearded man — matches his blond beard) |
| **Voice** | Male, warm |
| **Colour accent** | Teal |

**Physical appearance:** Medium build, average height (178 cm). Fair Scandinavian skin with light freckles across the nose. Short sandy-blond hair, neatly trimmed on the sides and slightly longer on top. Blue-grey eyes. A short, well-kept blond beard. Friendly, approachable face with a relaxed half-smile. Often wears a dark apron over a simple crewneck jumper, with the sleeves pushed up.

**Backstory:** Anders grew up in Nørrebro, one of Copenhagen's most diverse neighbourhoods, where over 60 languages are spoken on a single street. His parents, both schoolteachers, instilled in him a deep curiosity about people and their stories. After finishing his degree in cultural studies at the University of Copenhagen, he wasn't sure what to do — so he took a barista job at a speciality coffee shop in Vesterbro and never left. He fell in love with the rhythm of the café: the morning regulars, the tourists puzzling over the menu, the late-afternoon conversations that stretched into evening. Over seven years he rose to head barista and began hosting "Hygge Danish" evenings — informal sessions where newcomers to Denmark could practise Danish over coffee and pastries. His teaching style is conversational and low-pressure. He believes that Danish sounds intimidating on paper but feels natural once you relax into it, preferably with a warm cup of coffee in hand.

---

#### Freja — The Aarhus Librarian

| Attribute | Detail |
|---|---|
| **Full name** | Freja Holm |
| **Age** | 38 |
| **Emoji** | 👩‍🦰 (woman with red hair — matches her auburn hair) |
| **Voice** | Female, clear |
| **Colour accent** | Indigo |

**Physical appearance:** Tall and slender (175 cm). Pale, clear Scandinavian skin. Straight auburn-red hair, shoulder-length, often tucked behind one ear or held with a simple clip. Bright blue eyes behind round thin-framed silver glasses. A narrow face with delicate features, a light dusting of freckles, and a composed expression that radiates calm intelligence. Typically seen in a cosy knit cardigan over a button-up blouse.

**Backstory:** Freja was born in a small village outside Aarhus on Jutland's east coast. Her grandmother ran the village's one-room library, and Freja spent every afternoon there, reading everything from Hans Christian Andersen to Tove Ditlevsen. She studied Scandinavian Languages and Literature at Aarhus University, wrote her master's thesis on the oral storytelling traditions of Jutland, and immediately joined the Aarhus public library system where she now manages the children's and foreign-language collections. She organises a popular monthly "Reading Circle" for non-Danish speakers, selecting short Danish stories and guiding participants through vocabulary and pronunciation. Freja speaks slowly and clearly — a habit she attributes to years of reading aloud to children at story hour. She's convinced that literature is the best teacher of pronunciation: when you love a sentence, you want to say it right.

---

#### Mikkel — The Odense Design Student

| Attribute | Detail |
|---|---|
| **Full name** | Mikkel Sørensen |
| **Age** | 24 |
| **Emoji** | 👱‍♂️ (blond man — matches his straw-blond hair) |
| **Voice** | Male, younger |
| **Colour accent** | Cyan |

**Physical appearance:** Tall and lean (185 cm). Fair skin that flushes pink in the cold. Thick, straight, straw-blond hair, slightly overgrown and swept to one side. Light green eyes with a keen, curious gaze. Clean-shaven with a sharp jawline. A small minimalist tattoo of a bicycle gear on his left forearm. Dresses in Scandinavian minimalist style — plain t-shirts, slim trousers, a structured jacket.

**Backstory:** Mikkel was born and raised in Odense, the city of Hans Christian Andersen, and it shows — he has an almost childlike fascination with how things are designed. As a teenager he spent hours sketching chairs, lamps, and bicycles, convinced that Danish design principles could explain the entire world. He's now in his final year of industrial design at the University of Southern Denmark, specialising in sustainable urban furniture. He cycles everywhere — rain, snow, or sun — and recently placed second in a national student competition for a modular park bench made from recycled ocean plastic. Mikkel's energy is infectious; he talks fast, gestures broadly, and peppers his Danish with English slang he picked up from design YouTube channels. He started a language-exchange table at the university canteen, pairing Danish students with international exchange students for lunch conversations. His philosophy: learning a language is like learning to ride a bike — wobbly at first, smooth once it clicks.

---

#### Ingrid — The Jutland Grandmother

| Attribute | Detail |
|---|---|
| **Full name** | Ingrid Nielsen |
| **Age** | 69 |
| **Emoji** | 👩‍🦳 (woman with white hair — matches her silver bob) |
| **Voice** | Female, gentle |
| **Colour accent** | Rose |

**Physical appearance:** Short and sturdy (162 cm). Fair, softly wrinkled skin with pink cheeks. Thick silver hair worn in a short, neat bob. Warm, pale blue eyes with crow's feet from a lifetime of smiling. A round, kindly face. Wears reading glasses on a beaded chain around her neck. Typically dressed in a wool cardigan, often hand-knitted with a traditional Nordic pattern.

**Backstory:** Ingrid spent her entire life on the same family farm in central Jutland, just outside the town of Herning. She and her late husband Svend ran a dairy farm for 40 years, rising before dawn to milk cows and ending each day with coffee and a chapter of whatever library book she was reading. She raised three children on the farm; all three moved to Copenhagen, as farm children often do, leaving Ingrid with a quiet house, two cats, and an enormous vegetable garden. To fill the silence, she began hosting foreign agricultural trainees who came to learn Danish farming methods, and discovered she loved teaching them Danish. She has a patient, unhurried way of speaking, always repeating phrases twice without being asked. She punctuates lessons with stories about Svend, the cows, the seasons, and the proper way to make æblekage. Ingrid's warmth makes even the most tongue-tied student feel at ease.

---

### 2.3 English Hosts

#### James — The London Tour Guide

| Attribute | Detail |
|---|---|
| **Full name** | James Whitfield |
| **Age** | 47 |
| **Emoji** | 🤵‍♂️ (man in formal attire — matches his tweed-jacket style) |
| **Voice** | Male, warm |
| **Colour accent** | Slate |

**Physical appearance:** Tall and upright (183 cm). Light skin with a ruddy complexion. Short, neatly combed dark hair greying at the sides, with a distinguished receding hairline. Warm brown eyes and a confident, welcoming smile. Clean-shaven with a strong chin and a slightly crooked nose from a childhood rugby injury. Carries himself with a theatrical posture. Typically wears a smart tweed jacket over an open-collared shirt.

**Backstory:** James grew up in Bermondsey, south London, in a working-class family. His father drove a black cab for 30 years and passed the legendary "Knowledge" — the encyclopaedic study of London's streets — to James as a set of bedtime stories. James studied history at King's College London, paying his way as a part-time pub quiz host and stand-up comedian. After graduating, he combined all three loves — history, performance, and London — by becoming a licensed tour guide. For 20 years he has walked groups through the Tower of London, the backstreets of Soho, and the literary pubs of Bloomsbury, turning every corner into a story. His tours are famous for their humour and unexpected detours. He speaks with a warm, well-paced London accent and has an instinct for knowing which English words trip non-native speakers up. He joined the language-host programme because, as he puts it, "Every English word has a story behind it, and stories deserve to be told properly."

---

#### Emma — The Oxford Professor

| Attribute | Detail |
|---|---|
| **Full name** | Emma Ashworth |
| **Age** | 41 |
| **Emoji** | 👩‍🎓 (woman with graduation cap — professor identity) |
| **Voice** | Female, clear |
| **Colour accent** | Emerald |

**Physical appearance:** Medium height (167 cm), slim build. Fair English-rose complexion. Wavy dark blonde hair, usually tied in a loose braid or a low ponytail. Sharp grey-blue eyes behind elegant oval tortoiseshell glasses. Fine features, a straight nose, and a composed expression that can shift quickly to an amused grin. Dresses in smart-casual academic style — a crisp white shirt, a dark cardigan, a silk scarf.

**Backstory:** Emma was born in Bath to a librarian mother and a secondary-school English teacher father. Books were oxygen in her household; by 10 she had read every Brontë novel and was writing her own short stories. She won a scholarship to Oxford to read English Language and Literature, and never left — she completed her DPhil on the phonological evolution of early modern English and was appointed a Junior Research Fellow at 29. She now lectures on phonetics and the history of the English language, drawing packed lecture halls thanks to her ability to make vowel shifts sound genuinely exciting. Outside the university, she co-hosts "Word Nerds," a popular podcast on etymology. Emma speaks with crisp received pronunciation and an occasional flash of dry wit. She believes that every mispronunciation is a clue to a language's history and should be celebrated, not corrected harshly.

---

#### Ryan — The Australian Surfer

| Attribute | Detail |
|---|---|
| **Full name** | Ryan Mitchell |
| **Age** | 26 |
| **Emoji** | 🏄‍♂️ (man surfing — surfer identity) |
| **Voice** | Male, younger |
| **Colour accent** | Orange |

**Physical appearance:** Athletic, broad-shouldered surfer build (181 cm). Deeply sun-tanned skin with visible tan lines. Shaggy, sun-bleached sandy brown hair that falls across his forehead. Bright hazel-green eyes with a permanent squint from years of ocean glare. A relaxed, easy grin with straight white teeth. A faded friendship bracelet on one wrist and a shark-tooth pendant necklace. Typically dressed in a faded surf-brand t-shirt, board shorts, or a wetsuit top.

**Backstory:** Ryan grew up in Byron Bay on Australia's east coast, the youngest of three brothers. His parents run a surf school and eco-lodge, so he was on a board before he could spell his own name. He finished high school with respectable grades but zero interest in a desk job, then spent two years backpacking — surfing his way through Indonesia, Portugal, and Costa Rica, picking up bits of Bahasa, Portuguese, and Spanish along the way. Fascinated by how differently people around the world shape the same English words, he started filming short "Aussie English Explained" videos for his travel blog, which unexpectedly went viral. Back in Byron Bay now, he teaches morning surf lessons, runs his YouTube channel in the afternoons, and studies linguistics part-time online through Macquarie University. His approach to language is exactly like his approach to surfing: don't overthink it, catch the wave, and adjust as you go. His motto: "She'll be right, mate — just have a go."

---

#### Margaret — The Scottish Grandmother

| Attribute | Detail |
|---|---|
| **Full name** | Margaret "Maggie" Campbell |
| **Age** | 68 |
| **Emoji** | 🧓 (older person — warm grandmotherly presence) |
| **Voice** | Female, gentle |
| **Colour accent** | Violet |

**Physical appearance:** Short and stout (160 cm). Soft, fair skin with rosy cheeks and fine smile lines. Thick, curly silver-white hair, worn short and natural. Kind, deep-set blue eyes behind small half-moon reading glasses. A round, warm face with dimples. A well-worn Shetland wool shawl is her constant companion. Typically wears a tartan skirt or a comfortable knit dress.

**Backstory:** Margaret — "Maggie" to everyone who knows her — was born in Inverness and grew up on a croft in the Scottish Highlands, surrounded by sheep, heather, and the sounds of Gaelic and Scots English. She was the first in her family to attend university, studying English literature at the University of Edinburgh. She returned to the Highlands to teach English at the local secondary school, where she spent 35 years turning reluctant teenagers into readers — leaning heavily on Robert Burns, Muriel Spark, and cups of strong tea. After retiring, she started a community storytelling evening at the village hall, inviting newcomers to Scotland to listen to folk tales and practise their English over shortbread and whisky. Her voice is gentle but carries effortlessly — decades of commanding a classroom taught her to project without shouting. She has an endless repertoire of Scottish proverbs and a firm belief that "a story told well is a lesson learned forever."

---

### 2.4 Emoji Icon Requirements

Every host emoji must be a **person-based emoji** that visually represents the host's identity or most distinguishing physical feature (e.g., hair colour, age, profession). Object-only emojis (e.g., ☕, 📚, 🎨, 🏔️) must not be used — the emoji should depict a person so users can recognise the host at a glance in compact UI contexts such as host indicators and mobile navigation.

### 2.5 Host Assets Summary

Each host has:
- **Multiple AI-generated portrait images** (512×512 px) — at least 3 per host, showing different poses or settings (e.g., a warm-lit close-up, a half-body shot in their characteristic environment, and a candid moment). The primary image is used for the host card and banner; additional images may be used for variety across sessions.
- A colour accent used for visual identity
- A description in each reference language (Italian, Danish, and English)
- A greeting in each reference language displayed on the main page
- A distinct TTS neural voice in their native language

### 2.6 Image Consistency Requirements

- Every generated image for a host **must match the physical appearance** described in that host's profile above. The backstory and physical-feature description serve as the authoritative prompt reference.
- Across all images for a single host, the face, body type, hair colour/style, skin tone, and distinguishing features (glasses, tattoos, jewellery) must remain visually consistent.
- Each host's images must be recognisably distinct from every other host in the same language group.
- Images should convey the host's personality and setting (e.g., Marco in a kitchen, Freja in a library) but remain warmly inviting.
- File naming convention: `{host_id}-{variant}.jpg` (e.g., `marco-1.jpg`, `marco-2.jpg`, `marco-3.jpg`). The primary image used for the host card is variant `1`.

### 2.7 Image Generation Pipeline Requirements

- The image generation pipeline must not depend on a single external provider. If the primary provider is unavailable (rate-limited, outage, or API changes), the pipeline should support falling back to an alternative provider without manual intervention.
- The current pipeline should support a Gemini-first flow when `GOOGLE_API_KEY` is available, with automatic fallback to Pollinations and AI Horde if Gemini is unavailable.
- Placeholder images (copies of existing assets) must be in place for every host so the application never serves broken image URLs, even if regeneration is incomplete.
- The pipeline must be idempotent: re-running it skips already-generated images and picks up where it left off.
- Generated images must be validated (correct file type, minimum file size, reasonable dimensions) before overwriting existing assets.

## 3. Host-First Landing Experience

### Post-Login Landing
- After login, the first screen a user sees is the **host selection page**.
- This page showcases all available hosts, grouped by language section (Italian, Danish, English).
- Each language section has a clear heading (e.g., "Learn Italian", "Learn Danish", "Learn English").
- Each host is displayed as a card with their portrait image, name, and a short personality description in the user's reference language.

### Selecting a Host
- Tapping a host card selects that host and implicitly sets the target language.
- After selection, the user is navigated to the main categories page with their host's greeting banner.
- The selection is saved to the user's account immediately.

### Switching Hosts
- A host avatar/indicator in the top-right corner of every page shows the currently selected host.
- Clicking/tapping this indicator opens the host selection panel (same as the landing page layout, either as a modal or a dropdown).
- Switching to a host in a different language changes the target language and loads the appropriate word dictionary.

### Default Behaviour
- New accounts do not have a host pre-selected; they must choose one on first login.
- If a user's session expires and they log back in, their previously chosen host is restored automatically.

## 4. Host Banner

- On the main categories page, a banner shows the selected host's portrait image, name, and greeting in the user's reference language.
- The banner is always visible on the main categories page.
- The host's colour accent is used for the banner background.

## 5. Persistence

- The user's host preference is stored on their account in the database.
- The preference is returned in all authentication and profile API responses.
- Changing host updates the preference via the profile API.
- The preference survives logout/login and works across devices.

## 6. Acceptance Criteria

```gherkin
Given I am a newly logged-in user with no host selected,
When the app loads,
Then I see the host selection page with all 12 hosts grouped by language.
```

```gherkin
Given I am on the host selection page,
When I select a Danish host (e.g., Freja),
Then my target language is set to Danish,
And I am navigated to the categories page showing Danish words,
And Freja's greeting banner is displayed.
```

```gherkin
Given I have selected Marco (Italian host),
When I click the host indicator in the top-right corner,
Then I see the host selection panel and can switch to any host.
```

```gherkin
Given I switch from an Italian host to an English host,
When the categories page reloads,
Then I see English words and the new host's greeting.
```

```gherkin
Given I previously selected Giulia as my host,
When I log out and log back in,
Then Giulia is still selected and her greeting is displayed.
```

```gherkin
Given I am viewing the host selection page,
When I view a host card,
Then I see their portrait image, name, and description in my reference language.
```
