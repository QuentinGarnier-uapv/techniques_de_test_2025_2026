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
- coverage : coverage aprés implémentation d'environ 80%. Cela peut s'expliquer par le fait que, bien sur pour un étudiant comme moi qui met en place ses premiers tests je n'ai pas pu imaginer tout les cas possibles.Voici les types de test manquants principaux.
    * Test triangulator en fonctiond es réponses de l'API : Ayant déja implémenté les tests API, cela m'était totalement sortit de la tête qu'il aurait fallu tester la réaction de mon code en fonction des réponses de l'API. Ainsi j'ai ajouté des tests qui mockent les réponses de l'API et testent la réaction de mon code en fonction des réponses de l'API.
    * Cas trop spécifique pour y penser : Dans le triangulator, je n'avais pas imaginé le cas des points colinéaires trop proches. En effet, si quand on calcule la surface d'un potentiel triangle pour tester la colinéarité, si on attend que la surface soit > 0 on peut se retrouver dans des situation bizzares ou on a des valeurs extrêmement proches de 0 qui sont considérées comme égales à 0. Ainsi j'ai du rajouté un test pour ce cas.
    * Simple Oubli d'inattention : Dans les tests des models, j'ai, surement par manque de temps et de concentration, oublié de tester le "to_tuple" du Point. De plus je n'ai pas prévu de cas d'erreur levée dans le cas de données invalides rentrées (ex: : from_bytes avec des données trop petites)


coverage actuel :
python -m coverage report
Name                  Stmts   Miss  Cover
-----------------------------------------
Triangulator.py         128      9    93%
models\Point.py          17      0   100%
models\PointSet.py       26      0   100%
models\Triangle.py       18      2    89%
models\Triangles.py      38      0   100%
triangulator_app.py      25      2    92%
-----------------------------------------
TOTAL                   252     13    95%


Actuellement, dans le Triangulator je suis a 93% de coverage mais je ne sais pas comment augmenter le pourcentage ni dans le model Triangle et dans l'app. Cependant un coverage de 95% est déjà assez bon.

Enfin pour terminer correctement le projet il ne manquait plus qu'une CI qui lancait automatiquement les tests, le linter et le coverage, ce que j'ai créé avec le fichier ci.yml sur l'image classique ubuntu-latest.