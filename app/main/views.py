from flask_login import login_required,current_user#intercept a request and check is user is authenticated
from .forms import NewPitchForm
from flask import render_template,redirect,url_for,abort
from . import main
from ..models import Categories,User,PitchList#ineter python relative import system
from .. import db#external python import system


@main.route('/')
def index():
	'''
	main pages that returns a list of pitch category on the index page
	'''
	categories = Categories.list_categories()
	title = 'Home - welcome to Pitch Perfect'
	return render_template('index.html',title = title, categories = categories)

@main.route('/category/<int:id>')
def category(id):
	'''
	This route witll return the list of pitches for that particular category
	'''
	category = Categories.query.get(id)

	if category is None:
		abort(404)

	pitches = PitchList.list_all_pitches(id)
	#form = NewPitchForm()
	title = "PITCHES"

	return render_template('categories.html',title = title,category = category,pitches = pitches)

@main.route('/category/pitch/new/<int:id>', methods = ['GET','POST'])
@login_required#intercepts request to see if user is authenticated
def new_pitch(id):
		'''
		route for a displaying a new pitch form
		'''
		form = NewPitchForm()
		category = Categories.query.filter_by(id=id).first()

		if category is None:
			abort(404)

		if form.validate_on_submit():
			lines = form.lines.data
			new_pitch = PitchList(lines=lines,user_id=current_user.id,category_id=category.id)
			new_pitch.add_pitches()
			return redirect(url_for('.category', id = category.id))

		title = 'NEW PITCH'
		return render_template('new_pitch.html',title = title,pitch_form = form)

#@main.route('/category/pitch/new/<int:id>',methods = ["GET","POST"])
#@login_required
#def new_pitch(id):
	#'''
	#route for a displaying a new pitch form
	#'''
	#form = NewPitchForm()#
	#specific_category = Categories.query.filter_by(id=id).first()#get specific category

	#if specific_category in None:
		#abort(404)

	#if form.validate_on_submit():
		#lines = form.lines.data
		#update pitch instance
		#new_pitch = NewPitchForm(lines = lines,user_id = current_user.id,category_id = category.id)
		#save pitch to db
		#new_pitch.add_pitches()
		#return redirect(url_for('.category', id = category.id))

	#title = 'NEW PITCH'
	#return render_template('new_pitch.html',title = title, pitch_form = form)


@main.route('/pitch/<int:id>',methods = ['GET','POST'])
@login_required
def specific_pitch(id):
	'''
	returns specific pitch where comments can be viewed and added
	'''

	pitches = PitchList.query.get(id)

	if pitches is None:
		abort(404)

	title = 'COMMENTS'
	return render_template('pitch.html',title = title,pitches = pitches)
