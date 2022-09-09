from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import ProfileForm
from .models import Profile,Movie,paidMovie,CustomUser,Video
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def getlist(request):
    movie=paidMovie.objects.all()
    print(movie)

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # return redirect('profile/') or
            return redirect('NetflixApp:profile_list')
        return render(request,'index.html')

method_decorator(login_required,name='dispatch')
class ProfileList(View):
    def get(self,request, *args, **kwargs):
        profiles=request.user.profiles.all()
        return render(request,'profileList.html',{'profiles':profiles})

method_decorator(login_required,name='dispatch')
class ProfileCreate(View):
    def get(self,request, *args, **kwargs):
        #form for creating a profile
        form=ProfileForm()
        return render(request,'profileCreate.html',{'form':form})

    def post(self,request, *args, **kwargs):
        form=ProfileForm(request.POST or None)

        if form.is_valid():
            # print(form.cleaned_data) #returns data in form of dictionary
            profile=Profile.objects.create(**form.cleaned_data)
            if profile:
                request.user.profiles.add(profile) #use add for manytomany field
                return redirect('NetflixApp:profile_list')
        return render(request,'profileList.html',{'form':form})


method_decorator(login_required,name='dispatch')
class Watch(View):
    def get(self,request,profile_id,*args,**kwargs):
        try:
            profile=Profile.objects.get(uuid=profile_id)
            movie=Movie.objects.filter(age_limit=profile.age_limit)
            paid_movie=paidMovie.objects.filter(age_limit=profile.age_limit)
            purchasedMovie=request.user.purchased_movie.all()
            show_case=movie.first()
            if profile not in request.user.profiles.all():
                return redirect("NetflixApp:profile_list")

            return render(request,'movieList.html',{'movies':movie,'paid_movie':paid_movie, 'profile':profile,'show_case':show_case,'purchased_movie':purchasedMovie})
        
        except Profile.DoesNotExist:
            return render(request,'NetflixApp:profile_list')

method_decorator(login_required,name='dispatch')
class ShowMovieDetail(View):
    def get(self, request,movie_id, *args, **kwargs):
        try:
            movie=Movie.objects.get(uuid=movie_id)
            print(movie.flyer.url)
            return render(request,'movieDetail.html',{'movie':movie})

        except Movie.DoesNotExist:
            return redirect('NetflixApp:profile_list')

method_decorator(login_required,name='dispatch')
class ShowPaidMovieDetail(View):
    def get(self, request,movie_id, *args, **kwargs):
        try:
            movie=paidMovie.objects.get(uuid=movie_id)
            return render(request,'paidMovieDetail.html',{'movie':movie})

        except Movie.DoesNotExist:
            return redirect('NetflixApp:profile_list')

method_decorator(login_required,name='dispatch')
class ShowMovie(View):
    def get(self, request,movie_id, *args, **kwargs):
        try:
            movie=Movie.objects.get(uuid=movie_id)
            movie=movie.videos.values()
            # video=Video.objects.get(id=movie_id)
            return render(request,'showMovie.html',{'movie':list(movie)})

        except Movie.DoesNotExist:
            return redirect('NetflixApp:profile_list')

def home(request,amt,title):
    if request.method == "GET":
        # name = request.POST.get('name')
        amount = 100
 
        client = razorpay.Client(auth=("rzp_test_Eo5EGqrKuvDpQB", "r6hoSj0bCDGdsIIzlHJsTGOf"))

        payment = client.order.create({'amount':amount, 'currency': 'INR','payment_capture': '1'})

    return render(request, 'indexr.html',{'title':title,'amount':amount})

@csrf_exempt
def success(request):
    return render(request, "success.html")

def moviePurchased(request,movie_title):
    movie=paidMovie.objects.get(title=movie_title)
    request.user.purchased_movie.add(movie)
    return redirect('NetflixApp:watch/user.profile.uuid')
