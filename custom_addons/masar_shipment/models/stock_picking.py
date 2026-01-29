from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    x_tracking_code = fields.Char(
        string="Tracking Code",
        readonly=True,
        copy=False,
    )

    x_shipment_state = fields.Selection([
        ('created', 'Created'),
        ('picked', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string="Shipment Status", default='created', tracking=True)

    @api.model
    def create(self, vals):
        if not vals.get("x_tracking_code"):
            vals["x_tracking_code"] = self.env["ir.sequence"].next_by_code(
                "masar.shipment.tracking"
            )
        if not vals.get("x_shipment_state"):
            vals["x_shipment_state"] = 'created'
        return super().create(vals)

    def action_pick_up(self):
        self.write({'x_shipment_state': 'picked'})

    def action_in_transit(self):
        self.write({'x_shipment_state': 'in_transit'})

    def action_out_for_delivery(self):
        self.write({'x_shipment_state': 'out_for_delivery'})

    def action_delivered(self):
        self.write({'x_shipment_state': 'delivered'})

    def action_cancelled(self):
        self.write({'x_shipment_state': 'cancelled'})

    def button_validate(self):
        res = super().button_validate()

        for picking in self:
            if picking.x_shipment_state in ['created', 'picked']:
                picking.x_shipment_state = 'in_transit'

        return res
    def action_shipment_pickup(self):
        for picking in self:
            if picking.x_shipment_state == 'created':
                picking.x_shipment_state = 'picked'

    def action_shipment_out_for_delivery(self):
        for picking in self:
            if picking.x_shipment_state == 'in_transit':
                picking.x_shipment_state = 'out_for_delivery'

    def action_shipment_delivered(self):
        for picking in self:
            if picking.x_shipment_state == 'out_for_delivery':
                picking.x_shipment_state = 'delivered'

    def action_shipment_cancel(self):
        for picking in self:
            if picking.x_shipment_state != 'delivered':
                picking.x_shipment_state = 'cancelled'