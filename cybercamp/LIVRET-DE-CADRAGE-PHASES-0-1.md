# Introduction au DevOps & Fondations Applicatives

## Objectif du document
Ce guide contient les axes de recherche et les questions clés auxquelles vous devez répondre pour valider les deux premières étapes de votre workshop. Vous pouvez utilisez l'IA (ChatGPT, Claude, etc.) ou des ressources vidéo pour mener vos recherches, puis consignez vos réponses dans le rapport selon la structure demandée à la fin.

---

## PHASE 0 : Initialisation & Création des Environnements

### 1. Immersion Culturelle : Qu'est-ce que le DevOps ?

**Q1.1** : Expliquez avec vos propres mots ce qu'est le mouvement DevOps. Quelle est la différence majeure entre l'organisation d'une équipe technique avant le DevOps (le modèle traditionnel "Silos") et après l'adoption du DevOps ?

**Q1.2** : Quel est le but ultime du DevOps lorsqu'on développe et qu'on livre un logiciel à des utilisateurs ?

---

### 2. Configuration des Comptes (Livrable Obligatoire)

Vous devez créer un compte sur les trois plateformes industrielles suivantes. **Exigence** : Remplissez le tableau suivant dans votre rapport avec vos identifiants exacts :

| Plateforme | Utilité dans le Workshop | Nom d'utilisateur (Username) | URL du Profil |
| :--- | :--- | :--- | :--- |
| **GitHub** | Hébergement du code & Automatisation CI/CD | `Votre_User` | `https://github.com/YourUser` |
| **DockerHub** | Registre public pour nos conteneurs | `Votre_User` | `https://hub.docker.com/u/YourUser` |
| **Microsoft Azure** | Infrastructure Cloud de Production | `Votre_Email_Azure` | (Non applicable) |

---

## PHASE 1 : Fondations du Web Development & Gestion des Sources

### Module A : Architecture Web & Communication (The "Why")

**Q2.1** : Quelle est la différence fondamentale entre le Frontend et le Backend d'une application ? Quel est le rôle spécifique de la Base de données ?

**Q2.2** : Comparez brièvement l'Architecture Client-Serveur et l'Architecture 3-Tiers (3 couches). Pourquoi l'architecture 3-tiers est-elle considérée comme standard et plus sécurisée pour le web ?

**Q2.3** : Qu'est-ce qu'une API (Application Programming Interface) ? Prenez l'analogie d'un serveur dans un restaurant pour expliquer son rôle entre le Frontend et le Backend.

**Q2.4** : Comment sécurise-t-on la communication entre le Backend et la Base de données pour éviter que n'importe qui puisse lire ou modifier nos données ?

---

### Module B : Configuration, Frameworks & Écosystème

**Q3.1** : Que sont les variables d'environnement (`.env`) ? Pourquoi est-il strictement interdit d'écrire des mots de passe ou des clés d'API directement dans le code source (Hardcoding) ?

**Q3.2** : Comment configure-t-on le fichier `.gitignore` pour s'assurer que le fichier `.env` local ne soit jamais publié sur GitHub ?

**Q3.3** : Dans l'écosystème du développement moderne, expliquez brièvement la différence entre : Un Framework, une Dépendance (ou Package) et une Librairie Open Source.

---

### Module C : Anatomie d'un Projet & Risques (Dev VS Prod)

**Q4.1** : Observez l'arborescence standard d'un projet web moderne (exemple type d'un projet full-stack). Expliquez brièvement le rôle des dossiers clés :

my-app/
├── frontend/         # Code exécuté dans le navigateur de l'utilisateur
│   ├── src/
│   └── package.json  # Gestion des dépendances du Frontend
├── backend/          # Code exécuté sur le serveur (Logique métier)
│   ├── src/
│   ├── .env          # Variables de configuration confidentielles
│   └── package.json  # Gestion des dépendances du Backend
└── .gitignore        # Liste des fichiers à exclure du tracking Git

**Q4.2** : Qu'est-ce qui différencie un Environnement de Développement Local (votre PC) d'un Environnement de Production (le Cloud en ligne) ?

**Q4.3** : Citez 2 risques ou bugs majeurs qui peuvent survenir lorsqu'on passe une application du local à la production (le fameux "Mais ça marchait sur ma machine !"). Comment le DevOps aide-t-il à prévenir ces risques ?

### Module D : Maîtrise de Git & Préparation à l'Automatisation**

**Q5.1** : Quelle est la différence essentielle entre Git et GitHub ?

**Q5.2** : Qu'est-ce que le contrôle de version et pourquoi est-ce indispensable quand plusieurs ingénieurs travaillent sur le même projet ?

**Q5.3** : Expliquez le cycle de vie d'une modification de code à travers ces actions fondamentales : Commit → Push → Pull.

**Q5.4** : Comment fonctionnent les Branches dans Git ? Comment deux développeurs peuvent-ils coder en même temps sans écraser le travail de l'autre ?

**Q5.5** : Quelle est la différence entre un dépôt Public et Privé ? Dans quel cas choisit-on l'un ou l'autre ?

**Q5.6** : En grattant la surface : Qu'est-ce qu'un pipeline CI/CD et quel est le rôle de GitHub Actions dans ce processus d'automatisation ?

###  Structure de rapport demandée 

Tous les membres doivent rendre leur rapport au format Markdown (.md) nommé Rapport_Phase_0_1.md dans leur dépôt GitHub. Le document doit respecter scrupuleusement la structure suivante :
markdown

# Rapport d'Ingénierie : Initialisation & Fondations Web
**Titre de la phase :** Phase 0 & 1 - Initialisation & Fondations Web
**Préparé par :** `Vos Noms & Prénoms`
---

## 1. Comptes & Environnements (Phase 0)
* Inclure ici le tableau complété des plateformes (GitHub, DockerHub, Azure).
* Capture d'écran montrant vos profil GitHub actif.

## 2. Rapport de Concepts Théoriques (The "Why")
* Répondez ici à toutes les questions des Modules A, B, C et D de manière claire, concise et vulgarisée. 

## 3. Journal d'Implémentation Technique (The "How")
Racontez votre expérience pratique sur cette phase :
* Comment avez-vous initialisé votre premier dépôt Git ? (Fournir les commandes utilisées).
* Comment avez-vous testé l'isolation de votre fichier `.env` ?

## 4. Tableau Post-Mortem (Gestion des Erreurs)
Si vous avez rencontré des erreurs ou des blocages durant vos manipulations (Git, commandes, configuration), vous devez obligatoirement remplir ce tableau (Même si l'erreur a été résolue par l'IA) :

| Erreur / Message de Log | Cause de l'erreur | Comment l'avez-vous résolue ? |
| :--- | :--- | :--- |
| *Ex: fatal: pathspec '.env' did not match...* | *Le fichier n'était pas dans le bon dossier* | *Déplacement du fichier et réexécution de git add* |

## 5. Conclusion & Prochaine Étape
* Qu'avez-vous appris de plus important durant cette phase ?
* Vous sentez-vous prêt à passer à l'étape "Infrastructure & Linux" ?