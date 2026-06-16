#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_components.py
======================

Regra de design system da Easy 3.0:

    A página inicial (home.html) é a fonte da verdade.
    Todos os tokens (variáveis CSS) e classes de componentes
    presentes na home são considerados COMPONENTES MESTRE.

    Toda nova tela / página HTML do projeto deve:
      • usar apenas as variáveis --c-*, --ff-*, --shadow-*, --radius-*
        definidas na home;
      • reutilizar as classes mestre (.btn, .pill, .veja-card, …)
        sem redefini-las;
      • não introduzir cores hex/rgb avulsas, nem famílias de
        fonte fora do sistema.

Este script faz essa validação automaticamente. Rode da raiz do
projeto:

    python3 validate_components.py

Saída: relatório por arquivo com avisos e contagem total de
problemas. Exit code != 0 quando há violações (útil em CI).


══════════════════════════════════════════════════════════════════
PADRÃO DE RESPONSIVIDADE — sandbox v2 (home-2 / quem-somos-2)
══════════════════════════════════════════════════════════════════

As páginas /home-2/ e /quem-somos-2/ são as referências MESTRE.
Qualquer nova página da sandbox v2 (sufixo "-2") DEVE replicar
esse padrão sem desvios. Resumo:

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. BREAKPOINTS (canônicos — não inventar outros)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Desktop ........................... > 1024px
    • Tablet + Mobile (estrutura) ...... ≤ 1024px
    • Mobile (refinos de escala) ........ ≤ 640px

    Tablet e mobile compartilham a MESMA estrutura (1 coluna).
    Diferença só em 640: ajuste fino de fonte/padding/break.

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2. TOPO (NAV) — SEMPRE PADRÃO, NÃO MUDA ENTRE PÁGINAS
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Estrutura (desktop):
      .nav-inner → grid-template-columns: auto 1fr auto
        ├─ .nav-logo  (order: -1, justify-self: start)
        ├─ .nav-links (order:  0, justify-self: center, gap 20px)
        └─ .nav-cta   (order:  1, justify-self: end)

    Mobile (≤ 1024):
      • .nav-links → display: none
      • .nav-cta   → display: none
      • .nav-burger → display: inline-flex; justify-self: end; order: 2
      • Drawer logo SVG → texto "Menu" (Gyst, 18px, var(--c-text))
        via IIFE no [data-drawer-logo]
      • Itens do drawer espelham o top nav (mesma ordem)

    REGRA: nav e drawer NUNCA são redesenhados por página. Apenas
    items do menu podem variar (links). Estrutura é imutável.

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3. FOOTER — SEMPRE PADRÃO; SÓ A FRASE DO CTA MUDA
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Estrutura (desktop):
      footer.footer-bleed
        └─ .footer-inner (max-width 1200px, padding 80px 32px)
            ├─ .footer-cta-grid (2-col: CTA-left + CTA-right)
            │   ├─ .footer-cta-left  → h2 + bullets
            │   └─ .footer-cta-right → botão âncora
            ├─ .footer-sep
            └─ .footer-bottom
                ├─ .footer-logo
                ├─ .footer-nav (links horizontais)
                └─ .footer-copy-row (©, redes)

    Mobile (≤ 1024):
      • .footer-inner → max-width: 100%, padding 60px 24px
      • .footer-cta-grid → 1 col, gap 32px
      • .footer-cta-left h2 → 32px
      • .footer-bottom → flex-direction: column, align-items: start
      • .footer-nav → text-align: left, flex-wrap: wrap, gap 12px 18px
      • .footer-copy-row → column, gap 16px

    Mobile (≤ 640):
      • footer.footer-bleed padding-top/bottom: 0
      • .footer-nav flex-direction: column (1 link/linha)

    REGRA: A ÚNICA coisa que pode variar entre páginas é a frase
    do .footer-cta-left h2 (ex.: "Vamos transformar o seu salão"
    vs. "Conheça quem está por trás"). Tudo o resto — grid,
    bullets, botão, footer-bottom, copy-row — é imutável.

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4. TIPOGRAFIA — TABELA OBRIGATÓRIA DESKTOP → MOBILE (≤ 640)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Hero / H1
      ├─ Desktop ........ 50–64px (Gyst, line-height 1.05)
      └─ Mobile ......... 32px

    Section title / H2 grande
      ├─ Desktop ........ 36–44px
      └─ Mobile ......... 32px (line-height 1.05)

    Section sub-head / H2 médio
      ├─ Desktop ........ 30px
      └─ Mobile ......... 24px

    Card title / H3
      ├─ Desktop ........ 20–22px
      └─ Mobile ......... 18–20px

    Body / parágrafo
      ├─ Desktop ........ 15–17px
      └─ Mobile ......... 14px

    Footer CTA h2
      ├─ Desktop ........ 36–44px
      └─ Mobile ......... 32px (regra do footer, item 3)

    Pill / kicker / eyebrow
      ├─ Desktop ........ 13–14px
      └─ Mobile ......... 12–13px (mantém)

    Botão (.btn)
      ├─ Desktop ........ 14–15px
      └─ Mobile ......... 14px (mantém; só largura → 100%)

    REGRA DE OURO: títulos grandes (50px+ desktop) viram 32px
    no mobile. Títulos médios (30px desktop) viram 24px. Body
    (15-17px desktop) vira 14px. Sempre via @media (max-width: 640).

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5. PADDINGS DE SEÇÃO — DESKTOP 80 → MOBILE 60
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Padding vertical de section (.h2-section, .qs2-section):
      ├─ Desktop ........ 80px top / 80px bottom
      └─ Mobile (≤ 640).. 60px top / 60px bottom

    Padding horizontal (gutter):
      ├─ Desktop ........ 32px
      └─ Mobile ......... 24px

    Footer .footer-inner:
      ├─ Desktop ........ 80px 32px
      └─ Mobile ......... 60px 24px

    REGRA: tudo que é 80 no desktop → 60 no mobile. Tudo que é
    32 lateral → 24 lateral. Aplicar via @media 640 com
    !important quando houver override de :has() ou DS conflitando.

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6. GRIDS (≤ 1024)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Todos os grids 2/3/4 colunas → 1 coluna
    • Bento (1 grande + tiles) → tile-big/wide perdem span
    • Compare 2-col com divisor vertical → 1-col com divisor
      horizontal (apenas home-2)
    • Contato (channels + form) → channels stack + form abaixo

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7. CAROUSEL / SCROLL HORIZONTAL (≤ 1024, apenas home-2)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • .h2-method-list → overflow-x: auto com scroll-snap
    • Compare vira carousel snap horizontal (2 cards) ≤ 640
    • Mask gradient nas bordas (afordância de scroll)

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  8. HOVER vs TOUCH
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • Listeners mouseenter/leave SÓ atachados se
      matchMedia('(hover: hover)').matches === true
    • Em touch: usar click/tap; autoplay pausa via touchstart
      com retomada 800ms após touchend (apenas home-2 carousel)

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  9. REFINOS MOBILE EXTRAS (≤ 640)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • CTAs Hero → flex-direction: column + width: 100%
    • Form-row 2-col → 1 col
    • Bento aspect-ratio 16/10 → 4/3
    • Method steps: padding interno 0 24px + mask-fade ambos lados
    • <br class="qs2-br-desktop"> visível só desktop;
      <br class="qs2-br-mobile"> visível só mobile (controle fino
      de quebra de linha em títulos longos)

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  10. JS PATTERNS (sync helpers)
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    • syncFullBleed(): usa documentElement.clientWidth em vez de
      100vw — evita overflow horizontal em Chrome Windows com
      scrollbar clássico. Aplicar em qualquer seção full-bleed.
    • Drawer logo → "Menu": IIFE que sobrescreve o textContent
      do [data-drawer-logo] após DOM load.
    • BlurFade observer próprio por página (toggle 'is-in').

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHECKLIST — toda nova página "*-2" DEVE
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    1. Usar [data-screen-label="<Nome da Página>"] na <html>
    2. Escopar 100% do CSS a esse atributo (zero vazamento)
    3. Aplicar os 2 blocos @media canônicos (1024 + 640)
    4. Reutilizar nav/drawer/footer SEM redesenhar — só trocar
       a frase do .footer-cta-left h2 e os links do nav
    5. Seguir tabela de tipografia (item 4): título grande 50→32,
       título médio 30→24, body 15-17→14
    6. Seguir regra de padding (item 5): 80→60 vertical, 32→24
       horizontal no mobile
    7. Manter BlurFade scroll-in com observer próprio
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ───────────────────────────────────────────────────────────────
# Configuração
# ───────────────────────────────────────────────────────────────

MASTER_FILE = "index.html"
DESIGN_SYSTEM_FILE = "design-system.html"
DESIGN_SYSTEM_CSS = "design-system.css"

# Famílias de fonte permitidas (qualquer outra dispara aviso).
ALLOWED_FONT_FAMILIES = {
    "gyst", "manrope",
    # fallbacks neutros aceitos:
    "times new roman", "serif", "sans-serif", "system-ui",
    "-apple-system", "blinkmacsystemfont", "ui-monospace",
    "menlo", "consolas", "monaco", "monospace",
    "sf mono", "inherit", "currentcolor",
}

# Hex / rgb permitidos no markup direto (fora de :root).
# Tudo o que estiver em --c-* na home é considerado "ok"; o resto
# precisa estar nesta lista de exceções para passar.
ALLOWED_RAW_COLORS = {
    "transparent", "currentcolor", "inherit", "none",
    # texto branco/quase-branco usado dentro do .btn-primary:
    "rgb(244, 241, 234)",
    # fundo do bloco escuro (footer CTA):
    "rgb(33, 22, 18)",
    # gradient stops do hover do btn-primary:
    "rgb(214, 84, 64)", "rgb(186, 60, 44)",
    # cor de superfície usada em inputs/dropdown:
    "rgb(251, 251, 251)",
}

# Classes que são COMPONENTES MESTRE — não devem ser redefinidas
# fora do master / design system.
MASTER_CLASSES = {
    "btn", "btn-primary", "btn-outline", "btn-outline-dark",
    "btn-outline-cream", "btn-tan", "btn-tan-soft", "btn-cta-row",
    "pill", "pill-accent", "pill-green", "pill-outline", "pill-cream",
    "pill-glow", "pill-glow-cream",
    "veja-card", "demo-card", "section-card", "section-veja",
    "section-team",
    "nav", "nav-inner", "nav-links", "nav-cta", "nav-logo",
    "drawer", "drawer-link", "drawer-nav", "drawer-sep",
    "dropdown", "dropdown-content", "dropdown-item",
    "hero", "hero-top", "hero-title", "hero-sub", "hero-divider",
    "hero-claim", "hero-bleed",
    "footer-bleed", "footer-cta-grid", "footer-cta-left",
    "footer-cta-right", "footer-bullets", "footer-bottom",
    "footer-logo", "footer-nav",
}

# ───────────────────────────────────────────────────────────────
# Regex helpers
# ───────────────────────────────────────────────────────────────

RE_CSS_VAR_DEF = re.compile(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", re.IGNORECASE)
RE_HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RE_RGB_COLOR = re.compile(r"rgba?\(\s*[\d.\s,/%]+\)", re.IGNORECASE)
RE_FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;]+);", re.IGNORECASE)
RE_CLASS_RULE = re.compile(r"\.([a-zA-Z][\w-]*)\s*[\.,:#\[\s{]")
RE_STYLE_BLOCK = re.compile(r"<style[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
RE_ROOT_BLOCK = re.compile(r":root\s*\{([^}]*)\}", re.IGNORECASE | re.DOTALL)
# Responsive contract regexes
RE_MEDIA_BREAKPOINT = re.compile(r"@media\s*\([^)]*?max-width\s*:\s*(\d+)\s*px", re.IGNORECASE)
RE_MARGIN_INLINE = re.compile(r"margin\s*:\s*([^;\"]+)", re.IGNORECASE)
RE_INLINE_STYLE = re.compile(r'style\s*=\s*"([^"]+)"', re.IGNORECASE)

# Breakpoint canônico (definido em design-system.css). Outros valores em
# @media disparam aviso para manter consistência entre páginas.
CANONICAL_BREAKPOINT_PX = 640

# Margens laterais maiores que isso em px hardcoded são suspeitas
# (geralmente significa "centralização travada" no lugar de margin auto).
SIDE_MARGIN_PX_THRESHOLD = 100

# Páginas devem herdar do design-system.css. <style> inline com mais
# linhas (não-vazias) que isso dispara aviso — é sinal de que regras
# CSS deveriam ter sido movidas pro arquivo canônico. design-system.html
# é exempt (é a documentação do sistema, pode ter o próprio <style>).
INLINE_STYLE_LINES_THRESHOLD = 30


# ───────────────────────────────────────────────────────────────
# Resultado por arquivo
# ───────────────────────────────────────────────────────────────

@dataclass
class FileReport:
    path: str
    is_master: bool = False
    tokens_count: int = 0
    master_class_count: int = 0
    warnings: list[tuple[int, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.warnings

    def warn(self, line: int, msg: str) -> None:
        self.warnings.append((line, msg))


# ───────────────────────────────────────────────────────────────
# Master extraction
# ───────────────────────────────────────────────────────────────

def extract_master(master_path: Path, css_path: Path | None = None) -> tuple[set[str], set[str], set[str], set[int]]:
    """Retorna (tokens, valores_de_token, classes_mestre, breakpoints)
    considerando a home (home.html) e — se existir — design-system.css
    como fontes da verdade combinadas."""
    text = master_path.read_text(encoding="utf-8")

    tokens: set[str] = set()
    values: set[str] = set()
    classes: set[str] = set()
    breakpoints: set[int] = set()

    # Tokens: o que estiver dentro de :root { ... } da home
    for root_body in RE_ROOT_BLOCK.findall(text):
        for var, val in RE_CSS_VAR_DEF.findall(root_body):
            tokens.add(var.strip().lower())
            values.add(_normalize_color(val.strip()))

    # Classes: tudo dentro de qualquer <style>...</style> da home
    for css in RE_STYLE_BLOCK.findall(text):
        for cls in RE_CLASS_RULE.findall(css):
            classes.add(cls)
        for bp_m in RE_MEDIA_BREAKPOINT.finditer(css):
            breakpoints.add(int(bp_m.group(1)))

    # design-system.css (fonte canônica externa) também conta como mestre.
    if css_path and css_path.exists():
        css_text = css_path.read_text(encoding="utf-8")
        for root_body in RE_ROOT_BLOCK.findall(css_text):
            for var, val in RE_CSS_VAR_DEF.findall(root_body):
                tokens.add(var.strip().lower())
                values.add(_normalize_color(val.strip()))
        for cls in RE_CLASS_RULE.findall(css_text):
            classes.add(cls)
        for bp_m in RE_MEDIA_BREAKPOINT.finditer(css_text):
            breakpoints.add(int(bp_m.group(1)))

    # Garante que classes-mestre canônicas estão lá
    classes |= MASTER_CLASSES
    # Garante que o breakpoint canônico está sempre presente
    breakpoints.add(CANONICAL_BREAKPOINT_PX)

    return tokens, values, classes, breakpoints


def _normalize_color(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


# ───────────────────────────────────────────────────────────────
# Validação de um arquivo
# ───────────────────────────────────────────────────────────────

def validate_file(
    path: Path,
    master_tokens: set[str],
    master_values: set[str],
    master_classes: set[str],
    master_breakpoints: set[int],
    is_master: bool,
    is_design_system: bool,
) -> FileReport:
    report = FileReport(path=str(path), is_master=is_master)

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # ── 1) Conta tokens e classes mestre usadas
    used_tokens = {m.lower() for m in re.findall(r"--[a-z0-9-]+", text, re.IGNORECASE)}
    report.tokens_count = len(used_tokens & master_tokens)

    used_classes = set()
    for m in re.finditer(r'class\s*=\s*"([^"]+)"', text):
        for c in m.group(1).split():
            used_classes.add(c)
    report.master_class_count = len(used_classes & master_classes)

    # Master e design system não passam por validação de "violações"
    if is_master or is_design_system:
        return report

    # ── 2) Cores hex / rgb fora da paleta dentro de <style>
    for css_match in RE_STYLE_BLOCK.finditer(text):
        css_body = css_match.group(1)
        css_start_line = text[: css_match.start()].count("\n") + 1

        # remove o :root inteiro do escopo de checagem (lá pode definir cores)
        css_clean = RE_ROOT_BLOCK.sub("", css_body)

        for hex_m in RE_HEX_COLOR.finditer(css_clean):
            color = hex_m.group(0).lower()
            line = css_start_line + css_clean[: hex_m.start()].count("\n")
            if color in master_values or color in ALLOWED_RAW_COLORS:
                continue
            report.warn(line, f"cor hex {color} fora da paleta — use var(--c-…)")

        for rgb_m in RE_RGB_COLOR.finditer(css_clean):
            color = _normalize_color(rgb_m.group(0))
            line = css_start_line + css_clean[: rgb_m.start()].count("\n")
            if color in master_values or color in ALLOWED_RAW_COLORS:
                continue
            report.warn(line, f"cor {color} fora da paleta — use var(--c-…)")

        # ── 3) Famílias de fonte fora do sistema
        for ff_m in RE_FONT_FAMILY.finditer(css_clean):
            decl = ff_m.group(1)
            line = css_start_line + css_clean[: ff_m.start()].count("\n")
            for piece in decl.split(","):
                name = piece.strip().strip("'\"").lower()
                if not name or name.startswith("var("):
                    continue
                if name not in ALLOWED_FONT_FAMILIES:
                    report.warn(
                        line,
                        f"font-family '{name}' fora do sistema — use var(--ff-display) ou var(--ff-text)",
                    )

        # ── 4) Redefinição de classes mestre
        # Só conta como redefinição se o seletor for "puro" — apenas
        # `.classe` (com modificadores :hover, ::before, [attr], .cls.cls
        # tudo bem) e SEM combinador descendente/filho/irmão antes.
        # Ex.: `.btn { … }` é redefinição. `.cta-row .btn { … }` ou
        # `.page .nav { … }` é override de contexto, válido.
        for rule_m in re.finditer(r"([^{};]+)\{", css_clean):
            selector_list = rule_m.group(1)
            line = css_start_line + css_clean[: rule_m.start()].count("\n")
            for selector in selector_list.split(","):
                sel = selector.strip()
                if not sel:
                    continue
                # Pega o último "compound selector" — depois do último
                # combinador (espaço, >, +, ~). Se não houver combinador,
                # o seletor inteiro é o compound.
                tail = re.split(r"[\s>+~]+", sel)[-1]
                # Extrai a primeira classe do compound
                m = re.match(r"\.([a-zA-Z][\w-]*)", tail)
                if not m:
                    continue
                cls = m.group(1)
                # Se houve combinador antes, é override de contexto — ok.
                if len(re.split(r"[\s>+~]+", sel)) > 1:
                    continue
                if cls in master_classes:
                    report.warn(
                        line,
                        f"redefine .{cls} (componente mestre — edite em {MASTER_FILE})",
                    )

    # ── 5) Cores hex inline em style="..."
    for style_m in RE_INLINE_STYLE.finditer(text):
        body = style_m.group(1)
        line = text[: style_m.start()].count("\n") + 1
        for hex_m in RE_HEX_COLOR.finditer(body):
            color = hex_m.group(0).lower()
            if color in master_values or color in ALLOWED_RAW_COLORS:
                continue
            report.warn(line, f"style inline com cor hex {color} fora da paleta")
        for rgb_m in RE_RGB_COLOR.finditer(body):
            color = _normalize_color(rgb_m.group(0))
            if color in master_values or color in ALLOWED_RAW_COLORS:
                continue
            report.warn(line, f"style inline com cor {color} fora da paleta")

    # ── 6) Responsive contract: breakpoint deve estar no conjunto canônico
    # (extraído de home.html + design-system.css). Para adicionar um
    # breakpoint novo, declare-o primeiro num desses arquivos canônicos.
    for bp_m in RE_MEDIA_BREAKPOINT.finditer(text):
        bp = int(bp_m.group(1))
        if bp not in master_breakpoints:
            line = text[: bp_m.start()].count("\n") + 1
            allowed = ", ".join(f"{b}px" for b in sorted(master_breakpoints))
            report.warn(
                line,
                f"breakpoint @media max-width: {bp}px não está no conjunto "
                f"canônico ({allowed}). Declare em home.html ou "
                f"design-system.css se for um breakpoint legítimo.",
            )

    # ── 7) Responsive contract: margem lateral hardcoded em px
    # Pega `margin: ... NNNpx ...` em inline styles e em CSS, onde NNN >
    # threshold em posição de "sides" no shorthand. Detecta bugs como o
    # `margin: 0 472.5px 80px` que trava centralização em viewport único.
    def _check_margin_shorthand(value: str, src_line: int, source: str) -> None:
        # Tokens sem !important e sem espaços extras
        v = re.sub(r"\s*!important\s*$", "", value.strip(), flags=re.IGNORECASE)
        parts = v.split()
        # 1 valor: todos lados; 2 valores: top/bottom + sides;
        # 3 valores: top + sides + bottom; 4 valores: top right bottom left.
        sides_indexes: list[int] = []
        if len(parts) == 2:
            sides_indexes = [1]
        elif len(parts) == 3:
            sides_indexes = [1]
        elif len(parts) == 4:
            sides_indexes = [1, 3]
        for idx in sides_indexes:
            tok = parts[idx]
            m = re.match(r"^(\d+(?:\.\d+)?)px$", tok, re.IGNORECASE)
            if not m:
                continue
            px = float(m.group(1))
            if px > SIDE_MARGIN_PX_THRESHOLD:
                report.warn(
                    src_line,
                    f"margem lateral {tok} ({source}) — use 'auto' para "
                    f"centralização ou margem ≤ {SIDE_MARGIN_PX_THRESHOLD}px",
                )

    # Inline styles
    for style_m in RE_INLINE_STYLE.finditer(text):
        body = style_m.group(1)
        line = text[: style_m.start()].count("\n") + 1
        for mar_m in RE_MARGIN_INLINE.finditer(body):
            _check_margin_shorthand(mar_m.group(1), line, "style inline")

    # CSS rules dentro de <style>
    for css_match in RE_STYLE_BLOCK.finditer(text):
        css_body = css_match.group(1)
        css_start_line = text[: css_match.start()].count("\n") + 1
        css_clean = RE_ROOT_BLOCK.sub("", css_body)
        for mar_m in re.finditer(
            r"margin\s*:\s*([^;}]+)[;}]", css_clean, re.IGNORECASE
        ):
            line = css_start_line + css_clean[: mar_m.start()].count("\n")
            _check_margin_shorthand(mar_m.group(1), line, "CSS")

    # ── 8) <style> inline excessivo: páginas devem herdar do design-system
    # design-system.html é exempt (documentação do sistema)
    if not is_design_system:
        total_inline_lines = 0
        first_style_line = 0
        for css_match in RE_STYLE_BLOCK.finditer(text):
            if first_style_line == 0:
                first_style_line = text[: css_match.start()].count("\n") + 1
            css_body = css_match.group(1)
            total_inline_lines += sum(1 for ln in css_body.split("\n") if ln.strip())
        if total_inline_lines > INLINE_STYLE_LINES_THRESHOLD:
            report.warn(
                first_style_line,
                f"<style> inline com {total_inline_lines} linhas não-vazias — "
                f"páginas devem herdar de design-system.css. Mova as regras "
                f"pra lá e mantenha o inline ≤ {INLINE_STYLE_LINES_THRESHOLD} "
                f"linhas (preferencialmente vazio).",
            )

    return report


# ───────────────────────────────────────────────────────────────
# CLI
# ───────────────────────────────────────────────────────────────

# ANSI helpers (sem dependência externa)
def _c(code: str, s: str) -> str:
    if not sys.stdout.isatty():
        return s
    return f"\033[{code}m{s}\033[0m"

def red(s):    return _c("31", s)
def green(s):  return _c("32", s)
def yellow(s): return _c("33", s)
def dim(s):    return _c("2",  s)
def bold(s):   return _c("1",  s)


def find_html_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*.html"):
        # ignora qualquer pasta node_modules, dist, build, etc.
        parts = set(p.parts)
        if parts & {"node_modules", "dist", "build", ".git"}:
            continue
        out.append(p)
    return sorted(out)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path(".")
    master = root / MASTER_FILE
    if not master.exists():
        print(red(f"✗ master não encontrado: {master}"))
        return 2

    css = root / DESIGN_SYSTEM_CSS
    tokens, values, classes, breakpoints = extract_master(master, css if css.exists() else None)
    css_note = f" + {DESIGN_SYSTEM_CSS}" if css.exists() else ""
    bps_note = ", ".join(f"{b}px" for b in sorted(breakpoints))
    print(dim(f"master: {MASTER_FILE}{css_note} · {len(tokens)} tokens · "
              f"{len(classes)} classes · breakpoints {bps_note}"))
    print()

    files = find_html_files(root)
    if not files:
        print(yellow("nenhum .html encontrado"))
        return 0

    total_problems = 0
    ok_files = warn_files = 0

    for f in files:
        rel = f.relative_to(root) if f.is_relative_to(root) else f
        is_master = (f.resolve() == master.resolve())
        is_design_system = (f.name == DESIGN_SYSTEM_FILE)

        report = validate_file(f, tokens, values, classes, breakpoints, is_master, is_design_system)

        header = bold(f"━━━ {rel} ━━━")
        print(header)

        if is_master:
            print(green(f"  ✓ master file"),
                  dim(f"· {report.tokens_count} tokens · {report.master_class_count} componentes mestre"))
        elif is_design_system:
            print(green(f"  ✓ design system"),
                  dim(f"· {report.tokens_count} tokens · {report.master_class_count} componentes"))
        elif report.ok:
            print(green(f"  ✓ ok"),
                  dim(f"· {report.tokens_count} tokens · {report.master_class_count} componentes"))
            ok_files += 1
        else:
            warn_files += 1
            for line, msg in sorted(report.warnings):
                print(f"  {yellow('⚠')} linha {line:>4}: {msg}")
                total_problems += 1
        print()

    summary = (
        f"{ok_files} arquivos OK · {warn_files} com avisos · "
        f"{total_problems} problemas"
    )
    if total_problems:
        print(red(summary))
        return 1
    else:
        print(green(summary))
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
