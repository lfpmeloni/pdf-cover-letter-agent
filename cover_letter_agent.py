import os
import openai
import json
import datetime
from dotenv import load_dotenv
from notion_client import Client
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY


# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")

# Configure OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize Notion Client
notion = Client(auth=NOTION_API_KEY)
PAGE_ID = "10de7e0f4b84809f8162c744000d9790"

def read_notion_page_content(page_id):
    """Read a Notion page and retrieve the job description."""
    try:
        blocks = notion.blocks.children.list(block_id=page_id).get('results', [])
        content = []

        for block in blocks:
            block_type = block.get('type')
            block_data = block.get(block_type, {})

            if block_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3']:
                text_elements = block_data.get('rich_text', [])
                text = "".join([part['plain_text'] for part in text_elements])
                content.append(text)

        return " ".join(content).strip()
    except Exception as e:
        print(f"Error fetching Notion page {page_id}: {str(e)}")
        return ""

def generate_cover_letter(job_description):
    """You are a cover letter assistant that will match the provided cover letter model to any job description I provide."""
    # Custom prompt for ChatGPT
    prompt = f"""
    Based on the following job description, extract the company name, job title, and any other necessary information, ensuring that every placeholder in the provided cover letter template is properly filled with relevant details from the job description. The final output should not contain any unfilled placeholders, and if any information is missing from the job description, replace the placeholder with an appropriate context-specific substitution (e.g., 'the hiring team' for [Hiring Manager's Name]). Ensure that the resulting cover letter is fully personalized with no remaining placeholders or generic text.
    1. Ensure that the cover letter is written ENTIRELY in the language of the provided job description. If the job description is in English, the entire body of the cover letter must be in English. Conversely, if the job description is in German, the entire body of the cover letter MUST be in German. 
    2. While ensuring that the response doesn't contain unescaped control characters or improperly formatted quotes, please keep the necessary newline breaks (\n\n) that indicate paragraph breaks in the final output.
    3. Make sure all placeholders are properly filled and when the information is not found, substituted accordingly.
    4. Make sure the response is in a JSON containing:
    - "Job Description Language" (English or German)
    - "Company Name"
    - "Location" (Company Address, City OR Country)
    - "Current date" (Todays date formatted based on the language)
    - "Job Title"
    - "Body" (Write the cover letter using the provided model and adjusting the placeholders accordingly to the information found on the job description.)

    Job Description:
    {job_description}

    Cover Letter Model:
    Dear [Hiring Manager's Name],

    Why I Do What I Do
    Throughout my career, I have continuously sought to blend technology, AI, and operations to drive meaningful change by enhancing processes, empowering teams, and accelerating business growth. I am particularly passionate about the role automation and AI play in fostering efficient, scalable, and sustainable business practices. This passion is informed by my practical experience across various industries, from fintech at iFood to AI-driven initiatives in my current projects, where I have witnessed the transformative power of optimizing systems with innovative technologies. My motivation is rooted in my desire to help organizations unlock their full potential through automation and intelligent process integration. This aspiration drives me to pursue the [Key Responsibility] of [Position Title], where I can [Core Responsibilities] and facilitate long-term growth.

    How I Deliver Impact
    I offer a unique blend of strategic foresight, technical expertise, and a proven track record of achieving business outcomes through AI and process optimization. For instance, at iFood, I led the development of a 100 million Euros credit portfolio by implementing data-driven growth strategies, streamlining workflows, and introducing automation tools like Salesforce to enhance sales processes. This experience taught me how AI and automation can substantially improve operational efficiency, drive revenue growth, and enhance customer experiences.

    Additionally, my MBA thesis, "Analysis of Restaurant Behavior on Delivery Platforms for Financial Products," provided critical insights into data analytics and behavioral patterns, directly contributing to iFood's sales growth. My ability to analyze complex datasets and translate findings into actionable strategies has been a cornerstone of my work. Currently, as a freelance AI agent developer, I am advancing my expertise in AI-driven automation through personal projects that integrate OpenAIs API to automate routine tasks. I approach each challenge with a combination of [Essential Skills], consistently aligning technology with business objectives to drive innovation.

    What I Offer
    I am excited about the opportunity to bring my passion for automation, operational leadership, and extensive experience in AI integration to [company_name]. With a background that encompasses fintech, process optimization, and AI development, I possess the depth and versatility necessary to address [Current Challenges] while fulfilling [Core Responsibilities]. My ability to [Relevant Skills] makes me confident in my capacity to contribute to [Role Impact and Values] at [company_name].

    I am eager to discuss how my experience, particularly in [Desired Attributes], aligns with your organization's goals and vision for the future.

    Thank you for considering my application. I look forward to the opportunity to contribute to your team's success.

    Best regards,
    Luis Felipe Pellegrini Meloni
   """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=2500
        )
        
        # Print the raw response for debugging
        raw_content = response['choices'][0]['message']['content']
        print("Raw response from GPT:", raw_content)

        # Clean the response to make it valid JSON
        cleaned_content = raw_content.replace("```json\n", "").replace("```", "").strip()

        return cleaned_content  # Return the cleaned content directly
    except Exception as e:
        print(f"Error generating cover letter: {e}")
        return None

def format_date_by_language(language):
    """Format the date based on the language."""
    today = datetime.date.today()
    if language == 'German':
        return today.strftime("%d.%m.%Y")  # German date format
    return today.strftime("%d/%m/%Y")  # English date format

def sanitize_filename(filename):
    """Sanitize the filename by replacing problematic characters."""
    return filename.replace('/', '_').replace('\\', '_').replace(':', '_')

def export_to_pdf(data):
    """Export the generated cover letter to a PDF using ReportLab."""
    # Create directory if it doesn't exist
    folder_path = os.path.join(os.path.dirname(__file__), "Exported Cover Letters")
    os.makedirs(folder_path, exist_ok=True)

    # Personalized output filename (sanitize to prevent issues with special characters)
    sanitized_company_name = sanitize_filename(data['Company Name'])
    sanitized_job_title = sanitize_filename(data['Job Title'])
    output_filename = os.path.join(folder_path, f"CoverLetter_{sanitized_company_name}_{sanitized_job_title}.pdf")
    
    doc = SimpleDocTemplate(output_filename, pagesize=A4)

    # Define styles
    styles = getSampleStyleSheet()

    # Header style
    header_style = ParagraphStyle(
        name="Header",
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER  # Center aligned
    )

    # Body and alignment styles
    body_style = ParagraphStyle(
        name="Body",
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=TA_LEFT, # Left aligned
        spaceBefore=12,
        spaceAfter=12
    )

    left_align_style = ParagraphStyle(
        name="LeftAlign",
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        alignment=TA_LEFT  # Left aligned
    )

    right_align_style = ParagraphStyle(
        name="RightAlign",
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        alignment=TA_RIGHT  # Right aligned
    )

    title_style = ParagraphStyle(
        name="Title",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=14,
        alignment=TA_LEFT  # Left aligned
    )

    # Line break and spacing
    spacer = Spacer(1, 0.15 * inch)

    # Language-specific details
    if data['Job Description Language'] == 'German':
        phone_label = "Mobil: 015734367141"
        to_label = "An"
        title_label = f"Anschreiben - {data['Job Title']}"
    else:
        phone_label = "Phone: +49 1573 4367141"
        to_label = "To"
        title_label = f"Cover Letter - {data['Job Title']}"

    # Build the content for the PDF
    content = [
        Paragraph("Luis Felipe Pellegrini Meloni", header_style),
        Paragraph("Untere Au 43, 76646 Bruchsal", header_style),
        Paragraph("felipemeloni@hotmail.com", header_style),
        Paragraph(phone_label, header_style),
        spacer,
        Paragraph(f"{to_label} {data['Company Name']}", left_align_style),
        Paragraph(f"{data['Location']}", left_align_style),
        spacer,
        Paragraph(f"Bruchsal, {format_date_by_language(data['Job Description Language'])}", right_align_style),
        spacer,
        Paragraph(title_label, title_style),
        spacer,
        # Use the new function to create paragraphs from the body text
        *convert_body_to_paragraphs(data['Body'], body_style)  # Unpacking the list of paragraphs
    ]

    # Generate the PDF document
    doc.build(content)
    print(f"Cover letter saved as {output_filename}")

def convert_body_to_paragraphs(body_text, style):
    """Convert the body text into a list of Paragraph objects, preserving line breaks."""
    body_text = body_text.replace('\n', '\n\n')
    paragraphs = body_text.split('\n\n')  # Assuming double newlines denote paragraph breaks
    return [Paragraph(p.strip(), style) for p in paragraphs if p.strip()]  # Strip whitespace and filter out empty paragraphs

def main():
    """Main function to orchestrate cover letter generation."""
    # Step 1: Read the job description from Notion
    job_description = read_notion_page_content(PAGE_ID)

    if not job_description:
        print("No job description found.")
        return
    else:
        print("Successfully retrieved the job description from Notion.")

    # Step 2: Generate the cover letter and fetch required data
    cover_letter_json = generate_cover_letter(job_description)

    if not cover_letter_json:
        print("Cover letter generation failed.")
        return

    # Safely parse JSON using json.loads
    try:
        parsed_data = json.loads(cover_letter_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    # Extract necessary information from parsed JSON
    print("Retrieved Data from GPT.")

    # Step 3: Export the generated cover letter to a PDF
    export_to_pdf(parsed_data)

    print("PDF generation was successful.")

if __name__ == "__main__":
    main()
