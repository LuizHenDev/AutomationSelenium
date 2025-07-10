from selenium import webdriver;
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions as EX
from selenium.webdriver import Keys, ActionChains
from time import sleep
'from colorsfont import bcolors'

class AlinharApontamento():
    def Iniciar(self):
        self.AberturaNavegador()
        self.Localizar133()
        self.AdicinarBotaoAlinharApontamento()
        while True:
            sleep(3)
            self.ValorAlinharApontamento = self.driver.execute_script("return window.alinharApontamento")
            while self.ValorAlinharApontamento:
                self.ColetarValoresDosApontamentos()
                self.TratamentoDosHorariosDosApontamentos() 
                if self.horarioFormatado !=None:
                    self.AbrirJanelaDeEdicaoDeApontamento()
                    print("metodo abrir janela de edição efetuado com sucesso")
                    self.AlterarValorDoApontamentoNaJanela026()
                    self.SalvarValorDoApontamento()
                    self.FecharJanelaAjusteDeApontamento()
                break
        pass
    
    def AberturaNavegador(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://sistema.labelgroup.com.br/portal/")
        pass

    def Localizar133(self):
        self.buscandoJanela133 = True
        while self.buscandoJanela133:
            try:
                self.Janela133 = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@id, "ppcp133_r_")]')))
                self.buscandoJanela133 = False
                'bcolors.MensagemSucesso(texto="Janela 133 Localizada")'  
            except EX.TimeoutException:
                print("Janela não carregada, aguardando 5 segundos")
                sleep(5)
        pass
    

    def AdicinarBotaoAlinharApontamento(self):
        self.buscarToolbarlist = True
        ###Loop aguarda o carregamento da class da toolbar da janela 133 
        while self.buscarToolbarlist:
            try:
                self.Toolbars= WebDriverWait(self.Janela133, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME,'window-toolbar')))
                self.buscarToolbarlist = False
            except EX.TimeoutException:
                print("localizando a toolbar, aguardando 5s")
                sleep(5)
        self.Ulbars = self.Toolbars.find_element(By.CLASS_NAME,"toolbars-list-content")
        self.NavbarResolution = self.Toolbars.find_element(By.CLASS_NAME,"fixed-toolbar")
        self.Ulbars = self.Ulbars.find_element(By.TAG_NAME,"ul")
        ###Script para editar o HTML e inserir o botão de alinhar apontamento
        self.driver.execute_script("" \
        "window.alinharApontamento = false;" \
        "let li = document.createElement('li');" \
        "li.title='Alinhar Apontamento';" \
        "let botaoAlinhar = document.createElement('button');" \
        "arguments[0].style.width='750px';" \
        "botaoAlinhar.className= 'undefined';" \
        "botaoAlinhar.addEventListener('click', () => { window.alinharApontamento = !window.alinharApontamento;botaoAlinhar.style.color = (window.alinharApontamento) ? 'purple' : 'grey';});" \
        "let i = document.createElement('i');" \
        "i.className='fa fa-rocket';" \
        "botaoAlinhar.appendChild(i);" \
        "li.appendChild(botaoAlinhar);" \
        "arguments[1].appendChild(li);", self.NavbarResolution,self.Ulbars)
        pass
    def ColetarValoresDosApontamentos(self):
        ###Adicionar a verificação se é uma parada
        self.ApontamentoInicial = self.driver.find_element(By.XPATH,"//input[contains(@id, 'apontamentosDataHoraFim-20')]")
        ###Adicionar o click no botão para descer a lista de apontamento
        self.ApontamentoInicial = self.ApontamentoInicial.get_attribute("value")
        self.BotaoScrollParaBaixo = self.Janela133.find_element(By.XPATH," //*[contains(@id,'apontamentosBarraRolagem')]/div[5]/span")
        self.BotaoScrollParaBaixo.click()
        sleep(3)
        self.ApontamentoFinal = self.driver.find_element(By.XPATH,"//input[contains(@id, 'apontamentosDataHoraIni-20')]")
        self.ApontamentoFinal=self.ApontamentoFinal.get_attribute("value")
        print("---------------------------------------")
        print(f"Apontamento Inicial: {self.ApontamentoInicial}")
        print(f"Apontamento Final: {self.ApontamentoFinal}")
        print("---------------------------------------")
        pass
        
    def TratamentoDosHorariosDosApontamentos(self):
       ##Fazer ele retornar o valor corrigido
        sleep(5)
        self.dataFormatada = None
        self.horarioFormatado = None
        ###Fatiação do valor do apontamento final#####
        self.ApontamentoFinalPartes= self.ApontamentoFinal.split("/")
        self.diaFinal, self.mesFinal, self.anoETempoFinal = self.ApontamentoFinalPartes
        self.diaFinal = int(self.diaFinal)
        self.anoFinal = self.anoETempoFinal.split()[0]
        self.tempoFinal = self.anoETempoFinal.split()[-1]
        self.horaFinal = int(self.tempoFinal.split(":")[0])
        self.minutoFinal = int(self.tempoFinal.split(":")[-1])

        ###Fatiação do valor do apontamento inicial
        self.ApontamentoInicialPartes= self.ApontamentoInicial.split("/")
        self.diaInicial, self.mesInicial, self.anoETempoInicial = self.ApontamentoInicialPartes
        self.diaInicial = int(self.diaInicial) 
        self.anoInicial = self.anoETempoInicial.split()[0]
        self.tempoInicial = self.anoETempoInicial.split()[-1]
        self.horaInicial = int(self.tempoInicial.split(":")[0])
        self.minutoInicial = int(self.tempoInicial.split(":")[-1])
        
        ####Tratamento de dados####

        ###Caso o apontamento inicial seja igual o apontamento final; 
        
        if self.ApontamentoInicial == self.ApontamentoFinal:
                        print("Tempos iguais, coletando o valor do proximo apontamento")
                        sleep(2)
                        self.ApontamentoInicial = self.driver.find_element(By.XPATH,"//input[contains(@id, 'apontamentosDataHoraFim-20')]")
                        self.ApontamentoInicial = self.ApontamentoInicial.get_attribute("value")
                        sleep(1)
                        self.ApontamentoInicialPartes= self.ApontamentoInicial.split("/")
                        self.diaInicial, self.mesInicial, self.anoETempoInicial= self.ApontamentoInicialPartes
                        self.diaInicial = int(self.diaInicial)
                        self.anoInicial = self.anoETempoInicial.split()[0]
                        self.tempoInicial = self.anoETempoInicial.split()[-1]
                        self.horaInicial = int(self.tempoInicial.split(":")[0])
                        self.minutoInicial = int(self.tempoInicial.split(":")[-1])
                        print("---------------------------------------")
                        print(f"Apontamento Inicial: {self.ApontamentoInicial}")
                        print(f"Apontamento Final: {self.ApontamentoFinal}")
                        print("---------------------------------------")

                        if self.ApontamentoInicial != self.ApontamentoFinal:
                        
                            
                            """Dias iguais com alteração"""
                            if self.diaFinal == self.diaInicial and self.minutoFinal !=59:
                                print(f"O tempo está sobreposto, mas com possível alteração")
                                self.minutoFinal = self.minutoFinal+1
                                self.horarioFormatado = f"{self.horaFinal:02d}:{self.minutoFinal:02d}"
                                
                                """Dias iguais com alteração e mudança de horario"""
                            elif self.minutoFinal == 59:


                                if self.horaFinal <23:
                                    print(f"Mudança de horario")
                                    self.minutoFinal = 0
                                    self.horaFinal = self.horaFinal+1
                                    self.horarioFormatado = f"{self.horaFinal:02d}:{self.minutoFinal:02d}"
                                    
                                else: 
                                    ###Realizar ajuste
                                    print("tempo sobrepostos, com mudança de datas(Caso o minuto final seja 59)")
                                    self.minutoFinal = 0
                                    self.horaFinal= 0
                                    self.diaFinal= self.diaFinal+1
                                    self.horarioFormatado = f"{self.horaFinal:02d}:{self.minutoFinal:02d}"
                                    self.dataFormatada = f"{self.diaFinal:02d}/{self.mesFinal}/{self.anoFinal}"

                                """Mudança de dias"""
                            elif self.diaFinal != self.diaInicial:
                                print("Mudança de horario sobreposto, com permanencia do dia anterior")
                                self.minutoFinal = self.minutoFinal+1
                                self.horarioFormatado = f"{self.horaFinal:02d}:{self.minutoFinal:02d}"
                            else:
                                print("Sem possível alteração")

        elif self.minutoFinal != (self.minutoInicial+1) and self.diaFinal == self.diaInicial:
        
                        if self.minutoInicial <59:
                            print("-------Tempos diferentes-------")
                            self.minutoInicial = self.minutoInicial+1
                            self.horarioFormatado = f"{self.horaInicial:02d}:{self.minutoInicial:02d}"
                        else:
                            print("-------Tempo com adicional de hora------- ")
                            if self.horaInicial < 23:
                                if self.horaInicial+1 != self.horaFinal:
                                    self.minutoInicial= 0
                                    self.horaInicial=self.horaInicial+1
                                    self.horarioFormatado = f"{self.horaInicial:02d}:{self.minutoInicial:02d}"
                                    self.horarioFormatado
                                if self.horaInicial+1 == self.horaFinal and self.minutoFinal != 0:
                                    self.minutoInicial= 0
                                    self.horaInicial=self.horaInicial+1
                                    self.horarioFormatado = f"{self.horaInicial:02d}:{self.minutoInicial:02d}"
                                    self.horarioFormatado


        ###Dias diferentes 
        elif self.diaInicial != self.diaFinal:
                        ### Permanencia de horario
                        if self.minutoInicial <59:

                            print("Mudança de horario, permanecendo o horario anterio") 
                            self.minutoInicial = self.minutoInicial+1
                            self.horarioFormatado = f"{self.horaInicial:02d}:{self.minutoInicial:02d}"
                            self.dataFormatada = f"{self.diaInicial:02d}/{self.mesInicial}/{self.anoInicial}"
                            ###Adicionar Mudança de dia


                        ###Mudança de hora
                        elif self.minutoInicial==59:
                            
                            
                            if self.horaInicial < 23:
                                    
                                    self.minutoInicial= 0
                                    self.horaInicial=self.horaInicial+1
                                    self.horarioFormatado = f"{self.horaInicial:02d}:{self.minutoInicial:02d}"
                                    self.dataFormatada = f"{self.diaInicial:02d}/{self.mesInicial}/{self.anoInicial}"
                                    ###Adicionar Mudança de dia
                            
                            elif self.horaInicial ==23:

                                    self.minutoInicial = 0
                                    self.horaInicial= 0
                                    self.diaInicial= self.diaInicial+1
                                    self.horarioFormatado = f"{self.horaInicial:02d}:{self.minutoInicial:02d}"
                                    self.dataFormatadao = f"{self.diaInicial:02d}/{self.mesInicial}/{self.anoInicial}"
                                    ###Adicionar mudança de dia)    


        pass

    def AbrirJanelaDeEdicaoDeApontamento(self):
        
        self.botaoAbrirJanelaEdicao = self.driver.find_element(By.XPATH,"//button[contains(@id, 'apontamentosBotaoEditarRegistro-20')]")
        self.botaoAbrirJanelaEdicao.click()
        self.carregandoJanela026 = True
        while self.carregandoJanela026:
            try:
                self.janelaPcp026 = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH,"//div[contains(@id, 'ppcp026_r_')]")))
                self.carregandoJanela026 = False
                print('Janela 026, carregada com sucesso.')
            except EX.TimeoutException:
                    print("Janela não carregada, aguardando 5s")
                    sleep(5)  
        sleep(2)
        pass

    def AlterarValorDoApontamentoNaJanela026(self):
        self.carregandoJanela026 = True
        while self.carregandoJanela026:
             try:
                 self.valorInputDaJanela026 = WebDriverWait(self.driver, 5).until(
                 EC.presence_of_element_located((By.XPATH,"//input[contains(@id, 'pcpapproducaoDataHoraIni-0')]")))
                 self.carregandoJanela026= False
                 print("Janela carregada com sucesso")
             except EX.TimeoutException:
                  print("Esperando a janela 026 carregar por completo")                                                      
        self.valorInputDaJanela026.clear()
        sleep(2)
        #Adicionar o metodo TratamentoDosHorariosDosApontamentos dentro do send_keys
        self.valorInputDaJanela026.send_keys(self.horarioFormatado)
        sleep(2)
        self.driver.execute_script('' \
        'arguments[0].dispatchEvent(new Event("change",{ bubbles:true })); ' \
        'arguments[0].dispatchEvent(new Event("input",{ bubbles:true }))',self.valorInputDaJanela026)
        print("Valor alterado com sucesso")
        pass

    def SalvarValorDoApontamento(self):
        self.botaoSalvar = self.janelaPcp026.find_element(By.XPATH,"//div[contains(@id, 'ppcp026_r')]//button[contains(@class,'save')]")
        self.botaoSalvar.click()
        print('Valores salvos com sucesso')
        sleep(5)
        pass
    
    def FecharJanelaAjusteDeApontamento(self):
        ##Adicionar o click no botão de fechar      
        self.BotaoFechar = self.driver.find_element(By.XPATH,"//div[contains(@id, 'ppcp026_r')]//div[contains(@class,'buttons-header')]/span[2]")
        self.BotaoFechar.click()
        sleep(2)
        self.FechandoJanela026 = True
        while self.FechandoJanela026:
             self.ValorClasses133 = self.Janela133.find_element(By.XPATH, '//div[contains(@id, "janelaPrincipal")]')
             self.ValorClasses133 = self.ValorClasses133.get_attribute("class")
             self.ValorClasses133 = self.ValorClasses133.split()
             if len(self.ValorClasses133) != 1:
                  print("Esperando a janela 026 fechar")
                  sleep(5)
             else: 
                  print("Janela 026 fechada com sucesso")
                  self.FechandoJanela026 = False

    
        ###Fazer ele procurar pela classe waitingReponseLazy
        pass
        
iniciar = AlinharApontamento()
iniciar.Iniciar()
