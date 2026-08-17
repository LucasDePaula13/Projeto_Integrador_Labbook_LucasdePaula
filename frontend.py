import customtkinter as ctk
from tkinter import messagebox, ttk
from backend import GerenciadorReservas
from utils import aplicar_mascara_data_str, aplicar_mascara_hora_str

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
class AppLabBooking(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LabBooking - Gestão de Reservas")
        self.geometry("850x550")
        self.resizable(False, False)

        self.backend = GerenciadorReservas()
        self.frames = {}
        
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        for F in (TelaLogin, TelaInicial, TelaReservarSala, TelaConferirReservas, TelaPerfil):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.mostrar_tela("TelaLogin")

    def mostrar_tela(self, nome_tela):
        frame = self.frames[nome_tela]
        if hasattr(frame, "atualizar_tela"):
            frame.atualizar_tela()
        frame.tkraise()

class TelaLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="LOGIN - LABBOOKING", font=("Arial", 22, "bold")).pack(pady=(60, 20))

        self.ent_usuario = ctk.CTkEntry(self, placeholder_text="Usuário (vitor, wesley ou lopes)", width=300)
        self.ent_usuario.pack(pady=10)

        self.ent_senha = ctk.CTkEntry(self, placeholder_text="Senha (padrão: 123)", show="*", width=300)
        self.ent_senha.pack(pady=10)

        ctk.CTkButton(self, text="Entrar", width=300, command=self.fazer_login).pack(pady=20)

    def fazer_login(self):
        usuario = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()
        
        sucesso, msg = self.controller.backend.fazer_login(usuario, senha)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.ent_usuario.delete(0, 'end')
            self.ent_senha.delete(0, 'end')
            self.controller.mostrar_tela("TelaInicial")
        else:
            messagebox.showerror("Erro de Autenticação", msg, parent=self)

class TelaInicial(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.lbl_boas_vindas = ctk.CTkLabel(self, text="Tela Inicial", font=("Arial", 22, "bold"))
        self.lbl_boas_vindas.pack(pady=(40, 30))

        ctk.CTkButton(self, text="Reservar Sala", width=250, height=40,
                      command=lambda: controller.mostrar_tela("TelaReservarSala")).pack(pady=12)

        ctk.CTkButton(self, text="Conferir Reservas", width=250, height=40,
                      command=lambda: controller.mostrar_tela("TelaConferirReservas")).pack(pady=12)

        ctk.CTkButton(self, text="Perfil do Professor", width=250, height=40, fg_color="#4A5568",
                      command=lambda: controller.mostrar_tela("TelaPerfil")).pack(pady=12)

        ctk.CTkButton(self, text="Sair / Logout", width=150, fg_color="transparent", border_width=1,
                      command=lambda: controller.mostrar_tela("TelaLogin")).pack(pady=(30, 0))

    def atualizar_tela(self):
        usr = self.controller.backend.usuario_logado or "Professor"
        self.lbl_boas_vindas.configure(text=f"Painel Principal - Prof. {usr}")

class TelaReservarSala(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Reserva de Sala", font=("Arial", 20, "bold")).pack(pady=20)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(form_frame, text="Nome do Professor:").grid(row=0, column=0, sticky="w", padx=15, pady=5)
        self.ent_nome = ctk.CTkEntry(form_frame, width=250)
        self.ent_nome.grid(row=0, column=1, padx=15, pady=5)

        ctk.CTkLabel(form_frame, text="Nº da Sala / Laboratório:").grid(row=1, column=0, sticky="w", padx=15, pady=5)
        labs = self.controller.backend.obter_laboratorios()
        self.cb_lab = ctk.CTkComboBox(form_frame, values=labs, width=250, state="readonly")
        self.cb_lab.set(labs[0] if labs else "")
        self.cb_lab.grid(row=1, column=1, padx=15, pady=5)

        ctk.CTkLabel(form_frame, text="Data (DD/MM/AAAA):").grid(row=2, column=0, sticky="w", padx=15, pady=5)
        self.ent_data = ctk.CTkEntry(form_frame, placeholder_text="ex: 15/09/2026", width=250)
        self.ent_data.grid(row=2, column=1, padx=15, pady=5)
        self.ent_data.bind("<KeyRelease>", self.aplicar_mascara_data)

        ctk.CTkLabel(form_frame, text="Horário Início (HH:MM):").grid(row=3, column=0, sticky="w", padx=15, pady=5)
        self.ent_inicio = ctk.CTkEntry(form_frame, placeholder_text="ex: 08:00", width=250)
        self.ent_inicio.grid(row=3, column=1, padx=15, pady=5)
        self.ent_inicio.bind("<KeyRelease>", lambda event: self.aplicar_mascara_hora(event, self.ent_inicio))

        ctk.CTkLabel(form_frame, text="Horário Término (HH:MM):").grid(row=4, column=0, sticky="w", padx=15, pady=5)
        self.ent_fim = ctk.CTkEntry(form_frame, placeholder_text="ex: 10:00", width=250)
        self.ent_fim.grid(row=4, column=1, padx=15, pady=5)
        self.ent_fim.bind("<KeyRelease>", lambda event: self.aplicar_mascara_hora(event, self.ent_fim))

        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(pady=20)

        ctk.CTkButton(btn_box, text="Salvar Reserva", fg_color="green", command=self.salvar_reserva).pack(side="left", padx=10)
        ctk.CTkButton(btn_box, text="Limpar", fg_color="#D69E2E", command=self.limpar_campos).pack(side="left", padx=10)
        ctk.CTkButton(btn_box, text="Voltar", fg_color="gray", command=lambda: controller.mostrar_tela("TelaInicial")).pack(side="left", padx=10)

    def aplicar_mascara_data(self, event):
        novo = aplicar_mascara_data_str(self.ent_data.get(), event.keysym == "BackSpace")
        self.ent_data.delete(0, 'end')
        self.ent_data.insert(0, novo)

    def aplicar_mascara_hora(self, event, campo_entry):
        novo = aplicar_mascara_hora_str(campo_entry.get(), event.keysym == "BackSpace")
        campo_entry.delete(0, 'end')
        campo_entry.insert(0, novo)

    def limpar_campos(self):
        self.ent_data.delete(0, 'end')
        self.ent_inicio.delete(0, 'end')
        self.ent_fim.delete(0, 'end')
        labs = self.controller.backend.obter_laboratorios()
        if labs:
            self.cb_lab.set(labs[0])

    def atualizar_tela(self):
        if self.controller.backend.usuario_logado:
            self.ent_nome.delete(0, 'end')
            self.ent_nome.insert(0, self.controller.backend.usuario_logado)

    def salvar_reserva(self):
        prof = self.ent_nome.get()
        lab = self.cb_lab.get()
        data = self.ent_data.get()
        inicio = self.ent_inicio.get()
        fim = self.ent_fim.get()

        sucesso, msg = self.controller.backend.validar_e_adicionar(prof, lab, data, inicio, fim)

        self.controller.lift()
        self.controller.attributes('-topmost', True)
        self.controller.attributes('-topmost', False)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.limpar_campos()
            self.controller.mostrar_tela("TelaConferirReservas")
        else:
            messagebox.showerror("Erro de Validação", msg, parent=self)


class TelaConferirReservas(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Conferir Reservas Cadastradas", font=("Arial", 20, "bold")).pack(pady=15)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", rowheight=25)
        style.map("Treeview", background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self, columns=("ID", "Professor", "Laboratorio", "Data", "Inicio", "Fim"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Professor", text="Professor")
        self.tree.heading("Laboratorio", text="Laboratório")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Inicio", text="Início")
        self.tree.heading("Fim", text="Término")

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Professor", width=180)
        self.tree.column("Laboratorio", width=100, anchor="center")
        self.tree.column("Data", width=100, anchor="center")
        self.tree.column("Inicio", width=80, anchor="center")
        self.tree.column("Fim", width=80, anchor="center")

        self.tree.pack(pady=10, padx=20, fill="x")

        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(pady=15)

        ctk.CTkButton(btn_box, text="Cancelar Reserva Selecionada", fg_color="#C53030", command=self.cancelar_reserva).pack(side="left", padx=10)
        ctk.CTkButton(btn_box, text="Voltar para Início", fg_color="gray", command=lambda: controller.mostrar_tela("TelaInicial")).pack(side="left", padx=10)

    def atualizar_tela(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for r in self.controller.backend.reservas:
            self.tree.insert("", "end", values=(r["id"], r["professor"], r["laboratorio"], r["data"], r["inicio"], r["fim"]))

    def cancelar_reserva(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma reserva na tabela para cancelar.", parent=self)
            return

        valores = self.tree.item(item_selecionado, "values")
        reserva_id = int(valores[0])

        sucesso, msg = self.controller.backend.cancelar_reserva(reserva_id)
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.atualizar_tela()
        else:
            messagebox.showerror("Ação Negada", msg, parent=self)


class TelaPerfil(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(self, text="Perfil do Professor", font=("Arial", 20, "bold")).pack(pady=15)

        self.lbl_avatar = ctk.CTkLabel(self, text="👤", font=("Arial", 50))
        self.lbl_avatar.pack(pady=2)

        self.lbl_nome = ctk.CTkLabel(self, text="Nome: -", font=("Arial", 16, "bold"))
        self.lbl_nome.pack(pady=5)

        ctk.CTkLabel(self, text="Suas Reservas Agendadas:", font=("Arial", 14)).pack(pady=(10, 5))

        self.tree_minhas = ttk.Treeview(self, columns=("Laboratorio", "Data", "Horario"), show="headings", height=6)
        self.tree_minhas.heading("Laboratorio", text="Laboratório")
        self.tree_minhas.heading("Data", text="Data")
        self.tree_minhas.heading("Horario", text="Horário (Início - Término)")

        self.tree_minhas.column("Laboratorio", width=120, anchor="center")
        self.tree_minhas.column("Data", width=120, anchor="center")
        self.tree_minhas.column("Horario", width=200, anchor="center")

        self.tree_minhas.pack(pady=5, padx=30, fill="x")

        ctk.CTkButton(self, text="Voltar ao Menu", fg_color="gray", command=lambda: controller.mostrar_tela("TelaInicial")).pack(pady=15)

    def atualizar_tela(self):
        usr = self.controller.backend.usuario_logado or "Não identificado"
        self.lbl_nome.configure(text=f"Professor: {usr}")

        for i in self.tree_minhas.get_children():
            self.tree_minhas.delete(i)

        minhas_reservas = self.controller.backend.obter_reservas_usuario_logado()

        if not minhas_reservas:
            self.tree_minhas.insert("", "end", values=("Nenhuma", "-", "-"))
        else:
            for r in minhas_reservas:
                horario_formatado = f"{r['inicio']} às {r['fim']}"
                self.tree_minhas.insert("", "end", values=(r["laboratorio"], r["data"], horario_formatado))


if __name__ == "__main__":
    app = AppLabBooking()
    app.mainloop()