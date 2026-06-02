# Segmentácia koronálnych štruktúr v sekvencii obrazov slnečnej koróny

Tento repozitár obsahuje praktickú časť bakalárskej práce **„Segmentácia koronálnych štruktúr v sekvencii obrazov slnečnej koróny“**.

Práca porovnáva referenčný model **SCSS-Net** s navrhnutou architektúrou **ConvLSTM-SCSS-Net**. SCSS-Net slúži ako základný porovnávací model, ktorý spracúva jeden obraz, zatiaľ čo ConvLSTM-SCSS-Net spracúva krátku sekvenciu časovo blízkych obrazov slnečnej koróny.

Cieľom je overiť, či časový kontext získaný zo sekvencie obrazov môže zlepšiť segmentáciu koronálnych štruktúr.

## Štruktúra repozitára

```text
src/                 definície modelov a metrík
notebooks/           notebooky so štandardným pipeline
trained_models/      natrénované modely SCSS-Net a ConvLSTM-SCSS-Net
data/                kompaktné dátové sady na predikciu
outputs/             výstupy vytvorené po spustení notebookov
requirements.txt     Python závislosti
```

## Modely

Repozitár obsahuje dva modely:

* **SCSS-Net** — základný model pracujúci s jedným obrazom;
* **ConvLSTM-SCSS-Net** — navrhnutý model pracujúci so sekvenciou obrazov.

Štandardná sekvencia obsahuje tri predchádzajúce snímky a aktuálny cieľový obraz:

```text
input_1, input_2, input_3, target image
```

Model následne predikuje segmentačnú masku pre cieľový obraz.

## Dáta

Kompletné tréningové dátové sady nie sú súčasťou repozitára z dôvodu ich veľkosti.

Namiesto toho repozitár obsahuje kompaktné finálne dátové sady na predikciu:

```text
data/CH_predict_2021/
data/AR_predict_2021/
```

Tieto dátové sady slúžia na demonštráciu finálnej predikcie a post-processing pipeline s už natrénovanými modelmi.

## Notebooky

Repozitár obsahuje dva hlavné notebooky:

```text
notebooks/CH_demo.ipynb
notebooks/AR_demo.ipynb
```

Oba notebooky zachovávajú štruktúru kompletného štandardného pipeline:

1. nastavenie a konfigurácia;
2. vyhľadanie dát;
3. príprava časovej sekvencie;
4. predspracovanie a generátory;
5. vytvorenie modelov;
6. zástupná časť pre tréning;
7. načítanie natrénovaných modelov;
8. finálna predikcia;
9. post-processing;
10. vizuálne a numerické porovnanie.

Kompletný tréning je predvolene vypnutý, pretože úplná tréningová dátová sada nie je súčasťou repozitára. Namiesto toho notebooky načítavajú natrénované modely z priečinka:

```text
trained_models/
```

## Ako spustiť

Nainštalujte potrebné závislosti:

```bash
pip install -r requirements.txt
```

Spustite Jupyter Notebook:

```bash
jupyter notebook
```

Potom spustite jeden z notebookov v priečinku `notebooks/`.

Notebooky používajú relatívne cesty, preto by mala zostať zachovaná táto štruktúra repozitára:

```text
src/
notebooks/
trained_models/
data/
```

Počas spustenia sa ZIP súbory z priečinka `data/` automaticky rozbalia, natrénované modely sa načítajú a predikcie sa uložia do priečinka:

```text
outputs/
```

## Výstup

Notebooky generujú:

* predikované binárne masky;
* obrázky na vizuálne porovnanie;
* overlay porovnania;
* CSV súbory s metrikami;
* konfiguračné súbory spustenia.

Farby v overlay porovnaní:

```text
red    = iba baseline model
cyan   = iba ConvLSTM model
yellow = oba modely
```

## Poznámky

Repozitár slúži na demonštráciu praktického pipeline a procesu finálnej predikcie. Kompletný tréning od začiatku vyžaduje pôvodné úplné dátové sady, ktoré nie sú súčasťou tohto repozitára.
