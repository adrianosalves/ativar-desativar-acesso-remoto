# Gerenciador de Acesso Remoto ALVESNET

Software para gerenciar o serviço de suporte remoto A1Agent de forma simples e intuitiva.

![Gerenciar Aceeso Remoto](https://github.com/adrianosalves/ativar-desativar-acesso-remoto/blob/main/images/GerenciarAcessoRemoto.png)

## O que este programa faz?

Este programa permite **ativar** e **desativar** o serviço de suporte remoto (A1Agent) no seu computador com apenas um clique. Ideal para técnicos de suporte que precisam controlar o acesso remoto de forma rápida.

## Funcionalidades

- **Ativar Serviço**: Inicia o serviço de suporte remoto
- **Desativar Serviço**: Para o serviço e desabilita a inicialização automática
- **Visualizar Status**: Verifica se o serviço está em execução ou parado
- **Indicador Visual**: Círculo colorido mostra o status (verde = ativo, vermelho = parado)

## Requisitos

- Windows 10 ou Windows 11
- Permissão de Administrador (necessário para gerenciar serviços)
- Não requer Python instalado (exe compilado)

## Como usar

### Método 1: Executável pronto (Recomendado)

1. Baixe o arquivo `GerenciarAcessoRemoto.exe`
2. Clique com o botão direito → **Executar como Administrador**
3. Clique no botão **[+] ATIVAR** para ativar o suporte remoto
4. Clique no botão **[X] DESATIVAR** para desativar o suporte remoto

### Método 2: Executar via Python

1. Tenha o Python instalado (versão 3.7+)
2. Execute: `python gerenciar_acesso_remoto.py`
3. Execute como Administrador

## Problemas comuns

| Erro | Solução |
|------|---------|
| "Acesso negado" | Execute o programa como Administrador |
| "Serviço não encontrado" | Verifique se o A1Agent está instalado |
| "Serviço já está em execução" | O serviço já está ativo, não precisa ativar |

## Tecnologia usada

- **Linguagem**: Python 3.12
- **Interface Gráfica**: Tkinter (biblioteca padrão Python)
- **Compilação**: PyInstaller (cria o .exe independente)
- **Comandos**: Windows Service Control (sc.exe)

## Arquivos do projeto

```
/
├── gerenciar_acesso_remoto.py   # Código fonte Python
├── GerenciarAcessoRemoto.exe    # Executável compilado
├── ativar_acesso_remoto.bat     # Script antigo (ativo)
├── desativar_acesso_remoto.bat  # Script antigo (desativo)
└── README.md                    # Este arquivo
```

## Como funciona (técnico)

O programa utiliza comandos do Windows para gerenciar o serviço:

```bash
# Ativar serviço
sc config A1Agent start=demand
sc start A1Agent

# Desativar serviço
sc config A1Agent start=disabled
sc stop A1Agent
```

## Autor

ALVESNET Suporte Remoto

---

Dúvidas? Entre em contato com o suporte técnico.
