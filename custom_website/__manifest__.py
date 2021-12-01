# -*- coding: utf-8 -*-
{
    'name': "Custom Client ERP",

    'summary': """
        the module's purpose is to follow up with clients""",

    'description': """
        the module's purpose is to follow up with client
    """,

    'author': "Amel Salah",
    'category': 'Website',
    'version': '0.1',
    'depends': ['base','portal'],

    # always loaded
    'data': [
        # 'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/services_template.xml',
        'views/service_application_form.xml',
        'views/thank_u_page.xml',
        'views/shared_documents_template.xml',
        'views/portal_page_templates.xml'


    ],


}
