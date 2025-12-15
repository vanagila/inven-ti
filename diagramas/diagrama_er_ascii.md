# Diagrama ER - Sistema invenTI (ASCII Art)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Usuario     │       │   Equipamento   │       │ RegistroSuporte │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │       │ id (PK)         │
│ nome            │       │ patrimonio (UK) │       │ id_equipamento  │
│ email (UK)      │       │ tipo            │       │   (FK→Equip)    │
│ senha_hash      │       │ marca           │       │ id_usuario      │
│ departamento    │       │ modelo          │       │   (FK→Usuario)  │
│ cargo           │       │ numero_serie(UK)│       │ descricao       │
│ is_admin        │       │ data_aquisicao  │       │ data_suporte    │
│ data_criacao    │       │ localizacao     │       │ tipo_suporte    │
│ ativo           │       │ status          │       │ responsavel     │
└─────────────────┘       │ observacoes     │       │ custo           │
          │               │ data_cadastro   │       └─────────────────┘
          │               │ data_alteracao  │
          │               │ id_user_cad     │
          │               │   (FK→Usuario)  │
          │               │ id_user_alt     │
          │               │   (FK→Usuario)  │
          └─────────────────┘
                 │
                 │ 1:N
                 ▼
          ┌─────────────────┐
          │ RegistroSuporte │
          └─────────────────┘
```

## Legenda dos Relacionamentos

```
Usuario 1:N Equipamento
├── cadastra (id_usuario_cadastro)
└── altera (id_usuario_ultima_alteracao)

Usuario 1:N RegistroSuporte
└── registra (id_usuario)

Equipamento 1:N RegistroSuporte
└── possui (id_equipamento)
```

## Resumo das Entidades

### Usuario (Usuários do Sistema)
- **PK:** id
- **UK:** email
- **Relacionamentos:** Cadastra e altera equipamentos, registra suportes

### Equipamento (Inventário de TI)
- **PK:** id
- **UK:** patrimonio, numero_serie
- **FK:** id_usuario_cadastro, id_usuario_ultima_alteracao
- **Relacionamentos:** Possui múltiplos registros de suporte

### RegistroSuporte (Histórico de Manutenção)
- **PK:** id
- **FK:** id_equipamento, id_usuario
- **Relacionamentos:** Vinculado a um equipamento e opcionalmente a um usuário

## Status e Tipos

### Status do Equipamento
- Em Uso
- Em Manutenção
- Desativado
- Descartado

### Tipos de Suporte
- Manutenção Corretiva
- Manutenção Preventiva
- Atualização de Software
- Troca de Peça
- Outro