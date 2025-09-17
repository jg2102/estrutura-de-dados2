class Vertice:
    """
    Representa um vértice na Estrutura AVL.
    Cada vértice contém um valor, ponteiros para os descendentes e seu nível.
    """
    def __init__(self, valor):
        self.valor = valor
        self.filho_esquerdo = None
        self.filho_direito = None
        self.nivel = 1  # O nível de um novo vértice (folha) é sempre 1

class EstruturaAVL:
    """
    Implementa o funcionamento e as operações de uma Estrutura AVL.
    """
    def __init__(self):
        self.origem = None

    # ===============================================================
    # TAREFA 0: FUNÇÕES AUXILIARES E ROTAÇÕES
    # ===============================================================

    def calcular_nivel(self, vertice):
        return vertice.nivel if vertice else 0

    def calcular_fator_equilibrio(self, vertice):
        if not vertice:
            return 0
        return self.calcular_nivel(vertice.filho_esquerdo) - self.calcular_nivel(vertice.filho_direito)

    def _atualizar_nivel(self, vertice):
        vertice.nivel = 1 + max(self.calcular_nivel(vertice.filho_esquerdo), self.calcular_nivel(vertice.filho_direito))

    def encontrar_vertice_valor_minimo(self, vertice):
        corrente = vertice
        while corrente.filho_esquerdo:
            corrente = corrente.filho_esquerdo
        return corrente

    def _girar_direita(self, vertice_central):
        novo_central = vertice_central.filho_esquerdo
        segmento = novo_central.filho_direito

        # Executa rotação
        novo_central.filho_direito = vertice_central
        vertice_central.filho_esquerdo = segmento

        # Atualiza níveis
        self._atualizar_nivel(vertice_central)
        self._atualizar_nivel(novo_central)

        return novo_central

    def _girar_esquerda(self, vertice_central):
        novo_central = vertice_central.filho_direito
        segmento = novo_central.filho_esquerdo

        # Executa rotação
        novo_central.filho_esquerdo = vertice_central
        vertice_central.filho_direito = segmento

        # Atualiza níveis
        self._atualizar_nivel(vertice_central)
        self._atualizar_nivel(novo_central)

        return novo_central

    # ===============================================================
    # TAREFA 1: ADIÇÃO E REMOÇÃO COM BALANCEAMENTO
    # ===============================================================

    def adicionar(self, valor):
        self.origem = self._adicionar_recursivo(self.origem, valor)

    def _adicionar_recursivo(self, vertice_atual, valor):
        # Adição padrão BST
        if not vertice_atual:
            return Vertice(valor)
        elif valor < vertice_atual.valor:
            vertice_atual.filho_esquerdo = self._adicionar_recursivo(vertice_atual.filho_esquerdo, valor)
        elif valor > vertice_atual.valor:
            vertice_atual.filho_direito = self._adicionar_recursivo(vertice_atual.filho_direito, valor)
        else:
            raise ValueError("Valor duplicado não permitido.")

        # Atualiza nível
        self._atualizar_nivel(vertice_atual)

        # Verifica equilíbrio
        equilibrio = self.calcular_fator_equilibrio(vertice_atual)

        # Caso 1: Esquerda-Esquerda
        if equilibrio > 1 and valor < vertice_atual.filho_esquerdo.valor:
            return self._girar_direita(vertice_atual)

        # Caso 2: Direita-Direita
        if equilibrio < -1 and valor > vertice_atual.filho_direito.valor:
            return self._girar_esquerda(vertice_atual)

        # Caso 3: Esquerda-Direita
        if equilibrio > 1 and valor > vertice_atual.filho_esquerdo.valor:
            vertice_atual.filho_esquerdo = self._girar_esquerda(vertice_atual.filho_esquerdo)
            return self._girar_direita(vertice_atual)

        # Caso 4: Direita-Esquerda
        if equilibrio < -1 and valor < vertice_atual.filho_direito.valor:
            vertice_atual.filho_direito = self._girar_direita(vertice_atual.filho_direito)
            return self._girar_esquerda(vertice_atual)

        return vertice_atual

    def remover(self, valor):
        self.origem = self._remover_recursivo(self.origem, valor)

    def _remover_recursivo(self, vertice_atual, valor):
        if not vertice_atual:
            return vertice_atual

        # Remoção padrão BST
        if valor < vertice_atual.valor:
            vertice_atual.filho_esquerdo = self._remover_recursivo(vertice_atual.filho_esquerdo, valor)
        elif valor > vertice_atual.valor:
            vertice_atual.filho_direito = self._remover_recursivo(vertice_atual.filho_direito, valor)
        else:
            # Vértice com 1 filho ou nenhum filho
            if not vertice_atual.filho_esquerdo:
                return vertice_atual.filho_direito
            elif not vertice_atual.filho_direito:
                return vertice_atual.filho_esquerdo
            # Vértice com 2 filhos → substitui pelo sucessor
            temporario = self.encontrar_vertice_valor_minimo(vertice_atual.filho_direito)
            vertice_atual.valor = temporario.valor
            vertice_atual.filho_direito = self._remover_recursivo(vertice_atual.filho_direito, temporario.valor)

        # Atualiza nível
        self._atualizar_nivel(vertice_atual)

        # Verifica equilíbrio
        equilibrio = self.calcular_fator_equilibrio(vertice_atual)

        # Caso 1: Esquerda-Esquerda
        if equilibrio > 1 and self.calcular_fator_equilibrio(vertice_atual.filho_esquerdo) >= 0:
            return self._girar_direita(vertice_atual)

        # Caso 2: Esquerda-Direita
        if equilibrio > 1 and self.calcular_fator_equilibrio(vertice_atual.filho_esquerdo) < 0:
            vertice_atual.filho_esquerdo = self._girar_esquerda(vertice_atual.filho_esquerdo)
            return self._girar_direita(vertice_atual)

        # Caso 3: Direita-Direita
        if equilibrio < -1 and self.calcular_fator_equilibrio(vertice_atual.filho_direito) <= 0:
            return self._girar_esquerda(vertice_atual)

        # Caso 4: Direita-Esquerda
        if equilibrio < -1 and self.calcular_fator_equilibrio(vertice_atual.filho_direito) > 0:
            vertice_atual.filho_direito = self._girar_direita(vertice_atual.filho_direito)
            return self._girar_esquerda(vertice_atual)

        return vertice_atual

    # ===============================================================
    # TAREFA 2 E 3: CONSULTAS
    # ===============================================================

    def localizar_vertices_intervalo(self, valor1, valor2):
        resultado = []
        self._consultar_intervalo(self.origem, valor1, valor2, resultado)
        return resultado

    def _consultar_intervalo(self, vertice, valor1, valor2, resultado):
        if not vertice:
            return
        if valor1 < vertice.valor:
            self._consultar_intervalo(vertice.filho_esquerdo, valor1, valor2, resultado)
        if valor1 <= vertice.valor <= valor2:
            resultado.append(vertice.valor)
        if valor2 > vertice.valor:
            self._consultar_intervalo(vertice.filho_direito, valor1, valor2, resultado)

    def obter_nivel_vertice(self, valor):
        return self._localizar_nivel(self.origem, valor, 0)

    def _localizar_nivel(self, vertice, valor, nivel):
        if not vertice:
            return -1
        if valor == vertice.valor:
            return nivel
        elif valor < vertice.valor:
            return self._localizar_nivel(vertice.filho_esquerdo, valor, nivel + 1)
        else:
            return self._localizar_nivel(vertice.filho_direito, valor, nivel + 1)


# --- Bloco de Teste ---
if __name__ == "__main__":
    estrutura_avl = EstruturaAVL()
    
    print("\n--- ATIVIDADE PRÁTICA: ESTRUTURA AVL ---")
    
    print("\n--- 1. Adicionando vértices ---")
    valores_para_adicionar = [9, 5, 10, 0, 6, 11, -1, 1, 2]
    try:
        for valor in valores_para_adicionar:
            estrutura_avl.adicionar(valor)
        print("Adição concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A ADIÇÃO: {e}")

    print("\n--- 2. Removendo vértices ---")
    try:
        valores_para_remover = [10, 11]
        for valor in valores_para_remover:
            estrutura_avl.remover(valor)
        print("Remoção concluída (sem erros).")
    except Exception as e:
        print(f"\nERRO DURANTE A REMOÇÃO: {e}")

    print("\n--- 3. Localizando vértices no intervalo [1, 9] ---")
    try:
        vertices_no_intervalo = estrutura_avl.localizar_vertices_intervalo(1, 9)
        if vertices_no_intervalo is not None:
            print(f"Vértices encontrados: {sorted(vertices_no_intervalo)}")
        else:
            print("Método `localizar_vertices_intervalo` ainda não implementado.")
    except Exception as e:
        print(f"\nERRO DURANTE A CONSULTA POR INTERVALO: {e}")

    print("\n--- 4. Calculando nível do vértice 6 ---")
    try:
        nivel = estrutura_avl.obter_nivel_vertice(6)
        if nivel != -1:
            print(f"O vértice 6 está no nível: {nivel}")
        else:
            print("O vértice 6 não foi encontrado.")
    except Exception as e:
        print(f"\nERRO DURANTE O CÁLCULO DE NÍVEL: {e}")
