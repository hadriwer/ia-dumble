# Optimisation stratégique du jeu Dumble : une approche par apprentissage par renforcement.

## Auteur  

Lagier Hadrien

## Introduction

Ce projet consiste a faire une étude sur la stratégie optimale d'un jeu de carte. Voici un extrait de l'introduction de l'article de recherche, disponible dans le fichier *research*  : 

Le jeu Dumble est un jeu de cartes rapide et stratégique \cite{dumbleRules}. Utilisant un jeu de 52 cartes. Les règles seront expliquées un peu plus tard \ref{regle}. Le but de cette recherche est de trouver une manière efficace de gagner le jeu. Nous utiliserons l'intelligence artificielle pour nous aider a percer les mystères du jeu. Grâce au deep learning l'entrainement d'un modèle permettant a une IA de jouer contre elle même et apprendre de ses erreurs afin qu'elle établisse la meilleure stratégie a adopter.  

## Arborescence du projet

```
.
├── LICENSE
├── ppo_cardgame.zip
├── README.md
├── research
│   ├── research.pdf
│   └── research.tex
└── src
    ├── app
    │   ├── app.py
    │   └── cardSprite.py
    ├── game
    │   ├── boundary.py
    │   ├── cards.py
    │   ├── game.py
    │   ├── hand.py
    │   ├── __init__.py
    │   ├── pioche.py
    │   └── player.py
    ├── ia
    │   ├── CardGameEnv.py
    │   ├── __init__.py
    │   └── train_test.py
    └── tests
        └── test.py
```