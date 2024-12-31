import datetime
import requests
import re
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from PyPDF2 import PdfMerger
import os

def get_tide_info(start_date, end_date):
    station_id = "8442645"  # NOAA station ID for Salem, MA
    api_url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date={start_date}&end_date={end_date}&station={station_id}&product=predictions&datum=MLLW&time_zone=lst_ldt&units=english&interval=hilo&format=json"
    
    tide_data = None
    response = requests.get(api_url)
    if response.status_code == 200:
        tide_data = response.json()
        return tide_data['predictions']
    else:
        print(tide_data)
        return None

def create_week_page(week_number, page_data):
    with open('Template.svg', 'r') as file:
        svg_content = file.read()

    updated_svg_content = re.sub(r'NN', str(week_number), svg_content)
    for date in page_data:
        updated_svg_content = re.sub(r'XXXXXXXXX', date, updated_svg_content, count=1)
        num_tides = 0
        for tide in page_data[date]:
            time = tide['t'].split(' ')[1]
            height = tide['v']
            tide_type = tide['type']
            tide_description = ""
            if tide_type == "H":
                tide_description = "↑ " + time + " - " + height
            else:
                tide_description = "↓ "  + time + " - " + height
            updated_svg_content = re.sub(r'TTTTTTTTTT', tide_description, updated_svg_content, count=1)
            num_tides += 1
        while num_tides < 4:
            updated_svg_content = re.sub(r'TTTTTTTTTT', "", updated_svg_content, count=1)
            num_tides += 1   

    with open(f'week_{week_number}.svg', 'w') as file:
        file.write(updated_svg_content)

    drawing = svg2rlg(f'week_{week_number}.svg')
    renderPDF.drawToFile(drawing, f'week_{week_number}.pdf')
    os.remove(f'week_{week_number}.svg')

def create_calendar(start_date, end_date):
    current_date = start_date
    week_number = 1    
    while current_date <= end_date:
        page_data = {}
        print(f"Week {week_number}: {current_date.strftime('%Y-%m-%d')}")
        start_date = current_date.strftime('%Y%m%d')
        end_of_week = (current_date + datetime.timedelta(days=6)).strftime('%Y%m%d')
        tide_info = get_tide_info(start_date, end_of_week)
        if tide_info:
            for tide in tide_info:
                date = datetime.datetime.strptime(tide['t'], '%Y-%m-%d %H:%M')
                date_str = date.strftime('%Y-%m-%d')
                if date_str not in page_data:
                    page_data[date_str] = []
                page_data[date_str].append(tide)
        else:
            print(f"Could not retrieve tide information for {start_date}")
        create_week_page(week_number, page_data)
        current_date += datetime.timedelta(weeks=1)
        week_number += 1

def combine_week_pdfs():
    merger = PdfMerger()
    week_number = 1
    more = True

    while more:
        pdf_filename = f'week_{week_number}.pdf'
        if os.path.exists(pdf_filename):
            merger.append(pdf_filename)
            os.remove(pdf_filename)
            week_number += 1
        else:
            more = False
    
    if os.path.exists('Calendar.pdf'):
        os.remove('Calendar.pdf')
    with open('Calendar.pdf', 'wb') as output_pdf:
        merger.write(output_pdf)
    
    merger.close()
        
create_calendar(datetime.date(2024, 12, 30), datetime.date(2025, 12, 29))
combine_week_pdfs()
