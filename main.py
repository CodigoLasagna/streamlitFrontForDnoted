import streamlit as st
import user_control as uc
import appointments_control as ac

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if st.session_state["logged_in"]:
        menu = ["Listar Citas", "Crear Cita", "Cerrar sesión"]
        choice = st.sidebar.selectbox("Menú", menu)
        
        if choice == "Listar Citas":
            ac.list_appointments()
        elif choice == "Crear Cita":
            ac.create_appointment()
        elif choice == "Cerrar sesión":
            uc.login()
    else:
        menu = ["Iniciar Sesión", "Crear Usuario"]
        choice = st.sidebar.selectbox("Menú", menu)

        if choice == "Crear Usuario":
            uc.create_user()
        elif choice == "Iniciar Sesión":
            uc.login()

if __name__ == "__main__":
    main()
