import tkinter as tk
from tkinter import messagebox

class Memoria:
    def __init__(self, total_memoria):
        self.blocos = [(0, total_memoria, False)]  

    def alocar_memoria(self, processo_id, tamanho):
        for i, (inicio, tamanho_bloco, ocupado) in enumerate(self.blocos):
            if not ocupado and tamanho_bloco >= tamanho:
          
                self.blocos[i] = (inicio, tamanho, True, processo_id)
                
                if tamanho_bloco > tamanho:
                    self.blocos.insert(i + 1, (inicio + tamanho, tamanho_bloco - tamanho, False))
                return True
        return False  

    def desalocar_memoria(self, processo_id):
        for i, bloco in enumerate(self.blocos):
            if len(bloco) == 4 and bloco[3] == processo_id:
                
                self.blocos[i] = (bloco[0], bloco[1], False)
                
                
                self._consolidar_blocos()
                return True
        return False

    def _consolidar_blocos(self):
        i = 0
        while i < len(self.blocos) - 1:
            bloco_atual = self.blocos[i]
            proximo_bloco = self.blocos[i + 1]
            if not bloco_atual[2] and not proximo_bloco[2]:
                
                self.blocos[i] = (bloco_atual[0], bloco_atual[1] + proximo_bloco[1], False)
                del self.blocos[i + 1]
            else:
                i += 1

class InterfaceMemoria(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Alocação de Memória")
        self.geometry("400x500")
        
        self.memoria = Memoria(100)  
        
        self.label_id = tk.Label(self, text="ID do Processo:")
        self.label_id.pack()
        self.entry_id = tk.Entry(self)
        self.entry_id.pack()

        self.label_tamanho = tk.Label(self, text="Tamanho do Processo:")
        self.label_tamanho.pack()
        self.entry_tamanho = tk.Entry(self)
        self.entry_tamanho.pack()

        self.botao_alocar = tk.Button(self, text="Alocar", command=self.alocar)
        self.botao_alocar.pack()
        self.botao_desalocar = tk.Button(self, text="Desalocar", command=self.desalocar)
        self.botao_desalocar.pack()
        
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white")
        self.canvas.pack()
        
        self.atualizar_canvas()

    def alocar(self):
        try:
            processo_id = self.entry_id.get()
            tamanho = int(self.entry_tamanho.get())
            if tamanho <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Tamanho inválido!")
            return
        
        if not self.memoria.alocar_memoria(processo_id, tamanho):
            messagebox.showerror("Erro", "Memória insuficiente para alocar o processo.")
        self.atualizar_canvas()

    def desalocar(self):
        processo_id = self.entry_id.get()
        if not self.memoria.desalocar_memoria(processo_id):
            messagebox.showerror("Erro", "Processo não encontrado!")
        self.atualizar_canvas()

    def atualizar_canvas(self):
        self.canvas.delete("all")
        x = 10
        y = 10
        largura = 280
        
        for inicio, tamanho, ocupado, *resto in self.memoria.blocos:
            altura = (tamanho / self.memoria.total_memoria) * 280  
            cor = "red" if ocupado else "green"
            processo_id = resto[0] if ocupado else ""
            
            self.canvas.create_rectangle(x, y, x + largura, y + altura, fill=cor)
            if processo_id:
                self.canvas.create_text(x + largura / 2, y + altura / 2, text=processo_id, fill="white")
            y += altura

if __name__ == "__main__":
    app = InterfaceMemoria()
    app.mainloop()
