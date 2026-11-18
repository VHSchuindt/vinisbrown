#!/usr/bin/env python3
"""Monta a mensagem do pedido da Vinis Brown e o link do WhatsApp.

Uso:
    python3 gerar_link.py '<json do pedido>'
    echo '<json do pedido>' | python3 gerar_link.py

JSON de entrada:
{
  "whatsapp": "5565999999999",
  "itens": [{"nome": "Brownie Tradicional", "preco": 8.0, "quantidade": 2}],
  "nome": "Ana",
  "tipo": "entrega",            # "entrega" ou "retirada"
  "endereco": "Rua X, 123 - Bairro Y",   # so para entrega
  "taxa_entrega": 5.0,          # 0 para retirada
  "pagamento": "Pix",
  "observacoes": ""
}

Saida: JSON com "mensagem", "subtotal", "taxa_entrega", "total" e "link".
"""
import json
import re
import sys
import urllib.parse


def brl(valor: float) -> str:
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    bruto = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    pedido = json.loads(bruto)

    numero = re.sub(r"\D", "", str(pedido.get("whatsapp", "")))
    if not numero or set(numero[2:]) <= {"0"}:
        sys.exit("ERRO: numero de WhatsApp da loja nao configurado no estoque.json")

    itens = [i for i in pedido.get("itens", []) if int(i.get("quantidade", 0)) > 0]
    if not itens:
        sys.exit("ERRO: o pedido nao tem itens")

    linhas = ["Olá, Vinis Brown! Quero fazer um pedido:", ""]
    subtotal = 0.0
    for item in itens:
        qtd = int(item["quantidade"])
        valor = round(float(item["preco"]) * qtd, 2)
        subtotal += valor
        linhas.append(f"• {qtd}x {item['nome']} — {brl(valor)}")
    subtotal = round(subtotal, 2)

    tipo = str(pedido.get("tipo", "retirada")).lower()
    taxa = round(float(pedido.get("taxa_entrega", 0) or 0), 2) if tipo == "entrega" else 0.0
    total = round(subtotal + taxa, 2)

    linhas.append("")
    linhas.append(f"Subtotal: {brl(subtotal)}")
    if taxa:
        linhas.append(f"Taxa de entrega: {brl(taxa)}")
    linhas.append(f"*Total: {brl(total)}*")
    linhas.append("")
    linhas.append(f"Nome: {pedido.get('nome', '').strip()}")
    if tipo == "entrega":
        linhas.append(f"Entrega: {pedido.get('endereco', '').strip()}")
    else:
        linhas.append("Retirada no local")
    if pedido.get("pagamento"):
        linhas.append(f"Pagamento: {pedido['pagamento']}")
    if str(pedido.get("observacoes", "")).strip():
        linhas.append(f"Obs.: {pedido['observacoes'].strip()}")

    mensagem = "\n".join(linhas)
    link = f"https://wa.me/{numero}?text={urllib.parse.quote(mensagem, safe='')}"

    print(json.dumps({
        "mensagem": mensagem,
        "subtotal": brl(subtotal),
        "taxa_entrega": brl(taxa),
        "total": brl(total),
        "link": link,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
