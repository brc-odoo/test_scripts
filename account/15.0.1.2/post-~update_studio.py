# -*- coding: utf-8 -*-

from odoo.upgrade import util

import pudb
def migrate(cr, version):
    # o.type to o.move_type
    pu.db
    view_id = util.ref(cr, "__export__.ir_ui_view_1967_22f35e53")
    cr.execute(
        """
        UPDATE ir_ui_view
            SET arch_db = replace(arch_db,'o.type', 'o.move_type')
        WHERE id = %s
        """,
        [view_id],
    )

    view_id = util.ref(cr, "__export__report_lease_invoice_document_jro")
    cr.execute(
        """
        UPDATE ir_ui_view
        SET arch_db = replace(replace(replace(replace(replace(arch_db,'o.date_invoice', 'o.invoice_date'),
                                'o.payment_term_id', 'o.invoice_payment_term_id'),
                                'o.payment_term_id.note', 'o.invoice_payment_term_id.note'),
                                'o.date_due', 'o.invoice_date_due'),
                                'l.invoice_line_tax_ids','l.tax_ids'),
        WHERE id = %s
            """,
        [view_id],
    )
    
    '''
        <div t - if = "not is_html_empty(o.narration)" name = "comment" >
            <span t - field = "o.narration" / >
        </div>
        to
        <!-- <p t-if="o.comment">
            <span t-field="o.comment"/>
        </p> -->
    '''

    view_id = util.ref(cr, "studio_customization.report_invoice_docum_1d23d739-2031-46ba-8a69-eaa442f849c0")
    cr.execute(
        """
        UPDATE ir_ui_view
        SET arch_db = replace(replace(replace(replace(replace(arch_db,'o.type', 'o.move_type'),
                                'o.reference', 'o.ref'),
                                'line.uom_id', 'line.product_uom_id'),
                                'line.invoice_line_tax_ids','line.tax_ids'),
                                'o.comment', 'o.narration'),
        WHERE id = %s
        """,
        [view_id],
    )


    '''
    remove line: <td class="d-none"><span t-field="line.origin"/></td>

    replace complete clearfix node
    '''
