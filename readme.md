## Interpretador para Tiny

Este projeto contém a implementação em Python de um interpretador para a linguagem Tiny. O projeto consiste em um trabalho para fixação de contéudo da disciplina de Linguagens de Programação do CEFET-MG.

### Grupo
Cesar Henrique Resende Soares <br>
Emanuel Vieira Tavares<br>
Vinicius Alves Pereira<br>

### Características da linguagem

- Tiny é uma linguagem interpretada de brinquedo com uma sintaxe e semântica simples.
- A linguagem possui quatro tipos de comandos: comando condicional (if), comando de repetição (while), comando de atribuição (id = expr) e comando de saída (output expr).
- Esses comandos podem ser combinados para formar blocos de comandos. Um programa em Tiny começa com a palavra-reservada `program` seguida de um bloco de comandos.
- Identificadores (variáveis) começam com uma letra ou underscore (_) e podem ser seguidos de letras, dígitos e underscore (_). Esses armazenam apenas números inteiros.
- A linguagem permite avaliação de expressões lógicas simples em comandos condicionais e de repetição.
- As expressões lógicas suportadas são: igual (==), diferente (!=), menor (<), maior (>), menor igual (<=), maior igual (>=). Não existe forma de conectar múltiplas expressões lógicas com E/OU.
- A linguagem suporta constantes numéricas inteiras e leitura de um valor numérico inteiro do teclado (read).
- Expressões aritméticas são suportadas sobre números inteiros: adição (+), subtração (-), multiplicação (*), divisão (/) e resto da divisão (%). Expressões aritméticas compostas devem usar, necessariamente, identificadores auxiliares.
- A linguagem possui comentários de uma linha a partir do símbolo tralha (#).

Aqui está um exemplo de código em Tiny (somatorio.tiny):

```plaintext
# calcula o somatório de números obtidos pela entrada
program
    sum = 0;
    i = read;
    while i > 0 do
        sum = sum + i;
        i = read;
    done;
    output sum;

```

## Fases de Impementação

O projeto foi dividido em 3 fases principais durante a implemetação: analisador léxico, implementação de comandos e expressões e analisador sintático.


## Analisador Léxico para Linguagem Tiny

O [analisador léxico](lexical.py) é responsável por analisar o código-fonte da linguagem Tiny e converter o texto em uma sequência de tokens identificados. Os tokens são unidades básicas de código, como palavras-chave, operadores e identificadores. Este analisador atua como a primeira etapa do processo de compilação, onde o código-fonte é dividido em partes menores que facilitam a análise e a interpretação.


## Analisador Sintático para Linguagem Tiny

O analisador sintático é responsável por analisar a estrutura gramatical do código-fonte da linguagem Tiny. Ele recebe uma sequência de tokens gerada pelo analisador léxico e verifica se a estrutura do programa está de acordo com as regras sintáticas da linguagem. Além disso, ele constrói uma árvore de análise sintática que representa a estrutura hierárquica do programa.
A implementação do analisador sintático é um pouco mais extensa e os métodos que implementam [expressões](expr.py) e [comandos](command.py) da linguagem Tiny foram implementadas em classes auxiliares.



## Como executar

É necessário adicionar o arquivo .tiny no diretório "exemplos" e alterar em [main.py](main.py) o caminho do arquivo a ser executado pelo interpretador:

``` py
if __name__ == '__main__':
    lex = LexicalAnalysis('exemplos/pow.tiny')
    syntactic = SyntaticAnalysis(lex)
    cmd = syntactic.start()
    cmd.execute()

```

Após isso, basta executar o arquivo [main.py](main.py) normalmente.

```
python3 main.py
```