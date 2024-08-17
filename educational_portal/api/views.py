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


