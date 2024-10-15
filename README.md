# pdf-cover-letter-agent

## Description

pdf-cover-letter-agent is a Python tool that automates the creation of personalized cover letters in PDF format. By extracting job descriptions from Notion and utilizing OpenAI's GPT model, it fills placeholders in a customizable template and generates professional PDFs tailored to the job's language.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/mxALWQWPnX0/0.jpg)](https://www.youtube.com/watch?v=mxALWQWPnX0)

## Features

- **Job Description Extraction**: Reads job descriptions directly from Notion pages.
- **Automated Cover Letter Generation**: Uses GPT to personalize cover letters, filling in all placeholders with relevant details.
- **PDF Export**: Converts the generated cover letter into a well-formatted PDF document.
- **Language Support**: Automatically writes the cover letter in the language of the job description (English or German).
- **Customizable Templates**: Easily modify the cover letter template to suit different industries or roles.

## Technologies Used

- Python
- OpenAI GPT-4 API
- Notion API
- ReportLab (for PDF generation)
- dotenv (for environment variable management)

## Prerequisites

Before running the project, ensure you have the following:

- Python 3.x installed on your machine.
- A Notion account with an API token.
- OpenAI API key.
- Required Python libraries (install via `pip`).

## Installation

1. Clone this repository:
    git clone <https://github.com/yourusername/pdf-cover-letter-agent.git>
    cd pdf-cover-letter-agent

2. Create a `.env` file in the project root directory and add your API keys:
    OPENAI_API_KEY=your_openai_api_key
    NOTION_API_KEY=your_notion_api_key

3. Install the required packages:
    pip install -r requirements.txt

## Usage

1. Ensure you have a Notion page set up with the job description you want to use.
2. Update the `PAGE_ID` variable in the script to the ID of your Notion page.
3. Run the script:
    python test_cover_export.py

4. The generated PDF cover letter will be saved in the "Exported Cover Letters" directory.

## Customization

- Modify the `generate_cover_letter` function to change the cover letter template or the way information is extracted from the job description.
- Adjust the PDF styles in the `export_to_pdf` function to change the appearance of the generated documents.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for any feature requests or bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact:

- **Luis Felipe Pellegrini Meloni**
- [LinkedIn Profile](https://www.linkedin.com/in/lfpmeloni/)
