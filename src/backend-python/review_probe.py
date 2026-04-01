import httpx, json, sys

base = 'http://localhost:8000'

def login(email, pwd):
    r = httpx.post(base+'/api/auth/login', json={'email': email, 'password': pwd})
    if r.status_code == 200:
        return r.json().get('token', '')
    return None

def register_or_login(email, lang, name, pwd='TestPass1!'):
    r = httpx.post(base+'/api/auth/register', json={
        'email': email, 'password': pwd,
        'reference_language': lang, 'display_name': name
    })
    if r.status_code in (200, 201):
        return r.json().get('token') or r.json().get('access_token', '')
    return login(email, pwd)

tok_pat = register_or_login('patrizia@example.com', 'it', 'Patrizia')
tok_aid = register_or_login('aiden@example.com', 'en', 'Aiden')
tok_met = register_or_login('mette@example.com', 'da', 'Mette')

hp = {'Authorization': 'Bearer ' + (tok_pat or '')}
ha = {'Authorization': 'Bearer ' + (tok_aid or '')}
hm = {'Authorization': 'Bearer ' + (tok_met or '')}

print("=== HOSTS ===")
hosts_r = httpx.get(base+'/api/hosts', headers=hp)
hosts = hosts_r.json().get('hosts', [])
print('Total hosts:', len(hosts))
for hst in hosts:
    print(f"  {hst['id']:15} {hst['name']:10} lang={hst['language']}")

print("\n=== CATEGORIES (da, Aiden) ===")
cats_r = httpx.get(base+'/api/dictionary/categories?lang=da', headers=ha)
print('Status:', cats_r.status_code)
cats = cats_r.json() if cats_r.status_code == 200 else []
if isinstance(cats, list):
    print('Count:', len(cats))
    for c in cats[:5]:
        print(' ', c)
else:
    print(cats_r.text[:300])

print("\n=== WORDS (first category, da) ===")
if isinstance(cats, list) and cats:
    cid = cats[0].get('id') if isinstance(cats[0], dict) else cats[0]
    wr = httpx.get(base+'/api/dictionary/categories/'+str(cid)+'/words?lang=da', headers=ha)
    print('Status:', wr.status_code)
    words = wr.json() if wr.status_code == 200 else {}
    if isinstance(words, list):
        print('Word count:', len(words))
        for w in words[:3]:
            print(' ', w.get('word'), '|', w.get('translation_en'), '|', w.get('phonetic_hint'))
    else:
        print(wr.text[:400])

print("\n=== SEARCH ===")
for q, lang in [('hej', 'da'), ('ciao', 'it'), ('cafe', 'it'), ('hello', 'en')]:
    sr = httpx.get(base+'/api/dictionary/search?q='+q+'&lang='+lang, headers=ha)
    data = sr.json() if sr.status_code == 200 else sr.text[:80]
    count = len(data) if isinstance(data, list) else '?'
    print(f"  search '{q}' ({lang}): {sr.status_code}, {count} results")

print("\n=== PROFILE ===")
for name, hdr in [('Patrizia', hp), ('Aiden', ha), ('Mette', hm)]:
    pr = httpx.get(base+'/api/profile', headers=hdr)
    if pr.status_code == 200:
        p = pr.json()
        print(f"  {name}: ref_lang={p.get('reference_language')}, host={p.get('host_id')}, email={p.get('email')}")
    else:
        print(f"  {name}: {pr.status_code}")

print("\n=== WORD CONTRIBUTION ===")
contrib = httpx.post(base+'/api/dictionary/words', headers=ha, json={
    'word': 'hyggelig', 'language': 'da',
    'translation_en': 'cozy and comfortable',
    'translation_it': 'accogliente e confortevole',
    'phonetic_hint': 'HYG-eh-lee', 'difficulty': 'beginner'
})
print('Contribute status:', contrib.status_code, contrib.text[:200])

# Duplicate detection
contrib2 = httpx.post(base+'/api/dictionary/words', headers=ha, json={
    'word': 'hyggelig', 'language': 'da', 'translation_en': 'snug'
})
print('Duplicate detection:', contrib2.status_code, contrib2.text[:100])

# Long word validation
contrib3 = httpx.post(base+'/api/dictionary/words', headers=ha, json={
    'word': 'a' * 101, 'language': 'da', 'translation_en': 'too long'
})
print('Long word (101 chars):', contrib3.status_code, contrib3.text[:100])

print("\n=== AUTH SECURITY ===")
bad = httpx.post(base+'/api/auth/login', json={'email': 'aiden@example.com', 'password': 'wrongpass'})
print('Bad password:', bad.status_code, bad.text[:80])

noemail = httpx.post(base+'/api/auth/login', json={'email': 'noone@example.com', 'password': 'TestPass1!'})
print('Unknown email:', noemail.status_code, noemail.text[:80])

print('Rate limit test (5 bad attempts):')
rl_email = 'mette@example.com'
for i in range(6):
    rl = httpx.post(base+'/api/auth/login', json={'email': rl_email, 'password': 'badpass'})
    print(f'  attempt {i+1}: {rl.status_code}')

print("\n=== UNAUTHENTICATED ACCESS ===")
unauth = httpx.get(base+'/api/dictionary/categories')
print('Categories no auth:', unauth.status_code)

print("\n=== DELETE ACCOUNT ===")
# register throwaway user and delete
td = httpx.post(base+'/api/auth/register', json={'email': 'throwaway@example.com', 'password': 'TestPass1!', 'reference_language': 'en'})
if td.status_code == 409:
    td = httpx.post(base+'/api/auth/login', json={'email': 'throwaway@example.com', 'password': 'TestPass1!'})
td_tok = td.json().get('token') or td.json().get('access_token', '')
del_r = httpx.delete(base+'/api/profile', headers={'Authorization': 'Bearer '+td_tok})
print('Delete account:', del_r.status_code)
