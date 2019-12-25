from django import forms
from users.models import User


class SelectCrawlingModelForm(forms.Form):
    option = forms.ChoiceField(initial='all',
                               label='جهت شروع فرآیند، لطفا یکی از گزینه‌های زیر را انتخاب نمایید:',
                               choices=(('all', 'همه محصولات'), ('custom', 'تنظیمات اختیاری')),
                               widget=forms.RadioSelect())


class CustomForm(forms.Form):
    SelectList = (("mofidteb", "مفیدطب"), ("darukade", "داروکده"), ("mosbatesabz", "مثبت سبز"),
                  ("digikala", "دیجیکالا"), ("ezdaroo", "ایزی دارو"), ("shiderstore", "شیدر"))

    users = forms.MultipleChoiceField(label="ارسال اعلانات برای افراد منتخب",
                                      required=True,
                                      choices=((user.username, user.get_full_name()) for user in User.objects.all()),
                                      # choices=((1, 1), (2, 2)),
                                      error_messages={'required': 'حداقل یکی از کاربران باید انتخاب گردد'},
                                      widget=forms.CheckboxSelectMultiple)

    sites = forms.MultipleChoiceField(label="سایت های مورد نظر",
                                      required=True,
                                      initial=[site[0] for site in SelectList],
                                      choices=SelectList,
                                      error_messages={'required': 'حداقل یکی از سایت های موردنظر باید انتخاب گردد'},
                                      widget=forms.CheckboxSelectMultiple)

