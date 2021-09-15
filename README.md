# 📺 Animes API
### API de animes CRUD desenvolvida com Flask e PostgreSQL

#### Projeto concluído ✔️

[Sobre](#sobre) • [Tecnologias](#tecnologias) • [Demonstração](#demonstração) • [Autora](#autora) • [Licença](#licença)

## Sobre
É possivel criar, editar, visualizar e excluir animes utilizando o endpoint /animes. Exemplo dos campos necessários para a inserção de um anime:
```
{
	"anime": "",
	"released_date": "",
	"seasons": 1
}
```
\
Para rodar a aplicação é preciso que o PostgreSQL esteja instalado no seu computador, também lembre-se de entrar no ambiente virtual (venv) e instalar todas as dependências do projeto! 😄

## Tecnologias
As seguintes ferramentas foram utilizadas na construção do projeto:

* Python
* Flask
* PostgreSQL

## Demonstração
#### POST /animes - Retorna o post criado com id
![Rota post](https://i.imgur.com/BFs0wtb.png)
#### GET /animes - Retorna uma lista com todos os posts
![Rota get](https://i.imgur.com/ZZGT2wn.png)
#### GET /animes/<:id> - Retorna o post com id correspondente
![Rota get - id](https://i.imgur.com/CDbYr9t.png)
#### PATCH /animes/<:id> - Retorna o post atualizado
![Rota patch](https://i.imgur.com/vNOXEcf.png)
#### DELETE /animes/<:id> - Retorna 204 em caso de sucesso
![Rota delete](https://i.imgur.com/NhnJiZU.png)

## Autora
Feito com ❤️ por:

Laiane Suzart - <a href="https://www.linkedin.com/in/laianesuzart/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a> 
<a href="https://github.com/laianesuzart" target="_blank"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" target="_blank"></a>

## Licença
Este projeto está sob a licença [MIT](https://choosealicense.com/licenses/mit/).
