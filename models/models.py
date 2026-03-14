from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CrmLead(models.Model):
    _inherit = "crm.lead"

    referencia = fields.Char(string="Referência", readonly=True, copy=False)

    data_entrada = fields.Datetime(
        string="Data de Entrada",
        default=fields.Datetime.now,
        readonly=True
    )
    requisicao_externa = fields.Char(
        string="Requisição Externa"
    )
    tecnico_id = fields.Many2one(
        'hr.employee',
        string="Técnico Designado"
    )
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
    stage_enter_date = fields.Datetime(
        string="Entrada no Estágio"
    )

    @api.depends('create_date', 'date_closed')
    def _compute_tempo_total(self):
        for rec in self:
            if rec.date_closed:
                delta = rec.date_closed - rec.create_date
                rec.tempo_total = delta.days
            else:
                rec.tempo_total = 0

    @api.model
    def create(self, vals):
        if not vals.get('referencia'):
            vals['referencia'] = self.env['ir.sequence'].next_by_code('crm.referencia') or '/'
        vals['stage_enter_date'] = fields.Datetime.now()
        return super().create(vals)


    def action_concluir(self):
        for rec in self:
            if not rec.guia_remessa or not rec.folha_obra:
                raise ValidationError(
                    "Preencha os campos 'Guia de Remessa' e 'Folha de Obra' antes de concluir."
                )
        # marcar como ganho (Won)
        self.action_set_won()

    def write(self, vals):
        for rec in self:
            # se houver mudança de estágio
            if 'stage_id' in vals and rec.stage_enter_date:
                now = fields.Datetime.now()
                delta = now - rec.stage_enter_date
                hours = delta.total_seconds() / 3600
                rec.tempo_total += hours  # acumula tempo em horas
                rec.stage_enter_date = now  # atualiza o início do novo estágio

        return super().write(vals)



