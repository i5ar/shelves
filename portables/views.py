from django.shortcuts import render
from django.http import HttpResponse
from django.templatetags.static import static
from django.utils import lorem_ipsum
from django.utils.translation import ugettext as _

# from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.graphics.shapes import Drawing, Line, String

import datetime
from io import BytesIO
from http import client

from .forms import DownloadForm
from .models import ContractModel, DownloadModel

# https://docs.djangoproject.com/en/1.8/howto/outputting-pdf/
def choose_contract(request):

    if request.method == 'POST':
        form = DownloadForm(request.POST)
        if form.is_valid():

            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="attestato.pdf"'


            buffer = BytesIO()


            formatted_date = datetime.datetime.now().strftime("%d/%m/%Y")
            formatted_time = datetime.datetime.now().strftime("%H:%M")
            # full_name = form.cleaned_data['name']
            company_name = form.cleaned_data['recipient'].contract.company.name
            company_address_list = [form.cleaned_data['recipient'].contract.company.address, ]
            contract_title = form.cleaned_data['recipient'].contract.title
            contract_content = form.cleaned_data['recipient'].contract.content

            recipient = form.cleaned_data['recipient'].recipient
            operation = form.cleaned_data['recipient'].operation

            tep = form.cleaned_data['recipient'].tep
            co2 = form.cleaned_data['recipient'].co2
            trees = form.cleaned_data['recipient'].trees

            p = SimpleDocTemplate(response, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18, pagesize=landscape(A4))

            # NOTE: Static files
            static_watermark = static('portables/images/watermark.png')
            static_logo = static('portables/images/logo.png')
            absolute_uri = request.build_absolute_uri()
            # NOTE: Check the HEAD
            # https://stackoverflow.com/questions/11261210/django-check-if-an-image-exists-at-some-particular-url
            conn = client.HTTPConnection(request.get_host())
            conn.request("HEAD", static_watermark)
            resp = conn.getresponse()
            head = dict(resp.getheaders())
            if head.get("Content-Type").startswith("image"):
                # NOTE: Development static path
                path_watermark = absolute_uri.replace(request.get_full_path(), static_watermark)
                path_logo = absolute_uri.replace(request.get_full_path(), static_logo)
            else:
                # NOTE: Production S3 static path
                path_watermark = static_watermark
                path_logo = static_logo
                # NOTE: Hardcoded static path
                # path_watermark = 'http://127.0.0.1:8000/static/portables/images/watermark.png'
                # NOTE: Using SITE_ID path
                # http://stackoverflow.com/questions/2345708/how-can-i-get-the-full-absolute-url-with-domain-in-django
                # path_watermark = ''.join(['http://', form.cleaned_data['recipient'].contract.company.site.domain, static('portables/images/watermark.png')])

            # http://stackoverflow.com/questions/8185438/reportlab-add-background-image-by-using-platypus
            def AllPageSetup(canvas, p):
                canvas.saveState()

                # NOTE: Header
                # canvas.drawString(72, 194*mm, 'top-left')
                # canvas.drawRightString(270*mm, 194*mm, 'top-right')

                # NOTE: Footer
                canvas.setFillColor(HexColor('#a2b9cf'))
                canvas.setFont("Helvetica", 8)
                canvas.drawString(72, 36, '%s, %s' % (company_name, company_address_list[0]))
                canvas.drawRightString(270*mm, 36, '%s' % (formatted_date, ))
                # canvas.drawRightString(270*mm, 36, '%d' % (p.page, ))

                # NOTE: Watermark Text
                # canvas.setFont('Helvetica', 24)
                # canvas.setStrokeGray(0.90)
                # canvas.setFillGray(0.90)
                # canvas.drawCentredString(140*mm, 82*mm, 'ENERGIA')

                # NOTE: Watermark Image
                # http://stackoverflow.com/questions/26128462/how-do-i-use-reportlabs-drawimage-with-an-image-url
                w, h = ImageReader(path_watermark).getSize()
                x, y = (landscape(A4)[0]/2 - w/2, 80)
                canvas.drawImage(path_watermark, x, y, width=w, preserveAspectRatio=True, mask='auto')

                canvas.restoreState()

            story=[]

            w, h = ImageReader(path_logo).getSize()
            aspect = h/float(w)
            logo = Image(path_logo,  width=w/3, height=(w/3*aspect))
            story.append(logo)
            story.append(Spacer(1, 24))

            # NOTE: Paragraph styles
            styles=getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
            styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
            styles.add(ParagraphStyle(name='Center Operation', alignment=TA_CENTER, leading=20))

            text = '<font size=20 color="#444655">%s</font>' % (recipient, )
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 16))

            text = '<font size=14 color="#444655">%s</font>' % (operation.upper(), )
            story.append(Paragraph(text, styles['Center Operation']))
            story.append(Spacer(1, 12))

            # for i in company_address_list:
            #     text = '<font size=12 color=#000>%s</font>' % (i.strip(), )
            #     story.append(Paragraph(text, styles["Normal"]))
            # story.append(Spacer(1, 12))

            # text = '<font size=12><b>%s</b></font>' % full_name.split()[0].strip()
            # story.append(Paragraph(text, styles["Normal"]))
            # story.append(Spacer(1, 12))

            text = '<font size=48 color="#a2b9cf"><b>%s</b></font>' % (contract_title.upper(), )
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 48))

            # contract_content = ''.join(str(e) for e in lorem_ipsum.paragraphs(3, False))
            text = '<font size=12 color="#444655">%s</font>' % (contract_content, )
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 48))

            text = '<font size=16 color="#444655">%s</font>' % ("A seguito dell'interveto sono state risparmiate:", )
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 24))

            text = '<font size=22 color="#444655">%s </font><font size=18 color="#444655">TEP (tonnellate equivlenti di petrolio) di energia primaria</font>' % tep
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 24))

            text = '<font size=22 color="#444655">%s </font><font size=18 color="#444655">tonnellate/anno di minori emissioni CO2</font>' % co2
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 24))

            text = '<font size=22 color="#444655">%s </font><font size=18 color="#444655">alberi salvati</font>' % trees
            story.append(Paragraph(text, styles["Center"]))
            story.append(Spacer(1, 24))

            # d = Drawing(0, 0)
            # d.add(Line(180, 0, 500, 0))
            # d.add(String(184, 4, company_name, fontName='Helvetica', fontSize=12))
            # story.append(d)
            # story.append(Spacer(1, 12))

            # text = '<font size=12>%s</font>' % (formatted_date, )
            # story.append(Paragraph(text, styles["Normal"]))
            # story.append(Spacer(1, 12))


            p.build(story, onFirstPage=AllPageSetup, onLaterPages=AllPageSetup)


            # NOTE: Add when using IO buffer
            # Get the value of the BytesIO buffer and write it to the response.
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)


            form.save()


            return response


    else:

        form = DownloadForm()

    return render(request, 'portables/index.html', {'form': form})
