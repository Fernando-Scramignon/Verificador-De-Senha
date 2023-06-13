# verificador_de_senha
Um projeto criado para um desafio técnico. É uma API que permite verificar a força da senha baseado em configurações enviadas em uma requisição. 

## tabela de conteúdos
- [Tecnologias](#tecnologias)
- [Rodando o Projeto](#rodando-o-projeto)
  - [Sem Docker](#sem-usar-o-docker)
  - [Com Docker](#usando-docker-e-docker-compose-recomendado)
- [Como utilizar](#como-utilizar)
- [Referência de regras](#referência-de-regras)
- [Testes](#testes)

## Tecnologias
- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/)

## Rodando o projeto
Primeiramente clone o repositório na máquina local.
Têm duas maneiras de rodar o projeto. Uma com **docker**(recomendado) e outra sem.

### Usando docker e docker compose (recomendado)
Desse modo é necessário ter instalado o [docker](https://docs.docker.com/get-docker/) e o [docker compose](https://docs.docker.com/compose/install/#install-compose).

Você pode criar o ambiente virtual e instalar as depêndencias para parar os erros de import, mas não é necessário.

Ambiente Virtual:
```python
python -m venv venv
```
Instalando dependências:
```python
pip install -r requirements.txt
```

Utilize o comando docker compose up

```python
docker compose up
```

Com isso o projeto já está funcionando em um container docker sem precisar de mais configurações</br>
Caso queria excluir os containers execute:

```python
docker compose down
```

### Sem usar o docker
Crie o ambiente virtual com o comando

```python
python -m venv venv
```

Se você estiver no windows é necessário que rode o comando que permite a criação do venv antes

```shell
Set-ExecutionPolicy AllSigned
```

Ative o ambiente virtual.

windows:
</br>
```shell
.\venv\Scripts\activate
```

linux:
```python
source venv/bin/activate
```

Agora instale as dependências

```python
pip install -r requirements.txt
```

Por último rode a api com
```python
python manage.py runserver
```
obs: Irá rodar na porta 8080


## Como utilizar

Faça uma requisição POST para o endpoint /api/verify
</br>
Se rodar localmente a url será http://localhost:8080/api/verify
</br>
Essa requisição precisa possuir a senha e as regras que vão ser utilizadas para validar ela
</br>
Ex: 

```
POST /api/verify
Host: http://localhost:8080
Authorization: None
Content-type: application/json
```

#### request body:

```json
{
  "password": "TesteSenhaForte!123&",
  "rules": [
      {"rule": "minSize","value": 8},
      {"rule": "minSpecialChars","value": 2},
      {"rule": "noRepeated","value": 0},
      {"rule": "minDigit","value": 4}
  ]
}
```

### Response

```json
{
  "verify": false,
  "noMatch": ["minDigit"]
}
```

Se uma regra falhar, a chave verify da resposta vem falsa e o nome da regra vai para a chave noMatch (Pode ter várias regras dentro)

## Referência de regras

- minSize: tem pelo menos x caracteres.
- minUppercase: tem pelo menos x caracteres maiúsculos
- minLowercase: tem pelo menos x caracteres minúsculos
- minDigit: tem pelo menos x dígitos (0-9)
- minSpecialChars: tem pelo menos x caracteres especiais ( Os caracteres especiais são os caracteres da seguinte string: "!@#$%^&*()-+\/{}[]" )
- noRepeated: não tenha nenhum caractere repetido em sequência ( ou seja, "aab" viola esta
condição, mas "aba" não)

## Testes

Para rodar os testes use o comando:

```python
python manage.py test
```
