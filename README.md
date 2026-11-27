# Jeu de Course 2D - Projet POO 2026

Ce projet est un jeu de course de voitures en 2D inspiré de Trackmania et Mario Kart, développé en Python selon l'architecture MVC.

## Installation

1. Assurez-vous d'avoir Python 3 installé sur votre ordinateur.
2. Ouvrez un terminal à la racine du dossier du projet.
3. Installez la dépendance requise (`pygame`) :

```bash
pip install -r requirements.txt
```

## Lancement

Depuis la racine du projet, lancez le jeu avec :

```bash
python main.py
```

Pour exécuter les tests unitaires :

```bash
python -m pytest tests
```

## Commandes

* **Joueur 1 :** `Z` / `W` (accélérer), `S` (freiner / reculer), `Q` / `A` (gauche), `D` (droite).
* **Joueur 2 :** Flèches directionnelles (`Haut`, `Bas`, `Gauche`, `Droite`).
* **Menus :** Flèches directionnelles et `Entrée` pour choisir le mode, le circuit et le nombre de tours.

## Répartition des tâches (Groupe CIMES)

* **Membre 1 (Assane) — Physique des véhicules :** Gérer la dynamique des voitures, incluant l'accélération, le freinage, le braquage et la logique de dérapage réaliste.
* **Membre 2 (Boaz) — Carte et environnement :** Implémenter les terrains (route, herbe, terre, glace, vide) avec leurs effets sur l'adhérence, programmer les blocs (départ, points de passage, ligne d'arrivée, boosts) et concevoir les circuits.
* **Membre 3 (Xu) — Interface et Contrôles :** Développer le menu de navigation, l'affichage global de la vue et la configuration du contrôleur pour gérer deux joueurs simultanément sur un seul clavier.


## Déclaration d'utilisation de l'IA

Conformément aux consignes du projet, voici les usages qui ont été faits d'outils d'IA :

* **Traduire ou expliquer le sujet :** Oui (vérification des consignes et du barème).
* **Aide à la phase de conception :** Oui.
* **Membre 1(ASSANE):**
* **Membre 2(BOAZ):**
* **Membre 3(Xu):**

* **Écriture de code :** Oui.
* **Membre 1(ASSANE):**
* **Membre 2(BOAZ):**
* **Membre 3(Xu):**

* **Débogage :** Oui.
* **Membre 1(ASSANE):**
* **Membre 2(BOAZ):**
* **Membre 3(Xu):**

* **Écriture de commentaires et docstrings :** Oui (reformulation et ajout de docstrings normalisées).
* **Dessin du diagramme de classes UML :** Non (non requis en filière CIMES).

* **Autres usages :**
* **Membre 1(ASSANE):**
* **Membre 2(BOAZ):**
* **Membre 3(Xu):** Génération d'une image de course de voiture et aide à l'importation de la bibliothèque de chemins pour l'afficher en décoration de fond.
 