import matplotlib.pyplot as plt
import numpy as np

#T1
class Vehicle:
    def __init__(self, matricula, tipo, marca, modelo, proprietario, ano_registo):
        self.__matricula = matricula
        self.__tipo = tipo.lower()
        self.__marca = marca
        self.__modelo = modelo
        self.proprietario = proprietario
        self.__ano_registo = ano_registo
    
#obter o valor de cada atributo
    @property
    def matricula(self):
        return self.__matricula
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def marca(self):
        return self.__marca
    
    @property
    def modelo(self):
        return self.__modelo
    
    @property
    def ano_registo(self):
        return self.__ano_registo
    
    def alterar_proprietario(self, novo_proprietario):
        self.proprietario = novo_proprietario

#converter o veiculo numa cadeia de caracteres
    def __str__(self):
        return (f'{self.__matricula}, {self.__tipo}, {self.__marca}, {self.__modelo}, {self.proprietario}, {self.__ano_registo}')

#comparar veiculos
    def __eq__(self, other):
        if isinstance (other, Vehicle):
            return self.__matricula == other.__matricula
        else:
            return False
    
v = Vehicle ('ZZ-99-ZZ', 'ligeiro', 'Seat', 'Ibiza', 'Zé', 2020)
b = Vehicle('ZZ-98-ZZ', 'ligeiro', 'Seat', 'Ibiza', 'Zé', 2020)
#print(v == b)

#T2
def ler_veiculos(ficheiro):
    registo_veiculos = {}
    try:
        with open(ficheiro, 'r') as f:
            for linha in f:
                matricula, tipo, marca, modelo, proprietario, ano_registo = linha.strip().split(',')
                veiculo = Vehicle(matricula, tipo, marca, modelo, proprietario, int(ano_registo))
                registo_veiculos[matricula] = veiculo #chave matricula
        f.close()
    except FileNotFoundError:
        print('Ficheiro não encontrado!')
    return registo_veiculos

#T3

class Park:
    def __init__(self, nome_parque, localizacao, lotacao, privado=False): #atributos fixos do parque
        #atributos fixos do parque
        self.__nome_parque = nome_parque
        self.__localizacao = localizacao #(latitude, longitude)
        self.__lotacao = lotacao
        self.__privado = privado
        
        #estado inicial do parque
        self.__veiculos_estacionados = {} # lista de matriculas estacionadas
        self.__matriculas_permitidas = ["LO-23-QS"] if privado else None #lista de matriculas permitidas se parque privado


#metodos para obter o valor de cada atributo
    @property
    def nome_parque(self):
        return self.__nome_parque
    
    @property
    def localizacao(self):
        return self.__localizacao
    
    @property
    def lotacao(self):
        return self.__lotacao
    
    @property
    def privado(self):
        return self.__privado
    
    @property
    def veiculos_estacionados(self):
        return self.__veiculos_estacionados
    @property
    def matriculas_permitidas(self):
        return self.__matriculas_permitidas
    
    @property
    def registo_veiculos(self):
        return self.__registo_veiculos

                
# registar entrada e saida de um veiculo do parque

    def entrada_veiculo(self, registo_veiculos):
        matricula = input('Matrícula: ').strip()
        if matricula not in registo_veiculos:
            print("O veículo não existe")
            return
        veiculo = registo_veiculos[matricula]
        if len(self.__veiculos_estacionados) >= self.__lotacao:
            print("Parque cheio!")
            return
        elif self.__privado and matricula not in self.__matriculas_permitidas:
            print ("O veículo não tem permissão para entrar no parque!")
            return
        elif matricula in self.__veiculos_estacionados:
            print ("O veículo já está estacionado no parque.")
            return
        elif veiculo.tipo == 'pesado':
            print ("Não são permitidos veículos pesados.")
            return
        else:
            self.__veiculos_estacionados[matricula] =veiculo
            print (f'Veículo com matrícula {matricula} entrou no parque.')
    
    def saida_veiculo(self):
        matricula = input('Matrícula: ').strip()
        if matricula in self.__veiculos_estacionados:
            self.__veiculos_estacionados.pop(matricula)
            print (f'Veículo com matrícula {matricula} saiu do parque.')
        else:
            print ("O veículo não está estacionado no parque")
        
    
#Verificar se um veiculo está no parque
    def veiculo_estacionado(self,matricula):
        if matricula in self.__veiculos_estacionados:
            return True
        else:
            return False

#Listar veiculos estacionados
    def listar_veiculos(self):
        if not self.__veiculos_estacionados:
            return("O parque está vazio!")
        print("___ Veículos Estacionados ___")
        for matricula, veiculo in self.__veiculos_estacionados.items():
            print(f'{matricula}: {veiculo}')
    
#numero de lugares ocupados e livres
    def lugares_ocupados(self):
        return len(self.__veiculos_estacionados)
    
    def lugares_livres(self):
        return self.__lotacao - len(self.__veiculos_estacionados)
    
#metodos para o parque privado
    def permitir_acesso(self):
        matricula = input("Matrícula: ").strip()
        if not self.__privado:         #se parque nao é privado
            print ("Parque público")
        elif matricula not in self.__matriculas_permitidas:
            self.__matriculas_permitidas.append(matricula)
            print (f"Acesso permitido {matricula}.")
        else:
            print (f"A matrícula {matricula} já tem acesso.")
    
    def revogar_acesso(self):
        matricula = input("Matrícula: ").strip()
        if not self.__privado:
            print ("Parque público.")
        elif matricula in self.__matriculas_permitidas:
            self.__matriculas_permitidas.remove(matricula)
            print (f"Acesso revogado {matricula}")
        else:   
            print ("A matrícula não está na ista de acesso.")
            
    def listar_permissoes(self):
        if not self.__matriculas_permitidas:
            print ("Nenhuma permissão concedida.")
        else:
            print ("Permissões atuais:")
            for matricula in self.__matriculas_permitidas:
                print(f' - {matricula}')

#representação textual do parque           
    
    def __str__(self):
        tipo_parque = "Privado" if self.__privado else "Público"
        ocupacao = self.lugares_ocupados()
        return f"{self.__nome_parque}; ({self.__localizacao[0]}, {self.__localizacao[1]}); {tipo_parque}; {ocupacao}/{self.__lotacao}"

    def exportar_estado(self):
        nome_ficheiro = input("Ficheiro: ").strip()
        try:
            with open(nome_ficheiro, 'w') as f:
                f.write(str(self) + '\n') #respresentaçao textual do parque
                f.write("Veículos estacionados:\n")
                for veiculo in self.__veiculos_estacionados.values():
                    f.write(f'{veiculo}\n') #usar str do veiculo
            print (f'Exportado para {nome_ficheiro}.')
        except Exception as e:
            print (f'Erro ao exportar: {e}')

            
class GestaoPark:
    def __init__(self):
        self.parques_existentes = [] #lista para parques

#Criar parque 3
    def criar_parque(self):
        while True:
            nome_parque = input('Nome do parque: ').strip()
            for parque in self.parques_existentes:
                if parque.nome_parque == nome_parque:
                    print ('Já existe um parque com esse nome')
                    return
            else:
                break
        while True:
            try:
                localizacao = input('Localização do parque (latitude, longitude): ')
                coordenadas = localizacao.split(',')
                latitude = float(coordenadas[0].strip())
                longitude = float(coordenadas[1].strip())
                if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                    break
                else:
                    print ('Coordenadas inválidas: latitude deve estar entre -90 e 90 e longitude entre -180 e 180')
            except (ValueError, IndexError):
                print ('Formato inválido! Introduza a localização: ')
        while True:
            try:
                lotacao = int(input('Lotação do parque: '))
                if lotacao < 1:
                    int(input('Introduza número inteiro positivo: '))
                break
            except ValueError:
                print ('Capacidade inválida\n Insira um número inteiro: ')
        while True:
            tipo = input('O parque é privado? (S/N): ').strip().upper()
            if tipo == 'S':
                privado = True
                break
            elif tipo == 'N':
                privado = False
                break
            else:
                print ('Opção inválida!\n O parque é privado? (S/N): ')
        
        parque = Park(nome_parque, (latitude, longitude), lotacao, privado)
        self.parques_existentes.append(parque)
        print ('Parque adicionado!')
       
            
#listar parques 1
    def listar_parque(self):
        print ("=== Lista de Parques ===")
        for parque in self.parques_existentes:
            print(parque)
    

#Remover parque 4
    def remover_parque(self):
        if not self.parques_existentes:
            print("Não existem parques registados")
            return
        nome_parque = input('Nome do parque: ').strip()
        for parque in self.parques_existentes:
            if parque.nome_parque == nome_parque:
                self.parques_existentes.remove(parque)
                print (f'Parque {nome_parque} removido com sucesso!')
                return
        print ('Não existe um parque com esse nome.')
                             

#Gerir parque 2
    
    def gerir_parque(self, registo_veiculos):
        nome_parque = input('Nome do parque: ').strip()
        for parque in self.parques_existentes:
            if str(parque.nome_parque) == nome_parque:
                self.menu_gestao_parque(parque,registo_veiculos)
                return
        print ('Não existe um parque com esse nome.')

#T5 menu de gestao de parque
    def menu_gestao_parque(self,parque,registo_veiculos):
        print (f'\n*** Gestão do Parque {parque.nome_parque} ***')
        print ('1. Registar entrada')
        print ('2. Registar saída')
        print ('3. Listar veículos')
        print ('4. Exportar estado')
        if parque.privado: #apenas para parques privados
            print ('5. Listar permissões')
            print ('6. Permitir acesso')
            print ('7. Revogar acesso')
        print ('0. Voltar')
        while True:
            opcao = input('Escolhe uma opção: ')
            if opcao == '0':
                menu_principal(self)
                break
            if opcao == '1':
                parque.entrada_veiculo(registo_veiculos)
            elif opcao == '2':
                parque.saida_veiculo()
            elif opcao == '3':
                parque.listar_veiculos()
            elif opcao == '4':
                parque.exportar_estado()
            elif parque.privado and opcao == '5':
                parque.listar_permissoes()
            elif parque.privado and opcao == '6':
                parque.permitir_acesso()
            elif parque.privado and opcao == '7':
                parque.revogar_acesso()
            else:
                print("Opção inválida! Insira um número.")
                

#estatistica 5
    def numero_lugares_livres(self):
        total_lugares_livres = sum(parque.lugares_livres()for parque in self.parques_existentes)
        print(f'Número total de lugares livres: {total_lugares_livres}.')
        
    def taxa_ocupacao_media(self):
        total_ocupados = sum(parque.lugares_ocupados() for parque in self.parques_existentes)
        total_lotacao = sum(parque.lotacao for parque in self.parques_existentes)
        if total_lotacao >0:
            taxa_media= (total_ocupados/total_lotacao) * 100
            print(f'Taxa de ocupação média é {taxa_media:.2f}')
        else:
            print("Nenhum parque registado.")
            
    def numero_parques_privados(self):
        total_parques=len(self.parques_existentes)
        parques_privados= sum(1 for parque in self.parques_existentes if parque.privado)
        if total_parques > 0:
            percentagem_privados = (parques_privados/total_parques) *100
            print(f'Número de parques privados {parques_privados} ({percentagem_privados:.2f})%')
        else:
            print("Não existem parques privados registados.")

    def veiculos_por_ano_registo(self,registo_veiculos):
        anos =[]
        for parque in self.parques_existentes:
            for matricula in parque.veiculos_estacionados:
                veiculo = registo_veiculos.get(matricula)
                if veiculo:
                    anos.append(veiculo.ano_registo)
        if not anos:
            print("Nenhum veiculo estacionados nos parques.")
            return
        contagem_anos = {}
        for ano in anos:
            if ano in contagem_anos:
                contagem_anos[ano] += 1
            else:
                contagem_anos[ano] = 1
        print(f"Veículos por ano de registo:")
        for ano_registo, quantidade in sorted(contagem_anos.items()): #sorted ordena os pares, enquanto contagem_anos.items devolve uma lista de pares a partir do dicionario
            print(f'Ano {ano_registo}: {quantidade} veículo(s)')
        plt.bar(contagem_anos.keys(), contagem_anos.values(), color='blue')
        plt.xlabel("Ano de Registo")
        plt.ylabel("Número de Veículos")
        plt.title("Veículos por Ano de Registo")
        plt.show()
    
    def visualizar_mapa_parques(self):
        if not self.parques_existentes:
            print("Não existem parques registados.")
            return
        
        fig, ax = plt.subplots(figsize=(12,8)) #configurar a figura e eixos
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Mapa dos Parques")
        ax.set_aspect('equal') #para garantir q os eixos tem proporçao igual
        
        #definir limites dos eixos com base na localização dos parques
        ax.set_xlim(-200,200)
        ax.set_ylim(-100,100)
        
        #adicionar circulos dos parques
        for parque in self.parques_existentes:
            latitude, longitude = parque.localizacao
            lotacao = parque.lotacao
            ocupacao = parque.lugares_ocupados()
            taxa_ocupacao = ocupacao/lotacao if lotacao > 0 else 0
            if taxa_ocupacao < 0.75: #definir cor
                cor = 'green'
            elif taxa_ocupacao < 1:
                cor = 'yellow'
            else:
                cor = 'red'
            raio = 5*np.log10(lotacao)  #raio usando logaritmo para escala
            circle = plt.Circle((longitude,latitude),raio,color=cor, alpha=0.5)
            ax.add_patch(circle)
            ax.text(longitude,latitude,parque.nome_parque, fontsize=9, ha='center')
        ax.grid(True)
        plt.show()
           
    
    def estatistica(self, registo_veiculos):
        print("\n*** Estatística e Informações ***")
        print('1. Número total de lugares livres')
        print('2. Taxa de ocupação média')
        print('3. Número de parques privados')
        print('4. Veículos por ano de registo')
        print('5. Visualizar mapa de parques')
        print('0. Voltar')
        while True:
            opcao = input('Escolhe uma opção: ').strip()
            if opcao == '0':
                menu_principal(self)
                break
            elif opcao == '1':
                self.numero_lugares_livres()
            elif opcao == '2':
                self.taxa_ocupacao_media()
            elif opcao == '3':
                self.numero_parques_privados()
            elif opcao == '4':
                self.veiculos_por_ano_registo(registo_veiculos)
            elif opcao == '5':
                self.visualizar_mapa_parques()
            else:
                print("Opção inválida. Insira um número.")

        
def menu_principal(gestao):
    registo_veiculos = ler_veiculos("lista_veiculos.txt")
    while True: #iniciar loop aqui
        print ("\n*** Menu Principal ***")
        print ('1. Listar Parques')
        print ('2. Gerir Parques')
        print ('3. Criar Parque')
        print ('4. Remover Parque')
        print ('5. Estatística e Informações')
        print ('0. Sair')
        opcao = input('Escolhe uma opção: ').strip()
        if opcao == '0':
            break
        elif opcao == '1':
            gestao.listar_parque()
        elif opcao == '2':
            gestao.gerir_parque(registo_veiculos)
        elif opcao == '3':
            gestao.criar_parque()
        elif opcao == '4':
            gestao.remover_parque()
        elif opcao =='5':
            gestao.estatistica(registo_veiculos)
        else: print("Opção inválida. Insira um número.")
        
gestao = GestaoPark()
menu_principal(gestao)
        

