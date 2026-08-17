from datetime import datetime

class GerenciadorReservas:
    def __init__(self):
        self.reservas = []
        self.usuario_logado = None
        self.usuarios_validos = {
            "vitor": "123",
            "wesley": "123",
            "lopes": "123"
        }
        self.laboratorios_disponiveis = ["Lab 1", "Lab 2", "Lab 3", "Lab 4"]

    def obter_laboratorios(self):
        return self.laboratorios_disponiveis

    def fazer_login(self, nome_usuario, senha):
        nome_limpo = nome_usuario.strip().lower()
        senha_limpa = senha.strip()

        if not nome_limpo or not senha_limpa:
            return False, "Por favor, preencha o usuário e a senha."
        
        if nome_limpo not in self.usuarios_validos:
            return False, f"Acesso negado! O usuário '{nome_usuario}' não está cadastrado."
        
        if self.usuarios_validos[nome_limpo] != senha_limpa:
            return False, "Senha incorreta! Tente novamente."
        
        self.usuario_logado = nome_limpo.capitalize()
        return True, f"Bem-vindo(a), Prof. {self.usuario_logado}!"

    def obter_reservas_usuario_logado(self):
        if not self.usuario_logado:
            return []
        return [r for r in self.reservas if r["professor"].lower() == self.usuario_logado.lower()]

    def validar_e_adicionar(self, professor, laboratorio, data_str, inicio_str, fim_str):
        if not all([professor.strip(), laboratorio.strip(), data_str.strip(), inicio_str.strip(), fim_str.strip()]):
            return False, "Todos os campos devem ser preenchidos."

        data_str_limpa = data_str.replace("-", "/").strip()
        
        try:
            data_reserva = datetime.strptime(data_str_limpa, "%d/%m/%Y").date()
        except ValueError:
            return False, "Data inválida! Use o formato DD/MM/AAAA (ex: 15/09/2026)."

        try:
            inicio = datetime.strptime(inicio_str.strip(), "%H:%M").time()
            fim = datetime.strptime(fim_str.strip(), "%H:%M").time()
        except ValueError:
            return False, "Horário inválido! Use o formato HH:MM (ex: 08:00)."

        hoje = datetime.now().date()
        if data_reserva < hoje:
            return False, "A data da reserva não pode ser no passado."
        if fim <= inicio:
            return False, "O horário de término deve ser posterior ao horário de início."
        for r in self.reservas:
            if r['laboratorio'].lower() == laboratorio.strip().lower() and r['data'] == data_str_limpa:
                r_inicio = datetime.strptime(r['inicio'], "%H:%M").time()
                r_fim = datetime.strptime(r['fim'], "%H:%M").time()

                if max(inicio, r_inicio) < min(fim, r_fim):
                    return False, f"Conflito! O {laboratorio} já possui reserva das {r['inicio']} às {r['fim']} nesta data."

        nova_reserva = {
            "id": len(self.reservas) + 1,
            "professor": professor.strip(),
            "laboratorio": laboratorio.strip(),
            "data": data_str_limpa,
            "inicio": inicio_str.strip(),
            "fim": fim_str.strip()
        }
        self.reservas.append(nova_reserva)
        return True, "Reserva realizada com sucesso!"

    def cancelar_reserva(self, reserva_id):
        reserva = next((r for r in self.reservas if r["id"] == reserva_id), None)
        if not reserva:
            return False, "Reserva não encontrada."

        if self.usuario_logado and reserva["professor"].lower() != self.usuario_logado.lower():
            return False, f"Acesso Negado! Apenas o(a) Prof. {reserva['professor']} pode cancelar esta reserva."

        self.reservas.remove(reserva)
        return True, "Reserva cancelada com sucesso!"