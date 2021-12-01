# -*- coding: utf-8 -*-
from odoo import http,_
from odoo.http import request, route
import base64
from io import BytesIO
from odoo.tools.mimetypes import guess_mimetype
File_Type = ['application/pdf', 'image/jpeg', 'image/png']  # allowed file types

class services(http.Controller):



    @http.route('/services', auth='user', website=True, type='http')
    def services(self, **kw):
        services = request.env['services'].sudo().search([])
        values = {'services': services}
        return request.render("custom_website.services_template", values)

    @http.route('''/services/<model("services"):service>''', auth='user', website=True, type='http')
    def service_details(self, service):
        partner = request.env.user.partner_id
        values = {'service': service,'partner':partner}
        return request.render("custom_website.service_form_application", values)

    @http.route('/apply/submit',method='post' ,auth='user', website=True, type='http')
    def service_apply_submit(self, **post):
        client_request = request.env['clients.requests'].sudo().create(post)
        if client_request :
            return request.render("custom_website.thank_u_page")

    @route(['/my/documents'], type='http', auth="user", website=True)
    def shared_documents(self, **kw):
        partner = request.env.user.partner_id
        values = {}
        attachment_ids  = request.env['ir.attachment'].sudo().search([('res_model','=','res.partner'),('res_id','=',partner.id)])
        values.update({'attachment_ids': attachment_ids,
                       'page_name': 'shared_documents'})
        qcontext = http.request.httprequest.full_path
        request.session['shared_doc_url'] = qcontext

        return request.render("custom_website.shared_documents_template", values)

    @route(['/upload_my_documents'], method="post", type='http', auth="user", website=True)
    def upload_my_docs(self, **post):
        partner = request.env.user.partner_id
        if post['attach']:
            model_name = 'res.partner'
            record = request.env[model_name].browse(partner.id)
            file = post['attach']
            attachment_value = {
                        'name': file.filename,
                        'datas': base64.encodebytes(file.read()),
                        'res_model': model_name,
                        'res_id': record.id,
                    }

            file = post.get('attach')
            attachment = file.read()
            mimetype = guess_mimetype(base64.b64decode(base64.encodebytes(attachment)))
            if mimetype in File_Type:
                partner.write({'attachment_ids': base64.encodebytes(attachment)})

            attachment_id = request.env['ir.attachment'].sudo().create(attachment_value)
        return request.redirect('my/documents')

    @http.route(['/attachment/download'], type='http', auth="public", methods=['GET'], website=True)
    def download_attachment_2(self, attachment_id=0):
        # Check if this is a valid attachment id
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "mimetype", "res_model", "res_id", "type", "url"]
        )

        if attachment:
            attachment = attachment[0]
        else:
            return request.redirect('/shop')

        if attachment["type"] == "url":
            if attachment["url"]:
                return request.redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            data = BytesIO(base64.b64decode(attachment["datas"]))
            return http.send_file(data, filename=attachment['name'], as_attachment=True)
        else:
            return request.not_found()

    @http.route('''/remove/<model("ir.attachment"):attachment>''', type='http', auth="public", website=True)
    def remove_shared(self, attachment, **post):
        if attachment:
            partner_id = request.env.user.partner_id
            url = request.session['shared_doc_url']

            if partner_id:
                attachment_id = request.env['ir.attachment'].sudo().search([('id','=',attachment.id),('res_model','=','res.partner'),('res_id','=',partner_id.id)])
                if attachment_id:
                    attachment_id.sudo().unlink()
        return request.redirect(url)


