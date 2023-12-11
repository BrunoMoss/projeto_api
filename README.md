# API's da aplicação de comparação de fundos de investimento

Coleção de API's desenvolvidas para coletar e exibir dados qualitativos e quantitativos de fundos de investimento.

### Objetivo:

* Permitir a gestores visualizar como seus fundos estão perante seus melhores concorrentes.
* Permitir aos acessores verificar se estão oferecendo os melhores investimentos.
* Permitir aos investidores saber se estão alocando seus recursos nos melhores fundos.
* Permitir tanto a gestores, acessores e investidores visualizar os ativos que mais impactaram positivamente e   negativamente a carteira do fundo.

### Metodologia:

Foram selecionados para compor nossa amostra fundos de ações com patrimônio líquido > 100MM, que não sejam fundo de cotas e não invistam no exterior.Isso foi feito para que ao analizarmos somente a composição do portfolio de ações tenhamos uma boa prévia dos ativos que mais impactaram a rentabilidade do fundo em um determinado período.Para se chegar ao ganho percentual por ativo foi realizada uma aproximação onde o resultado financeiro do ativo no mês foi dividido pelo patrimônio de fechamento do mês imediatamente anterior.


### API's
API | Descrição |
|---|---|
|Atualiza|Coleta dados cadastrais de fundos, dados qualitativos como valor da cota e patrimonio líquido e composição da carteira, divulgados pela CVM|
|Cota|Busca a rentabilidade acumulada para uma lista de fundos dado um intervalo de datas |
|Fundo |Busca dados cadastrais dado uma lista de fundos|
|Portfolio|Busca as 5 maiores contribuições positivas e negativas para a rentabilidade do fundo no mês de referência|

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
