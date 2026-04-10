import bcrypt

# CONFIGURA TUS USUARIOS AQUÍ
# ---------------------------
# "usuario": ["nombre_completo", "email", "password_real"]
user_data = {
    "admin":      ["Administrador", "agueromiguel7@gmail.com", "Coromoto_22"],
    "Mleccese":   ["Mleccese",    "michele.leccese.petrucci@gmail.com",    "Mlezk_l22"],
    "JFarinas":   ["JFarinas",    "farinasjg1@gmail.com",    "Fark_l27"],
    "Myanez":     ["Myanez",      "medardo.yanez@gmail.com",    "Myez_l25"],
    "AFernandez": ["AFernandez",  "alis.fernandezt@gmail.com",    "Afernd_l26"],
    "LFernandez": ["LFernandez",  "luisfernandezpino@gmail.com",    "Hzk_l21"],
    "GVegas":     ["Gustavo Vegas", "Gus@corainsights.com",    "Gveg_L28"],
    "usuario7":   ["Usuario Siete", "u7@campor2.com",    "Pass123"],
}

print("\n--- GENERANDO FORMATO PARA SECRETS (COPIA ESTO) ---\n")

for username, info in user_data.items():
    name, email, plain_pass = info
    
    # Generar Hash Nativo (Garantiza 60 caracteres)
    salt = bcrypt.gensalt(12)
    hashed_pass = bcrypt.hashpw(plain_pass.encode('utf-8'), salt).decode('utf-8')
    
    # Verificación de Largo
    if len(hashed_pass) != 60:
        continue

    print(f"[{username}]")
    print(f"email = '{email}'")
    print(f"name = '{name}'")
    print(f"password = '{hashed_pass}'")
    print()

print("--- FIN DEL ARCHIVO ---")
