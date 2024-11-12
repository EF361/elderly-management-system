import streamlit as st
import home
import features
import login

st.set_page_config(page_title="Carelink", page_icon=":material/spa:")


def logged_in():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("app.py", label="Switch accounts")
    st.sidebar.page_link("pages/user.py", label="Your profile")
    if st.session_state.role in ["admin", "super-admin"]:
        st.sidebar.page_link("pages/admin.py", label="Manage users")
        st.sidebar.page_link(
            "pages/super-admin.py",
            label="Manage admin access",
            disabled=st.session_state.role != "super-admin",
        )


def logged_out():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("home.py", label="Home")
    st.sidebar.page_link("features.py", label="Features")
    st.sidebar.page_link("login.py", label="Login")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        logged_out()
        return
    logged_in()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("app.py")
    menu()
