
from django.http import JsonResponse, request
from django.shortcuts import render
from django.shortcuts import redirect
from user.models import UserInfo
import os
import travel.settings as settings
import django.utils.timezone as timezone


# Create your views here.
def login(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            try:
                user = UserInfo.objects.get(username=username)
            except UserInfo.DoesNotExist:
                return JsonResponse({'code': 400, 'msg': '用户名不存在'})
            
            if user.password != password:
                return JsonResponse({'code': 400, 'msg': '用户名或密码错误'})
            
            request.session['uid'] = user.id
            request.session['uname'] = user.username
            request.session['avatar'] = user.avatar

            return JsonResponse({'code': 200, 'msg': '登录成功'})

        except Exception as e:
            return JsonResponse({'code': 500, 'msg': f'服务器错误{str(e)}'})
        
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            if UserInfo.objects.filter(username=username).exists():
                return JsonResponse({'code': 400, 'msg': '用户名已存在'})
            if UserInfo.objects.filter(uemail=email).exists():
                return JsonResponse({'code': 400, 'msg': '邮箱已存在'})
            
            UserInfo.objects.create(
                username=username, 
                uemail=email, 
                password=password,
                uaddress='',
                uphone='',
                uyoubian = '',
                avatar = '',
            )
            return JsonResponse({'code': 200, 'msg': '注册成功'})

        except Exception as e:
            return JsonResponse({'code': 500, 'msg': f'服务器错误{str(e)}'})
    else:
        return render(request, 'register.html')
    
def changeinfo(request):
    uid = request.session.get('uid')
    if request.method == 'POST':
        try:
            user = UserInfo.objects.get(id=uid)

            # 获取表单数据
            username = request.POST.get('username')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            youbian = request.POST.get('youbian')

            # 检查用户名是否被其他用户占用
            if username and username != user.username:
                if UserInfo.objects.filter(username=username).exclude(id=uid).exists():
                    return render(request, 'changeinfo.html', {
                        'user': user,
                        'success':None,
                        'error':'用户名已存在'
                    })
                user.username = username

            # 检查邮箱是否被其他用户占用
            if email and email != user.uemail:
                if UserInfo.objects.filter(uemail=email).exclude(id=uid).exists():
                    return render(request, 'changeinfo.html', {
                        'user': user,
                        'success':None,
                        'error':'邮箱已存在'
                    })
                user.uemail = email

            # 更新其他信息
            if phone:
                user.uphone = phone
            if address:
                user.uaddress = address
            if youbian:
                user.uyoubian = youbian
            user.save()

            # 更新session中的用户名
            request.session['uname'] = user.username

            return render(request, 'changeinfo.html', {
                'user': user,
                'success':'个人信息更新成功',
                'error':None
                })
        except UserInfo.DoesNotExist:
            return render(request, 'changeinfo.html', {
                'success':None,
                'error':'用户不存在'
                })
        except Exception as e:
            return render(request, 'changeinfo.html', {
                'success':None,
                'error':f'服务器错误{str(e)}'
                })
    else:
        # GET请求，显示个人信息
        try:
            user = UserInfo.objects.get(id=uid)
            return render(request, 'changeinfo.html', {
                'user': user,
                'success':None,
                'error':None
                })
        except UserInfo.DoesNotExist:
            return render(request, 'changeinfo.html', {
                'success':None,
                'error':'用户不存在'
                })
        
def upload_avatar(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        try:
            user = UserInfo.objects.get(id=uid)

            if 'avatar' not in request.FILES:
                return JsonResponse({'code': 400, 'msg': '请选择头像文件'})
            
            avatar_file = request.FILES['avatar']

            # 验证文件类型
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if avatar_file.content_type not in allowed_types:
                return JsonResponse({'code': 400, 'msg': '仅支持jpg、png、gif、webp格式的图片'})
            
            # 验证文件大小（最大2MB）
            if avatar_file.size > 2 * 1024 * 1024:
                return JsonResponse({'code': 400, 'msg': '图片大小不能超过2MB'})
            
            # 创建头像存储目录
            avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)

            # 生成文件名
            file_extension = os.path.splitext(avatar_file.name)[1]
            filename = f'avatar_{uid}_{int(timezone.now().timestamp())}{file_extension}'
            filepath = os.path.join(avatar_dir, filename)

            # 保存文件
            with open(filepath, 'wb+') as destination:
                for chunk in avatar_file.chunks():
                    destination.write(chunk)

            # 更新用户头像路径
            avatar_url = f'/media/avatars/{filename}'
            user.avatar = avatar_url
            user.save()

            # 更新session中的头像路径
            request.session['avatar'] = avatar_url

            return JsonResponse({
                'code': 200,
                'msg': '头像上传成功', 
                'avatar_url': avatar_url
            })
        
        except UserInfo.DoesNotExist:
            return JsonResponse({'code': 404, 'msg': '用户不存在'})
        except Exception as e:
            return JsonResponse({'code': 500, 'msg': f'服务器错误{str(e)}'})
    
    return JsonResponse({'code': 400, 'msg': '请求方法错误'})

def logout(request):
    request.session.clear()
    return redirect('user:login')