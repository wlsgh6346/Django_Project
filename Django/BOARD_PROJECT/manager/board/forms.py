from django import forms


class BoardForm(forms.Form):
    title = forms.CharField(
        error_messages={
            'required': '제목을 입력해주세요.'
        },
        max_length=128, label="제목")
    contents = forms.CharField(
        error_messages={
            'required': '내용을 입력해주세요.'
        },
        widget=forms.Textarea, label="내용")
    writer = forms.CharField(max_length=32, label="작성자")


class CommentForm(forms.Form):
    comment = forms.CharField(
        error_messages={
            'required': '내용 입력해주세요.'
        },
        max_length=255, label="댓글")
