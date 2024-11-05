from django.shortcuts import render
from rest_framework.views import APIView
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
import os
import google.generativeai as genai

# إعداد مفتاح الـ API لـ Generative AI
genai.configure(api_key="AIzaSyC_7sXsoqlmDMWVysUZQn1SUa4-KkAYlyw")

class ResumeBuilder:
    def __init__(self, user_data):
        self.data = user_data

    def generate_summary_with_ai(self):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Write a professional summary for a resume based on this data: {self.data['name']}, {self.data['email']}, {self.data['phone']}, skills: {', '.join(self.data['skills'])}."
        response = model.generate_content([prompt])
        return response.text

    def generate_experience_with_ai(self):
        model = genai.GenerativeModel('gemini-1.5-flash')
        experiences = self.data['work_experience']
        prompt = f"Generate the experience section for a resume based on the following data: {experiences}."
        response = model.generate_content([prompt])
        return response.text

    def generate_education_with_ai(self):
        model = genai.GenerativeModel('gemini-1.5-flash')
        education = self.data['education']
        prompt = f"Generate the education section for a resume based on the following data: {education}."
        response = model.generate_content([prompt])
        return response.text

    def generate_skills_with_ai(self):
        model = genai.GenerativeModel('gemini-1.5-flash')
        skills = self.data['skills']
        prompt = f"Generate the skills section for a resume based on the following skills: {', '.join(skills)}."
        response = model.generate_content([prompt])
        return response.text

    def generate_resume(self):
        pdf_file = "resume.pdf"
        document = SimpleDocTemplate(pdf_file, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # معلومات شخصية
        story.append(Paragraph(self.data['name'], styles['Title']))
        story.append(Paragraph(self.data['email'], styles['Normal']))
        story.append(Paragraph(self.data['phone'], styles['Normal']))
        story.append(Spacer(1, 12))

        # ملخص شخصي باستخدام الـ AI
        story.append(Paragraph("Summary:", styles['Heading2']))
        summary_text = self.generate_summary_with_ai()
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 12))

        # الخبرة باستخدام الـ AI
        story.append(Paragraph("Experience:", styles['Heading2']))
        experience_text = self.generate_experience_with_ai()
        story.append(Paragraph(experience_text, styles['Normal']))
        story.append(Spacer(1, 12))

        # التعليم باستخدام الـ AI
        story.append(Paragraph("Education:", styles['Heading2']))
        education_text = self.generate_education_with_ai()
        story.append(Paragraph(education_text, styles['Normal']))
        story.append(Spacer(1, 12))

        # المهارات باستخدام الـ AI
        story.append(Paragraph("Skills:", styles['Heading2']))
        skills_text = self.generate_skills_with_ai()
        story.append(Paragraph(skills_text, styles['Normal']))

        # ل PDF
        document.build(story)

        return pdf_file

class ResumeAPIView(APIView):
    def post(self, request):
        user_data = request.data
        resume = ResumeBuilder(user_data)
        pdf_file = resume.generate_resume()

        with open(pdf_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_file}"'
        
        os.remove(pdf_file)

        return response
