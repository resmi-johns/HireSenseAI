from django.shortcuts import render
from PyPDF2 import PdfReader
import docx
import re
import google.generativeai as genai
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'HiresenseAI/index.html')

def dashboard(request):
    return render(request, 'HiresenseAI/dashboard.html')


def analyze_resume(request):

    if request.method == 'POST' and request.FILES.get('resume'):

        file = request.FILES['resume']
        text = ""

        # PDF
        if file.name.endswith('.pdf'):
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text()

        # DOCX
        elif file.name.endswith('.docx'):
            doc = docx.Document(file)
            for para in doc.paragraphs:
                text += para.text + " "

        text_lower = text.lower()

        score = 0
        found_skills = []

        skills = [
            'python','java','html','css',
            'javascript','django','sql',
            'c','c++','php','excel'
        ]

        for skill in skills:
            if skill in text_lower:
                found_skills.append(skill.title())
                score += 5

        # Sections
        sections = ['education','skills','experience','project']
        found_sections = []

        for sec in sections:
            if sec in text_lower:
                found_sections.append(sec.title())
                score += 10

        # Email
        if re.search(r'\S+@\S+', text):
            score += 10

        # Phone
        if re.search(r'\d{10}', text):
            score += 10

        if score > 100:
            score = 100

        context = {
            'score': score,
            'skills': found_skills,
            'sections': found_sections,
            'filename': file.name,
            'resume_text': text
        }

        return render(request, 'HiresenseAI/result.html', context)

    return render(request, 'HiresenseAI/dashboard.html')


def gemini_suggestions(request):

    if request.method == 'POST':

        text = request.POST.get('resume_text', '')

        genai.configure(api_key="AIzaSyDokzbi6YAjJJHAJBHgLf76R7pxZ6ml8Bc")

        model = genai.GenerativeModel("gemini-2.5-flash-lite")


        prompt = f"""
        Analyze this resume and give suggestions:

        {text}

        Give:
        - Missing skills
        - Better summary
        - ATS improvements
        - Do NOT use markdown
        - Do NOT use # or * symbols
        """

        response = model.generate_content(prompt)

        return render(request, 'HiresenseAI/gemini.html', {
            'suggestions': response.text
        })

    return render(request, 'HiresenseAI/dashboard.html')


def login_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/launch/')

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login/')

    return render(request, 'HiresenseAI/login.html')




def signup_page(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('/signup/')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists. Try a different username")
            return redirect('/signup/')

        user=User.objects.create_user(
            username=username,
            password=password,
             )
        login(request, user)
        messages.success(request, "Account created successfully")
        return redirect('/launch/')

    return render(request, 'HiresenseAI/signup.html')

    
@login_required
def launch_page(request):
    return render(request, 'HiresenseAI/launch.html')


