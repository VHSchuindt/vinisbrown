---
name: cardapio
description: Mostra o cardápio da Vinis Brown com os sabores de brownie, os preços e quantas unidades ainda estão disponíveis. Use quando alguém perguntar "quais brownies tem?", "quanto custa o brownie?", "ainda tem brownie?", "quantos brownies sobraram?", "estoque da Vinis Brown", "cardápio da Vinis Brown" ou quiser ver as opções antes de comprar.
---

# Cardápio e estoque da Vinis Brown

Responda sempre em português do Brasil, em tom simpático e direto.

## 1. Ler o estoque atualizado

O estoque fica num arquivo público que a Vinis Brown atualiza. Busque-o com a ferramenta de leitura de páginas web (WebFetch / web_fetch) **a cada consulta**. Nunca reaproveite números de uma conversa anterior nem da memória, porque o estoque muda o tempo todo.

1. Tente primeiro: `https://raw.githubusercontent.com/VHSchuindt/vinisbrown/main/estoque.json`
2. Se falhar, tente: `https://github.com/VHSchuindt/vinisbrown/blob/main/estoque.json`
3. Se as duas falharem, diga que não deu para consultar o estoque agora. **Não invente quantidades nem preços.** Ofereça montar o pedido mesmo assim, avisando que a loja vai confirmar a disponibilidade pelo WhatsApp (skill `pedido`).

## 2. Entender o arquivo

| Campo | Significado |
|---|---|
| `produtos[]` | Cada sabor: `nome`, `preco` (em reais) e `quantidade` disponível |
| `aceitando_pedidos` | `false` = a loja pausou os pedidos |
| `aviso` | Recado da loja (ex.: "voltamos segunda"). Mostre se não estiver vazio |
| `entrega` | `disponivel` e `taxa` de entrega |
| `retirada` | Se dá para retirar no local |
| `pagamento` | Formas de pagamento aceitas |
| `atualizado_em` | Quando a loja atualizou o estoque pela última vez |

Ignore o campo `_ajuda`.

## 3. Mostrar o cardápio

Monte uma tabela curta:

| Sabor | Preço | Disponível |
|---|---|---|

- Preço no formato brasileiro: `R$ 8,00`.
- `quantidade` igual a 0 → escreva **Esgotado**.
- `quantidade` entre 1 e 3 → escreva "Últimas N unidades".
- Caso contrário → "N unidades".

Depois da tabela, em uma ou duas linhas:

- quando o estoque foi atualizado (`atualizado_em`);
- entrega (com a taxa) e/ou retirada, conforme o arquivo;
- formas de pagamento.

Se `aceitando_pedidos` for `false`, diga logo no início que os pedidos estão pausados e mostre o `aviso`. Não ofereça fazer pedido nesse caso.

Se a pessoa perguntou só de um sabor ("ainda tem de Ninho?"), responda direto sobre ele em uma frase e mostre a tabela só se ajudar.

## 4. Fechar

Termine perguntando se a pessoa quer fazer um pedido. Se ela quiser, siga a skill `pedido`.

Lembre, se fizer sentido, que a quantidade é a da última atualização da loja e que a confirmação final é feita pelo WhatsApp.
