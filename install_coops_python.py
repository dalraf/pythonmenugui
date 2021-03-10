#!/usr/bin/env python
import PySimpleGUI as sg
import subprocess
import requests
import os
import shutil
import zipfile

varprogramasinstall = 'programasinstall'
varspark = 'spark'
varsisbrinstall = 'sisbrinstall'
varcitrixinstall = 'citrixinstall'
varcitrixcleanup = 'citrixcleanup'
varsicoobnetinstall = 'sicoobnetinstall'
varadicionarodominio = 'adicionaraodominio'
varlimpezageral = 'limpezageral'
varlimpezageral = 'limpezageral'
varreniciar = 'varreiniciar'
vardiretorioarcom = 'diretorioarcom'
vardominio = 'dominio'
varusuario = 'usuario'
varsenha = 'senha'

diretorioarcomdefault = "c:\\Arcom"
chocolateypath = "c:\\ProgramData\\chocolatey\choco.exe"

filestringspark= """passwordSaved=true
server=arcompbx.gotdns.com
hostAndPort=false
DisableHostnameVerification=true
"""

programas = {
            "Adobe Reader":"adobereader",
            "Adobe Air": "adobeair",
            "Java" : "javaruntime --x86SteamSteam",
            "Spark": "spark",
            "Teamviewer": "teamviewer",
            "Anydesk": "anydesk.install",
            "Google Chrome": "googlechrome" ,
            "Firefox": "firefox"
            }

#Alterar campos do domínio
def mudarestadocamposdominio(window,estado):
    window['dominio'].update(disabled = not estado)
    window['usuario'].update(disabled = not estado)
    window['senha'].update(disabled = not estado)
    pass

#Função para adicionar no domínio
def addtodomain(dominio,usuario,senha):
    subprocess.call(f'@"%SystemRoot%\System32\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command \"$domain = "{dominio}"; $password = "{senha}" | ConvertTo-SecureString -asPlainText -Force; $username = \'{usuario}@$domain\';$credential = New-Object System.Management.Automation.PSCredential($username,$password);Add-Computer -DomainName $domain -Credential $credential\"', shell=True)
 
#Configura spark
def configurespark():
    appdata = os.getenv('APPDATA')
    if not os.path.exists(appdata + '\\Spark'):
        os.mkdir(appdata + '\\Spark')
    filesparkconf = appdata + '\\Spark\\spark.properties'
    with open(filesparkconf, "w") as sparkconf:
        sparkconf.write(filestringspark)
    sparkconf.close()


#Executa instalacao de programas
def installprograma(diretorioarcom, programa):
    if not os.path.isfile(chocolateypath):
        print("Executando chocolatey")
        subprocess.call('@"%SystemRoot%\System32\WindowsPowerShell\\v1.0\\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"', shell=True)
    subprocess.call(chocolateypath + " config set cacheLocation " + diretorioarcom, shell=True)
    subprocess.call(chocolateypath + " install -y " + programa, shell=True)

def criardiretorio(diretorio):
    if not os.path.exists(diretorio):
        os.mkdir(diretorio)    

#Cria Diretorio Arcom
def createdirarcom(diretorioarcom):
    criardiretorio(diretorioarcom)

#Baixa arquivos do google drives
def download_file_from_google_drive(id, destination):
    
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


#Função que é executada de acordo com o retorno do valor do GUI
def executarscripts(values):

    diretorioarcom = values[vardiretorioarcom]

    for descricao, comando in programas.items():
        if values[comando]:
            print("Instalando " + descricao )
            installprograma(diretorioarcom,comando)
    
    if values[varprogramasinstall]:
        print("Executando instalacao de todos os programas")
        for descricao, comando in programas.items():
                installprograma(diretorioarcom,comando)

    if values[varspark]:
        configurespark()
    
    if values[varsisbrinstall]:
        createdirarcom(diretorioarcom)
        print("Baixando sisbr 2.0")
        if not os.path.isfile(diretorioarcom + "\\sisbr2.0.exe"):
            file_id = '13E-X5fZZrj2FMZDIcLWJ94c9DgTqUA3f'
            destination = diretorioarcom + '\\sisbr2.0.exe'
            download_file_from_google_drive(file_id, destination)
            print("Download finalizado")
        print("Executando instalacao")
        subprocess.call(diretorioarcom + "\\sisbr2.0.exe")

    if values[varcitrixinstall]:
        createdirarcom(diretorioarcom)
        diretoriocitrix = diretorioarcom + "\\Citrix"
        criardiretorio(diretoriocitrix)
        print("Baixando citrix 10")
        if not os.path.isfile(diretorioarcom + "\\Citrix10.zip"):
            file_id = '19o1eGqGL6xR1B9b3VYunea4zzYe3Heb9'
            destination = diretorioarcom + '\\Citrix10.zip'
            download_file_from_google_drive(file_id, destination)
            print("Download finalizado")
        print("Executando descompacação")
        with zipfile.ZipFile(diretorioarcom + '\\Citrix10.zip', 'r') as citrixzip:
            citrixzip.extractall(diretoriocitrix)
        subprocess.call('msiexec /i "' + diretoriocitrix + '\\Citrix10\\Versao 10.1\\PN_10_1.msi"')
    
    if values[varcitrixcleanup]:
        print("Removendo registro")
        subprocess.call("reg delete HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\MSLicensing /f")
    
    if values[varsicoobnetinstall]:
        createdirarcom(diretorioarcom)
        if not os.path.isfile(diretorioarcom + "\\instalador-sicoobnet-windows-amd64.exe"):
            print("Baixando Sicoobnet Empresarial")
            urlsicoobnet = "https://office-sicoob-instalador.s3-us-west-2.amazonaws.com/instalador-sicoobnet-windows-amd64.exe"
            download = requests.get(urlsicoobnet, allow_redirects=True)
            open(diretorioarcom + "\\instalador-sicoobnet-windows-amd64.exe", 'wb').write(download.content)
        subprocess.call(diretorioarcom + "\\instalador-sicoobnet-windows-amd64.exe")
    
    if values[varadicionarodominio]:
        addtodomain(values[vardominio],values[varusuario],values[varsenha])
    
    if values[varlimpezageral]:
        if os.path.exists(diretorioarcom):
            shutil.rmtree(diretorioarcom)

    if values[varreniciar]:
        subprocess.call("shutdown /t0 /r")


#Funcao que gera o a GUI
def Menu():
    sg.theme('LightBlue')
    sg.SetOptions(text_justification='right')
    listainstalacao = []

    for descricao, comando in programas.items():
        listainstalacao.append([sg.Checkbox('Instalar ' + descricao, key=comando, size=(24, 1))])


    instalacao = [
            [sg.Checkbox('Instalar programas padrão', key=varprogramasinstall, size=(24, 1))],
            [sg.Checkbox('Instalar Sisbr 2.0', key=varsisbrinstall, size=(24, 1))],
            [sg.Checkbox('Instalar Citrix 10', key=varcitrixinstall, size=(24, 1))],
            [sg.Checkbox('Instalar SicoobNet empresarial', key=varsicoobnetinstall, size=(24, 1))],
            ]
    dominio = [
            [sg.Checkbox('Adicionar ao domínio', key=varadicionarodominio, size=(24, 1), enable_events=True)],
            [sg.Text('Domínio: '),sg.Input('',key=vardominio, background_color = 'white', border_width = 1, justification='left', size=(12, 1) , disabled=True)],
            [sg.Text('Usuário:  '),sg.Input('',key=varusuario, background_color = 'white', border_width = 1, justification='left', size=(12, 1), disabled=True)],
            [sg.Text('Senha:    '),sg.Input('',key=varsenha, password_char='*', background_color = 'white', border_width = 1, justification='left', size=(12, 1), disabled=True)],
            ]
    configuracao = [
            [sg.Text('Diretório Arcom:'),sg.Input(diretorioarcomdefault,key=vardiretorioarcom, background_color = 'white', border_width = 1, justification='left', size=(12, 1))],
            [sg.Checkbox('Remover registro do Citrix', key=varcitrixcleanup, size=(24, 1))],
            [sg.Checkbox('Limpeza do diretório Arcom', key=varlimpezageral, size=(24, 1))],
            [sg.Checkbox('Reniciar cpu após execuçào', key=varreniciar, size=(24, 1))],
            [sg.Frame('Domínio:', dominio , font='Any 12', title_color='black')],
             ]

    layout = [[sg.Frame('Instalação:', listainstalacao + instalacao , font='Any 12', title_color='black'),sg.Frame('Configuração:',configuracao , font='Any 12', title_color='black')]
              ,[sg.Button('Executar'), sg.Button('Cancelar')]]

    window = sg.Window('Arcom Install', font=("Helvetica", 12)).Layout(layout)

    while True:
        event, values = window.read()

        if event == 'adicionaraodominio':
            mudarestadocamposdominio(window,values['adicionaraodominio'])

        if event == 'Executar':
            executarscripts(values)

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
    
    window.close()

if __name__ == '__main__':
    Menu()
