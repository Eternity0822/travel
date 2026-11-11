
from django.shortcuts import render
from django.http import JsonResponse
from utils import util

# 展示数据分析 & 可视化图表
def part1(request):
    # 从 part1 中找景点评分数据
    sql1 = 'select * from part1'
    res1 = util.query(sql1)
    data_list = [{'value': item[2], 'name': item[1]} for item in res1]

    # 从 part8 中找省份景点平均评分数据
    sql2 = 'select * from part8'
    res2 = util.query(sql2)
    name_list = [item[1] for item in res2]
    travel_num_list = [item[2] for item in res2]
    avg_score_list = [item[3] for item in res2]

    content = {
        'data_list': data_list,
        'name_list': name_list,
        'travel_num_list': travel_num_list,
        'avg_score_list': avg_score_list,
    }

    return render(request, 'ksh/part1.html', content)

# 展示景点热度数据
def part2(request):
    # 从 part2 中找景点评论数
    sql1 = 'select * from part2'
    res1 = util.query(sql1)
    name_list = [{'name': item[1]} for item in res1]
    data_list = [{'value': item[2], 'name': item[1]} for item in res1]

    sql2 = 'select distinct city from part7'
    res2 = util.query(sql2)
    selected_list = [item[0] for item in res2]

    content = {
        'data_list': data_list,
        'name_list': name_list,
        'selected_list': selected_list,
    }

    return render(request, 'ksh/part2.html', content)

def get_cityData(request):
    city = request.GET.get('city', '')

    sql = f"select name,value from part7 where city='{city}'"
    res = util.query(sql)

    name_list = [i[0] for i in res]
    value_list = [i[1] for i in res]

    content = {
        'names':name_list,
        'values':value_list,
    }

    return JsonResponse({"data": content})

def part3(request):

    sql = 'select * from part3'
    res = util.query(sql)

    name_list = [i[1] for i in res]
    value_list = [i[2] for i in res]

    content = {
        'name_list':name_list,
        'value_list':value_list,
    }

    return render(request, 'ksh/part3.html', content)

def part4(request):

    sql = 'select * from part4'
    res = util.query(sql)
    data_list = [{'name':i[1], 'value':i[2]} for i in res]

    content = {
        'data_list':data_list,
    }

    return render(request, 'ksh/part4.html', content)

def part5(request):

    # 景点地区分布
    sql = 'select * from part6'
    res = util.query(sql)
    mapData = [{'name':i[1], 'value':i[2]} for i in res]

    content = {
        'mapData':mapData,
    }

    return render(request, 'ksh/part5.html', content)
