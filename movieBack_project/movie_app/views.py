import ast
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse,JsonResponse,HttpResponseBadRequest
from .models import *
from .serializers import *
from rest_framework import status
from django.views import View
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from django.db.models import Q
from pymongo import MongoClient
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            refresh=RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SignInView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data
            # token = Token.objects.get_or_create(user=user) 
            # return Response({'detail': 'POST answer', 'token': token[0].key})
            refresh=RefreshToken.for_user(user)
            return JsonResponse({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
            },status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def user_view(request: HttpRequest):
    if (request.method == 'GET'):
        user = User.objects.get(id=request.user.id)
        serialized_user = UserSerializer(user)
        return Response(serialized_user.data)
    
class GetAllMovies(APIView):
    def get(self,request):
        movies=Movie.objects.all().values()
        paginator = Paginator(movies,6)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        movie_pages=page_obj.object_list
        #serialized_output=MovieSerializer(movie_pages,many=True).data
        return JsonResponse(list(movie_pages),safe=False)
        # movies=Movie.objects.all().values()
        # paginator = Paginator(movies,2)
        # page_number=request.GET.get('page')
        # page_obj=paginator.get_page(page_number)
        # movie_pages=page_obj.object_list
        # return JsonResponse(list(movie_pages),safe=False)
        
    
    
class GetMovieDetails(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,movie_id):            
        try:            
            movie=Movie.objects.get(movie_id=movie_id)
            movie_details=MovieDetail.objects.get(movie_id=movie_id)
            response={
                "name": movie.name,
                "image": movie.image,
                "rating": movie.rating,
                "language":movie_details.language,
                "genre":movie_details.genre,
                "movie_id":movie.movie_id
            } 
            return JsonResponse(response,safe=False,status=200)             
        except Exception as e:
            return HttpResponseBadRequest(str(e))
        
class GetTheatresForMovie(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request,movie_id):       
        movie=Movie.objects.get(movie_id=movie_id) 
        theatres=movie.theatres.all()
        theatres_list=[]
        for each in theatres:
            theatre_data={
                "theatre_id": each.theatre_id,
                "theatre_name":each.theatre_name,                
            }
            movie_time=MovieTiming.objects.get(Q(movie_id=movie_id) & Q(theatre_id=each.theatre_id))
            theatre_data["timing"]=movie_time.timing
            theatres_list.append(theatre_data)
        response={
            "movie_id":movie_id,
            "name":movie.name,
            "theatres":theatres_list
        }
        return JsonResponse(response,safe=False,status=200)

class AddBookedSeats(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        dataGot=json.loads(request.body)
        val={}
        ids=[]
        for key,value in dataGot.items():
            val[key]=value
        print (val["theatre_name"])
        getTHId=Theatre.objects.get(theatre_name=val["theatre_name"])
        print(getTHId.theatre_id)        
        # record=MovieTiming.objects.get(Q(movie_id=val["movie_id"]) & Q(theatre_id=getTHId.theatre_id))  
        strToList=val["seat_no"]
        # strToList1=ast.literal_eval(strToList)
        for each in strToList:
             seats=Seat.objects.get(seat_no=each)
             ids.append(seats.seat_id)
        listTostr=str(ids)
        # record=MovieTiming.objects.get(Q(movie_id=val["movie_id"]) & Q(theatre_id=getTHId.theatre_id)) i dont know why this didnt work!!!
        # dataToAppend={
        #     "movie_id": val["movie_id"],
        #     "theatre_id": getTHId.theatre_id,
        #     "timing":record.timing,
        #     "bookedSeats":listTostr
        # }
        conn = MongoClient('localhost', 27017)
        try:             
             conn = MongoClient() 
             print("Connected successfully!!!") 
        except:   
             print("Could not connect to MongoDB") 
  
# database 
        db = conn.movieDB 
  
# Created or Switched to collection names: my_gfg_collection 
        collection = db.movie_app_movietiming
        rec_id1 = collection.update_one({"movie_id":val["movie_id"],"theatre_id":getTHId.theatre_id},{
             "$set":{ 
                        "bookedSeats":listTostr
                        }, 
              

        })
        cursor = collection.find() 
        for record in cursor: 
            print(record)
        return JsonResponse("success",safe=False)
         

        # setattr(record,record.bookedSeats,listTostr)
        # record.save()
       
        # return JsonResponse(record.bookedSeats,safe=False,status=200)
    
class AddTiming(View):
    def post(self,request):
        movie_data=json.loads(request.body)    
        try:
            MovieTiming.objects.create(**movie_data)
            return JsonResponse(movie_data,status=201)
        except Exception as e:
            return HttpResponseBadRequest(str(e))   
        
class GetBookedSeats(View):
    def get(self,request,theatre_name,movie_id):
        ids=[]
        getTHId=Theatre.objects.get(theatre_name=theatre_name)
        bookedseats=MovieTiming.objects.get(Q(movie_id=movie_id) & Q(theatre_id=getTHId.theatre_id))
        for each in ast.literal_eval(bookedseats.bookedSeats):             
            seats=Seat.objects.get(seat_id=each)
            ids.append(seats.seat_no)
        return JsonResponse(ids,safe=False)
    
class MovieFilterApi(View):
    def get(self,request):
        movie=request.GET.get("movie")
        city=request.GET.get('city')
        theatres_list=[]
        final_output=[]
        if movie:
            movies=Movie.objects.get(name=movie)
        theatres=movies.theatres.all()
        for each in theatres:
            theatre_data={
                "theatre_id": each.theatre_id,
                "theatre_name":each.theatre_name, 
                "city":each.city,          
            }
            theatre_data["name"]=movies.name
            theatre_data["image"]=movies.image
            theatre_data["rating"]=movies.rating
            theatres_list.append(theatre_data)
        for each in theatres_list:
            if each["city"] ==city:
                final_output.append(each)
        return JsonResponse(final_output,safe=False)
        