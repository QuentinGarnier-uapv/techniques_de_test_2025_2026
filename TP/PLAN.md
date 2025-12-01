# PLAN - Stratégie de test

> **Note préliminaire :** Avant de débuter ce plan, il est important de souligner le fait que **seul le service
Triangulator sera implémenté et testé**. Les autres services (`PointSetManager`) seront simulés via des mocks pour
> permettre des tests isolés et contrôlés.

Cela constitue pour moi une problématique importante, car cela nécessite de bien comprendre les interactions entre les
services afin de ne pas implémenter inutilement des fonctionnalités hors du périmètre du TP. Ainsi, il est possible que
ce plan évolue légèrement en fonction de la compréhension des interactions entre services.

---

### 1. Tests d’API — Routes Flask (`Triangulator`)

**Objectif :**
Vérifier que le service **Triangulator** respecte la spécification OpenAPI et interagit correctement avec le *
*PointSetManager (PSM)**.

**Méthode :**
Utiliser `Flask.test_client()` et un mock du PSM simulant :

* `POST /pointset` — création d’un PointSet
* `GET /pointset/{pointSetId}` — récupération d’un PointSet existant

**Cas normaux :**

* `GET /triangulation/{pointSetId}`
    * `->` Le Triangulator contacte le PSM.
    * `->` Le PSM mock renvoie **200** avec un binaire `PointSet` valide.
    * `->` Le Triangulator calcule la triangulation.
    * **Attendu :** `200` + `application/octet-stream` contenant un binaire `Triangles` cohérent.

**Cas d’erreur :**

* **Mauvais format de requête** (id invalide, etc.)
    * `->` Attendu : Le Triangulator renvoie **400** (erreur syntaxe).

* **PointSetID introuvable** (PSM renvoie null)
    * `->` Attendu : Le Triangulator renvoie **404** (ressource inexistante).

* **Erreur interne de triangulation** (Données corrompues, points dupliqués)
    * `->` Attendu : Le Triangulator renvoie **500** avec message JSON.

* **Service PSM indisponible** (Timeout / 503 du mock)
    * `->` Attendu : Le Triangulator renvoie **503**.

**Formats attendus :**

* **Succès** : `application/octet-stream`
* **Erreur** : `application/json` (`{"code": "...", "message": "..."}`)

---

### 2. Tests unitaires — Algorithme de triangulation

**But :** Valider la logique mathématique indépendamment de l’API.

**Méthode :**

* **Cas simples (Nominaux) :**
    * 3 points formant un triangle `->` 1 triangle attendu.
    * 4 points formant un carré `->` 2 triangles.
    * Polygones réguliers `->` n-2 triangles.
* **Cas dégénérés (Limites) :**
    * Aucun point, 1 point, 2 points `->` 0 triangle.
    * Points doublons ou colinéaires `->` aucun triangle ou comportement défini.

---

### 3. Tests unitaires — Encodage/Décodage binaire

Il me semble nécessaire de tester l'encodage et le décodage. Cela revient à tester la structure des données du projet :
`Point`, `PointSet`, `Triangle`, `Triangles`.

**But :** Vérifier que les fonctions de lecture/écriture des structures binaires fonctionnent correctement pour chaque
modèle.

**Méthode :**

* Tester un aller-retour complet `encode -> decode -> encode`.
* Vérifier les cas limites : données trop courtes, valeurs incohérentes.

---

### 4. Tests d’intégration (partiel)

**But :** Tester l’enchaînement complet `Binaire entrée -> Calcul -> Binaire sortie`.

**Méthode :**

* Fournir un `PointSet` binaire connu.
* Appeler le service complet.
* Décoder la réponse et vérifier la cohérence (indices valides, nombre correct de triangles, etc.).

---

### 5. Tests de performance

**But :** Mesurer la rapidité de l’encodage/décodage et du calcul sur des volumes variés.

**Méthode :**

* **Génération paramétrique :** Utilisation de `pytest.mark.parametrize` pour croiser :
    * **Tailles :** 100, 1000, 5000, 10000, 20000 points.
    * **Distributions :** Uniforme, Linéaire, Clustered (Gaussian Blobs).
    * **Amplitudes :** (0-10) à (0-10000).
* **Métriques :** Temps d'encodage binaire et temps de triangulation pur.
* **Seuils :** Assertions dynamiques selon la taille (ex: < 0.5s pour < 2000 pts).

---

## 6. Jeux de données de test

| Type              | Détails                                                                                                                                                 |
|:------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Déterministes** | Vide, 1pt, 2pts, Triangle, Carré, Polygones réguliers, Doublons                                                                                         |
| **Aléatoires**    | **Uniforme** (Bruit blanc)<br>**Linéaire** ($y=ax+b + \epsilon$)<br>**Clustered** (Gaussian Blobs, mélange de gaussiennes autour de centres aléatoires) |

---

## 7. Outillage & Commandes

* `pytest` pour tous les tests.
* `coverage` pour la couverture.
* `ruff` pour la qualité du code (Configuré pour ignorer les règles de documentation trop strictes `D`).
* `pdoc3` pour la documentation automatique.
* `Makefile` pour centraliser les commandes.

### Commandes Makefile

* `make test` : lance tous les tests.
* `make unit_test` : lance tous les tests sauf les tests de performance.
* `make perf_test` : lance uniquement les tests de performance.
* `make coverage` : génère un rapport de couverture de code.
* `make lint` : valide la qualité de code.
* `make doc` : génère la documentation en HTML.

---

## 8. Critères de validation

* [x] Tous les tests passent (Green) ou échouent pour les bonnes raisons (Red state TDD).
* [ ] Obtenir un très bon score de couverture (>90%).
* [ ] La documentation `pdoc3` générée automatiquement.
* [ ] Les tests de performance s’exécutent sans dépassement excessif de temps.