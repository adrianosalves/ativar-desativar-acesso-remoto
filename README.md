# desativar-acesso-remoto.ps1

# Configura o Serviço do A1Agent service para "Desativado"
sc.exe config A1Agent start=disabled

# Mostrar o status do serviço
sc.exe query A1Agent

# Para o serviço, no de estar em execução
sc.exe stop A1Agent

# Mostra o status novamente, so para garantir
sc.exe query A1Agent

# verifique se está REALMENTE desativado - o valor inicial deve ser 0x4
REG.exe QUERY HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\A1Agent /v Start 
