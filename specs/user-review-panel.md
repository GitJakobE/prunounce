# 👥 User Review Panel

**Parent PRD:** [prd.md](prd.md)

---

## 1. Purpose

The User Review Panel is a standing group of six representative personas used to evaluate every major change to Pronuncia before release. Each panellist embodies a distinct user group, set of motivations, and level of technical comfort. By reviewing features, flows, and content through these lenses, the team ensures the product works well for its full audience — not just the "average" user.

### How to Use This Panel

- **Before each major release or feature launch**, walk through the change from the perspective of every panellist.
- **For each panellist, ask:**
  1. Can they discover and use the new feature given their goals and comfort level?
  2. Does anything in the change create a barrier specific to their situation (language, device, accessibility, attention span)?
  3. Would this change delight them, frustrate them, or go unnoticed?
- **Document findings** as a short review note per panellist, flagging issues by severity.

---

## 2. The Panel

### 2.1 Patrizia — "The Determined Newcomer"

| Attribute | Detail |
|---|---|
| **Age** | 62 |
| **Location** | Recently moved from Naples, Italy to a suburb of Copenhagen, Denmark |
| **Languages** | Native Italian; very limited English; no Danish yet |
| **Device** | Android smartphone (hand-me-down from her son-in-law); occasionally borrows her daughter's laptop |
| **Tech comfort** | Low — can use WhatsApp and browse photos, but new apps make her anxious |

**Background:** Patrizia is a retired elementary-school teacher who moved to Denmark to be closer to her daughter's family. Her three grandchildren are growing up bilingual (Danish/Italian), and she hates not being able to chat with their Danish friends or understand the parents at school pick-up. She tried Duolingo once but found it overwhelming. Her daughter showed her Pronuncia and set Italian as the reference language so everything makes sense. Patrizia's goal is simple: learn enough Danish words to have small conversations at the local bakery and at her grandchildren's birthday parties.

**What she tests:**
- Can someone with minimal tech skills navigate the app after a quick intro from a family member?
- Does the Italian UI translation feel natural and complete, with no untranslated English fragments?
- Is audio playback obvious and instant — no hidden buttons or confusing icons?
- Are touch targets large enough for someone who isn't precise with a phone screen?
- Does the host persona (likely Ingrid, the cosy Danish grandmother) feel warm and encouraging rather than intimidating?

---

### 2.2 Aiden — "The Immersed Student"

| Attribute | Detail |
|---|---|
| **Age** | 21 |
| **Location** | Originally from Vancouver, Canada; now living in Lyngby, Denmark |
| **Languages** | Native English; beginner Danish; conversational French from high school |
| **Device** | MacBook Pro and iPhone 15; always on fast campus Wi-Fi or 5G |
| **Tech comfort** | Very high — computer science student, notices every UI delay |

**Background:** Aiden arrived at DTU (Technical University of Denmark) on a two-year exchange programme. His courses are in English, but his flatmates are Danish and he's tired of being the one who can't follow the jokes. He's competitive and tracks everything — steps, grades, streaks. He picked Anders (the Copenhagen barista host) because the hygge angle amused him. Aiden uses Pronuncia in short, focused bursts between lectures, racing through categories to fill his progress bar.

**What he tests:**
- Is the UI snappy on desktop and mobile, with no unnecessary loading spinners?
- Does progress tracking update in real time after playing a word?
- Can he search for a specific Danish word he just heard in the hallway and get a result instantly?
- Is the word contribution flow fast enough that he'll actually bother adding slang he picks up?
- Does switching between Danish categories feel seamless, or does he hit dead ends?

---

### 2.3 Mette — "The Professional Polisher"

| Attribute | Detail |
|---|---|
| **Age** | 34 |
| **Location** | Born in Copenhagen; relocated to Milan, Italy for work |
| **Languages** | Native Danish; fluent English; intermediate Italian (good reading, shaky pronunciation) |
| **Device** | Work-issued Windows laptop; personal iPhone; uses the app on both |
| **Tech comfort** | High — UX designer by profession, opinionated about design quality |

**Background:** Mette works at a design studio in Milan. Her Italian grammar is decent, but she mispronounces words in client presentations and it undermines her confidence. She chose Giulia (the Florentine professor host) for clarity and authority. Mette uses Pronuncia deliberately: she browses the "Business & Work" and "Food & Drink" categories before meetings and dinners, replaying tricky words until the pronunciation feels right. She also uses it with Danish as the reference language, since seeing Italian words translated into Danish is more intuitive for her than English.

**What she tests:**
- Does the responsive layout work well on a laptop browser during a lunch break and on a phone during a commute?
- Is the reference-language switcher easy to find and does it update everything cleanly?
- Are category and difficulty labels helpful for someone targeting specific professional or social contexts?
- Does the design feel polished and trustworthy — or are there rough edges that a design-trained eye would catch?
- Can she replay words multiple times without the UI getting in the way?

---

### 2.4 Thomas — "The Phrase-Grabber"

| Attribute | Detail |
|---|---|
| **Age** | 45 |
| **Location** | Birmingham, United Kingdom |
| **Languages** | Native English; a handful of Italian and Danish phrases from holidays |
| **Device** | Android phone (mid-range); sometimes a work PC during breaks |
| **Tech comfort** | Moderate — uses apps confidently but has no patience for sign-up friction or tutorials |

**Background:** Thomas is a logistics manager who takes three or four short holidays a year — often a long weekend in Copenhagen or a week on the Italian coast. He doesn't want to "learn a language"; he wants to order food, ask for directions, and say thank you without embarrassing himself. He found Pronuncia through a search for "how to pronounce Danish words" and signed up because the host selection page looked friendly. He picked Ryan (the Australian host) for English and toggles to Italian or Danish hosts depending on his next trip. Thomas uses the app in five-minute bursts: search for a word, hear it, move on.

**What he tests:**
- Is the sign-up process quick and painless, with no unnecessary fields?
- Can someone who dips in and out find value without committing to a structured learning path?
- Does word search work well for partial or approximate spellings (e.g., "tak" or "gratsie")?
- Are the "Travel" and "Food & Drink" categories easy to find from the landing page?
- Does the mobile layout work well for quick, one-handed use on a train or at an airport?

---

### 2.5 Farah — "The Inclusive Tester"

| Attribute | Detail |
|---|---|
| **Age** | 29 |
| **Location** | London, United Kingdom |
| **Languages** | Native English; conversational Somali; learning Italian |
| **Device** | Windows laptop with NVDA screen reader; iPhone with VoiceOver enabled |
| **Tech comfort** | High — professional translator, deeply familiar with assistive technology |

**Background:** Farah is a freelance translator specialising in English–Somali legal documents. She's learning Italian because she's planning a long sabbatical in Sicily and wants to be able to navigate daily life independently. She has low vision (legally blind) and uses a screen reader for nearly everything. She chose Emma (the Oxford professor host) for the clear, precise voice. Farah doesn't just test whether Pronuncia works for her — she notices every missing aria-label, every colour-contrast failure, and every keyboard trap. She's the conscience of the panel.

**What she tests:**
- Can every feature be operated with keyboard-only navigation and a screen reader?
- Are all images (host portraits, icons, progress indicators) described with meaningful alt text?
- Does colour contrast meet WCAG AA standards throughout, including on host colour-accent banners?
- Are audio controls properly labelled and reachable without a mouse?
- Do dynamic updates (e.g., search results, progress changes, language switching) announce correctly to assistive technology?
- Is the word contribution form fully accessible, with labelled inputs and clear error messages?

---

### 2.6 Nikolaj — "The Power Contributor"

| Attribute | Detail |
|---|---|
| **Age** | 17 |
| **Location** | Aarhus, Denmark |
| **Languages** | Native Danish; fluent English; basic Italian from family holidays in Sardinia |
| **Device** | Gaming PC with ultrawide monitor; Samsung Galaxy phone |
| **Tech comfort** | Very high — builds hobby projects, finds edge cases for fun |

**Background:** Nikolaj is a high-school student who stumbled on Pronuncia while helping his Italian exchange-student classmate practise Danish. He thought the host concept was cool and immediately picked Mikkel (the Odense design student) because of the cycling connection. Nikolaj quickly exhausted the seeded word list and started contributing slang, informal expressions, and words he thinks are missing. He switches between all three languages to check translations and spot inconsistencies. He's the user who will file the weirdest bug reports and push the contribution system to its limits.

**What he tests:**
- Does the word contribution flow handle edge cases: very long words, special characters (æ, ø, å, è, ù), duplicate detection, and empty optional fields?
- Is progress tracking accurate across all three languages when switching hosts frequently?
- Can a user who moves fast between categories, hosts, and languages hit any broken states?
- Does the search handle diacritical-mark tolerance correctly (e.g., searching "café" vs "cafe")?
- Are user-contributed words visible to everyone and indistinguishable from seeded words?
- Does the UI scale well on an ultrawide desktop monitor?

---

## 3. Coverage Matrix

The table below maps each panellist to the product dimensions they are best positioned to evaluate.

| Dimension | Patrizia | Aiden | Mette | Thomas | Farah | Nikolaj |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| First-time onboarding | ● | | | ● | | |
| Host selection & switching | ● | ● | ● | ● | ● | ● |
| Italian as target language | | | ● | ● | ● | |
| Danish as target language | ● | ● | | ● | | ● |
| English as target language | | | | | | ● |
| Italian as reference language | ● | | | | | |
| Danish as reference language | | | ● | | | ● |
| English as reference language | | ● | | ● | ● | ● |
| Audio playback & latency | ● | ● | ● | ● | ● | ● |
| Word search | | ● | | ● | ● | ● |
| Progress tracking | | ● | ● | | | ● |
| Word contribution | | ● | | | | ● |
| Mobile usability | ● | ● | ● | ● | ● | |
| Desktop / wide-screen layout | | ● | ● | | ● | ● |
| Accessibility (assistive tech) | | | | | ● | |
| Low tech comfort / simplicity | ● | | | ● | | |
| Design quality & polish | | | ● | | ● | |
| Edge cases & stress testing | | | | | | ● |
| Multi-language switching | | | ● | ● | | ● |

---

## 4. Review Process

1. **Trigger:** Any change classified as "major" — new feature, significant UI redesign, new language addition, or breaking change to an existing flow.
2. **Prepare:** Copy [`reviews/_template.md`](reviews/_template.md) to `reviews/YYYY-MM-DD-<short-description>.md`.
3. **Walkthrough:** For each panellist, a team member (or the panellist's description itself, when used as a heuristic) steps through the change and answers the three questions from Section 1.
4. **Log:** Record findings in the review file, one section per panellist, tagging every issue as **blocker**, **significant**, or **minor**.
5. **Resolution:** Blockers must be resolved before release. Significant issues are scheduled for the next iteration. Minor issues are added to the backlog.

All review files live in the [`reviews/`](reviews/) folder. See [`reviews/README.md`](reviews/README.md) for naming conventions and severity definitions.
