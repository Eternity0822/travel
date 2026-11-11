
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render
from home.models import TravelInfo
from user.models import UserInfo
from utils import util
from AI.Get_Message import Get_DeepSeek

# 展示前端页面
def index(request):

    # 数据统计
    non_free_count = TravelInfo.objects.exclude(
        Q(actual_price='免费') | Q(actual_price__isnull=True)
    ).count()

    pro_count = TravelInfo.objects.values('province').distinct().count()
    city_count = TravelInfo.objects.values('city').distinct().count()
    total_reviews = TravelInfo.objects.aggregate(total_reviews=Sum('review_count'))['total_reviews'] or 0

    # 地图数据
    sql = 'select * from part6'
    res = util.query(sql)
    mapData = [{'name': item[1], 'value': item[2]} for item in res]

    # 景区热度排行
    top_5_travel = TravelInfo.objects.all().order_by('-popularity_score')[:5]
    top_10_travel = TravelInfo.objects.all().order_by('-review_count')[:10]

    # 用户创建时间分布数据
    daily_users = UserInfo.objects.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    name_list = [str(item['date']) for item in daily_users]
    value_list = [item['count'] for item in daily_users]

    content = {
        'non_free_count': non_free_count,
        'pro_count': pro_count,
        'city_count': city_count,
        'total_reviews': total_reviews,
        'mapData': mapData,
        'top_5_travel': top_5_travel,
        'top_10_travel': top_10_travel,
        'name_list': name_list,
        'value_list': value_list,
    }

    return render(request, 'index.html', content)

# 展示旅游景点列表
def travel_list(request):
    # 获取所有省份数据，展示在 国内旅游景点 模块
    provinces = TravelInfo.objects.exclude(province__isnull=True).values_list('province', flat=True).distinct()

    # 初始化查询条件
    travels = TravelInfo.objects.all()

    # 获取搜索条件
    search_name = request.GET.get('search_name', '')
    selected_province = request.GET.get('province', '')

    # 应用筛选条件
    if search_name:
        travels = travels.filter(Q(name__icontains=search_name))

    if selected_province:
        travels = travels.filter(province=selected_province)

    # 排序
    travels = travels.order_by('-popularity_score')

    # 分页效果
    paginator = Paginator(travels, 10)

    # 获取当前页码
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    content = {
        'provinces': provinces,
        'page_obj': page_obj,
        'search_name': search_name,
        'selected_province': selected_province,
    }

    return render(request, 'travel_list.html', content)

def get_ai_travelRoute(request):

    if request.method == 'POST':
        try:
            # 获取数据
            if hasattr(request, 'data'):
                data = request.data
            else:
                try:
                    data = json.loads(request.body.decode('utf-8'))
                except json.JSONDecodeError:
                    return JsonResponse({
                        'code':400,
                        'message':'无效的json数据',
                        'data':None
                    })
            # 字段检查
            required_fields = ['city', 'season', 'days']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                    'code':400,
                    'message':f'缺少必要字段{field}',
                    'data':None
                })

            budget = data.get('budget', 0)
            if budget == 0:
                budget = '无预算'
                
            dp = Get_DeepSeek()
            result = dp._get_travel_plan(city=data['city'], season=data['season'], days=data['days'], budget=budget)
            if result['code'] == 200:
                return JsonResponse({
                    'code':200,
                    'message':'旅游路线生成成功',
                    'data':result['data']
                })
            else:
                return JsonResponse({
                    'code':result['code'],
                    'message':'旅游路线生成失败',
                    'data':None
                })

        except Exception as e:
            return JsonResponse({
                    'code':500,
                    'message':f'服务器内部错误：{str(e)}',
                    'data':None
                })
    else:
        return render(request, 'get_ai_travelRoute.html')