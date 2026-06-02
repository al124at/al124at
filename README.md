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

## Spustenie

Najprv je potrebné nainštalovať závislosti:

```bash
pip install -r requirements.txt
```

Ak bol repozitár klonovaný cez Git, je potrebné mať aktivovaný Git LFS:

```bash
git lfs install
git lfs pull
```

Potom je možné otvoriť Jupyter Notebook:

```bash
jupyter notebook
```

a spustiť jeden z notebookov:

```text
CH_demo.ipynb
AR_demo.ipynb
```

## Výber experimentu v notebooku

V notebooku sa experiment volí zmenou premennej `CONFIG_PATH`.

Príklad pre štandardný CH experiment:

```python
CONFIG_PATH = "configs/CH_standard.json"
```

Príklad pre CH low-parameter experiment:

```python
CONFIG_PATH = "configs/CH_low.json"
```

Príklad pre AR experiment:

```python
CONFIG_PATH = "configs/AR_standard.json"
```

Po zmene configu notebook automaticky použije modely, dáta, threshold a výstupný priečinok definované v danom konfiguračnom súbore.

## Výstupy

Po spustení predikčnej časti notebook vytvorí výstupy v priečinku definovanom v configu. Výstupy sa ukladajú do štruktúry:

```text
outputs/<experiment_name>/prediction_on_additional_evaluation_set/
```

V tejto zložke sa vytvoria:

```text
baseline_masks/             binárne masky modelu SCSS-Net
convlstm_masks/             binárne masky modelu ConvLSTM-SCSS-Net
baseline_probabilities/     pravdepodobnostné mapy modelu SCSS-Net
convlstm_probabilities/     pravdepodobnostné mapy modelu ConvLSTM-SCSS-Net
collages/                   vizuálne porovnania
<experiment>_metrics.csv    numerické metriky
used_config.json            použitý konfiguračný súbor
```

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
