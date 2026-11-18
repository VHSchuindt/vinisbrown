<p align="center">
  <img src="assets/logo.png" alt="Vinis Brown" width="200">
</p>

# Vinis Brown — plugin para o Claude

Peça brownies da Vinis Brown direto pelo Claude: veja o cardápio, confira quantos ainda tem disponível e receba um link do WhatsApp com o pedido pronto para enviar.

## O que o plugin faz

| Skill | Como usar | O que faz |
|---|---|---|
| `cardapio` | "quais brownies tem?" ou `/vinisbrown:cardapio` | Mostra sabores, preços e quantas unidades ainda estão disponíveis |
| `pedido` | "quero comprar brownie" ou `/vinisbrown:pedido` | Monta o pedido, confere o estoque, calcula o total e gera o link do WhatsApp |

O pedido só fica confirmado quando a Vinis Brown responde no WhatsApp.

## Como instalar

**Pelo arquivo (Claude ou ChatGPT)**

1. Baixe o plugin: https://github.com/VHSchuindt/vinisbrown/raw/main/baixar/vinisbrown.zip
2. **No Claude:** Customize > Plugins > Adicionar > **Fazer upload de plugin** e escolha o `.zip`.
3. **No ChatGPT:** Plugins > Adicionar > **Enviar arquivo compactado do plugin** e escolha o `.zip`.

**No Claude (site, app ou desktop)**

1. Abra **Customize > Plugins**.
2. Clique em **Add > Add marketplace**.
3. Digite `VHSchuindt/vinisbrown` e confirme.
4. Adicione o plugin **Vinis Brown**.

**No Claude Code**

```
/plugin marketplace add VHSchuindt/vinisbrown
/plugin install vinisbrown@vinisbrown
```

## Para a Vinis Brown: como atualizar o estoque

Todo o cardápio fica no arquivo [`estoque.json`](estoque.json). O plugin lê esse arquivo na hora de cada consulta, então basta editá-lo:

1. Abra o `estoque.json` aqui no GitHub e clique no lápis (✏️ **Edit**).
2. Mude o que precisar:
   - `quantidade`: quantos brownies daquele sabor ainda tem (0 = esgotado);
   - `preco`: com ponto, ex.: `8.50`;
   - `aceitando_pedidos`: `false` para pausar os pedidos, com um recado em `aviso`;
   - `atualizado_em`: data e hora da atualização.
3. Clique em **Commit changes**.

Para adicionar um sabor, copie uma linha de `produtos` e troque `id`, `nome`, `preco` e `quantidade`.

> A baixa do estoque é manual: quando confirmar uma venda pelo WhatsApp, diminua a `quantidade`. O GitHub pode levar alguns minutos para mostrar a versão nova.

## Antes de publicar

- [ ] Trocar `whatsapp` no `estoque.json` pelo número real (só dígitos: 55 + DDD + número)
- [ ] Ajustar sabores, preços e quantidades
- [ ] Deixar o repositório **público**, para qualquer pessoa conseguir instalar e o Claude conseguir ler o estoque
