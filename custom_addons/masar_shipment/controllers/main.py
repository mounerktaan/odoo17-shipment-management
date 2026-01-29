from odoo import http
from odoo.http import request

class ShipmentTracking(http.Controller):

    @http.route(['/track'], type='http', auth='public', website=True)
    def track_page(self, **kw):
        return request.render('masar_shipment.track_page', {})

    @http.route(['/track/result'], type='http', auth='public', website=True)
    def track_result(self, tracking_code=None, **kw):
        picking = request.env['stock.picking'].sudo().search([
            ('x_tracking_code', '=', tracking_code)
        ], limit=1)

        return request.render('masar_shipment.track_page', {
            'picking': picking,
            'tracking_code': tracking_code
        })