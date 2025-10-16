# Mise en place de l’environnement GitHub / Intégration d’outils de sécurité automatisée

**Résumé** : Dépôt de démonstration pour la mise en place d’une CI sécurisée (GitHub Actions + CodeQL) + SCA (Dependabot) et module pédagogique (Kahoot + mini-CTF via CTFd).

🔗 Liens rapides :
- **CTF (CTFd)** : En cours....
- **Quiz Kahoot** : https://create.kahoot.it/share/kahoot-cyber/8801ad18-1e16-42b3-89ba-b731c60ca02e
- **Docs / Challenges** : `docs/ctf_description.md` et `kahoot_questions.md` (dans ce repo)
- **CTF local avec Docker** : 'ctf' télécharger le dossier et exécuter le compose.

## Structure du repo
- `.github/workflows/` — CI (main.yml, codeql.yml)  
- `.github/dependabot.yml` — Dependabot config  
- `requirements.txt` — dépendances Python  
- `kahoot_questions.md` — description + lien quiz  
- `docs/` — guides & instructions CTF

> Pour lancer CTFd local : `docker-compose up -d` dans le dossier `CTFd/` (voir docs/ctfd_setup.md)

