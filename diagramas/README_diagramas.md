# Diagramas ER - Sistema invenTI

Este diretório contém os diagramas de entidade-relacionamento (ER) do sistema invenTI, uma aplicação web para gerenciamento de equipamentos de TI.

## Arquivos de Diagrama

### 1. `diagrama_er.md`
- **Formato:** Mermaid (visualizável no VS Code)
- **Conteúdo:** Diagrama ER completo com entidades, atributos e relacionamentos
- **Como visualizar:** Abra o arquivo no VS Code (requer extensão Mermaid)

### 2. `diagrama_er_plantuml.puml`
- **Formato:** PlantUML
- **Conteúdo:** Diagrama ER profissional com anotações visuais
- **Como visualizar:**
  - Instale extensão PlantUML no VS Code
  - Ou use online: https://www.plantuml.com/plantuml

### 3. `diagrama_er_detalhado.md`
- **Formato:** Documentação textual detalhada
- **Conteúdo:** Descrição completa de todas as entidades, atributos, relacionamentos e regras
- **Como visualizar:** Abra em qualquer editor de markdown

### 4. `diagrama_er_ascii.md`
- **Formato:** ASCII Art + Markdown
- **Conteúdo:** Representação simplificada em texto
- **Como visualizar:** Abra em qualquer editor de texto

## Estrutura do Banco de Dados

### Entidades Principais

1. **Usuario** - Usuários do sistema (admin/comum)
2. **Equipamento** - Inventário de equipamentos de TI
3. **RegistroSuporte** - Histórico de manutenções/suporte

### Relacionamentos

- **Usuario → Equipamento** (1:N)
  - Um usuário pode cadastrar/alterar múltiplos equipamentos
- **Usuario → RegistroSuporte** (1:N)
  - Um usuário pode registrar múltiplos atendimentos
- **Equipamento → RegistroSuporte** (1:N)
  - Um equipamento pode ter múltiplos registros de suporte

### Tecnologias Utilizadas

- **Backend:** Flask (Python)
- **ORM:** SQLAlchemy
- **Banco:** PostgreSQL/MySQL (configurável)
- **Frontend:** Bootstrap 5, Chart.js
- **Migrações:** Alembic

## Como Usar os Diagramas

1. **Para desenvolvimento:** Use `diagrama_er.md` para referência rápida
2. **Para documentação:** Use `diagrama_er_detalhado.md` para especificações completas
3. **Para apresentações:** Use `diagrama_er_plantuml.puml` para diagramas visuais
4. **Para versionamento:** Use `diagrama_er_ascii.md` para diffs legíveis

## Atualização dos Diagramas

Quando modificar os modelos (`app/models/`), atualize os diagramas:

1. Execute as migrações: `flask db migrate`
2. Atualize os arquivos de diagrama correspondentes
3. Teste as alterações no ambiente de desenvolvimento