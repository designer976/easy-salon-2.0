# Bibliotecas UI — referência para migração futura

Lista de componentes externos a serem incorporados **após** a migração
do site estático (HTML + design-system.css) para Next.js + Tailwind CSS.

## Aceternity UI

- **Bento Grids** — https://ui.aceternity.com/blocks/bento-grids
  - Stack: React + Tailwind + Framer Motion
  - Uso previsto: blocos tipo bento (grade modular) — features, dashboards, comparativos visuais

## Efferd

- **Header** — https://efferd.com/blocks/header
  - Componente de cabeçalho/navegação alternativo
- **Features** — https://efferd.com/blocks/features
  - Blocos de apresentação de features/funcionalidades

## Pré-requisitos antes de instalar

1. Migrar projeto para Next.js (ou React + Vite)
2. Instalar e configurar Tailwind CSS
3. Migrar `design-system.css` → tokens Tailwind (cores, fontes, espaçamentos)
4. Converter páginas HTML em componentes React
5. Reusar paleta + tipografia do design-system atual nos blocos importados

## Como integrar (quando chegar a hora)

- Aceternity: cada bloco vem com código pronto (copy/paste) — adaptar paleta para tokens do projeto
- Efferd: provavelmente mesmo padrão (verificar licença antes de uso comercial)
