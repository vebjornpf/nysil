from django.shortcuts import render

def admin_index(req):
    return render(req,'adminpage/admin_header.html')
