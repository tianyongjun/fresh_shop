
from django import forms

from goods.models import Goods, GoodsCategory


class GoodsForm(forms.Form):
    """
    商品表单
    """
    category = forms.CharField(required=True,error_messages={'required': '商品分类必填'})
    goods_sn = forms.CharField(required=True, error_messages={'required': '商品唯一货号必填'})
    name = forms.CharField(required=True, error_messages={'required': '商品名称必填'})
    goods_nums = forms.IntegerField(required=True,
                                    error_messages={'required': '商品库存必填',
                                                    'invalid': '库存数为整型'})
    market_price = forms.DecimalField(required=True,
                                      error_messages={'required': '市场价格必填',
                                                      'invalid': '市场价格为整型'})
    shop_price = forms.DecimalField(required=True,
                                    error_messages={'required': '本店价格必填',
                                                    'invalid': '本店价格为整型'})
    goods_front_image = forms.ImageField(required=False)
    goods_brief = forms.CharField(required=False,
                                  error_messages={'required': '商品简短描述必填'})

    def clean_category(self, *args, **kwargs):
        category = self.cleaned_data.get('category')
        goods_category = GoodsCategory.objects.filter(category_type=category)
        if goods_category:
            goods_category = goods_category.first()
            return goods_category
        else:
            raise forms.ValidationError({'category': '商品分类错误'})