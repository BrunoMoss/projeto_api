# API's da aplicação de comparação de fundos de investimento

Coleção de API's desenvolvidas para coletar e exibir dados qualitativos e quantitativos de fundos de investimento.

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
