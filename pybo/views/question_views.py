from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

########################################################################################################

@login_required(login_url='common:login')
def question_create(request):
    ''' pybo 질문등록 '''
    #
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        #
        if form.is_valid():
            question = form.save(commit=False)  # commit=False는 데이터베이스에 저장하지 않고 모델 객체만 반환
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            #
            return redirect('pybo:index')
            #
        #
    else:
        form = QuestionForm()  # GET 요청인 경우 빈 QuestionForm 객체를 생성
        #
    #
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)  # question_form.html 파일을 렌더링하여 HTML 코드로 변환한 결과를 HttpResponse 객체로 반환
    #
#

########################################################################################################

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """ pybo 질문 수정 """
    #
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, 

        '수정권한이 없습니다'

        )
        #
        return redirect('pybo:detail', question_id=question.id)
        #
    #
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        #
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
            #
        #
    #
    else:
        form = QuestionForm(instance=question)
        #
    #
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
    #
#

########################################################################################################

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """ pybo 질문 삭제 """
    #
    question = get_object_or_404(Question, pk=question_id)
    #
    if request.user != question.author:
        messages.error(request, 

        '삭제권한이 없습니다'

        )
        #
        return redirect('pybo:detail', question_id=question.id)
        #
    #
    question.delete()
    return redirect('pybo:index')
    #
#

########################################################################################################

@login_required(login_url='common:login')
def question_vote(request, question_id):
    """ pybo 질문 추천 """
    #
    question = get_object_or_404(Question, pk=question_id)
    #
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
        #
    #
    else:
        question.voter.add(request.user)
        #
    #
    return redirect('pybo:detail', question_id=question.id)
    #
#

########################################################################################################