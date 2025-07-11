import requests
import json

def obtener_token(url="http://localhost:5000/api/login", username="admin", password="admin123"):
    payload = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # lanza excepción si hay error HTTP
        token = response.json().get("access_token")
        if token:
            print("Token JWT completo:")
            print(token)
            # Opcional: guardarlo en un archivo para uso posterior
            with open("token.jwt", "w") as f:
                f.write(token)
            print("\nToken guardado en token.jwt")
            return token
        else:
            print("No se recibió token en la respuesta.")
            return None
    except requests.RequestException as e:
        print(f"Error en la petición: {e}")
        return None

if __name__ == "__main__":
    obtener_token()
