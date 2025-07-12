import streamlit as st
from database import Products, Vendas
from sqlalchemy import select, update

st.set_page_config(page_title='Cadastrar Vendas', layout='wide')

conn = st.connection('postgres', type='sql')

if not 'client_order' in st.session_state:
    st.session_state['client_order'] = {'COCA': 0, 'AGUA':0, 'GUARANA': 0, 'SUCO': 0, 'CHOPP': 0, 'PROMO CHOPP': 0, 'VINHO': 0, 'PROMO VINHO': 0, 'GUARAVITA': 0}


def get_unit_values(_conn):
    with _conn.session as session:
        product_data =  session.query(Products).all()
        st.session_state['product_unit_value'] = {product.product_name:product.unit_value for product in product_data}

if 'product_unit_value' not in st.session_state:
    get_unit_values(conn)

def total_client_order():
    
    total_order_value = 0
    for item in st.session_state['product_unit_value'].items():
        total_order_value += item[1] * st.session_state['client_order'][item[0]]
    return total_order_value

with st.container(border=True):
    st.header('Cadastrar Vendas')


with st.container(border=True):

    add_buttons_column, delete_buttons_column, sumary_col = st.columns(3, vertical_alignment='center')
    add_coca = add_buttons_column.button('+1 COCA')
    add_agua = add_buttons_column.button('+1 AGUA')
    add_guarana = add_buttons_column.button('+1 GUARANA')
    add_suco = add_buttons_column.button('+1 SUCO')
    add_chopp = add_buttons_column.button('+1 CHOPP')
    add_promo_chopp = add_buttons_column.button('+1 PROMO CHOPP')
    add_vinho = add_buttons_column.button('+1 VINHO')
    add_promo_vinho = add_buttons_column.button('+1 PROMO VINHO')
    add_guaravita = add_buttons_column.button('+1 GUARAVITA')

    delete_coca = delete_buttons_column.button('-1 COCA')
    delete_agua = delete_buttons_column.button('-1 AGUA')
    delete_guarana = delete_buttons_column.button('-1 GUARANA')
    delete_suco = delete_buttons_column.button('-1 SUCO')
    delete_chopp = delete_buttons_column.button('-1 CHOPP')
    delete_promo_chopp = delete_buttons_column.button('-1 PROMO CHOPP')
    delete_vinho = delete_buttons_column.button('-1 VINHO')
    delete_promo_vinho = delete_buttons_column.button('-1 PROMO VINHO')
    delete_guaravita = delete_buttons_column.button('-1 GUARAVITA')
    
    if add_coca:
        st.session_state['client_order']['COCA'] += 1
    
    if add_agua:
        st.session_state['client_order']['AGUA'] += 1
    
    if add_guarana:
        st.session_state['client_order']['GUARANA'] += 1

    if add_suco:
        st.session_state['client_order']['SUCO'] += 1

    if add_chopp:
        st.session_state['client_order']['CHOPP'] += 1

    if add_promo_chopp:
        st.session_state['client_order']['PROMO CHOPP'] += 1

    if add_vinho:
        st.session_state['client_order']['VINHO'] += 1

    if add_promo_vinho:
        st.session_state['client_order']['PROMO VINHO'] += 1

    if add_guaravita:
        st.session_state['client_order']['GUARAVITA'] += 1

    if delete_coca:
        if st.session_state['client_order']['COCA'] > 0:
            st.session_state['client_order']['COCA'] -= 1

    if delete_agua:
        if st.session_state['client_order']['AGUA'] > 0:
            st.session_state['client_order']['AGUA'] -= 1
    
    if delete_guarana:
        if st.session_state['client_order']['GUARANA'] > 0:
            st.session_state['client_order']['GUARANA'] -= 1
    if delete_chopp:
        if st.session_state['client_order']['CHOPP'] > 0:
            st.session_state['client_order']['CHOPP'] -= 1
    if delete_promo_chopp:
        if st.session_state['client_order']['PROMO CHOPP'] > 0:
            st.session_state['client_order']['PROMO CHOPP'] -= 1
    if delete_vinho:
        if st.session_state['client_order']['VINHO'] > 0:
            st.session_state['client_order']['VINHO'] -= 1
    if delete_promo_vinho:
        if st.session_state['client_order']['PROMO VINHO'] > 0:
            st.session_state['client_order']['PROMO VINHO'] -= 1
    if delete_suco:
        if st.session_state['client_order']['SUCO'] > 0:
            st.session_state['client_order']['SUCO'] -= 1

    if delete_guaravita:
        if st.session_state['client_order']['GUARAVITA'] > 0:
            st.session_state['client_order']['GUARAVITA'] -= 1

    sumary_col.subheader('Pedido Atual')
    for item, quantity in st.session_state['client_order'].items():
        sumary_col.write(f'{item} - {quantity}')

    total_order_value = total_client_order()
    sumary_col.subheader(f'Total da Venda: R${total_order_value:.2f}'.replace('.', ','))

    confirm_button = sumary_col.button('Concluir venda')

    if confirm_button:


        with conn.session as session:

            for item in st.session_state['client_order'].keys():
                if st.session_state['client_order'][item] != 0:
                    product_data = session.query(Products).filter(Products.product_name == item).scalar()
                    statement2 = update(Products).where(Products.product_name == item).values(quantity=product_data.quantity-st.session_state['client_order'][item])
                    session.execute(statement2)
                    session.commit()
            

            session.add(
                Vendas(
                    coca = st.session_state['client_order']['COCA'],
                    agua = st.session_state['client_order']['AGUA'],
                    guarana = st.session_state['client_order']['GUARANA'],
                    suco = st.session_state['client_order']['SUCO'],
                    chopp = st.session_state['client_order']['CHOPP'],
                    promo_chopp = st.session_state['client_order']['PROMO CHOPP'],
                    vinho = st.session_state['client_order']['VINHO'],
                    promo_vinho = st.session_state['client_order']['PROMO VINHO'],
                    guaravita = st.session_state['client_order']['GUARAVITA'],
                    total_value = total_order_value
                )
            )

            session.commit()

        st.session_state['client_order'] = {'COCA': 0, 'AGUA':0, 'GUARANA': 0, 'SUCO': 0, 'CHOPP': 0, 'PROMO CHOPP': 0, 'VINHO': 0, 'PROMO VINHO': 0, 'GUARAVITA': 0}
        st.rerun()