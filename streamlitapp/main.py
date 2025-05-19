import streamlit as st
import requests

API_URL = "https://localhost:8000/api/v1/auth"  # Update this to your deployed URL

def show_login():
    st.markdown("<h1 style='text-align: center;'>📚 Bookly App</h1>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        show_password = st.checkbox("Show Password")
        if show_password:
            st.text(password)

        if st.button("🔐 Login"):
            try:
                response = requests.post(
                    f"{API_URL}/login",
                    json={"email": email, "password": password},
                    verify=False  # Only use this for localhost with self-signed certs!
                )
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    st.success("✅ Login successful!")
                    st.session_state.token = token
                else:
                    st.error(f"❌ Login failed: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

        if st.button("📝 Register"):
            st.session_state.page = "register"

        st.markdown("<p style='text-align: center;'><a href='#'>Forgot Password?</a></p>", unsafe_allow_html=True)

if __name__ == "__main__":
    show_login()
