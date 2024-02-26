import streamlit as st 
import pandas as pd 
import plotly.express as px
import base64
from io import StringIO , BytesIO

def generate_excel_download_link(data) : 
    ecrire = BytesIO()
    data.to_excel(ecrire   ,index = False , header= True)
    ecrire.seek(0)
    b64 = base64.b64encode(ecrire.read()).decode()
    href = f'<a href = "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64, {b64}" downlaod="data_download.xlsx"> Telecharger le fichier excel</a>'
    return st.markdown(href , unsafe_allow_html=True)


def generatte_html_download_link(fig) : 
    ecrire = StringIO()
    fig.write_html(ecrire ,include_plotlyjs = 'cdn')
    ecrire = BytesIO(ecrire.getvalue().encode())
    b64 = base64.b64encode(ecrire.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8; base64 , {b64}" download="plot.html">Telecharger le fichier</a>'
    return st.markdown(href , unsafe_allow_html=True)

def statistique_specifique(variable) : 
        # Analyse de valeurs quantitatives 
    st.subheader('Analyse de valeurs quantitatives ')
    correpondance_entier = st.radio('Que voulez vous analyser ?' , (element for element in variable.select_dtypes('int')))

    # Connaitre les proportions des valeurs entieres 
    st.subheader('Proportions : Valeur quantitatives')
    autre_correpondance_entier = variable[correpondance_entier].value_counts(normalize = True)
    for index , value in autre_correpondance_entier.items() : 
        st.write(f"{index}  : {value: .2f}% ")
  



    placeholder = st.empty()
    st.subheader('Autre donnée statstique : Valeurs entiere')
    # Ce qui pemet de donner des donnée statistiques avec des variale quantitative 
    autre_correpondance_entier = variable[correpondance_entier].describe()
    moyenne_entier = variable[correpondance_entier].mean()
    equart_type_entier = variable[correpondance_entier].std()
    minimum_entier = variable[correpondance_entier].min()
    maximum_entier = variable[correpondance_entier].max()
    
    with placeholder.container() : 
        col1 , col2 , col3 , col4 = st.columns(4)
        col1.metric(label="Maximum :arrow_up: " , value=(maximum_entier))
        col2.metric(label="Minimum :arrow_down:" , value=(minimum_entier))
        col3.metric(label="Moyenne :+1:" , value=(moyenne_entier))
        col4.metric(label="Ecart type :loop:" , value=equart_type_entier)


      
    graphe = px.pie(variable , names = correpondance_entier)
    st.plotly_chart(graphe)

    st.markdown('---')



    # Analyse de valeurs qualitatives 
    st.subheader('Analyse de valeurs qualitatives')
    correpondance_object = st.radio('Que voulez vous analyser ? ' , (element for element in variable.select_dtypes('object')))


    # COnnaitre les proportin des valeurs categorielles 
    st.subheader('Proportions : Valeurs qualitatives')
    autre_correpondance_objet = variable[correpondance_object].value_counts(normalize = True) * 100
    st.write('Proportion : ')
    for index , value in autre_correpondance_objet.items() : 
        st.write(f"{index}  : {value: .2f}% ")




    st.subheader('Donnée statistique : Variable catégorielle')
    autre_correpondance_objet = variable[correpondance_object].describe()
    quantite_entreprise = variable[correpondance_object].count()
    quantite = variable[correpondance_object].describe()['unique']
    st.write("Nombre d'entreprise  : " , str(quantite_entreprise))
    st.write('Quantié : ' , str(quantite) )
    

    st.subheader('Graphiques illustratifs')
    graphe_obj = px.pie(variable , names = correpondance_object )
    bar = px.bar(variable , x = correpondance_object)
    col1 , col2  = st.columns(2)
    with col1 :
        st.plotly_chart(bar)
    with col2 : 
        st.plotly_chart(graphe_obj)


# parametrage du site
st.set_page_config(
    page_title='Tableau de bord de blum' , 
    page_icon=":bar_chart:" ,
    layout='wide'
)

# titre du site et du ligicile
st.title(':bar_chart: Tableau de bord blum')
fichier = st.file_uploader('Veuillez choisir un fichier' , type = 'xlsx')


if fichier is None:
    st.info('Veuillez charger un ficher valable' ) 
    st.stop()


st.markdown('---')
data = pd.read_excel(fichier)

with st.expander("Data Views") : 
    st.dataframe(data)



st.subheader('Veillez saisir la donéee à analyser')
groupe_colonne = st.selectbox('Que voulez vous analyser ?' , (element for element in data))
select_items = st.radio('Veuillez selectionner une valeur', data[groupe_colonne].unique())
ressortir =  data[data[groupe_colonne] == select_items]
st.dataframe(ressortir)

st.markdown('---')

# En mode application 
Nom_commercial = data[data['Nom commercial '] == select_items] 
nombre_gabarits = data[data['Nombre de gabarits '] == select_items] 
date_creation = data[data['Année de création '] == select_items]
jurique = data[data['Forme juridique'] == select_items]
machine = data[data['Machines'] == select_items]
adresse = data[data['adresse du siege'] == select_items]
arron = data[data['arrondissement / commune '] == select_items]
ville = data[data['Ville '] == select_items]
activité = data[data["But de l'activité"] == select_items]
domaine = data[data["Domaine d'activité "] == select_items]
commerce = data[data['commercialisation par internet '] == select_items]
marche = data[data['marché '] == select_items]
locaux = data[data['Locaux'] ==select_items]
personel= data[data['Personels'] == select_items]
gabarit = data[data['Gabarits '] == select_items]
 
if groupe_colonne == 'Nom commercial ' : 
    st.title('Informations sur les noms commerciaux ')
    anne = Nom_commercial['Année de création ']
    Effectif_travailleur = Nom_commercial['Effectif travailleur']
    statistique_specifique(Nom_commercial)
    # Creation de colonne  
    colonne_1  , colonne_2 = st.columns(2)

    with colonne_1: 
        st.subheader("Année de création")
        for element in anne:
            element = str(element)
            st.write(element)

    with colonne_2:
        st.subheader("Effectif de travailleurs")
        for element in Effectif_travailleur :
            element = str(element)
            st.write(element)
            
if groupe_colonne == 'Nombre de gabarits ' : 
    st.title('Information sur les gabarits')
    statistique_specifique(nombre_gabarits)

if groupe_colonne == 'Année de création ': 
    st.title('Information sur les années de création')
    statistique_specifique(date_creation)

if groupe_colonne == 'Forme juridique' :
    st.title('Information sur les formes juridique')
    statistique_specifique(jurique)

if groupe_colonne == 'Machines' :
    st.title('Information sur les machines')
    statistique_specifique(machine)

if groupe_colonne == 'adresse du siege' : 
    st.title('Information sur les adresse du siège')
    statistique_specifique(adresse)
 
if groupe_colonne == 'arrondissement / commune ' : 
    st.title('Information sur les arrondissements et les communes')
    statistique_specifique(arron)

if groupe_colonne == 'Ville ' : 
    st.title('Information sur les villes')
    statistique_specifique(ville)

if groupe_colonne == "But de l'activité" : 
    st.title('Information sur le but de differentes acivité')
    statistique_specifique(activité)

if groupe_colonne == "Domaine d'activité ":
    st.title("Information sur les domaines d'activité")
    statistique_specifique(domaine)

if groupe_colonne == "commercialisation par internet " : 
    statistique_specifique(commerce)
if groupe_colonne == "marché " :
    statistique_specifique(marche)

if groupe_colonne == "Locaux" : 
    statistique_specifique(locaux)
if groupe_colonne == "Personels" : 
    statistique_specifique()
if groupe_colonne == "Gabarits " : 
    statistique_specifique(gabarit)


valeurs_entiers =  [element for element in data.select_dtypes('int')]
valeurs_object = [element for element in data.select_dtypes('object')]


   
st.markdown('---')
data.dropna(inplace=True)
st.title('Analyse générale')

# initilalisation des colonnes 
left , right = st.columns(2)

with left:
    # pour afficher les grahes 
    st.subheader('Diagramme en bande ')
    fig = px.bar(
        data ,
        x = groupe_colonne ,
        color_continuous_scale =['red' , 'yellow' ,'green'] , 
        template='plotly_white'
    )
    st.plotly_chart(fig)

with right :
    st.subheader('Diagramme à secteur')
    camember = px.pie(data , names= groupe_colonne  )
    st.plotly_chart(camember)

st.title('Donnée statistique')
statistique = data[groupe_colonne].describe()
st.write(statistique)







# telecharger les fichiers sous formats excel rt lr graphe en format html 
st.subheader('Telecharger : ')
generate_excel_download_link(ressortir)
generatte_html_download_link(fig)

# Elnver le barre d'en abs et la forme de burger 
hide_st_style =""" 
    <style type="text/css">
    #Mainmenu {visibility:hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style> 
 """

st.markdown(hide_st_style , unsafe_allow_html=True)
 
    
st.markdown(
    """
    <style>
    body {
    font-size : 16px ;
    line-height: 1.5;
    background-color : red ;
}

.container {
    display : flex ;
    flex-wrap: wrap;
}

@media screen and (max-width :600px) {
    .container {
        flex-direction: column;
    }
}

st.Image > img {
    max-width  : 100%;
    height: auto;
}
</style>
    """ ,
    unsafe_allow_html = True
)