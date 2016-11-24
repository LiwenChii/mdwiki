import os

from flask import Blueprint, jsonify
from flask import render_template
from flask import request
from flask_login import login_required

from app import util
admin=Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/image/index')
@login_required
def imageIndex():
	imgDir=util.getAbsDataItemPath("upload")
	images=list()
	curPage=int(request.args.get('curPage',1))
	pageSize=int(request.args.get('pageSize',10))
	for filename in os.listdir(imgDir):
		if os.path.splitext(filename)[1][1:] in ['png','jpg','bmp','gif','jpeg']:
			img=dict(path='upload'+os.sep+filename,link='/data/upload/'+filename)
			images.append(img)
	if request.is_xhr:
		return jsonify(images[(curPage-1)*pageSize:curPage*pageSize])
	else:
		return render_template('picManager.html',images=images[:10],maxPage=len(images)//pageSize+1)

@admin.route('/image/delete',methods=['GET','POST'])
@login_required
def imageDelete():
	if request.args.get('path',''):
		path=util.urlDirPathFormat(request.args.get('path',''))
		path=util.getAbsDataItemPath(path)
		if os.path.exists(path):
			os.remove(path)
	return jsonify({'status':'ok'})