from django.shortcuts import render
from django.http import HttpResponse
import pickle
import numpy as np

def initialize_app():
    popular_df = pickle.load(open('myapp/data/courses.pkl', 'rb'))
    similarity_scores = pickle.load(open('myapp/data/similarity.pkl', 'rb'))
    return popular_df, similarity_scores

popular_df, similarity_scores = initialize_app()
courses_list = popular_df.to_dict('records')
context = {
        'courses': courses_list
    }
def index(request):
    return render(request, 'index1.html', context)

def recommend_ui(request):
    return render(request, 'recommend1.html')

def recommend(request):
    if request.method == 'GET':
        user_input = request.GET.get('user_input')
        try:
            index = popular_df[popular_df['course_name'] == user_input].index[0]
        except:
            return render(request, 'error.html', {'message': 'Course not found'})

        distances = sorted(list(enumerate(similarity_scores[index])), reverse=True, key=lambda x: x[1])
        data = []
        for i in distances[1:6]:
            item = []
            item.append(popular_df.iloc[i[0]].course_name)
            item.append(popular_df.iloc[i[0]].University)
            item.append(popular_df.iloc[i[0]].difficulty_level)
            item.append(popular_df.iloc[i[0]].course_rating)
            data.append(item)
        print(data)
        return render(request, 'recommend1.html', {'data': data})
    return HttpResponse('Invalid request')
