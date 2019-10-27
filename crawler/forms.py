from django import forms


class SelectCrawlingModelForm(forms.Form):
    option = forms.ChoiceField(initial='all',
                               label='جهت شروع فرآیند، لطفا یکی از گزینه‌های زیر را انتخاب نمایید:',
                               choices=(('all', 'همه محصولات'), ('custom', 'تنظیمات اختیاری')),
                               widget=forms.RadioSelect())
