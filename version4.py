import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

# Function to convert the dataframe to a CSV
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to generate a PDF
class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_left_margin(21)
        self.set_right_margin(21)

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Blue Earth County Career Workforce Center Experience', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_experience(self, data):
        self.chapter_title("Customer Service Rating")
        self.chapter_body(str(data['Customer Service Rating'][0]))

        self.chapter_title("Customer Service Feedback")
        self.chapter_body(data['Customer Service Feedback'][0])

        self.chapter_title("Experience Date")
        self.chapter_body(str(data['Experience Date'][0]))

        self.chapter_title("Experience Time")
        self.chapter_body(str(data['Experience Time'][0]))

        self.chapter_title("Employee Activities")
        self.chapter_body(data['Employee Activities'][0])

        self.chapter_title("Actual Experience")
        self.chapter_body(data['Actual Experience'][0])

        self.chapter_title("Prescribed Activities")
        self.chapter_body(data['Prescribed Activities'][0])

        self.chapter_title("Prescribed Notes")
        self.chapter_body(data['Prescribed Notes'][0])

        self.chapter_title("Experience Notes")
        self.chapter_body(data['Experience Notes'][0])

        # Add Employee Handbook Ratings
        self.chapter_title("Employee Performance Ratings")
        for criterion, rating in data['Employee Handbook Ratings'][0].items():
            self.chapter_body(f"{criterion}: {rating}/10")

def download_pdf(data):
    pdf = PDF()
    pdf.add_page()
    pdf.add_experience(data)

    pdf_output = BytesIO()
    pdf_str = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_str)
    pdf_output.seek(0)

    return pdf_output.read()

# Main function to run the app
def init_main():
    st.title("Blue Earth County Career Workforce Center")

    st.markdown(
        '[Visit the Minnesota Department of Employment and Economic Development (DEED) website](https://mn.gov/deed/)'
    )
    st.markdown(
        '[View the Workforce Development Policy](https://apps.deed.state.mn.us/ddp/PolicyDetail.aspx?pol=469)'
    )

    # Removed the Code of Conduct selection
    customer_service_rating = st.slider("Rate the customer service experience (1-5)", 1, 5)
    customer_service_feedback = st.text_area("Provide your qualitative feedback on the customer service experience")
    experience_date = st.date_input("Select the day of the experience")
    experience_time = st.time_input("Select the time of the experience")
    employee_activities = st.text_area("Describe the activities of the employees at the Career Workforce Center")
    actual_experience = st.text_area("Describe what actually happened during your experience")
    prescribed_activities = st.text_area("Describe any activities prescribed by the employees")
    prescribed_notes = st.text_area("Any notes regarding the prescribed activities")
    experience_notes = st.text_area("Any other notes regarding the experience")

    # Criteria from Employee Handbook for grading
    handbook_criteria = [
        "Act Professional and with Integrity",
        "Treat all people with respect",
        "Develop and maintain positive relationships",
        "Handle situations with integrity",
        "Maintain confidences and share credit",
        "Provide Customer Service",
        "Greet customers positively",
        "Provide timely and courteous assistance",
        "Communicate clearly",
        "Actively listen and respond with empathy",
        "Ensure customer satisfaction",
        "Ask for feedback from customers",
        "Contribute to Organizational Goals",
        "Adjust positively to changes",
        "Support organizational goals",
        "Identify self-development areas"
    ]

    # Collect ratings for each criterion
    st.subheader("Evaluate CareerForce Employee Performance")
    employee_ratings = {}
    for criterion in handbook_criteria:
        rating = st.slider(f"{criterion}", 0, 10, 5)
        employee_ratings[criterion] = rating

    # Data dictionary
    data = {
        "Customer Service Rating": [customer_service_rating],
        "Customer Service Feedback": [customer_service_feedback],
        "Experience Date": [experience_date],
        "Experience Time": [experience_time],
        "Employee Activities": [employee_activities],
        "Actual Experience": [actual_experience],
        "Prescribed Activities": [prescribed_activities],
        "Prescribed Notes": [prescribed_notes],
        "Experience Notes": [experience_notes],
        "Employee Handbook Ratings": [employee_ratings]
    }

    df = pd.DataFrame(data)

    # CSV download
    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='blue_earth_county_experience.csv',
        mime='text/csv',
    )

    # PDF download
    pdf = download_pdf(data)
    st.download_button(
        label="Download data as PDF",
        data=pdf,
        file_name='blue_earth_county_experience.pdf',
        mime='application/octet-stream'
    )

if __name__ == '__main__':
    init_main()
