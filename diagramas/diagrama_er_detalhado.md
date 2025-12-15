# Diagrama Entidade-Relacionamento - Sistema invenTI

## Visão Geral

O sistema invenTI é uma aplicação web para gerenciamento de equipamentos de TI, desenvolvida em Flask com SQLAlchemy. O diagrama abaixo representa as entidades principais e seus relacionamentos.

## Entidades e Atributos

### 1. Usuario (Usuários)
**Tabela:** `usuarios`

| Atributo | Tipo | Restrições | Descrição |
|----------|------|------------|-----------|
| id | INTEGER | PK, AutoIncrement | Identificador único |
| nome | VARCHAR(100) | NOT NULL | Nome completo do usuário |
| email | VARCHAR(120) | UNIQUE, NOT NULL | Email para login |
| senha_hash | VARCHAR(250) | NOT NULL | Senha criptografada |
| departamento | VARCHAR(100) | NOT NULL | Departamento do usuário |
| cargo | VARCHAR(100) | NOT NULL | Cargo/função |
| is_admin | BOOLEAN | DEFAULT FALSE | Permissões administrativas |
| data_criacao | DATETIME | DEFAULT NOW | Data de cadastro |
| ativo | BOOLEAN | DEFAULT TRUE | Status do usuário |

### 2. Equipamento (Equipamentos)
**Tabela:** `equipamentos`

| Atributo | Tipo | Restrições | Descrição |
|----------|------|------------|-----------|
| id | INTEGER | PK, AutoIncrement | Identificador único |
| patrimonio | VARCHAR(255) | UNIQUE, NOT NULL | Número do patrimônio |
| tipo | VARCHAR(100) | NOT NULL | Tipo do equipamento |
| marca | VARCHAR(100) | NOT NULL | Marca fabricante |
| modelo | VARCHAR(100) | NOT NULL | Modelo do equipamento |
| numero_serie | VARCHAR(255) | UNIQUE, NOT NULL | Número de série |
| data_aquisicao | DATE | NOT NULL | Data de compra/aquisição |
| localizacao | VARCHAR(255) | NOT NULL | Local onde está instalado |
| status | VARCHAR(50) | NOT NULL | Status atual |
| observacoes | TEXT | NULL | Observações adicionais |
| data_cadastro | DATETIME | DEFAULT NOW | Data de cadastro |
| data_ultima_alteracao | DATETIME | DEFAULT NOW | Última modificação |
| id_usuario_cadastro | INTEGER | FK → usuarios.id | Quem cadastrou |
| id_usuario_ultima_alteracao | INTEGER | FK → usuarios.id | Quem alterou por último |

### 3. RegistroSuporte (Registros de Suporte)
**Tabela:** `registros_suporte`

| Atributo | Tipo | Restrições | Descrição |
|----------|------|------------|-----------|
| id | INTEGER | PK, AutoIncrement | Identificador único |
| id_equipamento | INTEGER | FK → equipamentos.id, NOT NULL | Equipamento relacionado |
| id_usuario | INTEGER | FK → usuarios.id, NULL | Usuário que registrou |
| descricao | TEXT | NULL | Descrição do suporte |
| data_suporte | DATETIME | DEFAULT NOW | Data do atendimento |
| tipo_suporte | VARCHAR(100) | NOT NULL | Tipo de manutenção |
| responsavel | VARCHAR(255) | NOT NULL | Técnico responsável |
| custo | DECIMAL(10,2) | DEFAULT 0.00 | Custo do serviço |

## Relacionamentos

### 1. Usuario → Equipamento (1:N)
- **Cardinalidade:** Um usuário pode cadastrar/alterar múltiplos equipamentos
- **Chaves estrangeiras:**
  - `id_usuario_cadastro` → `usuarios.id`
  - `id_usuario_ultima_alteracao` → `usuarios.id`
- **Comportamento:** CASCADE (exclusão em cascata)

### 2. Usuario → RegistroSuporte (1:N)
- **Cardinalidade:** Um usuário pode registrar múltiplos atendimentos
- **Chave estrangeira:** `id_usuario` → `usuarios.id`
- **Comportamento:** SET NULL (define como nulo se usuário for excluído)

### 3. Equipamento → RegistroSuporte (1:N)
- **Cardinalidade:** Um equipamento pode ter múltiplos registros de suporte
- **Chave estrangeira:** `id_equipamento` → `equipamentos.id`
- **Comportamento:** CASCADE (exclusão em cascata)

## Enums/Domínios

### StatusEquipamento
- **Em Uso**: Equipamento ativo e em operação
- **Em Manutenção**: Equipamento em reparo/manutenção
- **Desativado**: Equipamento fora de uso mas ainda no inventário
- **Descartado**: Equipamento descartado/baixado

### TipoSuporte
- **Manutenção Corretiva**: Reparo de defeitos
- **Manutenção Preventiva**: Manutenção programada
- **Atualização de Software**: Updates de sistema/aplicações
- **Troca de Peça**: Substituição de componentes
- **Outro**: Outros tipos de atendimento

## Regras de Integridade

1. **Chaves Únicas:**
   - Usuario.email
   - Equipamento.patrimonio
   - Equipamento.numero_serie

2. **Obrigatoriedades:**
   - Todos os campos marcados como NOT NULL são obrigatórios
   - Campos de relacionamento podem ser NULL (exceto id_equipamento)

3. **Restrições de Domínio:**
   - status deve estar em StatusEquipamento.todos()
   - tipo_suporte deve estar em TipoSuporte.todos()

## Índices Recomendados

- usuarios.email (já UNIQUE)
- equipamentos.patrimonio (já UNIQUE)
- equipamentos.numero_serie (já UNIQUE)
- equipamentos.status
- equipamentos.localizacao
- registros_suporte.data_suporte
- registros_suporte.tipo_suporte

## Considerações de Performance

- **Paginamento:** Implementado nas listagens principais
- **Filtros:** Disponíveis por status, localização, tipo, responsável
- **Pesquisa:** Busca textual em patrimônio, marca, modelo
- **Relacionamentos:** Lazy loading para evitar N+1 queries