def aplicar_mascara_data_str(texto_atual: str, e_backspace: bool) -> str:
    if e_backspace:
        return texto_atual

    digitos = ''.join(filter(str.isdigit, texto_atual))
    novo_texto = ""

    if len(digitos) > 0:
        novo_texto += digitos[:2]
    if len(digitos) >= 3:
        novo_texto += "/" + digitos[2:4]
    if len(digitos) >= 5:
        novo_texto += "/" + digitos[4:8]

    return novo_texto


def aplicar_mascara_hora_str(texto_atual: str, e_backspace: bool) -> str:
    if e_backspace:
        return texto_atual

    digitos = ''.join(filter(str.isdigit, texto_atual))
    novo_texto = ""

    if len(digitos) > 0:
        novo_texto += digitos[:2]
    if len(digitos) >= 3:
        novo_texto += ":" + digitos[2:4]

    return novo_texto