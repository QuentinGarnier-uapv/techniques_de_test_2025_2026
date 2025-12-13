# TODO

Notes modifs tests :
- test perfs : réduction de la taille des tests pour éviter un make test trop long => besoin de définir des timeout plus réel masi trop arbitraire de le faire pour le moment
- Test_unit :
    J'ai pu imaginer durant mon implémentation des cas que j'avais oublié de prendre en charge lors de l'implémentation des tests unitaires
    - test_all_collinear : quand tout les points sont aligné => aucun triangle est formable donc un raise doit etre effectué
- coverage : diminnution du pourcentage de coverage du aux cas non prévu lors de l'implémentation des tests => ajout de tests necessaires 

Choix algo triangulation :
- Bowyer-Watson : 
    - Simple et robuste
    - Optimisé grace au tri et à la condition d'arrêt : on passe de de O(N^2) à O(NlogN) ce qui est moins complexe
    - garantie propriété Delaunay => qualité des triangles optimale
- Divide and Conquer : 
    - Le plus utilisé dans des projets qui demandent des performances (O(NlogN) strictement)
    - Extrémement difficile a implémenter 
    - Existe dans des librairies comme Qhull mais pas possible dans notre cas car interdit d'utiliser d'autres librairies dans le Sujet.md

=> Une implémentation personnelle sera forcement moins optimisé qu'une utilisation spécialisée. Ainsi la gestion de la mémoire est loin d'être optimale car beaucoup de listes sont crées

Tests fixés :
- linter : j'ai simplement corrigé les erreurs donnée en executant le make lint (beaucoup de docstring manquante, lignes trop longues, etc) => voir lint_report.txt

