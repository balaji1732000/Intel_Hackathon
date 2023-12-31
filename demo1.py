# Import the necessary libraries
import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

# Setup web page
st.set_page_config(
    page_title="Streamlit to Streamlit-in-Snowflake",
    layout="wide",
    menu_items={
        "Get Help": "https://developers.snowflake.com",
        "About": "The source code for this application can be accessed on GitHub https://github.com/iamontheinet/streamlit-to-sis",
    },
)

st.header(f"Streamlit to Streamlit in Snowflake (SiS)")
st.subheader("See which features in your Streamlit app are currently not supported in SiS")
st.caption(f"If you're new to Snowflake and Streamlit, checkout this step-by-step [QuickStart Guide](https://quickstarts.snowflake.com/guide/getting_started_with_snowpark_for_python_streamlit/index.html).")
st.caption(f"App developed by Dash | [Twitter](https://twitter.com/iamontheinet) | [LinkedIn](https://www.linkedin.com/in/dash-desai/)")
st.markdown("___")

docs_url = "https://docs.snowflake.com/developer-guide/streamlit/limitations#label-streamlit-unsupported-features"

def unsupported_features(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    features = []
    possible_features = []
    others = []
    features = soup.find_all("a", {"class": "reference external"})

    try:
        features = [f.text for f in features if f.text.startswith("st.")]
        features = features + [f.replace("st.", "st.sidebar.") for f in features]
    except:
        features += ['N/A']
    
    try:
        possible_features = features + [f.replace("st.", ".") for f in features]
    except:
        possible_features = ['N/A']
    
    try:
        others = soup.find("div", {"id": "limitations-and-unsupported-features-during-preview"}).find_all(
            "div"
        )
        others = [o.find("h3").text[:-1] for o in others]
    except:
        others = ['N/A']
        
    return features, possible_features, others

def check_valid_github_url(url):
    if "github" in url and ("blob" in url or "raw" in url):
        return True

uploaded_file = None

with st.container():
    col1,col2= st.columns(2, gap='large')

    with col1:
        st.subheader(
            "Upload your Streamlit app Python file, OR 👉"
        )
        uploaded_file = st.file_uploader(
            "Upload your Streamlit Python file", accept_multiple_files=False, label_visibility="hidden"
        )
    
    with col2:
        st.subheader("Provide the GitHub URL of your Streamlit app Python file")
        st.text("For example, https://github.com/iamontheinet/streamlit-to-sis/blob/main/streamlit_app.py")
        streamlit_link = st.text_input(
            "Enter the GitHub URL of your Streamlit app Python file",
            label_visibility="hidden"
        )

if uploaded_file is not None or check_valid_github_url(streamlit_link):
    features, possible_features, others = unsupported_features(docs_url)
    if uploaded_file is not None:
        code_lines = uploaded_file.getvalue().decode("utf-8").splitlines()
    elif check_valid_github_url(streamlit_link):
        streamlit_link = streamlit_link.replace("blob", "raw")
        response = requests.get(streamlit_link)
        code_lines = response.text.splitlines()

    if code_lines:
        with st.container():
            bad_features = []
            possible_bad_features = []
            for code_line in code_lines:
                for f in features:
                    idx = code_line.find(f)
                    if idx > 0:
                        bad_features.append([f, code_line.strip()])
                for p in possible_features:
                    idx = code_line.find(p)
                    if idx > 0:
                        possible_bad_features.append([p, code_line.strip()])

            if not (bad_features and possible_bad_features):
                st.snow()
                st.markdown("""<h1 style='color:#29b5e8; text-align:center'>Congratulations! Your Streamlit app is ready to be ported to SiS!</h1>""",unsafe_allow_html=True)          
            else:
                bdf = pd.DataFrame(bad_features, columns=["Unsupported Feature in SiS", "Line"])
                pbf = pd.DataFrame(
                    possible_bad_features, columns=["Possibly Unsupported Feature in SiS", "Line"]
                )

                # Remove any lines from pbf where the Line is in bdf
                pbf = pbf[~pbf["Line"].isin(bdf["Line"])]

                st.subheader("Unsupported Features")
                st.dataframe(bdf, use_container_width=True)

                st.markdown("___")
                st.subheader("Possibly Unsupported Features")
                st.dataframe(pbf, use_container_width=True)   

            st.markdown("___")

            st.subheader("Other Limitations To Keep In Mind")
            for o in others:
                st.text("* " + o)

            st.markdown("___")
            st.caption(f"For a full list and more information about unsupported features, please refer to the [documentation]({docs_url}).")

    else:
        st.write("Please upload a Streamlit app Python file or provide a GitHub URL for it.")