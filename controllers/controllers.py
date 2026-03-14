# -*- coding: utf-8 -*-
# from odoo import http


# class CrmInherit(http.Controller):
#     @http.route('/js_crm_task/js_crm_task', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/js_crm_task/js_crm_task/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('js_crm_task.listing', {
#             'root': '/js_crm_task/js_crm_task',
#             'objects': http.request.env['js_crm_task.js_crm_task'].search([]),
#         })

#     @http.route('/js_crm_task/js_crm_task/objects/<model("js_crm_task.js_crm_task"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('js_crm_task.object', {
#             'object': obj
#         })

