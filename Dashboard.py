import streamlit as st


def main():
    st.title("Welcome to Restaurant Review Analyzer")
    st.markdown("""
    Use the sidebar to choose:
    - **Review Dashboard** to analyze a single restaurant.
    - **Competitor Analysis** to compare two restaurants.
    """)

if __name__ == "__main__":
    main()