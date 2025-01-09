# Estrutura do Projeto: Case Infineat

Este documento descreve a estrutura do projeto Case Infineat e inclui instruções sobre como instalar o ambiente e executar o modelo.

## Estrutura de Diretórios

```
case_infineat/
├── data_results/
│   ├── trusted/
│       ├── case_data.xlsx
├── database/
│   ├── dabase.db
├── env/  # Ambiente virtual
├── ge/
│   ├── checkpoints/
│   ├── expectations/
│   ├── plugins/
│   ├── uncommitted/
│   ├── validation_definitions/
│   ├── great_expectations.yml
├── models/
│   ├── __pycache__/
│   ├── data_tests.py
│   ├── functions.py
│   ├── main.py
│   ├── test2.ipynb
├── pbi/
│   ├── dash.pbix
├── src/
│   ├── Planilha_case_dados.xlsx
```

## Configuração do Ambiente

Para configurar o ambiente virtual e executar o modelo, siga os passos abaixo:

### Pré-requisitos
- Python 3.8 ou superior instalado.
- Gerenciador de pacotes `pip`.

### Passos

1. **Clonar o repositório**:
   ```bash
   git clone https://github.com/Matheus-Barros/case_infineat.git
   cd case_infineat
   ```

2. **Criar o ambiente virtual**:
   Utilize o ambiente virtual disponibilizado na pasta `env`, basta ativá-lo.

4. **Executar o modelo**:
   - Para executar o script principal:
     ```bash
     python models/main.py
     ```

5. **Verificar a validação dos dados** (usando Great Expectations):
   Acesse os resultados dos testes de qualidade de dados abrindo o html no diretório ge\gx\uncommitted\data_docs\local_site\index.html

## Observações Adicionais
- O arquivo `dash.pbix` na pasta `pbi/` contém o dashboard criado no Power BI.
- Certifique-se de que as planilhas na pasta `data_results/` estejam atualizadas antes de rodar os scripts.

Caso encontre problemas, verifique as dependências instaladas.
