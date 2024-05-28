import streamlit as st
import requests
import jwt

BASE_URL = "https://dnoted.azurewebsites.net/api/user"

def login():
    st.title("Iniciar Sesión")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar Sesión"):
        login_data = {
            "Email": email,
            "Password": password
        }
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['token']
            st.session_state["token"] = token
            st.session_state["logged_in"] = True
            st.success("Sesión iniciada con éxito")
            st.rerun()
        else:
            st.error("Error al iniciar sesión")

def create_user():
    st.title("Crear Usuario")
    full_name = st.text_input("Nombre Completo")
    email = st.text_input("Email")
    password = st.text_input("Contraseña", type="password")
    phone_number = st.text_input("Número de Teléfono")
    address = st.text_input("Dirección")
    profession = st.text_input("Profesión")
    image_url = st.text_input("URL de la Imagen")

    if st.button("Crear Usuario"):
        user_data = {
            "FullName": full_name,
            "Email": email,
            "Password": password,
            "PhoneNumber": phone_number,
            "Address": address,
            "Profession": profession,
            "ImageUrl": image_url
        }
        response = requests.post(f"{BASE_URL}/create", json=user_data)
        if response.status_code == 200:
            st.success("Usuario creado con éxito")
        else:
            st.error("Error al crear el usuario")

def decode_jwt(token):
    secret_key = "LauraLaQueVendeMangosEnElMercado"
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        st.error("El token ha expirado")
        return None
    except jwt.InvalidTokenError:
        st.error("Token inválido")
        return None
