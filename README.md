# Easy 3.0 — Design System

Este projeto trata a **página inicial** (`home.html`) como a fonte da verdade do design system. Todos os tokens (variáveis CSS) e classes de componentes presentes na home são considerados **componentes mestre**.

## Arquivos

| Arquivo | Papel |
|---|---|
| `home.html` | **Master** — origem dos tokens e componentes |
| `Design System.html` | Guia visual com paleta, tipografia, componentes ao vivo e snippets |
| `validate_components.py` | Validador automático |

## Regra

Toda nova página HTML deste projeto deve:

1. **Reutilizar variáveis CSS** definidas em `:root` na home — `--c-bg`, `--c-text`, `--c-accent`, `--ff-display`, `--ff-text`, `--shadow-card`, etc. Nunca hex/rgb cru no markup.
2. **Reutilizar classes mestre** sem redefini-las — `.btn`, `.btn-primary`, `.pill`, `.veja-card`, `.demo-card`, etc.
3. **Usar apenas as duas famílias** do sistema: `Gyst` (display) e `Manrope` (text). Nada de Inter, Arial, Roboto.
4. **Seguir a escala** de raios (6 / 10 / 12 / 100), sombras (`--shadow-card`, `--shadow-card-2`) e espaçamento (múltiplos de 4).

Se um componente novo precisa existir e não está na home, ele entra **primeiro** na home e é refletido no `Design System.html` — só então pode ser usado nas demais páginas.

## Como validar

Da raiz do projeto:

```bash
python3 validate_components.py
```

O script:

- extrai tokens (`--c-*`, `--ff-*`, `--shadow-*`) e classes do `home.html`
- varre todos os `.html` do projeto
- reporta em cada arquivo:
  - cores hex/rgb fora da paleta
  - `font-family` fora do sistema
  - redefinição de classes mestre (`.btn-primary`, `.pill-accent`, …)
  - estilos inline com cores avulsas

Exit code `1` quando há violações — fácil de plugar em CI.

## Quando alterar o master

Mudou um token (cor, fonte, sombra) ou criou/alterou componente?

1. Edite **`home.html`** primeiro.
2. Reflita no **`Design System.html`** (swatch / snippet correspondente).
3. Rode `python3 validate_components.py` — todas as páginas devem continuar verdes.
