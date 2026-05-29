● Vou guiar você pelo processo de resetar os componentes do Windows Update.



&#x20; Passo 1: Abrir PowerShell como Administrador



&#x20; Clique com botão direito no Menu Iniciar → Windows PowerShell (Admin) ou Terminal (Admin)



&#x20; Passo 2: Execute estes comandos em sequência:



&#x20; # Parar os serviços

&#x20; Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue

&#x20; Stop-Service -Name TrustedInstaller -Force -ErrorAction SilentlyContinue

&#x20; Stop-Service -Name CryptSvc -Force -ErrorAction SilentlyContinue

&#x20; Stop-Service -Name BITS -Force -ErrorAction SilentlyContinue



&#x20; # Limpar a pasta de download do Windows Update

&#x20; Remove-Item -Path "C:\\Windows\\SoftwareDistribution\\Download" -Recurse -Force -ErrorAction SilentlyContinue



&#x20; # Reiniciar os serviços

&#x20; Start-Service -Name wuauserv

&#x20; Start-Service -Name CryptSvc

&#x20; Start-Service -Name BITS



&#x20; Passo 3: Verificar se há reserva de componentes corrompida (erro 0xd000003a)



&#x20; O erro GetUpdateReserveManagerCbs indica problema na reserva do Windows Update. Se os passos acima não resolverem, execute:



&#x20; dism /online /cleanup-image /startcomponentcleanup

