import streamlit as st
import smtplib
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


st.set_page_config(
    page_title="AI Job Application Mail Sender",
    page_icon="📧",
    layout="centered"
)

st.title("📧 AI Job Application Mail Sender")

# GMAIL CREDENTIALS

sender_email = "harshit73010@gmail.com"
app_password = "Gmail_APP_PASSWORD"


# RECRUITER EMAIL


receiver_email = st.text_input(
    "Recruiter Email",
    placeholder="recruiter@company.com"
)

# JOB ROLE

job_role = st.selectbox(
    "Select Role",
    [
        "AI/ML Engineer",
        "AI/ML Intern",
        "AI/ML Fresher",
        "Agentic AI Engineer",
        "AI Engineer",
        "AI Developer",
        "GenAI Engineer",
        "Machine Learning Engineer",
        "ML Intern",
        "Data Scientist",
        "Python Developer",
        "Python Internship"
    ]
)

subject = f"Application for {job_role} Position"


# RESUME UPLOAD

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)


# EMAIL BODY


default_body = f"""
Dear Hiring Team,

I am writing to express my interest in the {job_role} position. I have hands-on experience in Python, Machine Learning, RAG based Chatbots, Generative AI, AI Agents, and Streamlit-based applications, and I am eager to contribute my skills to your team.

Please find my resume attached for your review. I would welcome the opportunity to discuss how my background aligns with your requirements.

Thank you for your time and consideration.
Best Regards,

Harsh Kumar Sharma
Email: harshit73010@gmail.com
Phone: 7082723887
GitHub: https://github.com/harshit73010
LinkedIn: https://www.linkedin.com/in/harshsharma73
"""

body = st.text_area(
    "Email Body",
    value=default_body,
    height=350
)


# SEND EMAIL


if st.button("📨 Send Email"):

    # Validation
    if not sender_email:
        st.error("Please enter your Gmail address.")
        st.stop()

    '''if not app_password:
        st.error("Please enter your Gmail App Password.")
        st.stop()'''

    if not receiver_email:
        st.error("Please enter recruiter email.")
        st.stop()

    if uploaded_resume is None:
        st.error("Please upload your resume PDF.")
        st.stop()

    try:

        # Create email
        msg = MIMEMultipart()

        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Email body
        msg.attach(MIMEText(body, "plain"))

        # PDF attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(uploaded_resume.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{uploaded_resume.name}"'
        )

        msg.attach(part)

        # SMTP connection
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)

        st.success(
            f"✅ Email sent successfully to {receiver_email}"
        )

    except smtplib.SMTPAuthenticationError:
        st.error(
            "❌ Gmail Authentication Failed.\n\n"
            "Use a Gmail App Password, not your normal Gmail password."
        )

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
