## PLAN - Stratégie de test

Avant de débuter ce plan, il est important de souligner le fait que **seul le service Triangulator sera implémenté et
testé**. Les autres services (PointSetManager) seront simulés via des mocks pour permettre des tests isolés
et contrôlés. Cela constitue pour moi une problématique importante, car cela nécessite de bien comprendre les
interactions entre
afin de ne pas implémenter inutilement des fonctionnalités hors du périmètre du TP. Ainsi, il est possible que ce plan
évolue légèrement en fonction de la compréhension des interactions entre services. 

### 1. Tests d’API — Routes Flask (Triangulator)

**Objectif :**
Vérifier que le service **Triangulator** respecte la spécification OpenAPI et interagit correctement avec le **PointSetManager (PSM)**.

**Méthode :**
Utiliser Flask.test_client() et un mock du PSM simulant :

* POST /pointset — création d’un PointSet
* GET /pointset/{pointSetId} — récupération d’un PointSet existant

**Cas normaux :**

* GET /triangulation/{pointSetId}
  -> Le Triangulator contacte le PSM.
  -> Le PSM mock renvoie 200 avec un binaire PointSet valide.
  -> Le Triangulator calcule la triangulation.
  -> Attendu : 200 + application/octet-stream contenant un binaire Triangles cohérent.


**Cas d’erreur :**

* **Mauvais format de requête** -> Envoyer un id de point au mauvais format (ex. chaîne vide, caractères non valides).
  -> Attendu : le Triangulator renvoie **400**, indiquant une erreur de syntaxe dans la requête.

* **The specified PointSetID was not found (as reported by the PointSetManager).** -> Le mock du PSM renvoie null quand
  le Triangulator demande un PointSet inexistant.
  -> Attendu : le Triangulator renvoie **404**, indiquant que le PointSet demandé n’existe pas.

* **Erreur interne de triangulation** -> Injecter un PointSet valide mais non triangulable (ex. points dupliqués ou
  dégénérés) OU Le mock du PSM renvoie un corps application/octet-stream mal formé (ex. taille
  incorrecte, données tronquées).
  -> Attendu : le Triangulator échoue au calcul et renvoie **500** avec un message d’erreur.

* **Triangulator renvoie 503** -> Simuler une panne du service PSM (mock renvoyant une réponse 503 ou aucun retour).
  -> Attendu : le Triangulator renvoie **503**, indiquant que la couche de stockage du PSM est indisponible.

**Formats attendus :**

* Succès -> application/octet-stream ou application/json
* Erreur -> application/json "code": ..., "message": ...

---

### 2. Tests unitaires — Algorithme de triangulation

**But :** valider la logique mathématique indépendamment de l’API.
**Méthode :**

* Cas simples :

    * 3 points formant un triangle -> 1 triangle attendu.
    * 4 points formant un carré -> 2 triangles.
    * Polygones réguliers -> n-2 triangles.
* Cas dégénérés :
    * Aucun point -> 0 triangle.
    * Points doublons ou colinéaires -> aucun triangle ou comportement défini.

---

### 3. Tests unitaires — Encodage/Décodage binaire Triangles

Ici il ne me semble pas necessaire de tester l'encodage/décodage des points étant donné que cela sort du perimetre du TP.

**But :** vérifier que les fonctions de lecture/écriture des structures binaires fonctionnent correctement.
**Méthode :**

* Tester un aller-retour complet encode -> decode -> encode.
* Vérifier les cas limites : données trop courtes, valeurs incohérentes, nombres spéciaux (NaN, inf).

---

### 4. Tests d’intégration (partiel)

Pour cette partie, cela me semble complexe de faire un test d'intégration complet sans implémenter le PointSetManager.
Je vais ainsi tenter de respecter le plus possible le principe des tests d'intégration en mockant les interactions avec
le PointSetManager mais cela s'éloignera légèrement d'un test d'intégration classique.

**But :** tester l’enchaînement complet binaire -> triangulation -> binaire.
**Méthode :**

* Fournir un PointSet binaire connu.
* Appeler le service complet.
* Décoder la réponse et vérifier la cohérence (indices valides, nombre correct de triangles, etc.).

Pour cela, création d'un set de données associés avec les résultats attendus.

---

### 5. Tests de performance

**But :** mesurer la rapidité de l’encodage/décodage et du calcul.
**Méthode :**

* Générer aléatoirement des ensembles de 100, 500, 1000 et 2000 points.
* Mesurer séparément :
    * Temps d’encodage/décodage binaire.
    * Temps de triangulation.
* Comparer les résultats entre exécutions.
* Ces tests seront exclus des tests unitaires classiques.

---

## Jeux de données de test

* **Déterministes :**
    * Vide
    * 1 point
    * 2 points
    * Triangle simple
    * Carré
    * Polygones réguliers (5 à 8 côtés)
    * Points dupliqués
* **Aléatoires :**
    * Nuages de points aléatoires (non dupliqués) de tailles 100, 500, 1000, 2000.

---

## Outils

* pytest pour tous les tests.
* coverage pour la couverture.
* ruff pour la qualité du code.
* pdoc3 pour la documentation automatique.
* Makefile pour centraliser les commandes.

---

## Cibles Makefile

make
make test # tous les tests
make unit_test # sans les tests de perf
make perf_test # uniquement les tests de perf
make coverage # rapport de couverture
make lint # vérification du style
make doc # génération de la doc

---

## 7) Critères de validation

* Tous les tests passent.
* Obtenir un trés bon score de couverture (>90%) => à voir celon la pertinence des tests.
* La documentation pdoc3 générée automatiquement.
* Les tests de performance s’exécutent sans dépassement excessif de temps. => à définir selon les résultats obtenus.

---
