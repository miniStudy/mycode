from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from .serializers import * 
from rest_framework import status 
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

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
                filled_data = form.data
                return Response({
                    'status': False,
                    'message': 'Error occur',
                    'data': form.data
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
            filled_data = form.data
            print(filled_data)
            return Response({
                'status': True,
                'message': 'nothing happend',
                'data': filled_data
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
                filled_data = form.data
                return Response({
                    'status': 'Failed',
                    'message': 'Error occur',
                    'data': form.data
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
            filled_data = form.data
            print(filled_data)
            return Response({
                'status': True,
                'message': 'nothing happend',
                'data': filled_data
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
   
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)    
    return Response({
        'data' : serializer.data,
        'title' : 'Subjects',
        'std_data' : std_serializer.data,
    })
    


@api_view(['POST', 'GET'])
def api_update_subjects(request):
    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data, many = True)

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        std_data = std_data.filter(std_id = get_std) 

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
                        'status':'Error',
                        'message':'error in form'
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
                        'Status':'Form saved'
                    })
            else:
                return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'errors': form.errors,
                })
        
    return Response({'Message':'Something went Wrong'})   


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

    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std == 0:
            pass
        else:    
            data = data.filter(chep_sub__sub_std__std_id = get_std)
            subject_data = subject_data.filter(sub_std__std_id = get_std)
            get_std = Std.objects.get(std_id = get_std)
            


    if request.GET.get('get_subject'):
        get_subject = int(request.GET['get_subject'])
        if get_subject == 0:
            pass
        else:    
            data = data.filter(chep_sub__sub_id = get_subject)
            get_subject = Subject.objects.get(sub_id = get_subject)
            

    return Response({
        'Status': True,
        'Data': data_serializer.data,
        'Title': 'Chapters',
        'std': std_data_serializer.data,
        'subject': subject_serializer.data
    })


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
                        'status':'Error',
                        'message':'error in form'
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
                        'Status':'Form saved'
                    })
            else:
                return Response({
                    'Status': False,
                    'Message': 'Invalid data',
                    'errors': form.errors,
                })
            
    return Response({'Message':'Something went Wrong'}) 


@api_view(['POST', 'GET'])
def api_delete_faculties(request):
    if request.method == 'POST':
        selected_items = request.POST.get('selection', [])
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


#==============================================TimeTable==================================================================

@api_view(['GET'])
def api_timetable(request):
    data = Timetable.objects.all()
    data_serializer = TimetableSerializer(data)

    std_data = Std.objects.all()
    std_serializer = stdSerializer(std_data)

    # batch_data = Batches.objects.all()
    # batch_serializer = batchSerializer(batch_data)
   
 
    if request.GET.get('get_std'):
        get_std = int(request.GET['get_std'])
        if get_std != 0:  
            data = data.filter(tt_batch__batch_std__std_id=get_std)
            # batch_data = batch_data.filter(batch_std__std_id=get_std)
            get_std = Std.objects.get(std_id=get_std)
            serializer = stdSerializer(get_std)
            return Response({'data': data_serializer.data,
                            'Title': 'Timetable',
                            # 'batch_data': batch_data,
                            'get_std': serializer.data
                            })

    # if request.GET.get('get_batch'):
    #     get_batch = int(request.GET['get_batch'])
    #     if get_batch != 0:
    #         data = data.filter(tt_batch__batch_id=get_batch)
    #         get_batch = Batches.objects.get(batch_id=get_batch)
    #         batch_serializer = 
    #         return Response({'data': data, 'get_batch': get_batch})        
            
    return Response({
        'Status': False,
        'Error': 'Something is wrong'
    })