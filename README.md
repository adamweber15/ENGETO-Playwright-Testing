# ENGETO – Final Project 3
## Automated Testing with Playwright

**Author / Autor:** Adam Weber  
**Date / Datum:** 26. 11. 2026  
**Tested application:** [SauceDemo](https://www.saucedemo.com/)

[Česká verze (CZ)](#česká-verze-cz) | [English version (EN)](#english-version-en)

---

## Česká verze (CZ)

### Cíl projektu

Cílem projektu je vytvoření tří automatizovaných testů webové aplikace pomocí frameworku Playwright v jazyce Python s využitím pluginu pytest-playwright.

Testování je zaměřeno na funkčnost, validaci vstupních údajů, integritu produktových dat a nákupní proces testovacího e-shopu SauceDemo.

### Testovací scénáře

| ID | Testovací scénář | Výsledek |
|---|---|---|
| TC-01 | Validace povinných objednávkových údajů | PASS |
| TC-02 | Řazení produktů podle ceny a integrita katalogu | PASS |
| TC-03 | Dokončení nákupu po úpravě obsahu košíku | PASS |

### Výsledky testování

| Prohlížeč | Headed | Headless |
|---|---:|---:|
| Chromium | 3/3 PASS | 3/3 PASS |
| Firefox | 3/3 PASS | 3/3 PASS |
| WebKit | 3/3 PASS | 3/3 PASS |
| **Celkem** | **9/9 PASS** | **9/9 PASS** |

- Počet automatizovaných testů: 3
- Formální cross-browser exekuce: 18/18 PASS
- Diagnostická porovnání: 192/192 PASS
- Celkový počet provedení finální verze: 27/27 PASS
- Neúspěšné testy: 0

Dodatečné exekuce zahrnovaly kontrolní spuštění všech testů, samostatné spuštění jednotlivých testů a ověření v novém virtuálním prostředí na stejném počítači.

Během testování bylo zaznamenáno upozornění pytestu na zastaralý způsob definice fixture. Upozornění nezpůsobilo selhání žádného testu.

### Dokumentace a důkazní materiály

- [Kompletní PDF dokumentace](documentation/ENGETO_PROJECT_3.pdf)
- [Headed – XML report](evidence/results_headed.xml)
- [Headless – XML report](evidence/results_headless.xml)
- [Headed – výstup testování](evidence/test_execution_headed.txt)
- [Headless – výstup testování](evidence/test_execution_headless.txt)

Ve zveřejněných kopiích reportů byly anonymizovány lokální uživatelské jméno a název počítače. Výsledky testů a naměřené časy zůstaly nezměněny.

### Omezení testování

Testy ověřují uživatelské rozhraní demonstrační aplikace. Neověřují databázi, skutečné platby ani nezávislou správnost daňové sazby. Celková cena je kontrolována na základě vypočteného mezisoučtu a zobrazené daně.

V rozsahu provedených testů nebyly zjištěny žádné funkční defekty. Výsledky nepředstavují vyčerpávající ověření celé aplikace.

---

## English version (EN)

### Project objective

The objective is to implement three automated web tests using Python, Playwright and the pytest-playwright plugin.

The project focuses on input validation, product data integrity and the checkout process of the SauceDemo demonstration e-commerce application.

### Test scenarios

| ID | Test scenario | Result |
|---|---|---|
| TC-01 | Required checkout field validation | PASS |
| TC-02 | Product price sorting and catalogue integrity | PASS |
| TC-03 | Successful checkout after cart modification | PASS |

### Test results

| Browser | Headed | Headless |
|---|---:|---:|
| Chromium | 3/3 PASS | 3/3 PASS |
| Firefox | 3/3 PASS | 3/3 PASS |
| WebKit | 3/3 PASS | 3/3 PASS |
| **Total** | **9/9 PASS** | **9/9 PASS** |

- Automated tests: 3
- Formal cross-browser executions: 18/18 PASS
- Diagnostic comparisons: 192/192 PASS
- Total executions of the final implementation: 27/27 PASS
- Failed tests: 0

Additional executions included an initial verification run of all tests, individual test runs and verification in a newly created virtual environment on the same computer.

A pytest fixture deprecation warning was recorded. The warning did not cause any test failures.

### Documentation and evidence

- [Full project documentation (Czech)](documentation/ENGETO_PROJECT_3.pdf)
- [Headed – XML report](evidence/results_headed.xml)
- [Headless – XML report](evidence/results_headless.xml)
- [Headed – execution log](evidence/test_execution_headed.txt)
- [Headless – execution log](evidence/test_execution_headless.txt)

Local usernames and hostnames have been anonymized in the published report copies. Test results and execution times remain unchanged.

### Testing limitations

The tests cover the demonstration application's user interface. Database validation, real payments and independent tax rate verification are outside the scope. The order total is verified using the calculated subtotal and the displayed tax.

No functional defects were identified within the tested scope. The results do not constitute exhaustive testing of the entire application.

---

## Technology stack / Použité technologie

| Technology | Version |
|---|---|
| Python | 3.13.18 |
| Playwright | 1.65.2 |
| pytest | 9.2.0 |
| pytest-playwright | 0.10.0 |
| Operating system | macOS |
| IDE | Visual Studio Code |

## Installation / Instalace

Clone the repository / Naklonování repozitáře:

```bash
git clone https://github.com/adamweber15/ENGETO-Playwright-Testing.git
cd ENGETO-Playwright-Testing
```

Create a virtual environment / Vytvoření virtuálního prostředí:

```bash
python3 -m venv .venv
```

Activate the virtual environment / Aktivace virtuálního prostředí (macOS/Linux):

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and browsers / Instalace závislostí a prohlížečů:

```bash
python -m pip install -r requirements.txt
python -m playwright install
```

## Test execution / Spuštění testů

Default browser / Výchozí prohlížeč:

```bash
python -m pytest test_web.py -v
```

Visible browser with diagnostic output / Viditelný prohlížeč s diagnostickým výstupem:

```bash
python -m pytest test_web.py --headed -v -s
```

Cross-browser testing / Testování napříč prohlížeči:

```bash
python -m pytest test_web.py --browser chromium --browser firefox --browser webkit -v
```

Individual test / Samostatný test:

```bash
python -m pytest test_web.py::test_checkout_validation -v
```

## Repository structure / Struktura repozitáře

```text
ENGETO-Playwright-Testing/
├── test_web.py
├── requirements.txt
├── .gitignore
├── README.md
├── documentation/
│   └── ENGETO_PROJECT_3.pdf
└── evidence/
    ├── results_headed.xml
    ├── results_headless.xml
    ├── test_execution_headed.txt
    └── test_execution_headless.txt
```

## References / Zdroje

- ENGETO – Final Project 3 and course materials
- [SauceDemo](https://www.saucedemo.com/)
- [Playwright for Python](https://playwright.dev/python/docs/intro)
- [Playwright Locator API](https://playwright.dev/python/docs/api/class-locator)
- [pytest documentation](https://docs.pytest.org/)
