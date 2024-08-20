from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from .serializers import * 
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import math
import statistics
import random
from django.http import Http404,JsonResponse
from django.db.models import Count,Sum, F, Case, When, Value, IntegerField

#=========================================Boards======================================================

@api_view(['GET'])
def get_boards(request):
    result = Boards.objects.all()
    apidata = BoardsSerializer(result, many=True)
    print(apidata)
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
        print(instance)
        if request.method == "POST":
            form = BoardsSerializer(data = data, instance=instance, partial = True)
            print(form)
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
        print(selected_items)
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
        print(get_std)
        if get_std == 0:
            pass
        else:    
            data = data.filter(chep_sub__sub_std__std_id = get_std)
            data_serializer = chapterSerializer(data, many=True)
            print(data_serializer.data)
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
            print(data)
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



# ==================================================== Bank ==================================================================


def fees_collection_admin(request):
    cheque_collections_data = Cheque_Collection.objects.filter(cheque_paid=False)

    students_data = Students.objects.annotate(
    amount_paid=Sum('fees_collection__fees_paid'),
    discountt=Case(
        When(discount__discount_amount=None, then=Value(0)),
        default=F('discount__discount_amount'),output_field=IntegerField()
    ))

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


    context={
        'title':'Payments',
        'cheque_collections_data':cheque_collections_data,
        'total_amount_fees_paid':total_amount_fees_paid,
        'total_fees_amount_after_discount':total_fees_amount_after_discount,
        'total_pending_fees':total_pending_fees,
        'students_data':students_data,
    }
    return render(request, 'fees_collection_admin.html', context)
