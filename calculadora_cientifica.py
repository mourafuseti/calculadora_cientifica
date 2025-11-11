# calculadora_cientifica.py
# Calculadora científica com interface moderna (dark mode)
# Autor: Leonardo de Moura Fuseti

import customtkinter as ctk
from tkinter import END
import math

class CalculadoraCientifica:
    def __init__(self):
        # Configurações globais
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Janela principal
        self.root = ctk.CTk()
        self.root.title("Calculadora Científica")
        self.root.geometry("480x720")
        self.root.resizable(False, False)

        # Cores
        self.bg = "#1a1a1a"
        self.display_bg = "#2d2d2d"
        self.num_bg = "#404040"
        self.op_bg = "#ff6b35"
        self.func_bg = "#2e7d32"
        self.eq_bg = "#4CAF50"
        self.clear_bg = "#f44336"

        # Estado
        self.expressao = ""
        self.modo_graus = True  # True = graus, False = radianos

        self.criar_interface()

    def criar_interface(self):
        # Frame principal
        main = ctk.CTkFrame(self.root, fg_color=self.bg)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        # Display
        disp_frame = ctk.CTkFrame(main, height=140, fg_color=self.display_bg)
        disp_frame.pack(fill="x", pady=(0, 15))
        disp_frame.pack_propagate(False)

        self.display = ctk.CTkEntry(
            disp_frame,
            font=ctk.CTkFont(size=36, weight="bold"),
            justify="right",
            border_width=0,
            fg_color="transparent",
            text_color="#ffffff"
        )
        self.display.pack(fill="both", expand=True, padx=25, pady=25)
        self.display.insert(0, "0")

        # Frame de botões
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True)

        # Config padrão botão
        cfg = {"font": ctk.CTkFont(size=20, weight="bold"), "height": 65, "corner_radius": 14}

        # Linha 0 – Modo angular + funções avançadas
        self.criar_botao(btn_frame, "DEG", 0, 0, self.func_bg, self.toggle_modo, cfg)
        self.criar_botao(btn_frame, "π", 0, 1, self.func_bg, lambda: self.adicionar("math.pi"), cfg)
        self.criar_botao(btn_frame, "e", 0, 2, self.func_bg, lambda: self.adicionar("math.e"), cfg)
        self.criar_botao(btn_frame, "C", 0, 3, self.clear_bg, self.limpar, cfg)
        self.criar_botao(btn_frame, "⌫", 0, 4, self.clear_bg, self.apagar_ultimo, cfg)

        # Linha 1
        self.criar_botao(btn_frame, "sin", 1, 0, self.func_bg, lambda: self.funcao_trig("sin"), cfg)
        self.criar_botao(btn_frame, "cos", 1, 1, self.func_bg, lambda: self.funcao_trig("cos"), cfg)
        self.criar_botao(btn_frame, "tan", 1, 2, self.func_bg, lambda: self.funcao_trig("tan"), cfg)
        self.criar_botao(btn_frame, "x²", 1, 3, self.op_bg, lambda: self.adicionar("**2"), cfg)
        self.criar_botao(btn_frame, "÷", 1, 4, self.op_bg, lambda: self.adicionar_operador("/"), cfg)

        # Linha 2
        self.criar_botao(btn_frame, "sin⁻¹", 2, 0, self.func_bg, lambda: self.funcao_trig("asin"), cfg)
        self.criar_botao(btn_frame, "cos⁻¹", 2, 1, self.func_bg, lambda: self.funcao_trig("acos"), cfg)
        self.criar_botao(btn_frame, "tan⁻¹", 2, 2, self.func_bg, lambda: self.funcao_trig("atan"), cfg)
        self.criar_botao(btn_frame, "√", 2, 3, self.op_bg, lambda: self.adicionar("math.sqrt("), cfg)
        self.criar_botao(btn_frame, "×", 2, 4, self.op_bg, lambda: self.adicionar_operador("*"), cfg)

        # Linha 3
        self.criar_botao(btn_frame, "log", 3, 0, self.func_bg, lambda: self.adicionar("math.log10("), cfg)
        self.criar_botao(btn_frame, "ln", 3, 1, self.func_bg, lambda: self.adicionar("math.log("), cfg)
        self.criar_botao(btn_frame, "x!", 3, 2, self.func_bg, lambda: self.adicionar("math.factorial("), cfg)
        self.criar_botao(btn_frame, "(", 3, 3, self.op_bg, lambda: self.adicionar("("), cfg)
        self.criar_botao(btn_frame, "-", 3, 4, self.op_bg, lambda: self.adicionar_operador("-"), cfg)

        # Linha 4
        self.criar_botao(btn_frame, "7", 4, 0, self.num_bg, lambda: self.adicionar("7"), cfg)
        self.criar_botao(btn_frame, "8", 4, 1, self.num_bg, lambda: self.adicionar("8"), cfg)
        self.criar_botao(btn_frame, "9", 4, 2, self.num_bg, lambda: self.adicionar("9"), cfg)
        self.criar_botao(btn_frame, ")", 4, 3, self.op_bg, lambda: self.adicionar(")"), cfg)
        self.criar_botao(btn_frame, "+", 4, 4, self.op_bg, lambda: self.adicionar_operador("+"), cfg)

        # Linha 5
        self.criar_botao(btn_frame, "4", 5, 0, self.num_bg, lambda: self.adicionar("4"), cfg)
        self.criar_botao(btn_frame, "5", 5, 1, self.num_bg, lambda: self.adicionar("5"), cfg)
        self.criar_botao(btn_frame, "6", 5, 2, self.num_bg, lambda: self.adicionar("6"), cfg)
        self.criar_botao(btn_frame, "±", 5, 3, self.op_bg, self.inverter_sinal, cfg)
        self.criar_botao(btn_frame, "=", 5, 4, self.eq_bg, self.calcular, cfg, rowspan=2)

        # Linha 6
        self.criar_botao(btn_frame, "1", 6, 0, self.num_bg, lambda: self.adicionar("1"), cfg)
        self.criar_botao(btn_frame, "2", 6, 1, self.num_bg, lambda: self.adicionar("2"), cfg)
        self.criar_botao(btn_frame, "3", 6, 2, self.num_bg, lambda: self.adicionar("3"), cfg)
        self.criar_botao(btn_frame, "%", 6, 3, self.op_bg, lambda: self.adicionar("%"), cfg)

        # Linha 7 – Zero
        self.criar_botao(btn_frame, "0", 7, 0, self.num_bg, lambda: self.adicionar("0"), cfg, columnspan=2)
        self.criar_botao(btn_frame, ".", 7, 2, self.num_bg, lambda: self.adicionar("."), cfg)
        self.criar_botao(btn_frame, "^", 7, 3, self.op_bg, lambda: self.adicionar("**"), cfg)

        # Configurar grid
        for i in range(8):
            btn_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1)

    def criar_botao(self, parent, texto, linha, coluna, cor, comando, config, columnspan=1, rowspan=1):
        hover = self.brilho_cor(cor, 1.15)
        btn = ctk.CTkButton(
            parent, text=texto, command=comando,
            fg_color=cor, hover_color=hover, text_color="#ffffff", **config
        )
        btn.grid(row=linha, column=coluna, columnspan=columnspan, rowspan=rowspan,
                 padx=4, pady=4, sticky="nsew")
        return btn

    def brilho_cor(self, hex_cor, fator):
        hex_cor = hex_cor.lstrip('#')
        rgb = [min(255, int(int(hex_cor[i:i+2], 16) * fator)) for i in (0, 2, 4)]
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

    def adicionar(self, valor):
        atual = self.display.get()
        if atual in ("0", "Erro"):
            self.display.delete(0, END)
            self.display.insert(0, valor)
        else:
            self.display.insert(END, valor)
        self.expressao += valor

    def adicionar_operador(self, op):
        atual = self.display.get()
        if atual and atual[-1] not in "+-*/(":
            self.adicionar(op)

    def limpar(self):
        self.display.delete(0, END)
        self.display.insert(0, "0")
        self.expressao = ""

    def apagar_ultimo(self):
        atual = self.display.get()
        if len(atual) > 1:
            self.display.delete(len(atual)-1, END)
            self.expressao = self.expressao[:-1]
        else:
            self.limpar()

    def inverter_sinal(self):
        atual = self.display.get()
        if atual and atual != "0":
            if atual.startswith("-"):
                novo = atual[1:]
            else:
                novo = "-" + atual
            self.display.delete(0, END)
            self.display.insert(0, novo)

    def toggle_modo(self):
        self.modo_graus = not self.modo_graus
        texto = "DEG" if self.modo_graus else "RAD"
        # Atualiza botão (simulação – precisa de referência)
        pass

    def funcao_trig(self, func):
        atual = self.display.get()
        try:
            valor = float(atual)
            if not self.modo_graus:
                valor = math.radians(valor)
            resultado = {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan
            }[func](valor)
            self.mostrar_resultado(resultado)
        except:
            self.mostrar_erro()

    def calcular(self):
        try:
            expr = self.display.get()
            expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
            if "%" in expr:
                partes = expr.split("%")
                if len(partes) == 2 and partes[1] == "":
                    expr = partes[0] + "/100"
            resultado = eval(expr, {"__builtins__": {}}, {
                "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "asin": math.asin, "acos": math.acos, "atan": math.atan,
                "log10": math.log10, "log": math.log, "sqrt": math.sqrt,
                "factorial": math.factorial, "pi": math.pi, "e": math.e
            })
            self.mostrar_resultado(resultado)
        except Exception:
            self.mostrar_erro()

    def mostrar_resultado(self, valor):
        if valor == int(valor):
            valor = int(valor)
        else:
            valor = round(valor, 10)
        self.display.delete(0, END)
        self.display.insert(0, str(valor))
        self.expressao = str(valor)

    def mostrar_erro(self):
        self.display.delete(0, END)
        self.display.insert(0, "Erro")
        self.expressao = ""

    def run(self):
        self.root.mainloop()


# ========================================
# Execução
# ========================================
if __name__ == "__main__":
    app = CalculadoraCientifica()
    app.run()