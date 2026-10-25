# Kuusaa Karooraa – Waajjira Diinagdee Ganda Waajjuu Daalotaa

## Amaloota
- Karoora haaraa galmeessuu, gulaaluu fi haquu
- Damee hojii, bara, kurmaana fi itti gaafatamaa galmeessuu
- Baajata, baasii fi dhibbeentaa raawwii hordofuu
- Gabaasa damee hojii ilaaluu fi maxxansuu/PDF gochuu
- Odeeffannoo SQLite keessatti kuusuu

## Akka kompiitara irratti hojii jalqabsiiftu
1. Python 3 install godhi.
2. Terminal/Command Prompt keessatti folder project kana bani.
3. Ajaja kana hojjedhu:
   ```bash
   pip install -r requirements.txt
   python app.py
   ```
4. Browser keessatti `http://127.0.0.1:5000` bani.

## GitHub irratti olkaa'uu
Faayilota kana hunda repository kee keessatti olkaa'i. `app.py`, `requirements.txt`, `templates/` fi `static/` hunda dabali.

## Hubachiisa hosting
Kun Flask + SQLite project jalqabaa dha. SQLite faayiliin kuusaa (`karooraa.db`) yeroo deployment irratti kuufama dhaabbataa qabaachuu qaba. Hosting tokko tokko keessatti disk dhaabbataa barbaachisa; yoo hosting faayilota yeroo restart bade, PostgreSQL ykn persistent disk fayyadami.

## Nageenya
Kun prototype jalqabaa dha. Odeeffannoo hojii dhugaa kuusuu dura login/role, backup, secret key nageenya qabu, validation dabalataa fi HTTPS dabaluu gorfama. `app.secret_key` jijjiiri.
