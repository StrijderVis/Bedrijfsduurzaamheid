import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Inlezen van de data
unidata = 'Unilever CSRD data.xlsx'  # Zorg ervoor dat het bestand in dezelfde map staat
unigas = pd.read_excel(unidata, sheet_name='Energie en broeikasgassen')
unival = pd.read_excel(unidata, sheet_name='Afval')
uniwater = pd.read_excel(unidata, sheet_name='Water')
uniheid = pd.read_excel(unidata, sheet_name='Arbeidsveiligheid')

arladata = 'Arla CSRD data.xlsx'  # Zorg ervoor dat het bestand in dezelfde map staat
arlagas = pd.read_excel(arladata, sheet_name='Energie en broeikasgassen')
arlaval = pd.read_excel(arladata, sheet_name='Afval')
arlawater = pd.read_excel(arladata, sheet_name='Water')
arlaheid = pd.read_excel(arladata, sheet_name='Arbeidsveiligheid')

campidata = 'FrieslandCampina CSRD data.xlsx'
campigas = pd.read_excel(campidata, sheet_name='Energie en broeikasgassen')
campival = pd.read_excel(campidata, sheet_name='Afval')
campiwater = pd.read_excel(campidata, sheet_name='Water')
campiheid = pd.read_excel(campidata, sheet_name='Arbeidsveiligheid')

# Streamlit-app
st.title("Bedrijfsduurzaamheidsgegevens")

# Bedrijfselectie (voor nu slechts één voorbeeld)
bedrijven = ["Unilever", "Arla", "Campina"]
bedrijf = st.selectbox("Selecteer een bedrijf", bedrijven)

# Data matchen met het goede bedrijf
if bedrijf == "Unilever":
    gas = unigas
    afval = unival
    water = uniwater
    arbeid = uniheid
elif bedrijf == "Arla":
    gas = arlagas
    afval = arlaval
    water = arlawater
    arbeid = arlaheid
elif bedrijf == "Campina":
    gas = campigas
    afval = campival
    water = campiwater
    arbeid = campiheid

# Categorie-selectie
categorie = st.selectbox(
    "Selecteer een categorie",
    ["Energie en broeikasgassen", "Afval", "Water", "Arbeidsveiligheid"]
)

# Grafieken:
# Energie en broeikasgassen
if categorie == "Energie en broeikasgassen":
    st.header("Energie en Broeikasgassen")
    
    # Campina geeft maar 2 jaar vrij, dus een waarschuwing
    if bedrijf == "Campina":
        st.subheader(":red[Campina geeft maar data vrij van 2 jaar i.p.v. 3. ]")

    # Grafiek 1: CO2 uitstoot per jaar
    fig, ax = plt.subplots()
    ax.bar(gas['Jaar'], gas['CO2 uitstoot in ton'], color='skyblue')
    ax.set_title("CO2-uitstoot per jaar")
    ax.set_xlabel("Jaar")
    ax.set_ylabel("CO2 uitstoot (ton)")
    ax.set_xticks(gas['Jaar'])
    st.pyplot(fig)

    # Grafiek 2: Vermindering CO2 in tonnen en percentage
    fig, ax1 = plt.subplots()

    # Grafiek 2: Eerste y-as (vermindering in tonnen)
    color = 'tab:blue'
    ax1.bar(gas['Jaar'], gas['Vermindering CO2 vergeleken met vorige jaar in tonnen'], 
            color=color, label="Reductie (ton)")
    ax1.set_xlabel("Jaar")
    ax1.set_ylabel("Reductie (ton)", color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(gas['Jaar'])

    # Grafiek 2: Tweede y-as (% vermindering)
    ax2 = ax1.twinx()
    color = 'tab:green'
    ax2.plot(gas['Jaar'], gas['Vermindering CO2 vergeleken met vorig jaar in %'], 
             color=color, marker='o', label="Reductie (%)")
    ax2.set_ylabel("Reductie (%)", color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    # Grafiek 2: Titel en legenda
    fig.suptitle("CO2-reductie in tonnen en percentage")
    fig.tight_layout()
    st.pyplot(fig)

    if bedrijf == "Unilever":
        # Grafiek 3: Energieverbruik
        st.subheader(":red[_Unilever weergeeft energie per ton productie, geen totaal!_]")
        fig, ax = plt.subplots()
        ax.bar(gas['Jaar'], gas['Energie verbruik in gigajoules per ton'], color='orange')
        ax.set_title("Energieverbruik per ton productie")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Gigajoules per ton")
        ax.set_xticks(gas['Jaar'])
        st.pyplot(fig)
    else:
        # Grafiek 3: Energieverbruik
        fig, ax = plt.subplots()
        ax.bar(gas['Jaar'], gas['Totaal energieverbruik in MWH'], color='orange')
        ax.set_title("Energieverbruik in MWH")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Gigajoules per ton")
        ax.set_xticks(gas['Jaar'])
        st.pyplot(fig)

# Afval
elif categorie == "Afval":
    st.header("Afval")

    if bedrijf == "Unilever":
        # Grafiek: Unilever afval
        fig, ax = plt.subplots()
        ax.bar(afval['Jaar'], afval['Gevaarlijk afval in kg per ton productie'], label='Gevaarlijk afval', color='red')
        ax.bar(afval['Jaar'], afval['Niet-gevaarlijk afval in kg per ton productie'], 
           bottom=afval['Gevaarlijk afval in kg per ton productie'], label='Niet-gevaarlijk afval', color='green')
        ax.set_title("Afval per jaar")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Afval (ton)")
        ax.set_xticks(afval['Jaar'])
        ax.legend()
        st.pyplot(fig)
    else:
        # Campina geeft geen afval nummers vrij :/
        if bedrijf == "Campina":
            st.header(":red[Campina geeft geen afval gegevens vrij, dus data ontbreekt!]")

        # Grafiek: resterend afval Arla
        fig, ax = plt.subplots()
        ax.bar(afval['Jaar'], afval['Gevaarlijk afval in ton'], label='Gevaarlijk afval', color='red')
        ax.bar(afval['Jaar'], afval['Niet-gevaarlijk afval in ton'], 
           bottom=afval['Gevaarlijk afval in ton'], label='Niet-gevaarlijk afval', color='green')
        ax.set_title("Afval per jaar")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Afval (ton)")
        ax.set_xticks(afval['Jaar'])
        ax.legend()
        st.pyplot(fig)

# Water
elif categorie == "Water":
    st.header("Water")

    if bedrijf == "Unilever":
        st.subheader(":red[_Unilever weergeeft data per ton productie, geen totaal!_]")
        # Grafiek 1: Wateronttrekking in m3 per ton productie
        fig, ax = plt.subplots()
        ax.bar(water['Jaar'], water['Wateronttrekking in m3 per ton productie'], color='blue')
        ax.set_title("Wateronttrekking per ton productie")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Wateronttrekking in m3 per ton productie")
        ax.set_xticks(water['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)

        # Grafiek 2: Emissions of COD in kg per ton productie
        fig, ax = plt.subplots()
        ax.bar(water['Jaar'], water['Emissions of chemical oxygen demand (COD) in kg per tonne of production'], color='purple')
        ax.set_title("COD-emissies (chemical oxygen demand) per ton productie")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Emissions of chemical oxygen demand (COD) in kg per tonne of production")
        ax.set_xticks(water['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)
    elif bedrijf == "Arla":
        # Grafiek 1: Wateronttrekking in m3 per ton productie
        fig, ax = plt.subplots()
        ax.bar(water['Jaar'], water['Wateronttrekking in m3'], color='blue')
        ax.set_title("Wateronttrekking per ton productie")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Wateronttrekking in m3")
        ax.set_xticks(water['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)
        st.subheader(":red[Geen COD-emissie (chemical oxygen demand) data beschikbaar]")
    else:
        st.subheader(":red[Campina geeft maar data vrij van 2 jaar i.p.v. 3. ]")
        fig, ax = plt.subplots()
        ax.bar(water['Jaar'], water['Water consumptie in m3'], color='blue')
        ax.set_title("Wateronttrekking per ton productie")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Water consumptie in m3")
        ax.set_xticks(water['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)
        st.subheader(":red[Geen COD-emissie (chemical oxygen demand) data beschikbaar]")

# Arbeidsveiligheid
elif categorie == "Arbeidsveiligheid":
    st.header("Arbeidsveiligheid")

    if bedrijf != "Campina":
        # Grafiek 1: TRFR per 1.000.000 gewerkte uren
        fig, ax = plt.subplots()
        ax.bar(arbeid['Jaar'], arbeid['Ongevallenpercentage: Total Recordable Frequency Rate (TRFR) per 1.000.000 gewerkte uren'], color='cyan')
        ax.set_title("Total Recordable Frequency Rate (TRFR)")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("(TRFR) per 1.000.000 gewerkte uren")
        ax.set_xticks(arbeid['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)

        # Grafiek 2: Aantal dodelijke ongevallen
        if bedrijf == "Arla":
            st.subheader(":red[Arla geeft geen dodelijke ongevallen data weer]")
        fig, ax = plt.subplots()
        ax.bar(arbeid['Jaar'], arbeid['Aantal dodelijke ongevallen'], color='black')
        ax.set_title("Aantal dodelijke ongevallen")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Aantal ongevallen")
        ax.set_xticks(arbeid['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)
    else:
        st.subheader(":red[Campina geeft aantal ongelukken per 200.000 werkuren weer i.p.v. per milioen, daarnaast is er ook geen dodelijke ongevallen data beschikbaar en is er maar data van 2 jaar i.p.v. 3]")
        fig, ax = plt.subplots()
        ax.bar(arbeid['Jaar'], arbeid['Ongevallenpercentage: Total Recordable Frequency Rate (TRFR) per 200.000 gewerkte uren'], color='cyan')
        ax.set_title("Total Recordable Frequency Rate (TRFR)")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("(TRFR) per 1.000.000 gewerkte uren")
        ax.set_xticks(arbeid['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)

        # Grafiek 2: Aantal dodelijke ongevallen
        fig, ax = plt.subplots()
        ax.bar(arbeid['Jaar'], arbeid['Aantal dodelijke ongevallen'], color='black')
        ax.set_title("Aantal dodelijke ongevallen")
        ax.set_xlabel("Jaar")
        ax.set_ylabel("Aantal ongevallen")
        ax.set_xticks(arbeid['Jaar'])  # Alleen hele jaren
        st.pyplot(fig)