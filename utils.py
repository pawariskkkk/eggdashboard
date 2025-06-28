import streamlit as st

#function to style each container
def createContainerWithColor(id, color="#151717", gap=0):
    # todo: instead of color you can send in any css
    plh = st.container()
    html_code = """<div id = 'my_div_outer'></div>"""
    st.markdown(html_code, unsafe_allow_html=True)
   
    with plh:
        inner_html_code = """<div id = 'my_div_inner_%s'></div>""" % id
        plh.markdown(inner_html_code, unsafe_allow_html=True)

    ## applying style
    chat_plh_style = """
        <style>
            div[data-testid='stVerticalBlock']:has(div#my_div_inner_%s):not(:has(div#my_div_outer)) {
                background-color: %s;
                padding: 10px;
                border-radius: 5px;
                gap: %srem;
                box-shadow:
    0 2px 4px rgba(255, 255, 255, 0.05),
    0 8px 16px rgba(0, 0, 0, 0.3),
    inset 0 0 4px rgba(255, 255, 255, 0.05);
            };
        </style>
        """
    chat_plh_style = chat_plh_style % (id, color, gap)
    st.markdown(chat_plh_style, unsafe_allow_html=True)
    return plh

#seperate the farm selectbox
def farmSelectbox(container, disable=False, keys=""):
    farm_list = ["KK1", "SRK", "KK3", "LTK1", "LTK2", "LTK3", "KDF", "STD", "PSW", "BRG"]
    return container.selectbox("Farm", [""] + farm_list, disabled=disable, key=keys)
