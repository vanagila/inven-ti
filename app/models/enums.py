class StatusEquipamento:
    EM_USO = 'Em Uso'
    EM_MANUTENCAO = 'Em Manutenção'
    DESATIVADO = 'Desativado'
    DESCARTADO = 'Descartado'
    
    @classmethod
    def todos(cls):
        return [cls.EM_USO, cls.EM_MANUTENCAO, cls.DESATIVADO, cls.DESCARTADO]


class TipoSuporte:
    MANUTENCAO_CORRETIVA = 'Manutenção Corretiva'
    MANUTENCAO_PREVENTIVA = 'Manutenção Preventiva'
    ATUALIZACAO_SOFTWARE = 'Atualização de Software'
    TROCA_PECA = 'Troca de Peça'
    
    @classmethod
    def todos(cls):
        return [cls.MANUTENCAO_CORRETIVA, cls.MANUTENCAO_PREVENTIVA, 
                cls.ATUALIZACAO_SOFTWARE, cls.TROCA_PECA]