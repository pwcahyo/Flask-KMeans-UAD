# Import flask dependencies
from flask import Blueprint, request, render_template, jsonify
import numpy as np
import json

mod_purity = Blueprint('purity', __name__, url_prefix='/mod_purity')

@mod_purity.route('', methods=['GET','POST'])
def purity_route():
	results = 0
	status = 404
	clusters = list(json.loads(request.form['clusters']))
	clusters = filter(None, clusters)
	clusters = list(map(int, clusters))
	class_true = request.form['class_true']
	class_true = class_true.split(',')
	class_true = list(map(int, class_true))
	if(len(class_true) == len(clusters)):
		results = purity_score(clusters, class_true)
		message = True
	else:
		results = 'jumlah class tidak sesuai'
		message = False

	return jsonify(
		results = results,	
        message = message
    )
	# # Setting title
	# mainTitle = request.form["mainTitle"]
	# subTitle = "Silahkan cleaning data"

	# # Get table from input type selectedColumn
	# selectedColumn = request.form["selectedColumn"]
	# table = load_data_selected(selectedColumn)
	# data = table[1]

	# #Setting button and Command
	# button = ['Cleaning Data', 'hidden','%smod_cleaning'%(str(request.url_root))] #request.url_root = ambil root host, format button = [nama button, url]
	# command = "Tekan tombol %s agar data siap dilakukan cluster"%(button[0])

	# return render_template('upload/tables.html',tables=[data.to_html(classes='Alumni')], text = [mainTitle, subTitle, command, selectedColumn], button=button)

def purity_score(clusters, classes):
    A = np.c_[(clusters,classes)]

    n_accurate = 0.

    for j in np.unique(A[:,0]):
        z = A[A[:,0] == j, 1]
        x = np.argmax(np.bincount(z))
        n_accurate += len(z[z == x])

    return n_accurate / A.shape[0]
