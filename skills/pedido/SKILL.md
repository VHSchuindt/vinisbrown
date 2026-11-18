---
name: pedido
description: Faz um pedido de brownies da Vinis Brown. Confere quantos ainda tem disponível, monta o pedido com sabores, quantidades, entrega ou retirada e pagamento, calcula o total e gera um link do WhatsApp com a mensagem pronta para enviar à loja. Use quando alguém disser "quero comprar brownie", "fazer pedido na Vinis Brown", "encomendar brownie", "manda 2 brownies de Ninho", "quero pedir na Vinis Brown" ou algo parecido.
---

# Pedido na Vinis Brown

Responda sempre em português do Brasil, em tom simpático e direto. O objetivo é sair com um link do WhatsApp que o comprador só precisa abrir e tocar em enviar.

## 1. Ler o estoque atualizado

Busque o arquivo de estoque com a ferramenta de leitura de páginas web (WebFetch / web_fetch) **toda vez** que um pedido começar. Nunca use números de memória ou de conversas anteriores.

1. Primeiro: `https://raw.githubusercontent.com/VHSchuindt/vinisbrown/main/estoque.json`
2. Se falhar: `https://github.com/VHSchuindt/vinisbrown/blob/main/estoque.json`
3. Se as duas falharem: avise que não deu para conferir o estoque, não invente preços nem quantidades e pergunte se a pessoa quer mandar o pedido mesmo assim, para a loja confirmar preço e disponibilidade. Nesse caso, a mensagem vai sem valores e você não consegue gerar o link (o número da loja está no arquivo), então entregue só o texto para ela copiar.

Campos principais: `produtos[]` (`nome`, `preco`, `quantidade`), `aceitando_pedidos`, `aviso`, `entrega` (`disponivel`, `taxa`), `retirada` (`disponivel`), `pagamento` (lista) e `whatsapp` (número da loja). Ignore `_ajuda`.

Se `aceitando_pedidos` for `false`, diga que os pedidos estão pausados, mostre o `aviso` e pare por aqui.

## 2. Coletar o pedido

Se a pessoa ainda não disse o que quer, mostre só os sabores com `quantidade` maior que 0, com preço e quantidade disponível.

Pergunte apenas o que estiver faltando, de preferência tudo numa mensagem só:

1. **Sabores e quantidades**
2. **Nome** de quem está pedindo
3. **Entrega ou retirada**. Ofereça só as opções com `disponivel: true`. Na entrega, mencione a taxa e peça o endereço completo (rua, número, bairro e um ponto de referência).
4. **Forma de pagamento**, dentre as da lista `pagamento`
5. **Observações** (opcional, ex.: horário, presente)

Não peça CPF, dados de cartão, senha nem nada além disso. O pagamento é combinado direto com a loja.

## 3. Conferir disponibilidade

Para cada item:

- Sabor com `quantidade` 0 → diga que esgotou e sugira os disponíveis.
- Pedido maior que a `quantidade` → diga quantas unidades ainda tem e pergunte se a pessoa quer ajustar.
- Sabor que não existe no arquivo → mostre os sabores que existem.

Só siga quando todos os itens couberem no estoque.

## 4. Mostrar o resumo e confirmar

Mostre o resumo com itens, subtotal, taxa de entrega (se houver), total, nome, entrega/retirada e pagamento. Pergunte: "Está tudo certo?". Ajuste o que a pessoa pedir.

## 5. Gerar a mensagem e o link do WhatsApp

**Com execução de código disponível (preferível):** rode o script `scripts/gerar_link.py`, que fica na pasta desta skill. Ele calcula os valores, monta a mensagem e codifica o link:

```bash
python3 scripts/gerar_link.py '{"whatsapp":"<campo whatsapp>","itens":[{"nome":"Brownie Tradicional","preco":8.0,"quantidade":2}],"nome":"Ana","tipo":"entrega","endereco":"Rua X, 123 - Bairro Y (ref.: ...)","taxa_entrega":5.0,"pagamento":"Pix","observacoes":""}'
```

Use os preços do `estoque.json`, nunca os que o comprador digitar. Se o script responder `ERRO: numero de WhatsApp da loja nao configurado`, diga que a loja ainda não configurou o número e entregue só o texto do pedido para copiar.

**Sem execução de código:** monte a mensagem neste formato, conferindo cada conta duas vezes:

```
Olá, Vinis Brown! Quero fazer um pedido:

• 2x Brownie Tradicional — R$ 16,00
• 1x Brownie de Ninho com Nutella — R$ 10,00

Subtotal: R$ 26,00
Taxa de entrega: R$ 5,00
*Total: R$ 31,00*

Nome: Ana
Entrega: Rua X, 123 - Bairro Y (ref.: ...)
Pagamento: Pix
```

O link é `https://wa.me/<whatsapp>?text=<mensagem codificada>`. O número vai só com dígitos (DDI + DDD + número, ex.: `5565999999999`). Codifique o texto em UTF-8 com percent-encoding: quebra de linha `%0A`, espaço `%20`, `R$` → `R%24`, `•` → `%E2%80%A2`, `—` → `%E2%80%94`, letras acentuadas também.

## 6. Entregar

1. Mostre o link como botão clicável: `[📲 Enviar pedido no WhatsApp](<link>)`.
2. Logo abaixo, mostre a mensagem num bloco de código, para a pessoa copiar se o link não abrir.
3. Avise em uma frase:
   - o pedido só está confirmado quando a Vinis Brown responder no WhatsApp;
   - o estoque pode mudar entre esta consulta e a confirmação.

Você não envia a mensagem sozinho. O comprador precisa abrir o link e tocar em enviar.
