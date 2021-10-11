import streamlit as st
import pandas as pd
from PIL import Image
import re
import time

st.set_page_config(page_title="CNPJ Chek", page_icon=None, layout='centered', initial_sidebar_state='collapsed', menu_items=None)

foto = Image.open('RGB_logoslaranja_pack_prioritario.png')
st.image(foto)
st.markdown("<h1 style='text-align: center; color: DimGrey;'>Verificador de CNPJ</h1>", unsafe_allow_html=True)


sheet_url = "https://docs.google.com/spreadsheets/d/16pr14Fk6XQTAc5T02Gjgf-Ecl_8RDGdeSkWk1_-6VwQ/edit#gid=0"
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

df = pd.read_csv(url_1)
df.drop_duplicates(subset=['CNPJ'], inplace=True)
df.set_index("CNPJ", inplace=True)

input_cnpj = st.text_input(
      'Digite os números do CNPJ',
      value = '00.000.000/0000-00',
      max_chars = 18

)
count = 0
if input_cnpj == '00.000.000/0000-00':
    count +=1

elif input_cnpj != '00.000.000/0000-00':
    cnpj_p1 = re.sub('[^A-Za-z0-9]+', '', input_cnpj)
    reformat_cnpj = cnpj_p1[:2] + "." + cnpj_p1[2:5] + "." + cnpj_p1[5:8] + "/" + cnpj_p1[8:12] + "-" + cnpj_p1[-2:] 
    st.write(f"Verificando o CNPJ {reformat_cnpj} ...")

    time.sleep(1)
    
    if input_cnpj not in set(df.index):
        st.markdown("<h2 style='text-align: center; color: Green;'>Você pode cadastrar este CNPJ</h1>", unsafe_allow_html=True)
    
    elif input_cnpj in set(df.index):
        answer = df.loc[reformat_cnpj][0]
        if answer == 'go':
            st.markdown("<h2 style='text-align: center; color: Green;'>Você pode cadastrar este CNPJ</h1>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: Red;'>Você não pode cadastrar este CNPJ</h1>", unsafe_allow_html=True)




