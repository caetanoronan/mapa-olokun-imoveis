# Como publicar o mapa no GitHub Pages

Este repositório contém mapas gerados em HTML (por exemplo `mapa_imobiliaria_automatico.html`). Criei um workflow do GitHub Actions que copia os arquivos HTML para uma pasta `public/` e publica essa pasta na branch `gh-pages` usando `peaceiris/actions-gh-pages`.

O que foi criado:

- `.github/workflows/deploy-gh-pages.yml` — workflow que publica o HTML em `gh-pages` quando você fizer push na `main`.

Como acionar o deploy (PowerShell):

```powershell
git add .github/workflows/deploy-gh-pages.yml DEPLOY_GH_PAGES.md
git commit -m "Adiciona workflow para publicar mapa no GitHub Pages"
git push origin main
```

O push acima irá disparar o workflow automaticamente. O workflow:

- cria a pasta `public/` no runner
- copia `mapa_imobiliaria_automatico.html` (e `mapa_imobiliaria.html` se existir) para `public/`
- publica `public/` em `gh-pages`

Após o workflow rodar com sucesso, o conteúdo será publicado na branch `gh-pages`. Para acessar o site:

1. Vá em `https://github.com/<seu-usuario>/<seu-repo>/actions` para conferir a execução do workflow.
2. Vá em `https://github.com/<seu-usuario>/<seu-repo>/settings/pages` para verificar a URL do GitHub Pages ou ajustar a fonte (se necessário).

Observações:

- Se você prefere que os arquivos fiquem em `docs/` em vez de `gh-pages`, posso adaptar o workflow para copiar os arquivos para `docs/` e publicar a partir da branch `main`.
- Se quiser, eu também posso fazer o commit das mudanças locais e empurrar para o remoto (mas preciso das credenciais/configuração remota do git que você executará no seu terminal). 
\nRedeploy triggered: 2025-11-14T17:01:18.9891288-03:00
