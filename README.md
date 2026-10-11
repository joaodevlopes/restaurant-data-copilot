# Restaurant Data Copilot

Projeto de portfólio para estudo de engenharia de dados. Simula a operação de uma **rede fictícia** de restaurantes em Belo Horizonte para praticar, de ponta a ponta: ingestão de APIs públicas, pipeline em camadas (Bronze, Silver, Gold), modelagem dimensional com dbt, API em Spring Boot e um assistente de IA com consultas auditáveis.

> Não é um produto comercial nem foi feito para uma empresa. Os restaurantes existem no OpenStreetMap, mas pedidos, estoque e valores são gerados artificialmente.

**Status:** em construção · ingestão da camada Bronze

## O que estou praticando

- Consumir APIs públicas e guardar o dado cru de forma imutável e rastreável.
- Validar qualidade de dados e separar registros inválidos com o motivo da rejeição.
- Modelar um esquema estrela e escrever SQL analítico (CTEs, window functions).
- Expor dados por uma API REST com boas práticas de segurança.
- Usar IA com ferramentas restritas, de forma que cada resposta seja verificável.

## Perguntas que o projeto vai responder

- Qual o faturamento por dia, semana e mês de cada restaurante?
- Quais produtos e categorias dão mais margem?
- Quais itens estão perto de faltar no estoque?
- A chuva e a temperatura mudam o volume de pedidos e o canal (delivery ou presencial)?
- Como feriados e datas comemorativas afetam as vendas?

## Arquitetura planejada

```text
Fontes (OSM, Open-Meteo, BrasilAPI, IBGE + gerador sintético)
  -> Bronze (arquivos crus) -> Silver (Parquet validado) -> Gold (dbt + PostgreSQL)
  -> API Spring Boot -> Dashboard e Assistente de IA
```

## Stack planejada

| Camada | Tecnologia |
|---|---|
| Pipeline | Python 3.13, uv, Pandas, PyArrow, pytest |
| Transformação | dbt Core + dbt-postgres |
| Banco | PostgreSQL 16 em Docker Compose |
| API | Java 21, Spring Boot 3, springdoc-openapi |
| Interface | React + Vite + Recharts |
| IA | Spring AI + Ollama (modelo local) |

## Como executar

_Instruções serão adicionadas conforme cada etapa ficar pronta._

## Dados e licenças

- Estabelecimentos: © OpenStreetMap contributors, ODbL.
- Clima: Open-Meteo.
- Feriados: BrasilAPI. Inflação: IBGE (SIDRA).
- **Pedidos, clientes, estoque e valores são sintéticos e não representam operações reais.**
