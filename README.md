# BTG Energy Challenge

## Solução

Autor: Guilherme Kowalczuk

### Contexto

Esse desafio foi proposto no contexto da mesa de Energia do banco BTG. O objetivo era, em suma, usar os dados do INPE de níveis previstos de chuvas para estimar a previsão de precipitação acumulada no dia 01/12/2021 para a região de escoamento da usina Hidrelétrica Camargos (bacia do rio Grande).

### Explicação da Solução

Foi utilizada a biblioteca `geopandas`, que faz processamento de dados geoespaciais, principalmente envolvendo sistemas de coordenadas terrestres. O uso da biblioteca é bastante _straightforward_, bastando apenas criar os objetos de `Polygon` para formarem uma máscara e o `GeoDataFrame` com os dados do INPE para serem recortados.

Para cada arquivo na pasta `forecast_files` foi feito o recorte dos pontos de interesse e a criação de um `DataFrame` com esses dados. Todas as previsões foram concatenadas em um `DataFrame` só, de modo a poder serem feitas análises maiores.

### Ressalvas

- Foi percebido que, no roteiro do desafio, os _labels_ para os dados de latitude e longitude estavam trocados em praticamente todas as menções. Por exemplo, na figura de Carmargos, o _range_ de latitude varia entre -22.4 e -21.2, enquanto no arquivo `PSATCMG_CAMARGOS.bln` essa variação é percebida na longitude.

- O modelo, como descrito no roteiro, somente faz o "recorte" dos pontos na região de interesse. Como a granularidade dos dados do INPE é baixa em comparação a esse recorte, sobram poucos pontos com dados na região, o que limita um pouco a aplicação prática do modelo. Em versões futuras, poderiam ser utilizadas técnicas de interpolação, por exemplo, para estimar o nível de chuvas em outros pontos fora da malha do INPE.

- O código foi formatado segundo o _styleguide_ do Google para Python. Foi adicionado um arquivo `pylintrc` com as diretrizes, que podem ser acessadas [aqui](https://google.github.io/styleguide/pyguide.html).

## Roteiro original

### Introdução

Trabalhando nos sistema da mesa de Energia do banco BTG Pactual, constantemente lidamos com dados de precipitação, tanto previsto como observado.
A informação de quanto choveu ou quanto choverá em determinado lugar é dada por uma malha de coordenadas
(latitude [lat] e longitude [long]) e uma terceira variável que é a precipitação diária acumulada naquele ponto.

Na pasta `forecast_files` é possivel encontrar a previsão de precipitação do modelo meteorológico ETA, desenvolvido pelo INPE.
O nome dos arquivos seguem o seguinte padrão: ETA40_p011221a021221.dat -> ETA40_p**ddmmyy**a**ddmmyy**.dat.
Em que a primeira data é referente a quando foi feita a previsão e a segunda data diz respeito qual data está sendo prevista.

Dentro do arquivo, os dados seguem o descrito acima:

```plaintext
lat     long    data_value
-75.00  -35.00  0.0
-75.00  -34.60  0.1
-75.00  -34.20  0.0
```

Porém, estes dados não são utilizados desta forma, eles passam por um processamento. Pois, uma das perguntas que queremos
responder no nosso dia a dia é: **Quanto choveu ou choverá em determinada região do Brasil?**.

Para isso, utilizamos um **contorno**, que é um polígono consistido das coordenadas que delimitam uma região.
Assim, conseguimos "recortar" os dados que caem dentro desta região e calcular, por exemplo, a precipitação média da região.

Por exemplo (valores inventados):

```plaintext
forecast_date   forecasted_date     data_value
01/12/2021      02/12/2021          1.4
01/12/2021      03/12/2021          2.1
...             ...                 ...
01/12/2021      07/12/2021          3.2
```

### O desafio

O desafio consiste em responder a seguinte pergunta: **Qual é a previsão de precipitação ACUMULADA dada pelo modelo ETA no dia 01/12/2021 para a região de escoamento da usina Hidrelétrica Camargos (bacia do rio Grande)?**

![Contorno de Camargos [Grande]](Contour_Camargos_Grande.png "Contorno de Carmargos")

Modifique o arquivo `main.py` para fazer o "recorte" dos dados de precipitação (para **todos** os dias previstos pelo modelo) e
apresente graficamente a resposta para a pergunta.

### Resalvas

- É permitido a utilização de bibliotecas extras
- A entrega do desafio deve ser feita por GIT. Responda o email com o link do seu repositório.
