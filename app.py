import streamlit as st
import pandas as pd
from PIL import Image
import re
import time
from datetime import datetime



#setup do título da página
st.set_page_config(page_title="CNPJ Check", page_icon=None, layout='centered', initial_sidebar_state='collapsed', menu_items=None)

#call para abrir a imagem da loft na página
foto = Image.open('RGB_logoslaranja_pack_prioritario.png')
st.image(foto)

# Título da página centralizado e na cor cinza
st.markdown("<h1 style='text-align: center; color: DimGrey;'>Verificador de CNPJ</h1>", unsafe_allow_html=True)

# Endereço da planilha (escondido no st.secrets para não ficar público no git hub)
sheet_url = st.secrets["public_gsheets_url"]
url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')

# Call para puxar a planilha atualizada
df = pd.read_csv(url_1)

# dropamos qlqr cnpj duplicado, mantendo o primeiro que aparece no dataset
df.drop_duplicates(subset=['CNPJ'], inplace=True)

# Transformamos a coluna CNPJ em index para poder realizar buscas com .iloc no pandas
df.set_index("CNPJ", inplace=True)

# Instruções de uso da ferramenta
st.markdown("<h5 style='text-align: center; color: Grey;'>Digite ou copie e cole os números do CNPJ que deseja consultar.<br> Você pode colocar apenas os números '00000000000000' (14 dígitos)<br>ou usando o formato pradão '00.000.000/0000-00' (18 dígitos) </h1>", unsafe_allow_html=True)

# Campo de input do CNPJ
input_cnpj = st.text_input(
      # o primeiro valor é a label    
      'Após inserir o CNPJ, aperte enter no teclado do seu computador ou do seu celular.',
      # o segundo valor serve de referência 
      value = '',
      # colocamos o máximo de caracteres mas veremos que o script aceita apenas os números sem "." "-"  ou "/"
      max_chars = 18

)
# iniciamos um contador que não será usado de forma fundamental
count = 0

# este if considera o state inicial como padrão e nao faz nada até que o usuário add os números
if input_cnpj == '':
    count +=1
    
    

# quando temos uma mudança no estado inicial, o script começa
elif input_cnpj != '':
    # retiramos todos os "." "-" e "/" (caso tenha no input)
    cnpj_p1 = re.sub('[^A-Za-z0-9]+', '', input_cnpj)
    
    # reformatamos (principalmente para caso o usuário tenha colocado apenas os números)
    reformat_cnpj = cnpj_p1[:2] + "." + cnpj_p1[2:5] + "." + cnpj_p1[5:8] + "/" + cnpj_p1[8:12] + "-" + cnpj_p1[-2:] 
    # devolvemos um feedback para o usuário de que estamos analizando
    st.write(f"Verificando o CNPJ {reformat_cnpj} ...")
  
    # o sistema em geral é muito rápido, então damos uma pausa de 1 segundo
    time.sleep(1)
    
    # verificamos se o cnpj já existe no dataframe
    if reformat_cnpj not in set(df.index):
        # se não estiver, automaticamente ele pode cadastrar
        st.markdown("<h2 style='text-align: center; color: Green;'>Você pode cadastrar este CNPJ</h1>", unsafe_allow_html=True)
    
    # se tiver presente, precisamos identificar o status 
    elif reformat_cnpj in set(df.index):
        #armazenamos a resposta de "go" ou "ngo" na variável "answer"
        answer = df.loc[reformat_cnpj][0]

        # se a resposta for "call"
        if answer == 'call':
            st.markdown("<h3 style='text-align: center; color: Green;'>Para cadastrar este CNPJ entre em contato com o Rômulo!</h1>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center; color: Green;'><a href='mailto:romulo.prestes@loft.com.br'>romulo.prestes@loft.com.br</a></h1>", unsafe_allow_html=True)
        # se a resposta for "ngo"
        else:
            st.markdown("<h2 style='text-align: center; color: Red;'>Você não pode cadastrar este CNPJ</h1>", unsafe_allow_html=True)
    



