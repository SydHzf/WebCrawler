import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid
import re
import urllib.request 

# https://www.rottentomatoes.com/ -> links, images

def aggrid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    # gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    # gb.configure_side_bar() #Add a sidebar
    gb.configure_selection() #Enable multi-row selection
    gridOptions = gb.build()
    grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=True,
    theme='dark', #Add theme color to the table
    enable_enterprise_modules=True,
    height=350, 
    width='100%',
    reload_data=True
)
    data = grid_response['data']
    selected = grid_response['selected_rows']
    return grid_response['selected_rows']
def main():
    pattrn = {"Heading1":"<h1.*>(.+)</h1>",
    "Heading2":"<h2.*>(.+)</h2>",
    "Heading3":"<h3.*>(.+)</h3>",
    "Heading4":"<h4.*>(.+)</h4>",
    "Heading5":"<h5.*>(.+)</h5>",
    "Heading6":"<h6.*>(.+)</h6>",
    "Paragraph":'<p.*>(.+)</p>',
    "Website Links":'<a.*href="(http[s]://.*?)".*>.*</a>',
    "Images":'<img[^>]*src="(http[^"]+)"[^>]*>',
    "Youtube Videos":'(/watch\?v=\S{11})"'}
    # dframe = pd.DataFrame()
    html_temp1 = """<div style="background-color:#6D7B8D;padding:15px">
                            		<h4 style="color:white;text-align:center;">Web Crawler</h4>
                            		</div>
                            		<div>
                            		</br>"""
    st.markdown(html_temp1, unsafe_allow_html=True)
    
    menu = ["Website Links",
    "Images",
    "Youtube Videos",
    "Headings",
    "Heading1",
    "Heading2",
    "Heading3",
    "Heading4",
    "Heading5",
    "Heading6",
    "Paragraph"]
    link = st.sidebar.text_input('Enter the Link: ',"https://www.rottentomatoes.com/")
    base_site = link

    choice = st.sidebar.selectbox("What you want?", menu, 2)
        # for hide menu
    hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        </style>
                        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    if link:
        html = urllib.request.urlopen(base_site).read().decode()
        html_temp = """<div style="background-color:#6D7B8D;padding:10px">
                                                    <h4 style="color:white;text-align:center;">"""+choice+"""</h4>
                                                    </div>
                                                    <div>
                                                    </br>"""
        if choice == "Website Links":
            
            st.markdown(html_temp, unsafe_allow_html=True)
            pattern = pattrn[choice]#href="(http://.*?)"
            links = re.findall(pattern, html)
            dframe = pd.DataFrame(links) 
            dframe.columns = [choice]
            # st.dataframe(dframe)
            selected = aggrid(dframe)
            print(selected)
            if selected:
                html_temp = """<div style="background-color:#6D7B8D;padding:10px">
                                                <h4 style="color:white;text-align:center;">"""+"Website Display."+"""</h4>
                                                </div>
                                                <div>
                                                </br>"""
                st.markdown(html_temp, unsafe_allow_html=True)
                st.write(
    f'<iframe src="{selected[0][choice]}" width = 100% height = 500></iframe>',
    unsafe_allow_html=True,
)
    
        elif choice == "Youtube Videos":
            
            st.markdown(html_temp, unsafe_allow_html=True)
            pattern = pattrn[choice]
            links = re.findall(pattern, html)
            links = list(set(links))
            dframe = pd.DataFrame(links) 
            dframe.columns = [choice]
            dframe[choice] = "https://www.youtube.com"+dframe[choice]
            # st.dataframe(dframe)
            print(dframe.columns)
            selected = aggrid(dframe)
            print(selected)
            if selected:
                html_temp = """<div style="background-color:#6D7B8D;padding:10px">
                                                <h4 style="color:white;text-align:center;">"""+"Website Display."+"""</h4>
                                                </div>
                                                <div>
                                                </br>"""
                st.markdown(html_temp, unsafe_allow_html=True)
                # print(selected)
                st.video(selected[0]["Youtube Videos"])
 
            
                    
            


        elif choice == "Images":
            

            st.markdown(html_temp, unsafe_allow_html=True)

            pattern = pattrn[choice]

            links = re.findall(pattern, html)
            dframe = pd.DataFrame(links)
            dframe.columns = [choice]
            selected = aggrid(dframe) 
            _, col2, _ = st.columns([6,6,4])

            

            with col2:
                if selected:
                    html_temp = """<div style="background-color:#6D7B8D;padding:10px">
                                                    <h4 style="color:white;text-align:center;">"""+"Image Display."+"""</h4>
                                                    </div>
                                                    <div>
                                                    </br>"""
                    st.markdown(html_temp, unsafe_allow_html=True)
                    st.image(
            str(selected[0]["Images"]),
            width=250, 
        )

            
            
           
        elif choice == "Headings":

            st.markdown(html_temp, unsafe_allow_html=True)
            pattern = '<(h[1-6]).*>(.*)</h[1-6]>'
            links = re.findall(pattern, html)
            dframe = pd.DataFrame(links)
            dframe.columns = ["Tag","Text"]
            selected = aggrid(dframe) 
           
        elif choice == "Heading1" or \
        choice == "Heading2" or \
        choice == "Heading3" or \
        choice == "Heading4" or \
        choice == "Heading5" or \
        choice == "Heading6" or \
        choice == "Paragraph" :
            st.markdown(html_temp, unsafe_allow_html=True)
            pattern = pattrn[choice]
            links = re.findall(pattern, html)
            
            if len(links) != 0:
                dframe = pd.DataFrame(links)
                dframe.columns = ["Text"]
                selected = aggrid(dframe)
            else:
                st.write("Nothing Found")

        
        else:
            pass

        st.sidebar.markdown(
            """ Developed by Syed Huzaifa Ali    
                Email : huzaifa.ali532@gmail.com  
                """)

if __name__ == "__main__":
    main()