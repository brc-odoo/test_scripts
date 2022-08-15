# -*- coding: utf-8 -*-

from odoo.upgrade import util

import pudb
def migrate(cr, version):
    # 2862020
    pu.db
    cr.execute(
        """
            UPDATE ir_ui_view
                SET active = 'f'
            WHERE id = %s
        """,
        [util.ref(cr, "__export__.report_invoice_document_inherited_jro")]
    )

    view_id = util.ref(cr, "studio_customization.report_saleorder_doc_dce9c8e6-95fd-40b6-b4aa-a1d351f9a8e9")
    arch = """
    <t t-name="sale.report_saleorder_document_copy_1">
    <t t-call="web.external_layout">
        <t t-set="doc" t-value="doc.with_context(lang=doc.partner_id.lang)" />
        <t t-set="forced_vat" t-value="doc.fiscal_position_id.foreign_vat"/> <!-- So that it appears in the footer of the report instead of the company VAT if it's set -->
        <t t-set="address">
            <div t-field="doc.partner_id"
                t-options='{"widget": "contact", "fields": ["address", "name"], "no_marker": True}' />
            <p t-if="doc.partner_id.vat"><t t-esc="doc.company_id.account_fiscal_country_id.vat_label or 'Tax ID'"/>: <span t-field="doc.partner_id.vat"/></p>
        </t>
        <t t-if="doc.partner_shipping_id == doc.partner_invoice_id
                            and doc.partner_invoice_id != doc.partner_id
                            or doc.partner_shipping_id != doc.partner_invoice_id">
            <t t-set="information_block">
                <strong t-if="doc.partner_shipping_id == doc.partner_invoice_id">Invoicing and Shipping Address:</strong>
                <strong t-if="doc.partner_shipping_id != doc.partner_invoice_id">Invoicing Address:</strong>
                <div t-field="doc.partner_invoice_id"
                t-options='{"widget": "contact", "fields": ["address", "name", "phone"], "no_marker": True, "phone_icons": True}'/>
                <t t-if="doc.partner_shipping_id != doc.partner_invoice_id">
                    <strong>Shipping Address:</strong>
                    <div t-field="doc.partner_shipping_id"
                        t-options='{"widget": "contact", "fields": ["address", "name", "phone"], "no_marker": True, "phone_icons": True}'/>
                </t>
            </t>
        </t>
        <div class="page">
            <div class="oe_structure"/>

            <t t-if="is_so_invoice">
                <h2 class="mt16">
                    <span>Invoice # </span>
                    <span t-field="doc.name"/>
                </h2>
            </t>
            <t t-if="not is_so_invoice">
                <h2>
                    <t t-if="not (env.context.get('proforma', False) or is_pro_forma)">
                        <span t-if="doc.state not in ['draft','sent']">Order # </span>
                        <span t-if="doc.state in ['draft','sent']">Quotation # </span>
                    </t>
                    <t t-if="env.context.get('proforma', False) or is_pro_forma">
                        <span>Pro-Forma Invoice # </span>
                    </t>
                    <span t-field="doc.name"/>
                </h2>
            </t>
            <div class="row mt32 mb32" id="informations">
                <div t-if="doc.client_order_ref" class="col-auto col-3 mw-100 mb-2">
                    <strong>Your Reference:</strong>
                    <p class="m-0" t-field="doc.client_order_ref"/>
                </div>
                <div t-if="doc.date_order and doc.state not in ['draft','sent']" class="col-auto col-3 mw-100 mb-2">
                    <strong>Order Date:</strong>
                    <p class="m-0" t-field="doc.date_order"/>
                </div>
                <div t-if="doc.date_order and doc.state in ['draft','sent']" class="col-auto col-3 mw-100 mb-2">
                    <strong>Quotation Date:</strong>
                    <p class="m-0" t-field="doc.date_order" t-options='{"widget": "date"}'/>
                </div>
                <div name="payment_term" t-if="doc.payment_term_id" class="col-auto col-3 mw-100 mb-2">
                    <strong>Payment Terms:</strong>
                    <p class="m-0" t-field="doc.payment_term_id"/>
                </div>
                <div class="col-3" t-if="doc.incoterm" groups="sale_stock.group_display_incoterm">
                    <strong>Incoterms:</strong>
                    <p t-field="doc.incoterm.code"/>
                </div>
                <div t-if="doc.validity_date and doc.state in ['draft', 'sent']" class="col-auto col-3 mw-100 mb-2" name="expiration_date">
                    <strong>Expiration:</strong>
                    <p class="m-0" t-field="doc.validity_date"/>
                </div>
            </div>

            <!-- Is there a discount on at least one line? -->
            <t t-set="display_discount" t-value="any(l.discount for l in doc.order_line)"/>

            <table class="table table-sm o_main_table">
                <thead style="display: table-row-group">
                    <tr>
                        <th name="th_description" class="text-left">Description</th>
                        <th class="text-center"><span>PID</span></th>
                        <th name="th_quantity" class="text-center">Quantity</th>
                        <th name="th_priceunit" class="text-center">Unit Price</th>
                        <th name="th_discount" t-if="display_discount" class="text-right" groups="product.group_discount_per_so_line">
                            <span>Disc.%</span>
                        </th>
                        <th name="th_taxes" class="text-center">Taxes</th>
                        <th class="text-center"><span>Discount (%)</span></th>
                        <th name="th_subtotal" class="text-center">
                            <span groups="account.group_show_line_subtotals_tax_excluded">Amount</span>
                            <span groups="account.group_show_line_subtotals_tax_included">Total Price</span>
                        </th>
                    </tr>
                </thead>
                <tbody class="sale_tbody">

                    <t t-set="current_subtotal" t-value="0"/>

                    <t t-foreach="doc.order_line" t-as="line">

                        <t t-set="current_subtotal" t-value="current_subtotal + line.price_subtotal" groups="account.group_show_line_subtotals_tax_excluded"/>
                        <t t-set="current_subtotal" t-value="current_subtotal + line.price_total" groups="account.group_show_line_subtotals_tax_included"/>

                        <tr t-att-class="'bg-200 font-weight-bold o_line_section' if line.display_type == 'line_section' else 'font-italic o_line_note' if line.display_type == 'line_note' else ''">
                            <t t-if="not line.display_type">
                                <td>
                                    <span t-field="line.name" style="display:inline-block;width:250px"/>
                                    <t t-if="line.product_id.l10n_in_hsn_code">
                                        <h6>
                                            <strong class="ml16">HSN/SAC Code:</strong>
                                            <span t-field="line.product_id.l10n_in_hsn_code"/>
                                        </h6>
                                    </t>
                                </td>
                                <td class="text-right">
                                    <span t-field="line.pid_ids"/>
                                </td>
                                <td class="text-right">
                                    <span t-field="line.product_uom_qty"/>
                                    <span t-field="line.product_uom"/>
                                </td>
                                <td name="td_priceunit" class="text-right">
                                    <span t-field="line.price_unit"/>
                                </td>
                                <td t-if="display_discount" class="text-right" groups="product.group_discount_per_so_line">
                                    <span t-field="line.discount"/>
                                </td>
                                <td name="td_taxes" class="text-right">
                                    <span t-esc="', '.join(map(lambda x: (x.description or x.name), line.tax_id))"/>
                                </td>
                                <td style="width:70px" class="text-right">
                                    <span t-field="line.discount"/>
                                </td>

                                <td name="td_subtotal" class="text-right o_price_total">
                                    <span t-field="line.price_subtotal" groups="account.group_show_line_subtotals_tax_excluded"/>
                                    <span t-field="line.price_total" groups="account.group_show_line_subtotals_tax_included"/>
                                </td>
                            </t>
                            <t t-if="line.display_type == 'line_section'">
                                <td name="td_section_line" colspan="99">
                                    <span t-field="line.name"/>
                                </td>
                                <t t-set="current_section" t-value="line"/>
                                <t t-set="current_subtotal" t-value="0"/>
                            </t>
                            <t t-if="line.display_type == 'line_note'">
                                <td name="td_note_line" colspan="99">
                                    <span t-field="line.name"/>
                                </td>
                            </t>
                        </tr>

                        <t t-if="current_section and (line_last or doc.order_line[line_index+1].display_type == 'line_section')">
                            <tr class="is-subtotal text-right">
                                <td name="td_section_subtotal" colspan="99">
                                    <strong class="mr16">Subtotal</strong>
                                    <span
                                        t-esc="current_subtotal"
                                        t-options='{"widget": "monetary", "display_currency": doc.pricelist_id.currency_id}'
                                    />
                                </td>
                            </tr>
                        </t>
                    </t>
                </tbody>
            </table>

            <div class="clearfix" name="so_total_summary">
                <div id="total" class="row" name="total">
                    <div t-attf-class="#{'col-6' if report_type != 'html' else 'col-sm-7 col-md-6'} ml-auto">
                        <table class="table table-sm">
                            <!-- Tax totals -->
                            <t t-set="tax_totals" t-value="json.loads(doc.tax_totals_json)"/>
                            <t t-call="account.document_tax_totals"/>
                        </table>
                    </div>
                </div>
            </div>

            <p t-if="doc.payment_term_id.note">
                <span t-field="doc.payment_term_id.note"/>
            </p>
            <p t-if="doc.x_tuv_terms_id.x_terms">
                <span t-field="doc.x_tuv_terms_id.x_terms"/>
            </p>

            <p id="fiscal_position_remark" t-if="doc.fiscal_position_id and doc.fiscal_position_id.sudo().note">
                <strong>Fiscal Position Remark:</strong>
                <span t-field="doc.fiscal_position_id.sudo().note"/>
            </p>
            <div t-if="doc.sale_order_option_ids and doc.state in ['draft', 'sent']">
                <t t-set="has_option_discount" t-value="any(doc.sale_order_option_ids.filtered(lambda o: o.discount != 0.0))"/>
                <h4>
                    <span>Optional Products</span>
                </h4>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th class="text-left">Description</th>
                            <th t-if="has_option_discount" groups="sale.group_discount_per_so_line" class="text-left"/>
                            <th class="text-right">Unit Price</th>
                        </tr>
                    </thead>
                    <tbody class="sale_tbody">
                        <tr t-foreach="doc.sale_order_option_ids" t-as="option">
                            <td>
                                <span t-field="option.name"/>
                            </td>
                            <td t-if="has_option_discount" groups="sale.group_discount_per_so_line">
                                <strong t-if="option.discount != 0.0" class="text-info">
                                    <t t-esc="((option.discount % 1) and '%s' or '%d') % option.discount"/>
% discount
                                </strong>
                            </td>
                            <td>
                                <strong class="text-right">
                                    <div t-field="option.price_unit" t-options="{&quot;widget&quot;: &quot;monetary&quot;, &quot;display_currency&quot;: doc.pricelist_id.currency_id}" t-att-style="option.discount and 'text-decoration: line-through' or None" t-att-class="option.discount and 'text-danger' or None"/>
                                    <div t-if="option.discount">
                                        <t t-esc="'%.2f' % ((1-option.discount / 100.0) * option.price_unit)"/>
                                    </div>
                                </strong>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div t-if="doc.signature" class="mt32 ml64 mr4" name="signature">
                <div class="offset-8">
                    <strong>Signature</strong>
                </div>
                <div class="offset-8">
                    <img t-att-src="image_data_uri(doc.signature)" style="max-height: 4cm; max-width: 8cm;"/>
                </div>
                <div class="offset-8 text-center">
                    <p t-field="doc.signed_by"/>
                </div>
            </div>

            <div class="oe_structure"/>

            <p t-field="doc.note" />
            <p t-if="not is_html_empty(doc.payment_term_id.note)">
                <span t-field="doc.payment_term_id.note"/>
            </p>
            <p id="fiscal_position_remark" t-if="doc.fiscal_position_id and not is_html_empty(doc.fiscal_position_id.sudo().note)">
                <strong>Fiscal Position Remark:</strong>
                <span t-field="doc.fiscal_position_id.sudo().note"/>
            </p>
        </div>
    </t>
</t>
    """
    cr.execute("UPDATE ir_ui_view SET arch_db = %s WHERE id = %s", [arch, view_id])

    view_id = util.ref(cr, "__export__.ir_ui_view_1138")

    arch = '''
        <data>
            <xpath expr="//field[@name='currency_id']" position="before">
                <field name="x_tuv_terms_id" required="1"/>
                <field name="x_sotypeq"/>
            <xpath expr="//field[@name='warehouse_id']" position="move"/>
            </xpath>
            <field name="partner_shipping_id" position="after">
                <xpath expr="//field[@name='client_order_ref']" position="move"/>
            </field>
        </data>
        '''
    cr.execute("UPDATE ir_ui_view SET arch_db = %s WHERE id = %s", [arch, view_id])
