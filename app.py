import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

st.set_page_config(page_title="Carelink", page_icon=":material/spa:")
# Database connection setup
engine = create_engine("postgresql://postgres:12345@localhost:5432/elderlymanagement")

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Resident", "Staff", "Admin"]


def login():
    st.title("Login to Carelink")
    role = st.selectbox(
        "Choose your role", ROLES[1:]
    )  # Remove None option for role selection
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        if username and password and role:
            table_name = role.lower()
            query = text(
                f"SELECT * FROM {table_name} WHERE username = :username AND password = :password"
            )
            try:
                with engine.connect() as conn:
                    result = (
                        conn.execute(
                            query, {"username": username, "password": password}
                        )
                        .mappings()
                        .fetchone()
                    )
                    if result:
                        st.session_state.role = role
                        st.session_state.user_name = result[
                            "name"
                        ]  # Access using column name
                        st.success(f"Logged in successfully as {role}")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            except SQLAlchemyError as e:
                st.error("Error during login. Please try again later.")
                print(e)
        else:
            st.warning("Please enter all fields")


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

# objects for staff
staff_dashboard = st.Page(
    "staff/dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=(role == "Staff"),
)

staff_medication = st.Page(
    "staff/medication.py",
    title="Medication Record",
    icon=":material/medication:",
)
shift = st.Page(
    "staff/shift.py",
    title="Shift",
    icon=":material/bar_chart:",
)

# objects for resident
chatbot = st.Page(
    "resident/chatbot.py",
    title="Chatbot",
    icon=":material/robot:",
    default=(role == "Resident"),
)
resident_dashboard = st.Page(
    "resident/dashboard.py",
    title="Overview",
    icon=":material/dashboard:",
)

schedule = st.Page(
    "resident/schedule.py",
    title="Schedule",
    icon=":material/table:",
)

# objects for admin
admin_dashboard = st.Page(
    "admin/dashboard.py",
    title="Overview",
    icon=":material/bar_chart:",
    default=(role == "Admin"),
)
admin_medication = st.Page(
    "admin/medication.py",
    title="Medication Management",
    icon=":material/medication:",
)
reports = st.Page(
    "admin/reports.py",
    title="Generate Report",
    icon=":material/summarize:",
)
schedule_management = st.Page(
    "admin/schedule.py",
    title="Schedule Management",
    icon=":material/schedule:",
)
resident_management = st.Page(
    "admin/resident_management.py",
    title="Resident Management",
    icon=":material/people:",
)
staff_management = st.Page(
    "admin/staff_management.py",
    title="Staff Management",
    icon=":material/groups:",
)
admin_management = st.Page(
    "admin/admin_management.py",
    title="Admin Management",
    icon=":material/supervisor_account:",
)

account_pages = [logout_page]
staff_pages = [
    staff_dashboard,
    staff_medication,
    shift,
]
resident_pages = [
    resident_dashboard,
    schedule,
    chatbot,
]
admin_pages = [
    admin_dashboard,
    admin_medication,
    schedule_management,
    resident_management,
    staff_management,
    admin_management,
    reports,
]
st.logo("images/logo.png", icon_image="images/logo.png")

page_dict = {}
if st.session_state.role in ["Staff"]:
    page_dict["Staff"] = staff_pages
if st.session_state.role in ["Resident"]:
    page_dict["Resident"] = resident_pages
if st.session_state.role == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict, position="sidebar")
else:
    pg = st.navigation([st.Page(login)])

pg.run()
