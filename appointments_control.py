import streamlit as st
import requests
import jwt

BASE_URL = "https://dnoted.azurewebsites.net/api/appointment"

def decode_jwt(token):
    secret_key = "LauraLaQueVendeMangosEnElMercado"
    decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    return decoded

def get_color(status):
    if status == 0:
        return "#FF6347"
    elif status == 1:
        return "#1E90FF"
    elif status == 2:
        return "#2ec78c"
    else:
        return "#FFFFFF"

def list_appointments():
    st.title("Listar Citas")
    if "token" in st.session_state:
        status_options = {"Todas": 3, "Solicitadas": 1, "Aceptadas": 2, "Rechazadas": 0}
        selected_status = st.selectbox("Seleccione el estado de las citas:", options=list(status_options.keys()))

        response = requests.get(f"{BASE_URL}/GetAllAppointments/{status_options[selected_status]}")
        if response.status_code == 200:
            appointments = response.json()
            if appointments:
                for appointment in appointments:
                    color = get_color(appointment['status'])
                    st.markdown(f"""
                    <div style='background-color:{color}; padding:10px; border-radius:5px; margin-bottom:10px;'>
                        <strong>Cliente:</strong> {appointment['clientName']}<br>
                        <strong>Teléfono:</strong> {appointment['phoneNumber']}<br>
                        <strong>Fecha:</strong> {appointment['startDate']}<br>
                        <strong>Hora:</strong> {appointment['startTime']}<br>
                        <strong>Duración:</strong> {appointment['durationMinutes']} minutos
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No hay citas disponibles.")
        else:
            st.error("Error al obtener las citas.")
    else:
        st.warning("Debe iniciar sesión primero")

def create_appointment():
    st.title("Crear Cita")
    if "token" in st.session_state:
        token = st.session_state["token"]
        decoded_token = decode_jwt(token)
        service_provider_id = decoded_token["userId"]

        client_name = st.text_input("Nombre del Cliente")
        phone_number = st.text_input("Número de Teléfono")
        start_date = st.date_input("Fecha de Inicio")
        start_time = st.time_input("Hora de Inicio")
        duration_minutes = st.number_input("Duración (minutos)", min_value=0)
        user_image = st.text_input("URL de la Imagen")
        status = st.selectbox("Estado", options=[0, 1, 2])

        if st.button("Crear Cita"):
            appointment_data = {
                "ClientName": client_name,
                "PhoneNumber": phone_number,
                "StartDate": start_date.isoformat(),
                "StartTime": start_time.isoformat(),
                "DurationMinutes": duration_minutes,
                "UserImage": user_image,
                "ServiceProviderId": service_provider_id,
                "Status": status
            }
            response = requests.post(f"{BASE_URL}/create", json=appointment_data)
            if response.status_code == 200:
                st.success("Cita creada con éxito")
            else:
                st.error("Error al crear la cita")
    else:
        st.warning("Debe iniciar sesión primero")

# Inicia la aplicación
if st.button("Listar Citas"):
    list_appointments()

if st.button("Crear Cita"):
    create_appointment()
