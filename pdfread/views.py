from django.shortcuts import render
import pdfplumber
# Create your views here.
def 제거(st):
    for i in "�":
        st.replace(i, "")
    return st

def index(request):
    context = {}
    if request.method == "POST":
        p = request.FILES.get("pdf")
        pdf = pdfplumber.open(p)
        num = len(pdf.pages)
        st = ""
        for i in range(num):
            st += "="*40 + "\n"
            st += f"{i+1} PAGE TEXTS" + "\n"
            st += "="*40 + "\n"
            st += pdf.pages[i].extract_text()
            st += "\n\n"
        print(st)
        context["st"] = st
    return render(request, "pdfread/index.html", context)

