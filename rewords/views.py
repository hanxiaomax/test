#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from models import Notes,Words,LearningPlan,LearningList
from django.http import JsonResponse
from bs4 import BeautifulSoup
import arrow
import logging
import os
import requests
logger = logging.getLogger(__name__)
history_logger = logging.getLogger("history_logger")

headers = {
	    "Accept": "*/*",
	    "Accept-Encoding": "gzip,deflate",
	    "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
	    "Connection": "keep-alive",
	    "User-Agent": "Mozilla/5.1 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
	    }
# Create your views here.

def login(request):
	c=  {}
	c.update(csrf(request))
	return render_to_response('login.html',c)

def auth_view(request):
	username=request.POST.get('username')
	password=request.POST.get('password')
	user=auth.authenticate(username=username,password=password)
	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/login')	

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')


def index(request):
	#saveword2db() #导入单词
	#YouDaoSpider()  #爬取单词信息
	if request.user.is_authenticated():
		params={
			'user':request.user,
		}
		return render(request, 'index.html',params)
	else:
		return HttpResponseRedirect('/login')

def addNewNote(request):
	notebody = request.GET.get('note')
	word_id = request.GET.get('word_id')
	word=Words.objects.get(id=word_id)
	Notes.objects.create(
							author = request.user,
							target_word = word,
							body=notebody,
							time=arrow.utcnow().datetime
	)
	return JsonResponse({'status':'ok'})


def setLearningPlan(request):
	"设置或修改个人学习计划和单词等级"
	level = int(request.POST.getlist('levelselect')[0])#等级为1-4的数字
	number =  int(request.POST.get('number'))
	user = request.user
	try:
		plan = LearningPlan.objects.get(user=user)
		plan.level = level
		plan.num = number
		plan.save()
	except:
		LearningPlan.objects.create(
				level = level,
				num = number,
				user = request.user,
			)
	return HttpResponseRedirect('/')


def loadwordlist(request):
	"加载待学习单词表"
	user = request.user
	# "首先要设定学习计划否则会报错
	try:
		plan = LearningPlan.objects.get(user=user)
		number = plan.num
		level = plan.level
	except Exception, e:
		# 创建默认计划
		number = 50
		level = 1
		LearningPlan.objects.create(
				level = level,
				num = number,
				user = request.user,
			)
	#首先尝试从正在学习的单词中抽取 number 个
	#条件：	1.复习次数不满8次
	#		2.达到需要再次复习的时间（复习频率逐渐降低）
	print number
	review_words = LearningList.objects.filter(word__level=level,
												author=user,
												repeat_times__lt=8,
												review_time__lte=arrow.now().datetime).order_by('id')[:number]
	
	
	# 确定实际抽取的个数
	review_count = review_words.count()
	print review_count
	# 查询已经学习过的单词
	learning_words = LearningList.objects.filter(word__level=level,author=user).all()

	word_list={}
	for index,review_word in enumerate(review_words):
		word_list[review_word.word.english.strip('\n')]=review_word.word.toDict()

	#如果不足 number 则从单词表中提取剩余单词，作为新词
	if review_count<number:
		#需要过滤掉已经学习过的单词
		words = Words.objects.filter(level=level).exclude(id__in=[word.word_id for word in learning_words]).order_by('id')[:(number-review_count)]
		for index,word in enumerate(words):
			word_list[word.english.strip('\n')]=word.toDict()

	try:
		new_count = words.count()
	except Exception:
		new_count = 0;

	result = {
				'word_list':word_list,
				'review_count':review_count,
				'new_count':new_count
			}
	return JsonResponse(result)
	
def learningList(request):
	user=request.user
	repeat = int(request.GET.get('repeat'))#1或-1
	word_id = request.GET.get('word_id')
	word=Words.objects.get(id=word_id)	

	#复习单词
	try:
		w = LearningList.objects.get(word=word)
		if w.repeat_times + repeat < 0:
			w.repeat_times= 1#最少已重复次数为1
		else:
			w.repeat_times = w.repeat_times+repeat

		#下次复习时间为当前时间+（已重复次数-1）天
		#1/1 1/2 1/4 1/7 ....
		w.review_time = arrow.now().replace(days=w.repeat_times-1).datetime
		w.save()
	#首次学习
	except Exception:
		history_logger.info(u"存放新单词到学习列表")
		LearningList.objects.create(
			author = user,
			word = word,
			repeat_times=1,
			review_time=arrow.now().datetime
		)
	return HttpResponse(status=200)


def YouDaoSpider():
	"有道词典小爬虫"
	words = Words.objects.all().order_by('id')
	for index,word in enumerate(words):
		try:
			r = requests.get('http://dict.youdao.com/w/{0}/'.format(word.english),headers=headers)
			print index
			soup = BeautifulSoup(r.text)

			means = soup.find_all('div',class_='trans-container')[0].find_all('li')
			explanation = ""
			for mean in means:
				explanation += mean.text+'|'
			word.explanation = explanation
			try:
				synonyms = soup.find_all('div',id="synonyms")[0].find_all('p',class_='wordGroup')[0].find_all('span')
				syns = ""
				for syn in synonyms:
					syns+=syn.text.replace(' ','').replace(',','')+'|'
				word.synonym = syns
			except Exception, e:
				print "synonyms",e
			try:
				bilinguals = soup.find_all('div',id='bilingual')[0].find_all('p')
				example=""
				for bi in bilinguals:
					
					example += bi.text.strip('\n')+'|'
					
				word.example = example
			except Exception, e:
				print "bilinguals",e
			
			word.save()
		except Exception, e:
			print index,e

def saveword2db():
	"导入数据库"
	addwordsFromFile('CET4.txt',1)
	addwordsFromFile('CET6.txt',2)
	addwordsFromFile('TOEFL.txt',3)
	addwordsFromFile('IELTS.txt',4)



def addwordsFromFile(filename,level):
	"将文件单词表导入数据库"
	with open(os.getcwd()+'/'+filename,'r') as f:
		for word in set(f.readlines()):
			Words.objects.create(
							english = word,
							explanation = '',
							example = '',
							synonym = '',
							level = level
			)
