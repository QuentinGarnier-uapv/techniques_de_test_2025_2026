# RETEX

## Notes sur les modifications et corrections des tests

- **Tests de performance** : Réduction de la taille des tests pour éviter un `make test` trop long.
  => Besoin de définir des timeouts plus réels, mais trop arbitraire de le faire pour le moment.
- **Tests unitaires** :
  - J'ai pu imaginer durant mon implémentation des cas que j'avais oublié de prendre en charge lors de l'implémentation des tests unitaires.
  - `test_all_collinear` : Quand tous les points sont alignés => aucun triangle n'est formable, donc un `raise` doit être effectué.
- **Linter** : J'ai simplement corrigé les erreurs données en exécutant le `make lint` (beaucoup de docstrings manquantes, lignes trop longues, etc.) => voir `lint_report.txt`.
- **Coverage** : Diminution du pourcentage de coverage due aux cas non prévus lors de l'implémentation des tests (coverage initial d'environ 80%).
  - *Test triangulator en fonction des réponses de l'API* : Ayant déjà implémenté les tests API, cela m'était totalement sorti de la tête qu'il aurait fallu tester la réaction de mon code en fonction des réponses de l'API. Ainsi j'ai ajouté des tests qui mockent les réponses de l'API et testent la réaction de mon code. Point important a souligner : ces tests ont été ajoutés dans "test_integration_triangulator.py", se raprochant plus de l'intégration API que des tests unitaires.
  - *Cas trop spécifique pour y penser* : Dans le triangulator, je n'avais pas imaginé le cas des points colinéaires trop proches. En effet, quand on calcule la surface d'un potentiel triangle pour tester la colinéarité, si on attend que la surface soit > 0 on peut se retrouver dans des situations bizarres où on a des valeurs extrêmement proches de 0 qui sont considérées comme égales à 0. Ainsi j'ai dû rajouter un test pour ce cas.
  - *Simple oubli d'inattention* : Dans les tests des models, j'ai, sûrement par manque de temps et de concentration, oublié de tester le `to_tuple` du Point. De plus je n'ai pas prévu de cas d'erreur levée dans le cas de données invalides rentrées (ex: `from_bytes` avec des données trop petites).

## Choix de l'algorithme de triangulation

- **Bowyer-Watson** :
  - Simple et robuste.
  - Optimisé grâce au tri et à la condition d'arrêt : on passe de O(N²) à O(NlogN), ce qui est moins complexe.
  - Garantie la propriété de Delaunay => qualité des triangles optimale.
- **Divide and Conquer** :
  - Le plus utilisé dans des projets qui demandent des performances (O(NlogN) strictement).
  - Extrêmement difficile à implémenter.
  - Existe dans des librairies comme `Qhull` mais pas possible dans notre cas car interdit d'utiliser d'autres librairies dans le `Sujet.md`.

> Une implémentation personnelle sera forcément moins optimisée qu'une utilisation spécialisée. Ainsi la gestion de la mémoire est loin d'être optimale car beaucoup de listes sont créées.

## Coverage actuel

```bash
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
```

Actuellement, dans le `Triangulator` je suis à 93% de coverage mais je ne sais pas comment augmenter le pourcentage, ni dans le model `Triangle` et dans l'`app`. Cependant un coverage de 95% est déjà assez bon.

## Conclusion

Enfin, pour terminer correctement le projet il ne manquait plus qu'une CI qui lançait automatiquement les tests, le linter et le coverage, ce que j'ai créé avec le fichier `ci.yml` sur l'image classique `ubuntu-latest`. Cette derniére étape n'était pas citée dans le plan initial mais cela m'a semblé plus qu'indispensable pour terminer correctement le projet.

Je tien a enfin vous remercier pour ce sujet qui est fort original et qui nous force rééllement a nous concentrer sur la stratégie de test plutôt que sur l'implémentation réelle. 

cas déf auparavant

verif cas n-2 => avec le cas du sujet.