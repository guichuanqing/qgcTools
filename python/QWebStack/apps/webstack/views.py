from django.core.files.storage import default_storage
from django.shortcuts import render
from .models import Category, SubCategory, Site
from .forms import UploadXmindForm
from .countXmindTestCase import xmind_parse_file

# Create your views here.

def index_view(request):
    cates = Category.objects.all()
    total = []
    for cate in cates:
        subcates = SubCategory.objects.filter(parent=cate)
        c_res = {'cate':cate, 'subcate':[]}
        for subcate in subcates:
            sites = Site.objects.filter(category=subcate)
            c_res['subcate'].append({'subcate':subcate,'sites':sites})
        total.append(c_res)
    context = {
        "data": total
    }
    return render(request, 'webstack/index.html', context=context)

# def link_view(request):
#     cates = Category.objects.all()
#     total = []
#     for cate in cates:
#         subcates = SubCategory.objects.filter(parent=cate)
#         c_res = {'cate':cate, 'subcate':[]}
#         for subcate in subcates:
#             sites = Site.objects.filter(category=subcate)
#             c_res['subcate'].append({'subcate':subcate,'sites':sites})
#         total.append(c_res)
#     context = {
#         "data": total
#     }
#     return render(request, 'webstack/link.html', context=context)

def upload_xmind(request):
    if request.method == 'POST':
        form = UploadXmindForm(request.POST, request.FILES)
        if form.is_valid():
            xmind_file = form.cleaned_data['xmind_file']
            file_path = default_storage.save(xmind_file, xmind_file)
            local_file_path = default_storage.path(file_path)
            result_lines = xmind_parse_file(local_file_path)
            return render(request, 'webstack/result.html', {'result_lines': len(result_lines)})
    else:
        form = UploadXmindForm()
    return render(request, 'webstack/upload.html', {'form': form})

