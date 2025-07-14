# Usando o DeepDiff MCP com Clientes FastMCP

## Configuração Correta do Cliente

Ao usar o DeepDiff MCP com clientes FastMCP, existem algumas formas de configurar corretamente a conexão:

### Método 1: Usando Transporte Explícito (Recomendado)

```python
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

# Opção 1: Usando o pacote instalado
transport = StdioTransport(command="deepdiff-mcp")

# Opção 2: Usando um script Python
transport = StdioTransport(command="python", args=["caminho/para/servidor.py"])

# Crie o cliente com o transporte explícito
async with Client(transport=transport) as client:
    # Use o cliente normalmente
    result = await client.call_tool("compare", {"t1": {"a": 1}, "t2": {"a": 2}})
```

### Método 2: Usando Configuração MCP Padrão

```python
from fastmcp import Client

# Configuração padrão MCP
config = {
    "mcpServers": {
        "deepdiff": {
            "command": "deepdiff-mcp"
        }
    }
}

# Crie o cliente usando a configuração
client = Client(config)

async with client:
    # Use o cliente com prefixo do servidor
    result = await client.call_tool("deepdiff_compare", {"t1": {"a": 1}, "t2": {"a": 2}})
```

## Exemplos de Comparação de Arquivos

### Exemplo Básico

```python
import asyncio
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

async def main():
    transport = StdioTransport(command="deepdiff-mcp")
    async with Client(transport=transport) as client:
        result = await client.call_tool(
            "compare_files", 
            {
                "file1_path": "dados1.csv", 
                "file2_path": "dados2.csv",
                "ignore_order": True
            }
        )
        print(result.text)

asyncio.run(main())
```

### Uso da Linha de Comando

Para facilitar o uso, incluímos o script `simple_file_comparison.py` que pode ser usado diretamente da linha de comando:

```bash
python simple_file_comparison.py arquivo1.csv arquivo2.csv
```

## Solução de Problemas

Se você encontrar o erro `ValueError: Could not infer a valid transport from...`, isso significa que o FastMCP não conseguiu determinar automaticamente o tipo de transporte. Use um dos métodos acima com transporte explícito para resolver o problema.
