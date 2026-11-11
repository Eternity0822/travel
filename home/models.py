
from django.db import models

# 创建旅游景点数据库模型
class TravelInfo(models.Model):
    unique_id = models.BigIntegerField(null=True, verbose_name='景点id')  # 唯一标识符
    area = models.CharField(max_length=255, null=True, verbose_name='区域名称')  # 区域名称
    name = models.CharField(max_length=255, null=True, verbose_name='景点名称')  # 景点名称
    review_count = models.IntegerField(null=True, verbose_name='评论数量')  # 评论数量
    rating = models.CharField(max_length=50, null=True, verbose_name='评分')  # 评分
    is_ad = models.BooleanField(default=False, verbose_name='是否为广告')  # 是否为广告
    is_recommended = models.BooleanField(default=False, verbose_name='是否为推荐')  # 是否为推荐
    city = models.CharField(max_length=50, null=True, verbose_name='城市名称')  # 城市
    image_url = models.CharField(max_length=500, null=True, verbose_name='封面图片链接')  # 图片链接
    distance_from_center = models.CharField(max_length=255, null=True, verbose_name='到市中心的距离')  # 市中心距离
    tags = models.CharField(max_length=255, null=True, verbose_name='标签列表')  # 标签
    detail_link = models.CharField(max_length=500, null=True, verbose_name='详情页链接') # 详情页链接
    market_price = models.CharField(max_length=255, null=True, verbose_name='市场价') # 市场价
    discount_price = models.CharField(max_length=255, null=True, verbose_name='优惠价') # 优惠价
    discount_description = models.CharField(max_length=255, null=True, verbose_name='优惠描述') # 优惠描述
    actual_price = models.CharField(max_length=255, null=True, verbose_name='价格') # 价格（实际票价）
    price_type = models.CharField(max_length=255, null=True, verbose_name='价格类型') # 价格类型
    price_type_description = models.CharField(max_length=255, null=True, verbose_name='价格类型描述') # 价格类型描述
    is_free = models.BooleanField(default=False, null=True, verbose_name='是否免费') # 是否免费
    latitude = models.FloatField(null=True, verbose_name='纬度') # 纬度
    longitude = models.FloatField(null=True, verbose_name='经度') # 经度
    popularity_score = models.CharField(max_length=255, null=True, verbose_name='热度评分') # 热度评分
    province = models.CharField(max_length=100, null=True, verbose_name='省份') # 省份

    class Meta:
        verbose_name_plural = '旅游景点管理'
