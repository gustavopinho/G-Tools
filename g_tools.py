# -*- coding: utf-8 -*-
# Autor: Jorge Gustavo do Santos Pinho

class GTools:
    """
        Classe de ferramentas usadas para as consultas de acessibilidade em grafos.
    """

    def __init__(self):
        self.white = 'white'
        self.gray = 'gray'
        self.black = 'black'
    
    def load_g(self, filename):
        """ Carrega o grafo a partir de um arquivo """
        G = {}
        with open(filename, 'rb') as input:
            for line in input:
                if line[0] != '#':
                    col_1, col_2 = line.split()
                    if not col_1 in G:
                        G[col_1] = []
                    if not col_2 in G:
                        G[col_2] = []
                    G[col_1].append(col_2)
        input.close()
        return G
        
    def is_acicle(self, G):
        """ Verifica se um grafo G é acíclico """
        self.acicle = False        
        color = {}
        for u in G:
            color[u] = self.white
        def dfs_visit(u):
            if self.acicle:
                return
            color[u] = self.gray
            for v in G[u]:
                if color[v] == self.white:
                    dfs_visit(v)
                elif color[v] == self.gray:
                    self.acicle = True
            color[u] = self.black
        for u in G:
            if self.acicle:
                break
            if color[u] == self.white:
                dfs_visit(u)
        return self.acicle
    
    def tarjan_scc(self, G):
        """ Usa o algoritmo de tarjan para criar os sccs """
        self.counter = 0
        S = []
        SCCS = []
        index = {}
        lowlink = {}
        
        def scc_visit(u):
            lowlink[u] = index[u] = len(index)
            S.append(u)
            for v in G[u]:
                if not v in index:
                    scc_visit(v)
                    lowlink[u] = min(lowlink[v], lowlink[u])
                elif v in S:
                    lowlink[u] = min(lowlink[u], index[v])
            if lowlink[u] == index[u]:
                scc = []
                v = None
                while u != v:
                    v = S.pop()
                    scc.append(v)
                SCCS.append(scc)
        for u in G:
            if not u in index:
                scc_visit(u)
        return SCCS
        
    def dag_associate(self, G, SCCS):
        """ Gera o DAG associado """
        COMP = {}
        DAG = {}
        for u in SCCS:
            DAG[u[0]] = []
            for c in u:
                COMP[c] = u[0]
        for u in G:
            cu = COMP[u]
            for v in G[u]:
                cv = COMP[v]
                if cu != cv:
                    if not cv in DAG[cu]:
                        DAG[cu].append(cv)
        return DAG
    
    def bfs(self, G, su, sv):
        """ Usa uma BFS para verificar se su alcaça sv """
        Q = []
        color = {}
        if su == sv:
            return True
        
        Q.append(su)
        while Q:
            u = Q.pop(0)
            for v in G[u]:
                if not v in color:
                    if v == sv:
                        return True
                    color[v] = self.gray
                    Q.append(v)
            color[u] = self.black
        return False

    def dfs(self, G, su, sv):
        """ Usa uma DFS para verificar se su alcaça sv """
        self.reach = False
        color = {}
        if su == sv:
            return True

        def dfs_visit(u):
            if self.reach:
                return
            color[u] = self.gray
            for v in G[u]:
                if not v in color:
                    if v == sv:
                        self.reach = True
                    dfs_visit(v)
                if self.reach:
                    break
            color[u] = self.black
        dfs_visit(su)
        return self.reach

    def scc_index(self, SCCS):
        """ Cria indice de representantes para otimizar na busca """
        index = {}
        for scc in SCCS:
            for c in scc:
               index[c] = scc[0]
        return index

    def save_graph(self, Ghaph, filename):
        """ Salva um grafo em um arquivo """
        with open(filename, 'wb') as output:
            pickle.dump(Ghaph, output, pickle.HIGHEST_PROTOCOL)
            
    def open_graph(self, filename):
        """ Abre um grafo salvo em arquivo """
        with open(filename, 'rb') as input:
            return pickle.load(input)

    
if __name__ == "__main__":
    import time, sys, pickle
    from decimal import Decimal
    
    sys.setrecursionlimit(100000000)
    
    GT = GTools()
    
    start = time.time()
    G = GT.load_g('web-NotreDame.txt')
    print 'Tempo para carregar o web-NotreDame: ' + str(time.time() - start) + 's'
    
    contador = 0
    for indx, e in enumerate(G):
        contador = contador + len(G[str(indx)])
        
    print 'Quantidade de vértices: '+ str(len(G))
    print 'Quantidade de arestas: '+ str(contador)
    
    print 'Verificando grafo acíclico'
    start = time.time()
    acicle = GT.is_acicle(G)
    print 'O grafo é acíclico? ' +  str(acicle) 
    print 'Tempo para verificar se o grafo é acíclico: ' + str(time.time() - start) + 's'
    
    print 'Construindo SCCS'
    start = time.time()
    SCCS = GT.tarjan_scc(G)
    print 'Tempo para construir SCCS: ' + str(time.time() - start) + 's'
    
    print 'Construindo DAG'
    start = time.time()
    DAG = GT.dag_associate(G, SCCS)
    print 'Tempo para construir o DAG: ' + str(time.time() - start) + 's'
        
    print 'Quantidade de componentes no SCC: ' + str(len(SCCS))
    print 'Quantidade de vertices do DAG: ' + str(len(DAG))
    dag_arestas = 0
    
    for indx, d in DAG.items():
        dag_arestas = dag_arestas + len(DAG[str(indx)])
    print 'Quantidade de arestas do DAG: ' + str(dag_arestas)
    
    start = time.time()
    acicle = GT.is_acicle(DAG)
    print 'DAG ciclos? ' +  str(acicle) 
    print 'Tempo para verificar o DAG: ' + str(time.time() - start) + 's'
    
    statistics  = { 
        'bfs' : { 'sim' : 0, 'nao' : 0, 'time_sim' : 0, 'time_nao': 0, 'time_t' : 0}, 
        'dfs' : { 'sim' : 0, 'nao' : 0, 'time_sim' : 0, 'time_nao': 0, 'time_t' : 0}
    }

    contador = 0
    start = time.time()
    index = GT.scc_index(SCCS) 
    print 'Tempo para construir indices: ' + str(time.time() - start) + 's'
 
    print 'Iniciando consultas (u acessa v) BFS e DFS'
    
    start = time.time()
    with open('consultas_buscas.txt', 'rb') as input:
        for line in input:
            if (contador % 10000) == 0 and contador != 0:
                print 'Consultas realizadas: ' + str(contador)

            u, v = line.split()
            
            u = index[u]
            v = index[v]
            
            start = time.time()
            if GT.bfs(DAG, u, v) == True:
                statistics['bfs']['sim'] = statistics['bfs']['sim'] + 1
                statistics['bfs']['time_sim'] = statistics['bfs']['time_sim'] + (time.time() - start)
            else:
                statistics['bfs']['nao'] = statistics['bfs']['nao'] + 1
                statistics['bfs']['time_nao'] = statistics['bfs']['time_nao'] + (time.time() - start)
            statistics['bfs']['time_t'] = statistics['bfs']['time_t'] + (time.time() - start)
            
            
            start = time.time()
            if GT.dfs(DAG, u, v) == True:
                statistics['dfs']['sim'] = statistics['dfs']['sim'] + 1
                statistics['dfs']['time_sim'] = statistics['dfs']['time_sim'] + (time.time() - start)
            else:
                statistics['dfs']['nao'] = statistics['dfs']['nao'] + 1
                statistics['dfs']['time_nao'] = statistics['dfs']['time_nao'] + (time.time() - start)
            statistics['dfs']['time_t'] = statistics['dfs']['time_t'] + (time.time() - start)
            
            contador = contador + 1
        print 'Consultas finalizadas: ' + str(contador)
    
    print 'Busca com BFS estatisticas'
    print "u alcaça v Sim: "+ str(statistics['bfs']['sim']) + ' Tempo médio:' + str(Decimal(statistics['bfs']['time_sim']/statistics['bfs']['sim'])) + ' s'
    print "u alcaça v Não: "+ str(statistics['bfs']['nao']) + ' Tempo médio:' + str(Decimal(statistics['bfs']['time_nao']/statistics['bfs']['nao'])) + ' s'
    print 'Tempo médio por consulta: ' + str(Decimal(statistics['bfs']['time_t']/(statistics['bfs']['sim'] + statistics['bfs']['nao']))) + ' s'
    print 'Tempo total: '+ str(Decimal(statistics['bfs']['time_t'])) + ' s'
    
    print 'Busca com DFS estatisticas'
    print "u alcaça v Sim: "+ str(statistics['dfs']['sim']) + ' Tempo médio:' + str(Decimal(statistics['dfs']['time_sim']/statistics['dfs']['sim'])) + ' s'
    print "u alcaça v Não: "+ str(statistics['dfs']['nao']) + ' Tempo médio:' + str(Decimal(statistics['dfs']['time_nao']/statistics['dfs']['nao'])) + ' s'
    print 'Tempo médio por consulta: ' + str(Decimal(statistics['dfs']['time_t']/(statistics['dfs']['sim'] + statistics['dfs']['nao']))) + ' s'
    print 'Tempo total: '+ str(Decimal(statistics['dfs']['time_t'])) + ' s'