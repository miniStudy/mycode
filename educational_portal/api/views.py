import datetime
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from .serializers import * 
from datetime import timezone, datetime
from django.utils import timezone
from django.db.models.functions import TruncDate, TruncHour, TruncMinute
from rest_framework import status 
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
import math
import statistics
from django.core.files.storage import FileSystemStorage
import random
from django.http import Http404,JsonResponse
from django.db.models import Count,Sum, F, Case, When, Value, IntegerField, Q

#=========================================Boards======================================================

@api_view(['GET'])
def get_boards(request):
    result = Boards.objects.all()
    apidata = BoardsSerializer(result, many=True)
    return Response ({
        'data': apidata.data,
        'message' : 'Boards',
    })


@api_view(['POST', 'GET'])  
def api_update_boards(request):
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(Boards, pk=pk)
        data = request.data
        if request.method == "POST":
            form = BoardsSerializer(data = data, instance=instance, partial = True)
      
            if form.is_valid():
                form.save()
                return Response({
                'status': True,
                'message': 'Update success',
                'data': form.data
            })
            else:
                return Response({
                    'status': False,
                    'message': 'Error occur',
                    'Required Field': form.errors
                })
    
    if request.GET.get('update_id'):
        update_id = request.GET['update_id']
        update_data = Boards.objects.get(brd_id = update_id)
        serializers = BoardsSerializer(update_data)
        return Response({
            'status': True,
            'message': 'data updated',
            'data': serializers.data
        })

    if request.method == "POST":
        data = request.data
        form = BoardsSerializer(data = data)
        if form.is_valid():
            form.save()
            return Response({
                'status': True,
                'message': 'Insert successfully',
                'data': form.data
            })
        else:
            return Response({
                'status': True,
                'message': 'nothing happend',
                'Required Field': form.errors
            })
    return Response({
        'message':'something is wrong'
    })
    

    
@api_view(['POST', 'GET'])
def delete_boards(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Boards.objects.filter(brd_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete"
                })
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


# ===================================================Logic for Std=====================================================

@api_view(['GET'])
def get_stds(request):
    data = Std.objects.all()
    serializers = stdSerializer(data, many = True)
    return Response({
        'Message': 'Data of Students',
        'data': serializers.data
    })

@api_view(['POST', 'GET'])
def api_update_stds(request):
    brddata = Boards.objects.all()
    brd_serializers = BoardsSerializer(brddata, many = True)
    if request.GET.get('pk'):
        pk = request.GET['pk']
        instance = get_object_or_404(Std, pk=pk)
        data = request.data
        if request.method == "POST":
            form = stdSerializer(data = data, instance=instance, partial = True)
            if form.is_valid():
                form.save()
                return Response({
                    'status': 'Success',
                    'Message': 'Update successfully',
                    'data': form.data,
                    'brddata':brd_serializers.data,
                })
            else:
                return Response({
                    'status': 'Failed',
                    'message': 'Error occur',
                    'Required Field': form.errors
                })
    
    if request.GET.get('update_id'):
        update_id = request.GET['update_id']
        update_data = Std.objects.get(std_id = update_id)
        std_serializers = stdSerializer(update_data)
        return Response({
            'Status': 'Updated info',
            'data': std_serializers.data
        })
    
    if request.method == "POST":
        data = request.data
        form = stdSerializer(data = data)
        if form.is_valid():
            form.save()
            return Response({
                'status': True,
                'message': 'Insert successfully',
                'data': form.data
            })
        else:
            return Response({
                'status': True,
                'message': 'nothing happend',
                'data': form.errors
            })
        
    return Response({
        'message':'something is wrong'
    })


@api_view(['POST', 'GET'])
def api_delete_stds(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:    
                Std.objects.filter(std_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                    
                })
            
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


#=========================================================Subject==========================================================

@api_view(['GET'])
def api_subjects(request):
    data = Subject.objects.all()
    serializer = subjectsSerializer(data, many = True)

    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many= True)
   
    apidata = {
        'data' : serializer.data,
        'title' : 'Subjects',
        'std_data' : std_serializer.data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(sub_std__std_id = get_std)
            serializer = subjectsSerializer(data, many = True)
            get_std = Std.objects.get(std_id = get_std)  
            get_std_serializer = stdSerializer(get_std)
            apidata.update({'data' : serializer.data, 'get_std': get_std_serializer.data})

    return Response(apidata)
    


@api_view(['POST', 'GET'])
def api_update_subjects(request):
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)

    apidata = {
        'std_data': std_serializer.data
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std) 
        std_serializer = stdSerializer(std_data, many = True)
        get_std = Std.objects.get(std_id = get_std)
        get_std_serializer = stdSerializer(get_std)
        apidata.update({'get_std ':get_std_serializer.data,'std_data':std_serializer.data})

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Subject, pk=request.GET['pk'])
            data = request.data
            form = subjectsSerializer(data=data, instance=instance, partial= True)
            check = Subject.objects.filter(sub_name = data['sub_name'], sub_std__std_id = data['sub_std']).count()
            if check >= 1:
                return Response({
                    'Message': 'already exits'
                })
            else:
                if form.is_valid():
                    form.save()
                    return Response({
                        'status': 'success',
                        'data': form.data,
                        'stdData':std_serializer.data
                    })
                else:
                    return Response({
                        'status': False,
                        'Required Field': form.errors
                    })
        
        update_data = Subject.objects.get(sub_id = request.GET['pk'])
        serializer = subjectsSerializer(update_data)
        return Response({
            'status': 'Done',
            'data':serializer.data
        })
      
        # ===================insert_logic===========================
    else:
        if request.method == 'POST':
            data = request.data
            form = subjectsSerializer(data = data)
            if form.is_valid():
                check = Subject.objects.filter(sub_name = data['sub_name'], sub_std__std_id = data['sub_std']).exists()
                if check:
                    return Response({
                        'Status': 'Error',
                        'Message':'Already exist'
                    })
                else:    
                    form.save()
                    return Response({
                        'Status':'Form saved',
                        'Data': form.data
                    })
            else:
                return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })
        
    return Response(apidata)   


@api_view(['POST', 'GET'])
def api_delete_subjects(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Subject.objects.filter(sub_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                    
                })
            
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


#====================================================Chapters=====================================================

@api_view(['GET'])
def api_chepters(request):
    data = Chepter.objects.all()
    data_serializer = chapterSerializer(data, many=True)
    std_data = Std.objects.all()
    std_data_serializer = stdSerializer(std_data, many=True)
    subject_data = Subject.objects.all()
    subject_serializer = subjectsSerializer(subject_data, many=True)

    apidata = {
        'Status': True,
        'Data': data_serializer.data,
        'std_data': std_data_serializer.data,
        'subject': subject_serializer.data
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(chep_sub__sub_std__std_id = get_std)
            data_serializer = chapterSerializer(data, many=True)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            subject_serializer = subjectsSerializer(subject_data, many=True)
            get_std = Std.objects.get(std_id = get_std)
            serializer = stdSerializer(get_std)
            apidata.update({'Data':data_serializer.data,
                            'get_std':serializer.data,
                            'subject':subject_serializer.data})
            
    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])

        if get_subject == 0:
            pass
        else:    
            data = data.filter(chep_sub__sub_id = get_subject)
            data_serializer = chapterSerializer(data, many=True) 
            get_subject = Subject.objects.get(sub_id = get_subject)
            get_subject_serializer = subjectsSerializer(get_subject)
            apidata.update({'Data':data_serializer.data, 'subject':subject_serializer.data,'get_subject':get_subject_serializer.data})
            
    return Response(apidata)


# @api_view(['POST', 'GET'])
# def insert_update_chepters(request):
#     std_data = Std.objects.all()
#     std_serializer = stdSerializer(std_data, many = True)

#     subject_data = Subject.objects.all()
#     subject_serializer = subjectsSerializer(subject_data, many = True)

#     if request.GET.get('get_std'):
#         get_std = int(request.GET['get_std'])
#         std_data = std_data.filter(std_id = get_std)
        

#     if request.GET.get('get_subject'):
#         get_subject = int(request.GET['get_subject'])
#         subject_data = subject_data.filter(sub_id = get_subject)
     
   
 # ================update Logic============================
    # if request.GET.get('pk'):
    #     if request.method == 'POST':
    #         instance = get_object_or_404(Chepter, pk=request.GET['pk'])
    #         data = request.data
    #         form = chapterSerializer(data = data, request.FILES, instance=instance, partial = True)
    #         check = Chepter.objects.filter(chep_name = form.data['chep_name'], chep_std__std_id = form.data['chep_std']).count()
    #         if check >= 1:
    #             return Response({
    #                 'Message': 'already exits'
    #             })
    #         else:
    #             if form.is_valid():
    #                 form.save()
    #                 return Response({
    #                     'status': 'success',
    #                     'data': form.data,
    #                     'stdData':std_serializer.data
    #                 })
    #             else:
    #                 return Response({
    #                     'status':'Error',
    #                     'message':'error in form'
    #                 })
        
    #     update_data = Chepter.objects.get(chep_id = request.GET['pk'])
    #     serializer = chapterSerializer(update_data)
    #     return Response({
    #         'status': 'Done',
    #         'data':serializer.data
    #     })   
    
        # ===================insert_logic===========================
    # else:
    #     if request.method == 'POST':
    #         data = request.data
    #         form = chapterSerializer(data = data, request.FILES)
    #         if form.is_valid():
    #             check = Chepter.objects.filter(chep_name = form.data['chep_name'], chep_std__std_id = form.data['chep_std']).count()
    #             if check >= 1:
    #                 return Response({
    #                     'Status': 'Error',
    #                     'Message':'Already exist'
    #                 })
    #             else:    
    #                 form.save()
    #                 return Response({
    #                     'Status':'Form saved'
    #                 })
    #         else:
    #             return Response({
    #                 'Status': False,
    #                 'Message': 'Invalid data',
    #                 'errors': form.errors,
    #             }) 
        
    # return Response({'Message':'Something went Wrong'})  
        
        
@api_view(['POST', 'GET'])
def api_delete_chepters(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Chepter.objects.filter(chep_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                    
                })
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


#======================================================Faculties====================================================================

@api_view(['GET'])
def api_faculties(request):
    faculties = Faculties.objects.all()
    serializer = FacultiesSerializer(faculties, many= True)
    return Response({
        'Title': 'Faculties',
        'Data': serializer.data
    })


@api_view(['POST', 'GET'])
def api_update_faculties(request):
    # Update Logic
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Faculties, pk=request.GET['pk'])
            data = request.data
            form = FacultiesSerializer(data=data, instance=instance, partial = True)
            check = Faculties.objects.filter(fac_email=data['fac_email']).exclude(pk=request.GET['pk']).count()
            if check >= 1:
                return Response({
                    'Message': 'already exits'
                })
            else:
                if form.is_valid():
                    form.save()
                    return Response({
                        'status': 'success',
                        'data': form.data
                    })
                else:
                    return Response({
                        'status':False,
                        'Required Field':form.errors
                    })

        update_data = Faculties.objects.get(fac_id=request.GET['pk'])
        serializer = FacultiesSerializer(update_data)
        return Response({
            'status': 'Done',
            'data':serializer.data
        })
    else:
        # Insert Logic
        if request.method == 'POST':
            data = request.data
            form = FacultiesSerializer(data = data)
            if form.is_valid():
                check = Faculties.objects.filter(fac_email=data['fac_email']).count()
                if check >= 1:
                    return Response({
                        'Status': 'Error',
                        'Message':'Already exist'
                    })
                else:
                    form.save()
                    return Response({
                        'Status':'Form saved',
                        'Data': form.data
                    })
            else:
                return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })
            
    return Response({'Message':'Something went Wrong'}) 


@api_view(['POST', 'GET'])
def api_delete_faculties(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        # selected_items = [3]
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Faculties.objects.filter(fac_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                    
                })
            
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })

#=====================================================Batches===========================================================

@api_view(['GET'])
def api_batches(request):
    data = Batches.objects.all()
    data_serializer = BatchSerializer(data, many=True)
    std_data = Std.objects.all()
    std_data_serializer = stdSerializer(std_data, many=True)

    apidata = {
        'Data': data_serializer.data,
        'Title': 'Standard',
        'Std_data': std_data_serializer.data
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(batch_std__std_id = get_std)
            data_serializer = BatchSerializer(data, many=True)
            get_std = Std.objects.get(std_id = get_std)
            get_std_serializer = stdSerializer(get_std)
            apidata.update({'Data':data_serializer.data,'get_std':get_std_serializer.data})     

    return Response(apidata)

@api_view(['POST', 'GET'])
def api_update_batches(request):
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)

    apidata = {'std_data': std_serializer.data}
    
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std)
        std_serializer = stdSerializer(std_data, many = True)
        get_std = Std.objects.get(std_id = get_std)
        get_std_serializer = stdSerializer(get_std)
        apidata.update({'get_std ':get_std_serializer.data,'std_data':std_serializer.data})
   

 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Batches, pk=request.GET['pk'])
            data = request.data
            form = BatchSerializer(data=data, instance=instance, partial = True)
            check = Batches.objects.filter(batch_name = data['batch_name'], batch_std__std_id = data['batch_std']).count()
            if check >= 1:
                return Response({
                    'Message': 'already exits'
                })
            else:
                if form.is_valid():
                    form.save()
                    return Response({
                        'status': 'success',
                        'data': form.data,
                        'stdData':std_serializer.data
                    })
                else:
                    return Response({
                        'status':'Error',
                        'Required Field':form.errors
                    })
        
        update_data = Batches.objects.get(batch_id = request.GET['pk'])
        serializer = BatchSerializer(update_data)
        return Response({
            'status': 'Done',
            'data':serializer.data
        }) 
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            data = request.data
            form = BatchSerializer(data = data)
            if form.is_valid():
                check = Batches.objects.filter(batch_name = data['batch_name'], batch_std__std_id = data['batch_std']).count()
                if check >= 1:
                    return Response({
                        'Status': 'Error',
                        'Message':'Already exist'
                    })
                else:    
                    form.save()
                    return Response({
                        'Status':'Form saved',
                        'Data': form.data
                    })
            else:
                return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })
            
    return Response(apidata)                   


@api_view(['POST', 'GET'])
def api_delete_batches(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        # selected_items = [7]
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Batches.objects.filter(batch_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                    
                })
            
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


#==============================================Announcements==============================================


@api_view(['GET'])
def api_announcements(request):
    data = Announcements.objects.all()
    data_serializer = AnnouncementSerializer(data, many=True)
    std_data = Std.objects.all()
    std_data_serializer = stdSerializer(std_data, many=True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many=True)
   
    apidata = {
        'title' : 'Announcements',
        'data' : data_serializer.data,
        'std_data' : std_data_serializer.data,
        'batch_data': batch_serializer.data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(announce_std__std_id = get_std)
            data_serializer = AnnouncementSerializer(data, many=True)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            batch_serializer = BatchSerializer(batch_data, many=True)
            get_std = Std.objects.get(std_id = get_std)
            get_std_serializer = stdSerializer(get_std)
            apidata.update({'data':data_serializer.data,'batch_data':batch_serializer.data,'get_std':get_std_serializer.data})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(announce_batch__batch_id = get_batch)
            data_serializer = AnnouncementSerializer(data, many=True)
            get_batch = Batches.objects.get(batch_id = get_batch)
            get_batch_serializer = BatchSerializer(get_batch)
            apidata.update({'data':data_serializer.data,'get_batch':get_batch_serializer.data})

    return Response(apidata)


@api_view(['POST', 'GET'])
def api_update_announcements(request):
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many=True)

    apidata = {
        'std_data': std_serializer.data,
        'batch_data': batch_serializer.data
    }

    # ------------getting students for mail------------------
    # students_for_mail = Students.objects.all()

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        get_std_serializer = stdSerializer(get_std)
        std_data = std_data.filter(std_id = get_std)
        std_serializer = stdSerializer(std_data, many = True)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        batch_serializer = BatchSerializer(batch_data, many=True)
        # students_for_mail = students_for_mail.filter(stud_std=get_std)
        apidata.update({'get_std ':get_std_serializer.data,'std_data':std_serializer.data,'batch_data':batch_serializer.data}) 
        
    
    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        get_batch_serializer = BatchSerializer(get_batch)
        batch_data = batch_data.filter(batch_id = get_batch)
        batch_serializer = BatchSerializer(batch_data, many=True)
        # students_for_mail = students_for_mail.filter(stud_batch=get_batch)
        apidata.update({'get_batch ':get_batch_serializer.data,'batch_data':batch_serializer.data})

    if request.method == 'POST':

        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Announcements, pk=request.GET['pk'])
            data = request.data
            form = AnnouncementSerializer(data=data, instance=instance, partial = True)       
            if form.is_valid():
                form.save()
                return Response({
                        'status': 'success',
                        'data': form.data,
                        'StdData':std_serializer.data
                    })
            else:
                return Response({
                        'status':'Error',
                        'Required Field':form.errors
                    })
            
        # ===================insert_logic===========================
        data = request.data
        form = AnnouncementSerializer(data=data)
        if form.is_valid():
            form.save()
            # ---------------------sendmail Logic===================================
            # students_email_list = []
            # for x in students_for_mail:
            #     students_email_list.append(x.stud_email)
            # print(students_email_list)    
            # announcement_mail(form.cleaned_data['announce_title'],form.cleaned_data['announce_msg'],students_email_list)
     
            return Response({
                    'Status':'Form saved',
                    'Data': form.data
                })
        else:
           return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })
        
    if request.GET.get('pk'):
        update_data = Announcements.objects.get(announce_id = request.GET['pk'])
        serializer = AnnouncementSerializer(update_data)
        return Response({
            'status': 'Done',
            'data':serializer.data
        }) 
    
    return Response(apidata)


@api_view(['POST', 'GET'])
def api_delete_announcements(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        # selected_items = [3]
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Announcements.objects.filter(announce_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                })

    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


#==============================================TimeTable==================================================================


@api_view(['GET'])
def api_timetable(request):
    data = Timetable.objects.all()
    data_serializer = TimetableSerializer(data, many =True)

    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many =True)

    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many =True)
   
    apidata = {
        'title': 'Timetable',
        'data': data_serializer.data,
        'std_data': std_serializer.data,
        'batch_data': batch_serializer.data,
        }
 
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std != 0:  
            data = data.filter(tt_batch__batch_std__std_id=get_std)
            data_serializer = TimetableSerializer(data, many =True)
            batch_data = batch_data.filter(batch_std__std_id=get_std)
            batch_serializer = BatchSerializer(batch_data, many =True)
            get_std = Std.objects.get(std_id=get_std)
            serializer = stdSerializer(get_std)
            apidata.update({'data': data_serializer.data, 'batch_data': batch_serializer.data, 'get_std': serializer.data}) 

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch != 0:
            data = data.filter(tt_batch__batch_id=get_batch)
            data_serializer = TimetableSerializer(data, many =True)
            get_batch = Batches.objects.get(batch_id=get_batch)
            get_batch_serializer = BatchSerializer(get_batch)       
            apidata.update({'data':  data_serializer.data, 'get_batch': get_batch_serializer.data})        
            
    return Response(apidata)


@api_view(['POST', 'GET'])
def api_update_timetable(request):
    std_data = Std.objects.all()
    std_data_serializer = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many=True)
    faculty_data = Faculties.objects.all()
    faculty_serializer = FacultiesSerializer(faculty_data, many= True)
    subject_data = Subject.objects.all()
    subject_serializer = subjectsSerializer(subject_data, many=True)
    # tt_students_for_mail = Students.objects.all()

    apidata = {
        'std_data': std_data_serializer.data, 
        'batch_data': batch_serializer.data, 
        'subject_data':subject_serializer.data,
        'faculty_data':  faculty_serializer.data,
        'DaysChoice': Timetable.DaysChoice,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id=get_std)
        std_data_serializer = stdSerializer(std_data, many = True)

        subject_data = Subject.objects.filter(sub_std__std_id = get_std)
        subject_serializer = subjectsSerializer(subject_data, many=True)
        
        batch_data = batch_data.filter(batch_std__std_id=get_std)
        batch_serializer = BatchSerializer(batch_data, many=True)
        
        get_std = Std.objects.get(std_id = get_std)
        get_std_serializer = stdSerializer(get_std)
        # tt_students_for_mail = tt_students_for_mail.filter(stud_std=get_std)
        apidata.update({'get_std': get_std_serializer.data,
                        'std_data': std_data_serializer.data,
                        'batch_data':batch_serializer.data,
                        'subject_data':subject_serializer.data}) 


    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        get_batch_serializer = BatchSerializer(get_batch)
        batch_data = batch_data.filter(batch_id=get_batch)
        batch_serializer = BatchSerializer(batch_data, many=True)
        # tt_students_for_mail = tt_students_for_mail.filter(stud_batch=get_batch)
        apidata.update({'get_batch': get_batch_serializer.data, 'batch_data': batch_serializer.data})

    if request.method == 'POST':
        # Update logic
        if request.GET.get('pk'):
            instance = get_object_or_404(Timetable, pk=request.GET['pk'])
            data = request.data
            form = TimetableSerializer(data=data, instance=instance, partial = True)
            if form.is_valid():
                form.save()
                return Response({
                        'status': 'success',
                        'Data': form.data,
                        'StdData':std_data_serializer.data
                    })
            else:
                apidata.update({'status':False,'Required Field':form.errors})
                return Response(apidata)

        # Insert logic
        data = request.data
        form = TimetableSerializer(data=data)
        if form.is_valid():
            form.save()
            # ---------------------sendmail Logic===================================
            # tt_students_email_list = []
            # for x in tt_students_for_mail:
            #     tt_students_email_list.append(x.stud_email)
            # print(tt_students_email_list)    
            # timetable_mail(tt_students_email_list)
            apidata.update({'Status':True,
                    'Data': form.data})
            return Response(apidata)
    
        else:
            return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })

    if request.GET.get('pk'):
        update_data = Timetable.objects.get(tt_id=request.GET['pk'])
        serializer = TimetableSerializer(update_data)
        return Response({
            'status': 'Done',
            'data':serializer.data,
            'Faculty': faculty_serializer.data
        }) 
    
    return Response(apidata)


@api_view(['POST', 'GET'])
def api_delete_timetable(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        selected_items = [5]
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Timetable.objects.filter(tt_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                })

    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


#=============================================================== Packages =======================================================================

@api_view(['GET'])
def api_packages(request):
    data = Packs.objects.prefetch_related('pack_subjects').all()
    data_serializer = PackageSerializer(data, many=True)
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)

    apidata = {
        'title' : 'Packages',
        'data' : data_serializer.data,
        'std_data' : std_serializer.data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(pack_std__std_id = get_std)
            data_serializer = PackageSerializer(data, many=True)
            get_std = Std.objects.get(std_id = get_std)
            serializer = stdSerializer(get_std)
            apidata.update({'data':data_serializer.data,'get_std':serializer.data}) 

    return Response(apidata)



@api_view(['POST', 'GET'])
def api_update_packages(request):
    std_data = Std.objects.all()
    std_data_serializer = stdSerializer(std_data, many = True)
    subjects_data = Subject.objects.all()
    subject_serializer = subjectsSerializer(subjects_data, many=True)

    apidata = {
        'std_data': std_data_serializer.data,
        'subjects_data': subject_serializer.data
    }

    if request.GET.get('get_std'): 
        get_std = int(request.GET['get_std'])  
        std_data = std_data.filter(std_id = get_std)
        std_data_serializer = stdSerializer(std_data, many = True)             # Testing  remaining
        subjects_data = subjects_data.filter(sub_std__std_id = get_std)
        subject_serializer = subjectsSerializer(subjects_data, many=True)
        get_std = Std.objects.get(std_id = get_std)
        get_std_serializer = stdSerializer(get_std)    # Doubt


        apidata.update({'get_std ':get_std_serializer.data,'std_data':std_data_serializer.data, 'subjects_data':subject_serializer.data})
        return Response(apidata)


 # ================update Logic============================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Packs, pk=request.GET['pk'])
            data = request.data
            form = PackageSerializer(data = data, instance=instance, partial = True)
            check = Packs.objects.filter(pack_name = data['pack_name'], pack_std__std_id = data['pack_std']).count()
            if check >= 1:
                return Response({
                    'Message': 'already exits',
                    'Data': form.data
                })
            else:
                if form.is_valid():
                    form.save()
                    return Response({
                        'Status': True,
                        'Data': form.data,
                        'std_data':std_data_serializer.data,
                        'subjects_data':subject_serializer.data 
                    })
                else:
                    filled_data = form.data
                    apidata.update({'filled_data ':filled_data,'errors':form.errors})
                
        update_data = Packs.objects.get(pack_id = request.GET['pk'])
        serializer = PackageSerializer(update_data)
        apidata.update({'data':serializer.data})
        
    
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            data = request.data
            form = PackageSerializer(data = data)
            if form.is_valid():
                check = Packs.objects.filter(pack_name = data['pack_name'], pack_std__std_id = data['pack_std']).count()
                if check >= 1:
                    return Response({
                        'Status': 'Error',
                        'Message':'Already exist'
                    })
                else:    
                    form.save()
                    return Response({
                        'Status':'Form saved',
                        'Data': form.data
                    })
            else:
                return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })

    return Response(apidata) 


@api_view(['POST', 'GET'])
def api_delete_package(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        selected_items = [9]
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Packs.objects.filter(pack_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                })

    return Response({
        'status': False,
        'message': 'Something is wrong'
    })



# ====================================================== Students ====================================================================

@api_view(['GET'])
def api_students(request):
    data = Students.objects.all()
    data_serializer = StudentSerializer(data, many = True)
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many = True)
     
    api_data = {
        'data': data_serializer.data,
        'std_data' : std_serializer.data,
        'batch_data':batch_serializer.data,
    } 
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(stud_std__std_id = get_std)
            data_serializer = StudentSerializer(data, many = True)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            batch_serializer = BatchSerializer(batch_data, many = True)
            get_std = Std.objects.get(std_id = get_std)
            get_std_serializer = stdSerializer(get_std)
            api_data.update({'data':data_serializer.data,'get_std' : get_std_serializer.data,
            'batch_data':batch_serializer.data,})
                       

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(stud_batch__batch_id = get_batch)
            data_serializer = StudentSerializer(data, many = True)
            get_batch = Batches.objects.get(batch_id = get_batch)
            get_batch_serializer = BatchSerializer(get_batch)       
            api_data.update({'data':data_serializer.data,'get_batch' : get_batch_serializer.data})
    
    return Response(api_data)


@api_view(['POST', 'GET'])
def api_update_students(request):
    std_data = Std.objects.all()
    std_data_serializer = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many = True)
    pack_data = Packs.objects.all()
    pack_serializer = PackageSerializer(pack_data, many = True)

    api_data = {
        'title' : 'Students',
        'std_data':std_data_serializer.data,
        'batch_data':batch_serializer.data,
        'pack_data':pack_serializer.data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        get_std_serializer = stdSerializer(get_std)
        std_data = std_data.filter(std_id = get_std)
        std_data_serializer = stdSerializer(std_data, many = True)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        batch_serializer = BatchSerializer(batch_data, many = True)
        pack_data = pack_data.filter(pack_std__std_id = get_std)
        pack_serializer = PackageSerializer(pack_data, many = True)
        api_data.update({'get_std ':get_std_serializer.data,
                        'std_data':std_data_serializer.data,
                        'batch_data':batch_serializer.data,
                        'pack_data':pack_serializer.data
                        }) 


    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        get_batch_serializer = BatchSerializer(get_batch)
        batch_data = batch_data.filter(batch_id = get_batch)
        batch_serializer = BatchSerializer(batch_data, many = True)
        api_data.update({'get_batch ':get_batch_serializer.data,'batch_data':batch_serializer.data})

    if request.method == 'POST':

        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Students, pk=request.GET['pk'])
            data = request.data
            form = StudentSerializer(data = data, instance=instance, partial = True)
            if form.is_valid():
                form.save()
                return Response({
                    'Status': True,
                    'Data': form.data
                })
            else:
                return Response({
                        'status':'Error',
                        'Required Field':form.errors
                    })
                
        # ===================insert_logic===========================
        data = request.data
        form = StudentSerializer(data = data)
        if form.is_valid():
            form.save()
            return Response({
                'Status':'Form saved',
                'Data': form.data
            })
        else:
            return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'Required Field': form.errors,
                })
        
    if request.GET.get('pk'):
        update_data = Students.objects.get(stud_id = request.GET['pk'])
        serializer = StudentSerializer(update_data, many = True)
        return Response({
            'status': 'Done',
            'data':serializer.data
        })  
    return Response(api_data)


@api_view(['POST', 'GET'])
def api_delete_students(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
        selected_items = [19,20,21]
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Students.objects.filter(stud_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete"
                })
            
    return Response({
        'status': False,
        'message': 'Something is wrong'
    })


# ========================================================= Admin =============================================================

@api_view(['GET'])
def api_admin_profile(request):
    admin_data = AdminData.objects.all()
    serializer = AdminSerializer(admin_data, many =True)
   
    return Response({
        'Title': 'Admin Profile',
        'Data': serializer.data
    })


# ==================================================== Attendance =============================================================

@api_view(['GET'])
def api_attendance(request):
    data = Attendance.objects.all()
    data_serializer = AttendanceSerializer(data, many = True)
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many = True)
    stud_data = Students.objects.all()
    stud_serializer = StudentSerializer(stud_data, many = True)
    subj_data = Subject.objects.all()
    subj_serializer = subjectsSerializer(subj_data, many = True)
    

    api_data ={
        'data' : data_serializer.data,
        'title' : 'Attendance',
        'std_data' : std_serializer.data,
        'batch_data':batch_serializer.data,
        'stud_data':stud_serializer.data,
        'sub_data':subj_serializer.data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(atten_timetable__tt_batch__batch_std__std_id = get_std)
            data_serializer = AttendanceSerializer(data, many = True)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            batch_serializer = BatchSerializer(batch_data, many = True)
            stud_data = stud_data.filter(stud_std__std_id = get_std)
            stud_serializer = StudentSerializer(stud_data, many = True)
            subj_data = subj_data.filter(sub_std__std_id = get_std)
            subj_serializer = subjectsSerializer(subj_data, many = True)
            get_std = Std.objects.get(std_id = get_std)
            get_std_serializer = stdSerializer(get_std)
            api_data.update({
                'data' : data_serializer.data,
                'get_std' : get_std_serializer.data,
                'batch_data':batch_serializer.data,
                'stud_data':stud_serializer.data,
                'sub_data':subj_serializer.data
                })
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(atten_timetable__tt_batch__batch_id = get_batch)
            data_serializer = AttendanceSerializer(data, many = True)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            stud_serializer = StudentSerializer(stud_data, many = True)
            get_batch = Batches.objects.get(batch_id = get_batch)
            get_batch_serializer = BatchSerializer(get_batch)
            api_data.update({
                'data' : data_serializer.data,
                'title' : 'Attendance',
                'stud_data':stud_serializer.data,
                'get_batch':get_batch_serializer.data
                })
            
            

    if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = data.filter(atten_student__stud_id = get_student)
            data_serializer = AttendanceSerializer(data, many = True)
            get_student = Students.objects.get(stud_id = get_student)
            get_stud_serializer = StudentSerializer(get_student)
            api_data.update({'data':data_serializer.data,'get_student': get_stud_serializer.data})                     


    attendance_present = data.filter(atten_present = True).count()
    attendance_all = data.all().count()
    if attendance_all>0:
        overall_attendance = round((attendance_present/attendance_all) * 100,2)
        api_data.update({'overall_attendance':overall_attendance})

    sub_list = subj_data.all().values('sub_name').distinct()
    subject_wise_attendance = []
    subjects = []
    for x in sub_list:
        sub_name = x['sub_name']
        sub_one = data.filter(atten_present = True,atten_timetable__tt_subject1__sub_name=sub_name).count()
        sub_all = data.filter(atten_timetable__tt_subject1__sub_name = sub_name).count()
        if sub_all>0:
            sub_attendance = round((sub_one/sub_all) * 100, 2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
    combined_data = zip(subject_wise_attendance, subjects)
    api_data.update({'combined_data': combined_data})
    
    return Response(api_data)


# ========================================================= Report Card ===============================================================

@api_view(['GET'])
def api_admin_report_card(request):
    data = Attendance.objects.all()
    Attendance_serial = AttendanceSerializer(data, many =True)
    
    std_data = Std.objects.all()
    std_serial = stdSerializer(std_data, many = True)
    
    batch_data = Batches.objects.all()
    batch_serial = BatchSerializer(batch_data, many = True)

    stud_data = Students.objects.all()
    stud_serial = StudentSerializer(stud_data, many = True)

    subj_data = Subject.objects.all()
    subj_serial = subjectsSerializer(subj_data, many = True)

    apidata ={
        'title' : 'Report-Card',
        'data' : Attendance_serial.data,
        'std_data' : std_serial.data,
        'batch_data':batch_serial.data,
        'stud_data':stud_serial.data,
        'sub_data':subj_serial.data,
    }

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(atten_timetable__tt_batch__batch_std__std_id = get_std)
            Attendance_serial = AttendanceSerializer(data, many =True)

            batch_data = batch_data.filter(batch_std__std_id = get_std)
            batch_serial = BatchSerializer(batch_data, many = True)

            stud_data = stud_data.filter(stud_std__std_id = get_std)
            stud_serial = StudentSerializer(stud_data, many = True)

            subj_data = subj_data.filter(sub_std__std_id = get_std)
            subj_serial = subjectsSerializer(subj_data, many = True)

            get_std = Std.objects.get(std_id = get_std)
            serializer = stdSerializer(get_std)
            apidata.update({'data': Attendance_serial.data,
                            'batch_data':batch_serial.data,
                            'get_std':serializer.data,
                            'stud_data':stud_serial.data,
                            'sub_data':subj_serial.data})
            
            student_std = get_std.std_name
        student_std = get_std.std_id
    
    
    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(atten_timetable__tt_batch__batch_id = get_batch)
            Attendance_serial = AttendanceSerializer(data, many =True)

            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            stud_serial = StudentSerializer(stud_data, many = True)

            get_batch = Batches.objects.get(batch_id = get_batch)
            get_batch_serial = BatchSerializer(get_batch)
            apidata.update({'data':Attendance_serial.data,'get_batch':get_batch_serial.data,'stud_data':stud_serial.data}) 
        student_batch = get_batch.batch_name
    
    
    if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = data.filter(atten_student__stud_id = get_student)
            Attendance_serial = AttendanceSerializer(data, many =True)

            get_student = Students.objects.get(stud_id = get_student)
            get_stud_serial = StudentSerializer(get_student)
            apidata.update({'data':Attendance_serial.data,'get_student':get_stud_serial.data})

        student_id = get_student.stud_id
        
    if ((request.GET.get('get_std')) and (request.GET.get('get_batch')) and (request.GET.get('get_student'))):
        # ===============Overall Attendance==================


        total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id).count()
        
        present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

        absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
        
        if total_attendence > 0:
            overall_attendence = (present_attendence/total_attendence)*100
        else:
            overall_attendence = 0


        # ==================Test Report and Attendance Report============
        students_li = Students.objects.filter(stud_std__std_id = student_std)
        overall_attendance_li = []
        for x in students_li:
            total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id).count()
            present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, atten_present=True).count()
          
            if total_attendence_studentwise > 0:
                overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
            else:
                overall_attendence_studentwise = 0
            

            total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
            
            
            obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
            

            if total_marks == 0:
                overall_result = 0
            else:
                overall_result = round((obtained_marks/total_marks)*100,2)
            if student_id == x.stud_id: 
                current_student_overall_test_result = overall_result
                apidata.update({'current_student_overall_test_result':current_student_overall_test_result})

            overall_attendance_li.append({'stud_name':x.stud_name, 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})
        overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
        overall_attendance_li = overall_attendance_li[:5]
        
        # ===================SubjectsWise Attendance============================


        subjects_li = Subject.objects.filter(sub_std__std_id = student_std).values('sub_name').distinct()
        overall_attendance_subwise = []
        for x in subjects_li:
            x = x['sub_name']
            total_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_student__stud_id=student_id).count()

            present_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_present=True,atten_student__stud_id=student_id).count()

            if total_attendence_subwise > 0:
                attendance_subwise = (present_attendence_subwise/total_attendence_subwise)*100
            else:
                attendance_subwise = 0
            overall_attendance_subwise.append({'sub_name': x, 'attendance_subwise':attendance_subwise})

        # ======================SubjectWise TestResult==============================
        subjects_data = Subject.objects.filter(sub_std=student_std)
        final_average_marks_subwise = []
        for x in subjects_data:
            total_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(total_sum_marks_subwise=Sum('tau_total_marks'))['total_sum_marks_subwise'] or 0
        

            obtained_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(obtained_sum_marks_subwise=Sum('tau_obtained_marks'))['obtained_sum_marks_subwise'] or 0
            
            
            if total_marks_subwise == 0:
                average_marks_subwise = 0
            else:
                average_marks_subwise = round((obtained_marks_subwise/total_marks_subwise)*100,2)
            
            final_average_marks_subwise.append({'subject_name':x.sub_name, 'average_marks_subwise':average_marks_subwise})

        # ====================Average Test Result=================================
        overall_results = [i['overall_result'] for i in overall_attendance_li]
        if overall_results:
            class_average_result = round(statistics.mean(overall_results),2)
        else:
            class_average_result = 0

        total_test_conducted = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id).count()

        absent_in_test = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id,tau_obtained_marks = 0).count()


        # =============Doubts and Solution Counts================================

        doubt_asked = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).count()

        solutions_gives = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).annotate(verified_solution=Count(
            Case(
                When(doubt_solution__solution_verified=True, then=1),
                output_field=IntegerField(),
            )))
        
        my_solve_doubts = 0
        for x in solutions_gives:
            if x.verified_solution > 0:
                my_solve_doubts += 1
            else:
                print("no verified")

        doubt_solved_byme = Doubt_solution.objects.filter(solution_stud_id__stud_id = student_id, solution_verified = True).count()
        
        apidata.update({
            'title': 'Report-Card',
            'logo_url': 'https://metrofoods.co.nz/1nobg.png',
            'overall_attendence':overall_attendence,
            'overall_attendance_li':overall_attendance_li,
            'overall_attendance_subwise':overall_attendance_subwise,
            'total_attendence':total_attendence,
            'absent_attendence':absent_attendence,
            'class_average_result':class_average_result,
            'final_average_marks_subwise':final_average_marks_subwise,
            'doubt_asked':doubt_asked,
            'solutions_gives':solutions_gives,
            'doubt_solved_byme':doubt_solved_byme,
            'my_solve_doubts':my_solve_doubts,
            'total_test_conducted':total_test_conducted,
            'absent_in_test':absent_in_test,
        })
    else:
        noreport_card = 1
        message =  'Please Select Standard, Batch and Student!'
        apidata.update({'message':message, 'noreport_card':noreport_card})
    return Response(apidata)



# ==================================================== Fees ==================================================================

@api_view(['GET'])
def api_fees_collection(request):
    cheque_collections_data = Cheque_Collection.objects.filter(cheque_paid=False)
    collection = Cheque_Collection_serial(cheque_collections_data, many = True)

    students_data = Students.objects.annotate(
    amount_paid=Sum('fees_collection__fees_paid'),
    discountt=Case(
        When(discount__discount_amount=None, then=Value(0)),
        default=F('discount__discount_amount'),output_field=IntegerField()
    ))
    Studentdata = StudentSerializer(students_data, many = True)

    #=================Total Amount Fees Paid============================================
    total_amount_fees_paid = Fees_Collection.objects.all().aggregate(total_amu_paid = Sum('fees_paid'))
    
    if total_amount_fees_paid['total_amu_paid'] != None:
        total_amount_fees_paid = total_amount_fees_paid['total_amu_paid']
    else:
        total_amount_fees_paid = 0

    #==================Total Fees Amount After Discount=================================
    total_discount_amount = Discount.objects.all().aggregate(discount_amount=Sum('discount_amount'))
    if total_discount_amount['discount_amount'] != None:
        total_discount_amount = total_discount_amount['discount_amount']
    else:
        total_discount_amount = 0

    total_fees_amount = Students.objects.all().aggregate(fees_amount=Sum('stud_pack__pack_fees'))
    if total_fees_amount['fees_amount'] != None:
        total_fees_amount = total_fees_amount['fees_amount']
    else:
        total_fees_amount = 0

    total_fees_amount_after_discount = (total_fees_amount-total_discount_amount)
    
    #===================Total Pending Fees==============================================
    total_pending_fees = total_fees_amount_after_discount - total_amount_fees_paid
    stud_li = []
    for stud in students_data:
        li = {}
        if stud.amount_paid ==None:
            stud_amount_paid = 0
        else:
            stud_amount_paid= stud.amount_paid

        remaining_amount = stud.stud_pack.pack_fees - stud.discountt - stud_amount_paid
        li.update({'std':"{} - {}".format(stud.stud_std.std_name, stud.stud_std.std_board),
                   'name':"{} {}".format(stud.stud_name, stud.stud_lastname),
                   'Total payable amount': stud.stud_pack.pack_fees,
                   'Discount Fees': stud.discountt,
                   'Amount Paid': stud_amount_paid,
                   'Remaining Amount': remaining_amount})
        stud_li.append(li)
    apidata={
        'title':'Payments',
        'cheque_collections_data':collection.data,
        'total_amount_fees_paid':total_amount_fees_paid,
        'total_fees_amount_after_discount':total_fees_amount_after_discount,
        'total_pending_fees':total_pending_fees,
        'stud_data': stud_li,
        'students_data':Studentdata.data,
    }
    return Response(apidata)


@api_view(['POST', 'GET'])
def api_add_cheques(request):
    students = Students.objects.all()
    student_serial = StudentSerializer(students, many = True)
    banks = Banks.objects.all()
    bank_serial = BankSerializer(banks, many = True)

    apidata={
        'title' : 'Add Cheques',
        # 'students':student_serial.data,
        'banks':bank_serial.data,    
             }   

 # ================update Logic==================================
    if request.GET.get('pk'):
        if request.method == 'POST':
            instance = get_object_or_404(Cheque_Collection, pk=request.GET['pk'])
            data = request.data
            form = Cheque_Collection_serial(data = data, instance=instance, partial = True)
            if form.is_valid():
                
                if form.validated_data.get('cheque_paid') == True:
                    studid = form.validated_data.get('cheque_stud_id')
                    cheque_amt = form.validated_data.get('cheque_amount')
                    fees_mode = 'CHECK'
                    cheque_date = form.validated_data.get('cheque_date')
                    abcd = Fees_Collection.objects.create(fees_stud_id = studid,fees_paid=cheque_amt,fees_mode=fees_mode,fees_date=cheque_date)
              
                    

                form.save()
                return Response({
                    'Status': True,
                    'Data': form.data,
                    'students':student_serial.data,
                    'banks':bank_serial.data,   
                })
            else:
                filled_data = form.data
                apidata.update({'filled_data ':filled_data,'errors':form.errors})
        
        update_data = Cheque_Collection.objects.get(cheque_id = request.GET['pk'])
        update_serial = Cheque_Collection_serial(update_data)
        apidata.update({'update_data':update_serial.data})  
    else:
        # ===================insert_logic===========================
        if request.method == 'POST':
            data = request.data
            form = Cheque_Collection_serial(data = data)
            if form.is_valid():
                check = Cheque_Collection.objects.filter(cheque_number = data['cheque_number']).count()
                if check >= 1:
                    return Response({
                        'Status': 'Error',
                        'Message':'Already exist'
                    })
                else:    
                    form.save()
                    return Response({
                        'Status':'Form saved',
                        'Data': form.data
                    })
            else:
                filled_data = form.data
                apidata.update({'filled_data ':filled_data,'errors':form.errors})
                # return Response(apidata)          
            
    return Response(apidata)


@api_view(['POST', 'GET'])
def api_delete_cheques(request):
    if request.GET.get('delete_cheque'):
        del_id = request.GET['delete_cheque']
        try:
            check_data = Cheque_Collection.objects.get(cheque_id=del_id)
            check_data.delete()
        except Cheque_Collection.DoesNotExist:
            raise Http404("Cheque not found")
    return Response({
        'Status': True,
        'Message': 'Deleted Successfully'
    })

@api_view(['GET'])
def api_payments_history(request):
    fees_collections_data = Fees_Collection.objects.all()
    serializer = Fees_Collection_serial(fees_collections_data, many = True)

    return Response({
        'fees_collections_data':serializer.data,
    })


# =============================================== Events ===================================================================

@api_view(['GET'])
def api_events(request):
    events = Event.objects.all()
    event_serial = EventSerializer(events, many=True)
    events_imgs = Event_Image.objects.all()
    imgs = ImageSerializer(events_imgs, many = True)
    selected_events = Event.objects.all()[:1]
    selected_serial = EventSerializer(selected_events, many = True)
    apidata = {
        'title' : 'Events',
        'events':event_serial.data,
        'events_imgs':imgs,
        'selected_events':selected_serial.data,
    }
    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        selected_serial = EventSerializer(selected_events, many = True)
        events_imgs = Event_Image.objects.filter(event__event_id = event_id)
        imgs = ImageSerializer(events_imgs, many = True)
        apidata.update({'selected_events':selected_serial.data,'events_imgs':events_imgs})
    return Response(apidata)


def insert_events(request):
    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_desc = request.POST.get('event_desc')
        event_images = request.FILES.getlist('event_img')
        event = Event(event_name=event_name, event_date=event_date, event_desc=event_desc)
        serializer = EventSerializer(event)
        event.save()

        # fs = FileSystemStorage(location='media/uploads/events/')
        # for image in event_images:
        #     filename = fs.save(image.name, image)
        #     Event_Image.objects.create(event=event, event_img=filename)
    return Response({
        'Title': 'Event updated',
        'Event': serializer.data
    })

@api_view(['GET'])
def api_events(request):
    events = Event.objects.all()
    event_serial = EventSerializer(events, many = True)
    events_imgs = Event_Image.objects.all()
    images = ImageSerializer(events_imgs, many = True)
    selected_events = Event.objects.all()[:1]
    selected = EventSerializer(selected_events, many = True)
    apidata = {
        'title' : 'Events',
        'events':event_serial.data,
        'events_imgs':images.data,
        'selected_events':selected.data,
    }
    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        selected = EventSerializer(selected_events, many = True)
        events_imgs = Event_Image.objects.filter(event__event_id = event_id)
        images = ImageSerializer(events_imgs, many = True)

        apidata.update({'selected_events':selected.data,'events_imgs':images.data})
    return Response(apidata)



@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def api_insert_events(request):
    if request.method == 'POST':
        # Use request.data to retrieve form data
        event_name = request.data.get('event_name')
        event_date = request.data.get('event_date')
        event_desc = request.data.get('event_desc')
        event_images = request.FILES.getlist('event_img')  # Use the correct key name
        # Validate that all required fields are present
        if not event_name or not event_date or not event_desc or not event_images:
            return Response({'Status': False, 'Message': 'All fields are required'}, status=400)

        # Save the event
        event = Event(event_name=event_name, event_date=event_date, event_desc=event_desc)
        event.save()

        # Save each uploaded image associated with the event
        fs = FileSystemStorage(location='media/uploads/events/')
        for image in event_images:
            filename = fs.save(image.name, image)
            Event_Image.objects.create(event=event, event_img=filename)
        
        return Response({'Status': True, 'Message': 'Event created successfully'}, status=201)
    
    # Default response for GET request or other methods
    return Response({'Status': False, 'Message': 'Invalid request method'}, status=405)



def images(request):
    return HttpResponse('<form action="http://localhost:8000/api/api_insert_events/" method="post" enctype="multipart/form-data"><input type="text" name="event_name" placeholder="Event Name"><input type="date" name="event_date" placeholder="Event Date"><input type="text" name="event_desc" placeholder="Event Description"><input type="file" name="event_img" multiple><button type="submit">Submit</button></form>')


# ==============================================================================================================================
                                                     # STUDENTSIDE                  
# ==============================================================================================================================

@api_view(['GET'])
def student_profile(request):
    student_id = request.GET.get('stud_id')

    if not student_id:
        return Response({'error': 'stud_id parameter is required'}, status=400)

    try:
        student_profile = Students.objects.get(stud_id=student_id)
    except Students.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)

    profile_serializer = StudentSerializer(student_profile)

    return Response({
        'Title': 'Profile',
        'Data': profile_serializer.data
    })

@api_view(['GET', 'POST'])
def student_info_update(request):
    # student_id = request.session['stud_id']
    student_id = request.GET.get('stud_id')
    if not student_id:
        return Response({'error': 'stud_id parameter is required'}, status=400)
    
    student_obj = Students.objects.get(stud_id = student_id)
    stud = StudentSerializer(student_obj)
    apidata = {'title' : 'Update Info', 'Student': stud.data}
    if request.method == 'POST':
        instance = get_object_or_404(Students, pk=request.GET['stud_id'])
        data = request.data
        form = StudentSerializer(data = data, instance=instance, partial = True)
        if form.is_valid():
            form.save()
            apidata.update({
                'Status': True,
                'Message': 'Profile updated',
                'Form': form.data
            })
           
        else:
            apidata.update({
                'Status': False,
                'Message': 'Updation failed',
                'error': form.errors
            })
    else:
        form = StudentSerializer(instance=student_obj)
        apidata.update({'Form': form.data})
    return Response(apidata)


@api_view(['GET'])
def student_announcement(request):
    apidata = {'Title': 'Announcements'}

    stud_std = request.GET.get('stud_std')
    stud_batch = request.GET.get('stud_batch')

    if not stud_std:
        return Response({'error': 'stud_std parameter is required'}, status=400)

    announcements_data = Announcements.objects.filter(
        Q(announce_std=None, announce_batch=None) |
        Q(announce_std__std_id=stud_std, announce_batch=None) |
        Q(announce_std__std_id=stud_std, announce_batch__batch_id=stud_batch)
    ).order_by('-pk')[:50]  # Limit to 50 most recent announcements

    serializer = AnnouncementSerializer(announcements_data, many=True)
    apidata.update({'Announcement': serializer.data})

    return Response(apidata)

@api_view(['GET'])
def stud_subjects(request):
    stud_standard = request.GET.get('stud_std')
    if not stud_standard:
        return Response({'error': 'stud_std parameter is required'}, status=400)
    subjects = Subject.objects.filter(sub_std__std_id = stud_standard)
    serializer = subjectsSerializer(subjects, many = True)

    return Response({'Title': 'Subjects',
                     'Your Subjects': serializer.data})


@api_view(['GET'])
def stud_chepters(request):
    stud_subject = request.GET.get('sub_id')
    if not stud_subject:
        return Response({'error': 'sub_id parameter is required'}, status=400) 
    
    chepters = Chepter.objects.filter(chep_sub__sub_id = stud_subject)
    serializer = chapterSerializer(chepters, many = True)

    return Response({'Title': 'Chapters',
                   'Your Chapters': serializer.data})


@api_view(['GET'])
def stud_timetables(request):
    student_batch = request.GET.get('stud_batch')
    if not student_batch:
        return Response({'error': 'stud_batch parameter is required'}, status=400)
    
    timetable_data = Timetable.objects.filter(tt_batch__batch_id = student_batch)
    timetable = TimetableSerializer(timetable_data, many = True)

    return Response({'Title' : 'Timetable',
                   'Your TT': timetable.data})



@api_view(['GET'])
def stud_attendence(request):
    student_id = request.GET.get('stud_id')
    student_std = request.GET.get('stud_std')

    if not student_id or not student_std:
        return Response({'error': 'stud_id and stud_std parameters are required'}, status=400)

    attendence_data = Attendance.objects.filter(atten_student__stud_id=student_id).order_by('-pk')
    attend = AttendanceSerializer(attendence_data, many=True)

    total_days = attendence_data.count()
    present_days = attendence_data.filter(atten_present=True).count()

    if total_days > 0:
        attendence_prec = round((present_days / total_days) * 100, 2)
    else:
        attendence_prec = 0

    subject_attendance = []
    subjects = Subject.objects.filter(sub_std__std_id=student_std).values('sub_name').distinct()
    for subject in subjects:
        subject_name = subject['sub_name']
        total_days_subwise = Attendance.objects.filter(
            atten_student__stud_id=student_id,
            atten_timetable__tt_subject1__sub_name=subject_name
        ).count()
        present_days_subwise = Attendance.objects.filter(
            atten_student__stud_id=student_id,
            atten_timetable__tt_subject1__sub_name=subject_name,
            atten_present=True
        ).count()
        if total_days_subwise > 0:
            attendence_prec_subwise = round((present_days_subwise / total_days_subwise) * 100, 2)
            subject_attendance.append({
                'subject': subject_name,
                'attendance_percentage': attendence_prec_subwise,
            })

    absent_days = total_days - present_days

    apidata = {
        'title': 'Attendance',
        'attendance_data': attend.data,
        'attendance_percentage': attendence_prec,
        'subject_attendance': subject_attendance,
        'total_days': total_days,
        'absent_days': absent_days,
    }

    return Response(apidata)


@api_view(['GET'])
def stud_fees_collection(request):
    student_id = request.GET.get('stud_id')

    if not student_id:
        return Response({'error': 'stud_id parameter is required'}, status=400)
    try:
        student_data = Students.objects.get(stud_id=student_id)
    except Students.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    
    student = StudentSerializer(student_data)

    discount_amount = Discount.objects.filter(discount_stud_id__stud_id = student_id) 
    stud_discount = DiscountSerializer(discount_amount, many = True)
    if discount_amount:
        fees_to_paid = int(student_data.stud_pack.pack_fees) - int(discount_amount[0].discount_amount)
    else:
        fees_to_paid = int(student_data.stud_pack.pack_fees)

    # ===========================Paid Fees========================================

    fees_collection = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id)
    collection = Fees_Collection_serial(fees_collection, many = True)
    if fees_collection:
        paid_fees = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id).aggregate(tol_amount=Sum('fees_paid'))
        paid_fees = int(paid_fees['tol_amount'])
    else:
        paid_fees = 0

    # ==========================Remaining_Fees====================================

    remaining_fees = fees_to_paid - paid_fees
   
    # ===========================Cheque Fees======================================

    cheque_data = Cheque_Collection.objects.filter(cheque_stud_id__stud_id = student_id, cheque_paid = False)
    cheque = Cheque_Collection_serial(cheque_data, many = True)

    apidata = {
        'title': 'Payments',
        'fees_collection':collection.data, 
        'fees_to_paid':fees_to_paid, 
        'paid_fees':paid_fees,
        'student_data':student.data, 
        'remaining_fees':remaining_fees,
        'cheque_data':cheque.data,
        'discount_amount':stud_discount.data

    }
    return Response(apidata)



@api_view(['GET'])
def student_analysis_view(request): 
    student_id = int(request.GET.get('stud_id'))
    student_std = int(request.GET.get('stud_std'))

    # ===============Overall Attendance==================
    if not student_id or not student_std:
        return Response({'error': 'stud_id and stud_std parameter is required'}, status=400)
    try:
        student_info = Students.objects.get(stud_id=student_id)
    except Students.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    
    student = StudentSerializer(student_info)

    student_data = Students.objects.filter(stud_std__std_id = student_std)
    student_data_serial = StudentSerializer(student_data, many = True)

    total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id).count()
    
    present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

    absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
        
    if total_attendence > 0:
        overall_attendence = (present_attendence/total_attendence)*100
    else:
        overall_attendence = 0



    # ==================Test Report and Attendance Report============
    students_li = Students.objects.filter(stud_std__std_id = student_std)
    overall_attendance_li = []

    for x in students_li:
        total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id).count()
        present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, atten_present=True).count()
        if total_attendence_studentwise > 0:
            overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
        else:
            overall_attendence_studentwise = 0
        
      
        total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
        
        obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
        
        if total_marks == 0:
            overall_result = 0
        else:
            overall_result = round((obtained_marks/total_marks)*100,2)


        if student_id == x.stud_id: 
            current_student_overall_test_result = overall_result
            

        overall_attendance_li.append({'stud_name':x.stud_name, 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})

    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]
    


   # ===================SubjectsWise Attendance============================
    subjects_li = Subject.objects.filter(sub_std__std_id = student_std).values('sub_name').distinct()
    overall_attendance_subwise = []
    for x in subjects_li:
        x = x['sub_name']
        total_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_student__stud_id=student_id).count()

        present_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_present=True,atten_student__stud_id=student_id).count()

        if total_attendence_subwise > 0:
            attendance_subwise = (present_attendence_subwise/total_attendence_subwise)*100
        else:
            attendance_subwise = 0
        overall_attendance_subwise.append({'sub_name': x, 'attendance_subwise':attendance_subwise})
      
    # ======================SubjectWise TestResult==============================

    subjects_data = Subject.objects.filter(sub_std=student_std)
    final_average_marks_subwise = []

    for x in subjects_data:
        total_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(total_sum_marks_subwise=Sum('tau_total_marks'))['total_sum_marks_subwise'] or 0
       

        obtained_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(obtained_sum_marks_subwise=Sum('tau_obtained_marks'))['obtained_sum_marks_subwise'] or 0
        
        
        if total_marks_subwise == 0:
            average_marks_subwise = 0
        else:
            average_marks_subwise = round((obtained_marks_subwise/total_marks_subwise)*100,2)
        
        final_average_marks_subwise.append({'subject_name':x.sub_name, 'average_marks_subwise':average_marks_subwise})

    # ====================Average Test Result=================================

    overall_results = [i['overall_result'] for i in overall_attendance_li]
    if overall_results:
        class_average_result = round(statistics.mean(overall_results), 2)
    else:
        class_average_result = 0
    

    total_test_conducted = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id).count()
    
    absent_in_test = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id,tau_obtained_marks = 0).count()

    # =============Doubts and Solution Counts================================

    doubt_asked = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).count()
    solutions_gives = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).annotate(verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        )))
    solutions = DoubtSerializer(solutions_gives, many = True)
    
    my_solve_doubts = 0
    for x in solutions_gives:
        if x.verified_solution > 0:
            my_solve_doubts += 1
        else:
            print("no verified")

    doubt_solved_byme = Doubt_solution.objects.filter(solution_stud_id__stud_id = student_id, solution_verified = True).count()

    

    apidata = {
        'title': 'Report-Card',
        'student':student.data,
        'student_data':student_data_serial.data,
        'overall_attendence':overall_attendence,
        'overall_attendance_li':overall_attendance_li,
        'overall_attendance_subwise':overall_attendance_subwise,
        'total_attendence':total_attendence,
        'absent_attendence':absent_attendence,
        'class_average_result':class_average_result,
        'final_average_marks_subwise':final_average_marks_subwise,
        'doubt_asked':doubt_asked,
        'solutions_gives':solutions.data,
        'doubt_solved_byme':doubt_solved_byme,
        'current_student_overall_test_result':current_student_overall_test_result,
        'my_solve_doubts':my_solve_doubts,
        'total_test_conducted':total_test_conducted,
        'absent_in_test':absent_in_test,

    }

    return Response(apidata)


@api_view(['GET', 'POST'])
def student_inquiries_data(request):
    standard_data = Std.objects.all()
    standard = stdSerializer(standard_data, many = True)

    if request.method == 'POST':
        data = request.data
        form = InquiriesSerializer(data = data)
        if form.is_valid():
            form.save()
        else:
            return Response({
                'Status': False,
                'Error': form.errors
            })
        
    return Response({
        'Status': False,
        'Standard': standard.data
    })



# ==========================================================================================================================================
                                                        # PARENTSIDE
# ==========================================================================================================================================

@api_view(['GET'])
def api_parent_profile(request):
    parent_id = request.GET.get('parent_id')

    if not parent_id:
        return Response({'Status': False, 'Message': 'parent_id is required'})
    
    parent_profile = Students.objects.filter(stud_id = parent_id)
    parent = StudentSerializer(parent_profile, many = True)
    return Response({
        'Title': 'Profile',
        'Parent data': parent.data
    })


@api_view(['GET'])
def api_parent_events(request):
    event_data = Event.objects.all()
    event = EventSerializer(event_data, many = True)
    event_imgs = Event_Image.objects.all()
    event_image = ImageSerializer(event_imgs, many = True)
    selected_events = Event.objects.all()[:1]
    selected = EventSerializer(selected_events, many = True)

    apidata={
        'title': 'Events',
        'event_data':event.data,
        'event_imgs':event_image.data,
        'selected_events':selected.data
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        selected = EventSerializer(selected_events, many = True)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id)
        event_image = ImageSerializer(event_imgs, many = True)
        
        apidata.update({'selected_events':selected.data, 'events_img':event_image.data})

    return Response(apidata)


@api_view(['GET'])
def api_parentside_report_card(request):
    student_id = int(request.GET.get('stud_id'))
    student_std = int(request.GET.get('stud_std'))

    # ===============Overall Attendance==================
    if not student_id or not student_std:
        return Response({'error': 'stud_id and stud_std parameter is required'}, status=400)
    try:
        student_info = Students.objects.get(stud_id=student_id)
    except Students.DoesNotExist:
        return Response({'error': 'Student not found'}, status=404)
    
    student = StudentSerializer(student_info)

    student_data = Students.objects.filter(stud_std__std_id = student_std)
    student_data_serial = StudentSerializer(student_data, many = True)

    total_attendence = Attendance.objects.filter(atten_student__stud_id = student_id).count()
    
    present_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=True).count()

    absent_attendence = Attendance.objects.filter(atten_student__stud_id = student_id, atten_present=False).count()
    
    if total_attendence > 0:
        overall_attendence = (present_attendence/total_attendence)*100
    else:
        overall_attendence = 0



    # ==================Test Report and Attendance Report============
    students_li = Students.objects.filter(stud_std__std_id = student_std)
    overall_attendance_li = []
    for x in students_li:
        total_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id).count()
        present_attendence_studentwise = Attendance.objects.filter(atten_student__stud_id = x.stud_id, atten_present=True).count()
        if total_attendence_studentwise > 0:
            overall_attendence_studentwise = (present_attendence_studentwise/total_attendence_studentwise)*100
        else:
            overall_attendence_studentwise = 0
        

        total_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_sum_marks=Sum('tau_total_marks'))['total_sum_marks'] or 0
        
        
        obtained_marks = Test_attempted_users.objects.filter(tau_stud_id__stud_id = x.stud_id).aggregate(total_obtained_marks=Sum('tau_obtained_marks'))['total_obtained_marks'] or 0
        

        if total_marks == 0:
            overall_result = 0
        else:
            overall_result = round((obtained_marks/total_marks)*100,2)

        if student_id == x.stud_id: 
            current_student_overall_test_result = overall_result

        overall_attendance_li.append({'stud_name':x.stud_name, 'overall_attendance_studentwise':overall_attendence_studentwise, 'overall_result':overall_result})

    
    overall_attendance_li = sorted(overall_attendance_li, key=lambda x: x['overall_result'], reverse=True)
    overall_attendance_li = overall_attendance_li[:5]
    


   # ===================SubjectsWise Attendance============================
    subjects_li = Subject.objects.filter(sub_std__std_id = student_std).values('sub_name').distinct()
    overall_attendance_subwise = []

    for x in subjects_li:
        x = x['sub_name']
        total_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_student__stud_id=student_id).count()

        present_attendence_subwise = Attendance.objects.filter(atten_timetable__tt_subject1__sub_name = x, atten_present=True,atten_student__stud_id=student_id).count()

        if total_attendence_subwise > 0:
            attendance_subwise = (present_attendence_subwise/total_attendence_subwise)*100
        else:
            attendance_subwise = 0
        overall_attendance_subwise.append({'sub_name': x, 'attendance_subwise':attendance_subwise})
    
    # ======================SubjectWise TestResult==============================

    subjects_data = Subject.objects.filter(sub_std=student_std)
    final_average_marks_subwise = []

    for x in subjects_data:
        total_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(total_sum_marks_subwise=Sum('tau_total_marks'))['total_sum_marks_subwise'] or 0
       

        obtained_marks_subwise = Test_attempted_users.objects.filter(tau_test_id__test_sub__sub_name = x.sub_name, tau_stud_id__stud_id=student_id).aggregate(obtained_sum_marks_subwise=Sum('tau_obtained_marks'))['obtained_sum_marks_subwise'] or 0
        
        
        if total_marks_subwise == 0:
            average_marks_subwise = 0
        else:
            average_marks_subwise = round((obtained_marks_subwise/total_marks_subwise)*100,2)
        
        final_average_marks_subwise.append({'subject_name':x.sub_name, 'average_marks_subwise':average_marks_subwise})

    # ====================Average Test Result=================================
    overall_results = [i['overall_result'] for i in overall_attendance_li]
    if overall_results:
        class_average_result = round(statistics.mean(overall_results), 2)
    else:
        class_average_result = 0
    

    total_test_conducted = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id).count()

    absent_in_test = Test_attempted_users.objects.filter(tau_stud_id__stud_id = student_id,tau_obtained_marks = 0).count()


    # =============Doubts and Solution Counts================================

    doubt_asked = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).count()

    solutions_gives = Doubt_section.objects.filter(doubt_stud_id__stud_id = student_id).annotate(verified_solution=Count(
        Case(
            When(doubt_solution__solution_verified=True, then=1),
            output_field=IntegerField(),
        )))
    solutions = DoubtSerializer(solutions_gives, many = True)

    my_solve_doubts = 0
    for x in solutions_gives:
        if x.verified_solution > 0:
            my_solve_doubts += 1
        else:
            print("no verified")

    doubt_solved_byme = Doubt_solution.objects.filter(solution_stud_id__stud_id = student_id, solution_verified = True).count()

    

    apidata = {
        'title': 'Report-Card',
        'student':student.data,
        'student_data':student_data_serial.data,
        'overall_attendence':overall_attendence,
        'overall_attendance_li':overall_attendance_li,
        'overall_attendance_subwise':overall_attendance_subwise,
        'total_attendence':total_attendence,
        'absent_attendence':absent_attendence,
        'class_average_result':class_average_result,
        'final_average_marks_subwise':final_average_marks_subwise,
        'doubt_asked':doubt_asked,
        'solutions_gives':solutions.data,
        'doubt_solved_byme':doubt_solved_byme,
        'current_student_overall_test_result':current_student_overall_test_result,
        'my_solve_doubts':my_solve_doubts,
        'total_test_conducted':total_test_conducted,
        'absent_in_test':absent_in_test,

    }
    
    return Response(apidata)


@api_view(['GET'])
def api_parentside_payment(request):
    student_id = request.GET.get('stud_id')
    student_data = Students.objects.get(stud_id = student_id)
    student = StudentSerializer(student_data)

    discount_amount = Discount.objects.filter(discount_stud_id__stud_id = student_id) 
    discount_fee = DiscountSerializer(discount_amount, many = True)
    if discount_amount:
        fees_to_paid = int(student_data.stud_pack.pack_fees) - int(discount_amount[0].discount_amount)
    else:
        fees_to_paid = int(student_data.stud_pack.pack_fees)

    # ===========================Paid Fees========================================

    fees_collection = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id)
    feecollection = Fees_Collection_serial(fees_collection, many = True)
    if fees_collection:
        paid_fees = Fees_Collection.objects.filter(fees_stud_id__stud_id = student_id).aggregate(tol_amount=Sum('fees_paid'))
        paid_fees = int(paid_fees['tol_amount'])
    else:
        paid_fees = 0

    # ==========================Remaining_Fees====================================

    remaining_fees = fees_to_paid - paid_fees
   
    # ===========================Cheque Fees======================================

    cheque_data = Cheque_Collection.objects.filter(cheque_stud_id__stud_id = student_id, cheque_paid = False)
    cheque = Cheque_Collection_serial(cheque_data, many = True)

    apidata = {
        'title': 'Payments',
        'fees_collection':feecollection.data, 
        'fees_to_paid':fees_to_paid, 
        'paid_fees':paid_fees,
        'student_data':student.data, 
        'remaining_fees':remaining_fees,
        'cheque_data':cheque.data,
        'discount_amount':discount_fee.data

    }
    return Response(apidata)


@api_view(['GET'])
def api_parentside_announcement(request):
    announcements_data = Announcements.objects.filter(
    Q(announce_std=None, announce_batch=None) |
    Q(announce_std__std_id=request.session.get('stud_std'), announce_batch=None) |
    Q(announce_std__std_id=request.session.get('stud_std'), announce_batch__batch_id=request.session.get('stud_batch'))
    ).order_by('-pk')[:50]

    Announcement = AnnouncementSerializer(announcements_data, many = True)
    return Response({'Title': 'Announcement', 'Announcements': Announcement.data})


@api_view(['GET'])
def api_parentside_timetable(request):
    student_batch = request.GET.get('stud_batch')
    
    timetable_data = Timetable.objects.filter(tt_batch__batch_id = student_batch)
    Timetable_info = TimetableSerializer(timetable_data, many = True)

    return Response({'Title': 'Timetable', 'Timetable': Timetable_info.data})



# ========================================================================================================================================================
                                                            # TEACHERSIDE
# ========================================================================================================================================================

@api_view(['GET'])
def api_teacher_timetable(request):
     timetable_data = Timetable.objects.all()

     teacher_tt = TimetableSerializer(timetable_data, many = True)

     apidata = {
        'Title':'Timetable',
        'timetable_data':teacher_tt.data,
     }
     return Response(apidata)


@api_view(['GET', 'POST'])
def api_teacher_attendance(request):
     fac_id = request.GET.get('fac_id')
     faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
     batch_access_list = []
     std_access_list=[]
     for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)

     data = Attendance.objects.all()
     attended = AttendanceSerializer(data, many =True)
     std_data = Std.objects.filter(std_id__in = std_access_list)
     standard = stdSerializer(std_data, many = True)   
     batch_data = Batches.objects.filter(batch_id__in = batch_access_list)
     batch = BatchSerializer(batch_data, many = True)
     stud_data = Students.objects.all()
     student = StudentSerializer(stud_data, many = True)
     subj_data = Subject.objects.all()
     subject = subjectsSerializer(subj_data, many =True)
          
     today = timezone.localdate()
     
     today_records = Attendance.objects.filter(atten_date__contains=today)
     
     distinct_data = today_records.annotate(date=TruncDate('atten_date'),
                                            hour=TruncHour('atten_date'),
                                            minute=TruncMinute('atten_date'),
                                            ).values('date', 'hour', 'minute','atten_timetable').distinct()
     
     li = []
     for x in distinct_data:
        date_hour = x['hour'].hour
        date_minute = x['minute'].minute
        date_data = x['minute'].date()
        date_str = date_data.strftime('%Y-%m-%d')
        subjectt = Timetable.objects.get(tt_id = x['atten_timetable'])
        subj = TimetableSerializer(subjectt)
        li.append({'hour':date_hour,'date':date_str, 'minute':date_minute,'tt_id':x['atten_timetable'],'subject':subj.data})
    
    
    
     context ={
          'Title' : 'Attendance',
          'data' : attended.data,
          'std_data' : standard.data,
          'batch_data':batch.data,
          'stud_data':student.data,
          'sub_data':subject.data,
          'li':li,
    }
    
     if request.GET.get('get_std'):
          get_std = int(request.GET['get_std'])
          if get_std == 0:
               pass
          else:    
               data = data.filter(atten_timetable__tt_batch__batch_std__std_id = get_std)
               attended = AttendanceSerializer(data, many =True)
               batch_data = batch_data.filter(batch_std__std_id = get_std)
               batch_info = BatchSerializer(batch_data, many = True)
               stud_data = stud_data.filter(stud_std__std_id = get_std)
               student = StudentSerializer(stud_data, many = True)
               subj_data = subj_data.filter(sub_std__std_id = get_std)
               subject = subjectsSerializer(subj_data, many =True)
               get_std = Std.objects.get(std_id = get_std)
               getting_std = stdSerializer(get_std)
               context.update({'data':attended.data,'batch_data':batch_info.data,'get_std':getting_std.data, 'stud_data':student.data,'sub_data':subject.data})
     
     if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(atten_timetable__tt_batch__batch_id = get_batch)
            attended = AttendanceSerializer(data, many =True)
            stud_data = stud_data.filter(stud_batch__batch_id = get_batch)
            student = StudentSerializer(stud_data, many = True)
            get_batch = Batches.objects.get(batch_id = get_batch)
            getting_batch = BatchSerializer(get_batch)
            context.update({'data':attended.data,'get_batch':getting_batch.data,'stud_data':student.data}) 

     if request.GET.get('get_student'):
        get_student = int(request.GET['get_student'])
        if get_student == 0:
            pass
        else:
            data = data.filter(atten_student__stud_id = get_student)
            attended = AttendanceSerializer(data, many =True)
            get_student = Students.objects.get(stud_id = get_student)
            getting_stud = StudentSerializer(get_student)
            context.update({'data':attended.data,'get_student':getting_stud.data})                     


     attendance_present = data.filter(atten_present = True).count()
     attendance_all = data.all().count()
     if attendance_all>0:
        overall_attendance = round((attendance_present/attendance_all) * 100,2)
        context.update({'overall_attendance':overall_attendance})

     sub_list = subj_data.all().values('sub_name').distinct()
     subject_wise_attendance = []
     subjects = []
     for x in sub_list:
        sub_name = x['sub_name']
        sub_one = data.filter(atten_present = True,atten_timetable__tt_subject1__sub_name=sub_name).count()
        sub_all = data.filter(atten_timetable__tt_subject1__sub_name = sub_name).count()
        if sub_all>0:
            sub_attendance = round((sub_one/sub_all) * 100,2)
            subject_wise_attendance.append(sub_attendance)
            subjects.append(sub_name)
            
     combined_data = zip(subject_wise_attendance, subjects)

     context.update({'combined_data': combined_data})
     return Response(context)


@api_view(['GET', 'POST'])
def api_teacher_edit_attendance(request):
    if request.GET.get('get_std') and request.GET.get('get_batch'):
        get_std = request.GET['get_std']     
        get_batch = request.GET['get_batch']
        tt_id = request.GET['tt_id']
        std_data = Std.objects.get(std_id=get_std)
        standard_data = stdSerializer(std_data)
        batch_data = Batches.objects.get(batch_id=get_batch) 
        batch = BatchSerializer(batch_data)
        timetable_data = Timetable.objects.filter(tt_batch__batch_id = get_batch)
        teacher_tt = TimetableSerializer(timetable_data, many = True)
        students_data = Students.objects.filter(stud_std__std_id = get_std, stud_batch__batch_id = get_batch)
        student = StudentSerializer(students_data, many = True)
        get_hour = request.GET.get('hour','')    
        get_date = request.GET.get('date','')
        get_minute = request.GET.get('minute','')
        date_obj = datetime.strptime(get_date, '%Y-%m-%d')
        get_data = Attendance.objects.filter(atten_date__hour=get_hour, atten_date__date=date_obj,atten_timetable__tt_id=tt_id)
        data = AttendanceSerializer(get_data, many = True)
        context = {
          'title': 'Insert Attendence',
          'std_data':standard_data.data,
          'batch_data':batch.data,
          'students_data':student.data,
          'timetable_data':teacher_tt.data,
          'get_data':data.data,
          'get_date':get_date,
          'get_hour':get_hour,
          'get_minute':get_minute,
     
          }
    else:
        return Response({'Error' : 'Please! Select Standard (get_std) And Batch (get_batch)'})
    
    return Response(context)


# @api_view(['GET', 'POST'])
# def api_edit_handle_attendance(request):
#      if request.method == 'POST':
#         get_date = request.POST.get('get_date')
#         get_hour = request.POST.get('get_hour')
#         get_date = datetime.strptime(get_date, '%Y-%m-%d')
#         atten_timetable = request.POST.get('atten_timetable')
#         atten_tt = Timetable.objects.get(tt_id = atten_timetable)
#         # selected_items = request.POST.getlist('selection')
#         selected_items = [2]
#         if selected_items:
#           selected_ids = [int(id) for id in selected_items]
#         current_all_attendance = Attendance.objects.filter(atten_date__hour=get_hour, atten_date__date=get_date,atten_timetable__tt_id = atten_timetable)  
#         for i in current_all_attendance:
#             if i.atten_student.stud_id in selected_ids:
#                 instance = Attendance.objects.get(atten_date__hour=get_hour, atten_date__date=get_date, atten_student__stud_id=i.atten_student.stud_id)  
#                 instance.atten_present = 1
#                 instance.save()
#             else:
#                 instance = Attendance.objects.get(atten_date__hour=get_hour, atten_date__date=get_date, atten_student__stud_id=i.atten_student.stud_id)
#                 instance.atten_present = 0
#                 instance.save()

#         return Response({'Status': True, 'Message' : "Attendance has been updated!"})
#      return Response({'Status': 'Use post method'})


@api_view(['GET', 'POST'])
def api_edit_handle_attendance(request):
    if request.method == 'POST':
        get_date = request.POST.get('get_date')
        get_hour = request.POST.get('get_hour')
        
        # Check if get_date is provided
        if not get_date:
            return Response({'Status': False, 'Message': 'Date is required'}, status=400)
        
        try:
            # Convert get_date to a datetime object
            get_date = datetime.strptime(get_date, '%Y-%m-%d')
        except ValueError:
            return Response({'Status': False, 'Message': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)
        
        atten_timetable = request.POST.get('atten_timetable')
        try:
            atten_tt = Timetable.objects.get(tt_id=atten_timetable)
        except Timetable.DoesNotExist:
            return Response({'Status': False, 'Message': 'Timetable not found'}, status=404)

        # selected_items = request.POST.getlist('selection')
        selected_items = [2]  # Example: Replace this with actual data
        if selected_items:
            selected_ids = [int(id) for id in selected_items]

        # Query for the attendance records for the specified date, hour, and timetable
        current_all_attendance = Attendance.objects.filter(
            atten_date__hour=get_hour, 
            atten_date__date=get_date,
            atten_timetable__tt_id=atten_timetable
        )
        
        # Update attendance records based on selected items
        for i in current_all_attendance:
            instance = Attendance.objects.get(
                atten_date__hour=get_hour,
                atten_date__date=get_date,
                atten_student__stud_id=i.atten_student.stud_id
            )
            instance.atten_present = 1 if i.atten_student.stud_id in selected_ids else 0
            instance.save()

        return Response({'Status': True, 'Message': "Attendance has been updated!"})
    
    return Response({'Status': 'Use POST method'}, status=405)


@api_view(['GET'])
def api_insert_update_attendance(request):
     if request.GET.get('get_std') and request.GET.get('get_batch'):
        get_std = request.GET['get_std']     
        get_batch = request.GET['get_batch']
        std_data = Std.objects.get(std_id=get_std)
        std_serial = stdSerializer(std_data)
        batch_data = Batches.objects.get(batch_id=get_batch) 
        batch_serial = BatchSerializer(batch_data)
        timetable_data = Timetable.objects.filter(tt_batch__batch_id = get_batch)
        tt = TimetableSerializer(timetable_data, many = True)
        students_data = Students.objects.filter(stud_std__std_id = get_std, stud_batch__batch_id = get_batch)
        student = StudentSerializer(students_data, many = True)

        context = {
          'title': 'Insert Attendence',
          'std_data':std_serial.data,
          'batch_data':batch_serial.data,
          'students_data':student.data,
          'timetable_data':tt.data,
     
          }
     else:
        return Response({'Status': False, 'Message':"Please! Select get_std And get_batch"})
       
     return Response(context)


@api_view(['GET', 'POST'])
def api_handle_attendance(request):
     if request.method == 'POST':
        std_data = request.POST.get('std_data')
        batch_data = request.POST.get('batch_data')
        atten_timetable = request.POST.get('atten_timetable')
        atten_tt = Timetable.objects.get(tt_id = atten_timetable)
        # selected_items = request.POST.getlist('selection')
        selected_items = [2]
        students_all = Students.objects.filter(stud_batch__batch_id = batch_data, stud_std__std_id = std_data)
        if selected_items:
          selected_ids = [int(id) for id in selected_items]
        for i in students_all:
            if i.stud_id in selected_ids:
                Attendance.objects.create(atten_timetable=atten_tt, atten_student=i, atten_present=1)
            else:
                Attendance.objects.create(atten_timetable=atten_tt, atten_student=i, atten_present=0) 

            return Response({'Status': True, 'message':"Attendance has been submitted!"})
     return Response({'Status': False, 'Message': 'Use post method'})


@api_view(['GEt'])
def api_teacher_events(request):
    event_data = Event.objects.all()
    event_serial = EventSerializer(event_data, many = True)
    event_imgs = Event_Image.objects.all()
    image = ImageSerializer(event_imgs, many = True)
    selected_events = Event.objects.all()[:1]
    selected = EventSerializer(selected_events, many = True)
    context={
        'title':'Events',
        'event_data':event_serial.data,
        'event_imgs':image.data,
        'selected_events':selected.data,
    }

    if request.GET.get('event_id'):
        event_id = request.GET['event_id']
        selected_events = Event.objects.filter(event_id = event_id)
        selected = EventSerializer(selected_events, many = True)
        event_imgs = Event_Image.objects.filter(event__event_id = event_id)
        image = ImageSerializer(event_imgs, many = True)
        context.update({'selected_events':selected_events, 'events_img':event_imgs})

    return Response(context)


@api_view(['GET'])
def api_teacher_announcement(request):
    fac_id = request.GET.get('fac_id')
    faculty_access = Faculty_Access.objects.filter(fa_faculty__fac_id = fac_id)
    batch_access_list = []
    std_access_list=[]
    for x in faculty_access:
        batch_access_list.append(x.fa_batch.batch_id)
        std_access_list.append(x.fa_batch.batch_std.std_id)

    data = Announcements.objects.all()
    Announcement = AnnouncementSerializer(data, many =True)
    std_data = Std.objects.filter(std_id__in = std_access_list)
    standard = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.filter(batch_id__in = batch_access_list)
    batch = BatchSerializer(batch_data, many = True)
   
    context ={
        'title' : 'Announcements',
        'data' : Announcement.data,
        'std_data' : standard.data,
        'batch_data':batch.data,
    }
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(announce_std__std_id = get_std)
            Announcement = AnnouncementSerializer(data, many =True)
            batch_data = batch_data.filter(batch_std__std_id = get_std)
            batch = BatchSerializer(batch_data, many = True)
            get_std = Std.objects.get(std_id = get_std)
            getting_std = stdSerializer(get_std)
            context.update({'data':Announcement.data,'batch_data':batch.data,'get_std':getting_std.data})
            

    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        if get_batch == 0:
            pass
        else:
            data = data.filter(announce_batch__batch_id = get_batch)
            Announcement = AnnouncementSerializer(data, many =True)
            get_batch = Batches.objects.get(batch_id = get_batch)
            getting_batch = BatchSerializer(get_batch)
            context.update({'data':Announcement.data,'get_batch':getting_batch.data})        
            
    return Response(context)


@api_view(['GET', 'POST'])
def api_announcements_update_teacher(request):
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)
    batch_data = Batches.objects.all()
    batch_serializer = BatchSerializer(batch_data, many=True)

    apidata = {
        'std_data': std_serializer.data,
        'batch_data': batch_serializer.data
    }
    # ------------getting students for mail------------------
    # students_for_mail = Students.objects.all()

    
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        get_std_serializer = stdSerializer(get_std)
        std_data = std_data.filter(std_id = get_std)
        std_serializer = stdSerializer(std_data, many = True)
        batch_data = batch_data.filter(batch_std__std_id = get_std)
        batch_serializer = BatchSerializer(batch_data, many=True)
        # students_for_mail = students_for_mail.filter(stud_std=get_std)
        apidata.update({'get_std ':get_std_serializer.data,'std_data':std_serializer.data,'batch_data':batch_serializer.data}) 
    
    if request.GET.get('get_batch'):
        get_batch = int(request.GET['get_batch'])
        get_batch_serializer = BatchSerializer(get_batch)
        batch_data = batch_data.filter(batch_id = get_batch)
        batch_serializer = BatchSerializer(batch_data, many=True)
        # students_for_mail = students_for_mail.filter(stud_batch=get_batch)
        apidata.update({'get_batch ':get_batch_serializer.data,'batch_data':batch_serializer.data})

    if request.method == 'POST':

        # ================update Logic============================
        if request.GET.get('pk'):
            instance = get_object_or_404(Announcements, pk=request.GET['pk'])
            data = request.data
            form = AnnouncementSerializer(data=data, instance=instance, partial = True)       
            if form.is_valid():
                form.save()
                return Response({
                        'status': 'success',
                        'data': form.data,
                        'StdData':std_serializer.data
                    })
            else:
                filled_data = form.data
                return Response({'filled_data ':filled_data,'errors':form.errors})

        # ===================insert_logic===========================
        data = request.data
        form = AnnouncementSerializer(data=data)
        if form.is_valid():
            form.save()
            # ---------------------sendmail Logic===================================
            # students_email_list = []
            # for x in students_for_mail:
            #     students_email_list.append(x.stud_email)
            # print(students_email_list)    
            # announcement_mail(form.cleaned_data['announce_title'],form.cleaned_data['announce_msg'],students_email_list)
         
            return Response({
                    'Status':'Form saved',
                    'Data': form.data
                })
        else:
            filled_data = form.data
            return Response({'filled_data ':filled_data,'errors':form.errors})

    if request.GET.get('pk'):
        update_data = Announcements.objects.get(announce_id = request.GET['pk'])
        serializer = AnnouncementSerializer(update_data)
        return Response({
            'status': 'Done',
            'data':serializer.data
        }) 
    
    return Response(apidata)


@api_view(['POST', 'GET'])
def api_announcements_delete_teacher(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selection')
        if selected_items:
            selected_ids = [int(id) for id in selected_items]
            try:
                Announcements.objects.filter(announce_id__in=selected_ids).delete()
                return Response({
                    'status': True,
                    'Message': 'Deleted successfully'
                })
            except Exception as e:
                return Response({
                    'status': False,
                    'message': "Can't delete {}".format(e)  
                })

    return Response({
        'status': False,
        'message': 'Something is wrong'
    })