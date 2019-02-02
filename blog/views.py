from django.shortcuts import render

posts = [
    {
        'author':'Jake',
        'title':'blog post 1',
        'content':'FIRST Post',
        'date_posted':"November 3rd, 2018"
    },
    {
        'author':'Jake',
        'title':'blog post 2',
        'content':'Second Post',
        'date_posted':'November 3rd, 2018'
    }
]
def home(request):
    context = {
        'posts' : posts
    }
    return render(request, 'blog/home.html',context)


def about(request):
    return render(request, 'blog/about.html',{'title':'About'})
