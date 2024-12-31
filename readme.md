# Calendar Generator

This project generates a PDF calendar with weekly tide information for Salem, MA. The calendar is created using SVG templates and tide data retrieved from the NOAA API.

## Requirements

To run this project, you need to have the following Python packages installed:

```
requests
PyPDF2
svglib
reportlab
cairosvg
```

You can install these packages using the following command:

```sh
pip install -r requirements.txt
```

## Usage

The main script `CalendarGenerator.py` performs the following tasks:

1. **Retrieve Tide Information**: Fetches tide data from the NOAA API for each week within the specified date range.
2. **Create Weekly Pages**: Generates a PDF page for each week using an SVG template. The template is updated with the week number and tide information.
3. **Combine Weekly PDFs**: Combines all the weekly PDF pages into a single PDF file named `Calendar.pdf`.

### Functions

- `get_tide_info(start_date, end_date)`: Fetches tide predictions from the NOAA API for the given date range.
- `create_week_page(week_number, page_data)`: Creates a PDF page for the specified week number using the provided tide data.
- `create_calendar(start_date, end_date)`: Generates weekly PDF pages for the date range from `start_date` to `end_date`.
- `combine_week_pdfs()`: Combines all the weekly PDF pages into a single PDF file.

### Example Usage

To generate a calendar for the year 2025, you can run the following code:

```python
create_calendar(datetime.date(2024, 12, 30), datetime.date(2025, 12, 29))
combine_week_pdfs()
```

This will create a `Calendar.pdf` file with weekly tide information for the specified date range.

## Template

The SVG template file `Template.svg` should contain placeholders for the week number (`NN`) and tide information (`XXXXXXXXX` for dates and `TTTTTTTTTT` for tide details). These placeholders will be replaced with actual data during the PDF generation process.

## Notes

- Ensure that the `Template.svg` file is present in the same directory as the script.
- The script will remove intermediate SVG and PDF files after combining them into the final `Calendar.pdf`.
