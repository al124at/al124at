# Segmentácia koronálnych štruktúr v sekvencii obrazov slnečnej koróny

Tento repozitár obsahuje praktickú časť bakalárskej práce **„Segmentácia koronálnych štruktúr v sekvencii obrazov slnečnej koróny“**.

Cieľom práce bolo porovnať základnú architektúru **SCSS-Net** s upravenou architektúrou **ConvLSTM-SCSS-Net**, ktorá okrem cieľového obrazu využíva aj časový kontext zo sekvencie predchádzajúcich snímok slnečnej koróny.

Základný model SCSS-Net spracúva jeden cieľový obraz. Model ConvLSTM-SCSS-Net spracúva sekvenciu:

```text
input_1, input_2, input_3, target image
```

a vytvára segmentačnú masku pre cieľový obraz `target image`.

## Štruktúra repozitára

```text
configs/          konfiguračné súbory jednotlivých experimentov
data/             dodatočné vyhodnocovacie výberky pre predikciu
src/              definície modelov a metrík
trained_models/   uložené natrénované modely
figures/          obrázky použité v notebookoch a dokumentácii
outputs/          výstupy vytvorené po spustení notebookov
AR_demo.ipynb     demonštračný pipeline pre aktívne oblasti
CH_demo.ipynb     demonštračný pipeline pre koronálne diery
requirements.txt  zoznam Python knižníc
```

## Poznámka k tréningovým dátam

Kompletné tréningové dáta nie sú súčasťou repozitára. Dôvodom je ich veľkosť, keďže pôvodná výberka bola rozšírená o časové sekvencie snímok. Celkový objem plných tréningových dát by bol príliš veľký na praktické uloženie v repozitári.

Notebooky preto neobsahujú plnohodnotné spustenie tréningu od začiatku. Tréningový pipeline je v nich opísaný slovne podľa pôvodných experimentálnych notebookov. Spustiteľná časť sa zameriava na predikciu pomocou už natrénovaných modelov.

## Dodatočné vyhodnocovacie výberky

Na porovnanie výsledkov natrénovaných modelov boli použité dodatočné vyhodnocovacie výberky. Tieto výberky neboli použité pri trénovaní modelov. Slúžia na vytvorenie predikcií oboch modelov a následné vizuálne a numerické porovnanie ich správania.

V repozitári sú uložené kompaktné predikčné dáta:

```text
data/CH_predict_2021/
data/AR_predict_2021/
data/CH_predict_2025_processed/
data/CH_predict_2025_raw/
```

Pre rok 2021 sú dáta uložené ako samostatné archívy s obrazmi, maskami a sekvenciami. Pre rok 2025 sú CH dáta uložené ako spracovaná a nespracovaná verzia.

## Modely

Repozitár obsahuje uložené modely pre jednotlivé experimentálne konfigurácie:

```text
trained_models/CH_standart_models/
trained_models/CH_low_models/
trained_models/CH_Region_growth_models/

trained_models/AR_standart_models/
trained_models/AR_low_models/
trained_models/AR_spoca_models/
```

Pre každý experiment sa používa dvojica modelov:

```text
baseline model  = SCSS-Net
temporal model  = ConvLSTM-SCSS-Net
```

Modely a väčšie dátové archívy sú uložené pomocou Git LFS.

## Konfiguračné súbory

Každý experiment je opísaný samostatným JSON súborom v priečinku `configs/`.

Dostupné konfigurácie pre koronálne diery:

```text
configs/CH_standard.json
configs/CH_low.json
configs/CH_region_growth.json
configs/CH_2025_processed.json
configs/CH_2025_raw.json
```

Dostupné konfigurácie pre aktívne oblasti:

```text
configs/AR_standard.json
configs/AR_low.json
configs/AR_spoca.json
```

Konfiguračný súbor obsahuje dve hlavné časti:

```text
training_config
prediction_config
```

Časť `training_config` opisuje, v akých podmienkach boli modely natrénované. Obsahuje napríklad použitú tréningovú výberku, zdroje anotácií, veľkosť obrazu, dĺžku sekvencie a parametre modelu.

Časť `prediction_config` určuje, ktoré uložené modely a ktoré dátové archívy sa majú použiť pri spustení notebooku. Obsahuje aj threshold a výstupný priečinok.

## Experimentálne konfigurácie

### CH konfigurácie

```text
CH_standard
```

Štandardná konfigurácia pre koronálne diery. Modely boli trénované na plnej dostupnej CH tréningovej výberke.

```text
CH_low
```

Konfigurácia so zníženým počtom parametrov. Používa menší počet filtrov, menej úrovní encoder-decoder architektúry a menší počet ConvLSTM filtrov.

```text
CH_region_growth
```

Konfigurácia, v ktorej boli modely trénované iba na časti výberky s anotáciami Region Growth.

```text
CH_2025_processed
```

Predikcia pomocou štandardných CH modelov na spracovanej dodatočnej vyhodnocovacej výberke z roku 2025.

```text
CH_2025_raw
```

Predikcia pomocou štandardných CH modelov na nespracovanej dodatočnej vyhodnocovacej výberke z roku 2025.

### AR konfigurácie

```text
AR_standard
```

Štandardná konfigurácia pre aktívne oblasti. Modely boli trénované na plnej dostupnej AR tréningovej výberke.

```text
AR_low
```

Konfigurácia so zníženým počtom parametrov.

```text
AR_spoca
```

Konfigurácia, v ktorej boli modely trénované iba na časti výberky s anotáciami SPoCA.

Pri AR experimentoch sa používa threshold `0.25`. Tento prah bol použitý preto, že pri dodatočnej vyhodnocovacej výberke modely pri vyššom prahu častejšie označovali aj nežiadúce pixely, najmä v oblasti okrajového svitu slnečného disku.

## Notebooky

Repozitár obsahuje dva hlavné demonštračné notebooky:

```text
CH_demo.ipynb
AR_demo.ipynb
```

Notebooky majú rovnakú základnú štruktúru:

1. opis pôvodného tréningového pipeline;
2. výber konfiguračného súboru;
3. načítanie modelov a dát podľa configu;
4. predikcia na dodatočnej vyhodnocovacej výberke;
5. výpočet metrík;
6. uloženie masiek, pravdepodobnostných máp a vizuálnych porovnaní.

Tréningová časť je v notebookoch opísaná slovne, pretože kompletné tréningové dáta nie sú v repozitári. Predikčná časť je spustiteľná.

## Spustenie projektu

Projekt obsahuje uložené natrénované modely a dátové archívy, ktoré sú uložené pomocou Git LFS. Preto je po stiahnutí repozitára potrebné skontrolovať, či sa veľké súbory stiahli správne.

### 1. Klonovanie repozitára

```bash
git clone https://github.com/al124at/al124at.git
cd al124at
```

Ak sa veľké súbory nestiahnu automaticky, je potrebné spustiť:

```bash
git lfs install
git lfs pull
```

### 2. Vytvorenie Python prostredia

Projekt odporúčame spúšťať v samostatnom Python prostredí. Na Windows je možné vytvoriť lokálne prostredie `.venv` priamo v priečinku projektu:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Po aktivácii prostredia by sa mal v termináli zobraziť prefix:

```text
(.venv)
```

### 3. Inštalácia závislostí

Po aktivácii prostredia je potrebné nainštalovať knižnice zo súboru `requirements.txt`:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Otvorenie projektu vo VS Code

Projekt je možné otvoriť vo VS Code priamo z aktívneho prostredia:

```bash
code .
```

Následne je možné otvoriť jeden z notebookov:

```text
CH.ipynb
AR.ipynb
```

Vo VS Code je potrebné ako kernel zvoliť Python prostredie `.venv`, teda interpreter:

```text
.venv\Scripts\python.exe
```

Notebook musí byť spustený v tom istom prostredí, v ktorom boli nainštalované závislosti z `requirements.txt`.

### 5. Výber experimentu

Experiment sa volí v prvej spustiteľnej bunke notebooku pomocou premennej `CONFIG_PATH`.

Príklad pre štandardný experiment koronálnych dier:

```python
CONFIG_PATH = "configs/CH_standard.json"
```

Príklad pre aktívne oblasti:

```python
CONFIG_PATH = "configs/AR_standard.json"
```

Podľa zvoleného konfiguračného súboru sa automaticky načítajú príslušné modely, dátové archívy, threshold a výstupný priečinok.

### 6. Spustenie notebooku

Notebook obsahuje dve hlavné spustiteľné časti:

1. načítanie knižníc, konfigurácie, ciest a parametrov,
2. predikcia na dodatočnej vyhodnocovacej množine.

Predikcia sa vykonáva postupne po jednotlivých obrázkoch, aby sa nezvyšovala pamäťová náročnosť. Výstupy sa ukladajú do priečinka definovaného v konfiguračnom súbore.

### 7. Výstupy

Po spustení predikcie sa vytvorí priečinok:

```text
outputs/<experiment_name>/prediction_on_additional_evaluation_set/
```

V ňom sa nachádzajú:

```text
baseline_masks/       binárne masky modelu SCSS-Net
convlstm_masks/       binárne masky modelu ConvLSTM-SCSS-Net
collages/             koláže s vizuálnym porovnaním
metrics.csv           numerické metriky
used_config.json      použitý konfiguračný súbor
```

### 8. Poznámka ku Git LFS

Súbor `.gitattributes` musí zostať v repozitári, pretože určuje, ktoré typy súborov sa majú ukladať pomocou Git LFS.

Používa sa najmä pre:

```text
*.keras
*.zip
```

Tieto súbory obsahujú natrénované modely a dátové archívy potrebné na spustenie predikčnej časti notebookov.


## Overlay vizualizácia

V kolážach sa používa overlay porovnanie predikcií oboch modelov:

```text
červená = pixely označené iba základným modelom SCSS-Net
modrá   = pixely označené iba modelom ConvLSTM-SCSS-Net
žltá    = pixely označené oboma modelmi
```

Táto vizualizácia slúži najmä na ručné porovnanie rozdielov medzi modelmi.

## Poznámky

Repozitár je určený na demonštráciu praktického pipeline a reprodukciu predikčnej časti experimentov pomocou uložených modelov. Plné trénovanie od začiatku vyžaduje kompletné tréningové dáta, ktoré nie sú súčasťou repozitára z dôvodu veľkosti.
