from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = "crm.lead"

    referencia = fields.Char(string="Referência", readonly=True, copy=False)
    data_entrada = fields.Datetime(string="Data de Entrada", default=fields.Datetime.now)
    requisicao_externa = fields.Char(string="Requisição Externa")
    tecnico_id = fields.Many2one('hr.employee', string="Técnico Designado")
    tipo_processo = fields.Selection([
        ('fornecimento', 'Fornecimento'),
        ('assistencia', 'Assistência Técnica'),
        ('instalacao', 'Nova Instalação'),
        ('projeto', 'Projeto')
    ], string="Tipo de Processo")
    tempo_total = fields.Float(
        string="Tempo Total do Processo (horas)",
        default=0,
        readonly=True
    )
    guia_remessa = fields.Char(string="Guia de Remessa")
    folha_obra = fields.Char(string="Folha de Obra")
    stage_enter_date = fields.Datetime(string="Entrada no Estágio")

    @api.model
    def create(self, vals):
        # Gera referência automática
        if not vals.get('referencia'):
            vals['referencia'] = self.env['ir.sequence'].next_by_code('crm.referencia') or '/'
        # Marca o início do stage atual
        vals['stage_enter_date'] = fields.Datetime.now()
        return super().create(vals)

    def write(self, vals):
        # Se houver mudança de stage, calcula o tempo no stage anterior
        if 'stage_id' in vals:
            now = fields.Datetime.now()
            for rec in self:


                if rec.stage_enter_date:
                    delta = now - rec.stage_enter_date
                    total_seconds = delta.total_seconds()
                    hours = int(total_seconds // 3600)
                    minutes = int((total_seconds % 3600) // 60)

                    rec.tempo_total += hours

                # Atualiza o início do novo stage
                rec.stage_enter_date = now

        return super().write(vals)

    def action_concluir(self):
        for rec in self:
            if not rec.guia_remessa or not rec.folha_obra:
                raise ValidationError(
                    "Preencha os campos 'Guia de Remessa' e 'Folha de Obra' antes de concluir."
                )
        # marca como ganho (Won)
        self.action_set_won()