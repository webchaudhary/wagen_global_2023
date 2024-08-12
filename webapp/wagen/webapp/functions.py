#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 23:27:45 2021

@author: lucadelu
@author: spareeth
@author: AmanChawdhary
"""
import os
import sys
import time
from datetime import date
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
import pandas as pd
from bs4 import BeautifulSoup
import jinja2
from weasyprint import HTML
from django.template.loader import render_to_string


def send_mail_attach(sub, mess, to, attach):
    """Send email with attachment"""
    try:
        email = EmailMessage(
            sub,
            mess,
            settings.EMAIL_ADDR,
            [to],
        )
        email.attach_file(attach)
        email.send()
    except Exception as e:
        if e[0] == 551 and 'message sending quota exceeded' in e[1]:
            time.sleep(120)
            send_mail_attach(sub, mess, to, attach)
        else:

            return {"result": "There was an error sending email to {}".format(to),
                    "error": e}
    return True


def get_date():
    "Get today's date in German format"
    today = date.today()
    return today.strftime("%Y-%m-%d")

# -----------------------------------
# just for pdf generation testing purpose
# -----------------------------------
# def render_html(jobid, area):
#     """Render html page using jinja"""
#     template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(settings.BASE_DIR, 'webapp', "templates"))
#     template_env = jinja2.Environment(loader=template_loader)
#     template_file = "report.html"
#     template = template_env.get_template(template_file)
#     output_text = template.render(area=area.name, settings=settings, job=jobid)
#     html_path = os.path.join(settings.MEDIA_ROOT, jobid, 'index.html')
#     with open(html_path, 'w') as html_file:
#         html_file.write(output_text)
#     return html_path


def render_prod_html(jobid, area, stats):
    """Render html page using jinja"""
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(settings.BASE_DIR, 'webapp', "templates"))
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "report_custom_wb.html"
    template = template_env.get_template(template_file)
    output_text = template.render(area=area.name, settings=settings, job=jobid, stats=stats)
    html_path = os.path.join(settings.MEDIA_ROOT, jobid, 'index.html')
    with open(html_path, 'w') as html_file:
        html_file.write(output_text)
    return html_path


def render_pdf_html(jobid, area, stats):
    """Render HTML page using Django templates"""
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(settings.BASE_DIR, 'webapp', "templates"))
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "report_custom_pdf.html"
    template = template_env.get_template(template_file)

    base_url = settings.BASE_URL
    output_text = template.render(area=area.name, settings=settings, job=jobid, stats=stats, base_url=base_url)
    html_path = os.path.join(settings.MEDIA_ROOT, jobid, 'report1.html')
    with open(html_path, 'w') as html_file:
        html_file.write(output_text)
    return html_path


def render_pdf(htmlfile2, jobid):
    """Render pdf page from html using weasyprint"""
    table1path = os.path.join(settings.MEDIA_ROOT, jobid, 'Table1.csv')
    table2path = os.path.join(settings.MEDIA_ROOT, jobid, 'Table2.csv')
    table3path = os.path.join(settings.MEDIA_ROOT, jobid, 'Table3.csv')
    table4path = os.path.join(settings.BASE_DIR, 'webapp/static/data', 'datasource.csv')
    df_table_1 = pd.read_csv(table1path)
    df_table_2 = pd.read_csv(table2path)
    df_table_3 = pd.read_csv(table3path)
    df_table_4 = pd.read_csv(table4path)
    # Replace blank headers with empty strings
    df_table_1.columns = [col if not col.startswith('Unnamed') else '' for col in df_table_1.columns]
    df_table_2.columns = [col if not col.startswith('Unnamed') else '' for col in df_table_2.columns]
    df_table_3.columns = [col if not col.startswith('Unnamed') else '' for col in df_table_3.columns]
    df_table_4.columns = [col if not col.startswith('Unnamed') else '' for col in df_table_4.columns]
    # Convert the DataFrames to HTML tables with specified class and ID
    html_table_1 = df_table_1.to_html(index=False, classes='table table-bordered table-responsive', table_id='csv1Root', na_rep='')
    html_table_2 = df_table_2.to_html(index=False, classes='table table-bordered table-responsive', table_id='csv2Root', na_rep='')
    html_table_3 = df_table_3.to_html(index=False, classes='table table-bordered table-responsive', table_id='csv3Root', na_rep='')
    html_table_4 = df_table_4.to_html(index=False, classes='table table-bordered table-responsive', table_id='csv6Root', na_rep='')


    with open(htmlfile2, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find the table elements by their IDs
    table_element_1 = soup.find('table', {'id': 'csv1Root'})
    table_element_2 = soup.find('table', {'id': 'csv2Root'})
    table_element_3 = soup.find('table', {'id': 'csv3Root'})
    table_element_4 = soup.find('table', {'id': 'csv6Root'})


    # Replace the table content with the new HTML tables
    table_element_1.replace_with(BeautifulSoup(html_table_1, 'html.parser'))
    table_element_2.replace_with(BeautifulSoup(html_table_2, 'html.parser'))
    table_element_3.replace_with(BeautifulSoup(html_table_3, 'html.parser'))
    table_element_4.replace_with(BeautifulSoup(html_table_4, 'html.parser'))

    # Write the modified HTML back to the file
    report2path = os.path.join(settings.MEDIA_ROOT, jobid, 'report2.html')
    with open(report2path, 'w') as file:
        file.write(str(soup))

    reportpdfpath = os.path.join(settings.MEDIA_ROOT, jobid, 'report.pdf')
    HTML(report2path, base_url=settings.BASE_DIR).write_pdf(reportpdfpath)
    # HTML(report2path).write_pdf(reportpdfpath)
    return reportpdfpath

""" def render_pdf(html, jobid):
    with open(html) as inhtml:
        htmlstr = inhtml.read()
    # replace img to embed because they work really better in weasyprint
    htmlstr = htmlstr.replace("img", "embed")
    
    mystatic = "{ut}://{ba}{st}".format(ut=settings.HTTP_TYPE,
                                        ba=Site.objects.get_current().domain,
                                        st=os.path.join(settings.STATIC_URL))
    mymedia = "{ut}://{ba}{me}".format(ut=settings.HTTP_TYPE,
                                       ba=Site.objects.get_current().domain,
                                       me=os.path.join(settings.MEDIA_URL))
    htmlstr = htmlstr.replace("/static/", mystatic)
    htmlstr = htmlstr.replace("/media/", mymedia)
    with open("{}.new".format(html), 'w') as outhtml:
        outhtml.write(htmlstr)
    pdf = HTML(string=htmlstr).write_pdf()
    pdf_path = os.path.join(settings.MEDIA_ROOT, jobid, 'report.pdf')
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(pdf)
    return pdf_path """
    
