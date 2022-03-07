from django.shortcuts import render
from googletrans import Translator

# Create your views here.
def index(request):
    context = {}
    if request.method == "POST":
        bf = request.POST.get("bf")
        fr = request.POST.get("fr")
        to = request.POST.get("to")
        translator = Translator()
        if bf:
            trans = translator.translate(bf, src=fr, dest=to)
            context.update({
                "af" : trans.text,
                "bf" : bf,
                "fr" : fr,
                "to" : to,
            })
    return render(request, "trans/index.html", context)

# import googletrans

# print(googletrans.LANGUAGES)
# print(translator.detect(text1))

# trans1 = translator.translate(text1, src='en', dest='kn')
# print("English to Japanese: ", trans1.text)
