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


## Utilisation de l'IA

   Utilisation pour la création d'une image d'une course de voiture et l'importation du bibliothèque path pour utiliser l'image en tant que décoration de fond.