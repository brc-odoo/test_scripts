# -*- coding: utf-8 -*-

from odoo.upgrade import util

import pudb
def migrate(cr, version):
    pu.db
    view_id = util.ref(cr, "__export__.report_delivery_document_inherited_jro")
    with util.edit_view(cr, view_id=view_id) as arch:
        node = arch.find(".//xpath[@expr=\"//p[@t-if='doc.payment_term_id.note']\"]")
        node.set("expr", "//p[@t-if='not is_html_empty(doc.payment_term_id.note)']")

    view_id = util.ref(cr, "__export__.report_delivery_document_inherited_jro")
    '''
        <xpath expr="//th[@name='td_sched_date_h']" position="before">
            <th>
                <strong>Customer Ref.</strong>
            </th>
        </xpath>
        <xpath expr="//td[@name='td_sched_date']" position="before">
            <td>
                <span t-field="o.x_cust_ref"/>
            </td>
        </xpath>
    '''
    # to
    '''
        <xpath expr="//div[@name='div_sched_date']" position="before">
            <div t-if="o.x_cust_ref" class="col-auto">
                <strong>Customer Ref.</strong>
                <br/>
                <span t-field="o.x_cust_ref"/>
            </div>
        </xpath>
    '''

    view_id = util.ref(cr, "__export__.report_shipping2_inherit")
    # comment out sections
    '''
    <xpath expr="//table/thead/tr/th[5]" position="replace"/>
    <xpath expr="//table/tbody/tr/td[5]" position="replace"/>
    '''
