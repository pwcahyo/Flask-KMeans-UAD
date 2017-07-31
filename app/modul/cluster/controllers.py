# Import flask dependencies
from flask import Blueprint, request, render_template
from sklearn.cluster import KMeans
from openpyxl import load_workbook
import string
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import StringIO
import base64
import dbmodel as d
import silhoutte

mod_cluster = Blueprint('cluster', __name__, url_prefix='/mod_cluster')

@mod_cluster.route('', methods=['POST'])
def cluster():
	clusters = request.form["selectedColumn"]

	# Setting title
	mainTitle = request.form["mainTitle"]
	subTitle = "Data berhasil di jadikan %s clusters"%(clusters)

	# get table to mongodb
	dbmodel = d.DBModel()
	getDataCleaning = dbmodel.get_data_all("Alumni_UAD", "cleaning")
	getHeader = dbmodel.get_data_all("Alumni_UAD", "header")

	header = []

	for head in getHeader:
		for index in range(len(head)-1):
			header.append(head[str(index)])

	data = []
	for val in getDataCleaning:
		temp_val = []
		for head in header:
			temp_val.append(val[head])
		data.append(temp_val)

	result_kmeans = kmeans(data, int(clusters))

	# insert table to mongodb
	dbmodel = d.DBModel()

	dbmodel.drop_collection("Alumni_UAD", "cluster")

	list_data = []
	for val in result_kmeans['data_cluster']:
		temp_data = {}
		temp_data['coordinate'] = val['coordinate']
		for index, data in enumerate(val['data']):
			temp_data[header[index]] = data
		temp_data['cluster'] = int(val['cluster'])
		dbmodel.insert_one("Alumni_UAD", "cluster", temp_data)
		list_data.append(temp_data)
		

	img = StringIO.StringIO()
	result_kmeans['plot'].savefig(img, format='png')
	img.seek(0)
	plot_url = base64.b64encode(img.getvalue())

	results = pd.DataFrame(list_data)
	results = results.drop('_id', 1)

	#Setting button and Command
	button = ['Kembali Upload Data', 'hidden', '%smod_upload'%(str(request.url_root))] #request.url_root = ambil root host, format button = [nama button, url]
	command = "Tekan tombol %s, untuk kembali melakukan cluster dengan data yang baru"%(button[0])

	return render_template('upload/tables.html',tables=[results.to_html(classes='Alumni', index=False)], text = [mainTitle, subTitle, command], button=button, plot_url=plot_url)

def kmeans(X, clusters):
	kmeans = KMeans(n_clusters=clusters)
	kmeans.fit(X)

	centroids = kmeans.cluster_centers_
	labels = kmeans.labels_

	colors = ['g.','r.','b.','m.','g.','c.','y.']

	plt.figure(figsize=(10,5))

	results = {}
	list_cluster = []
	point = {}
	plt.scatter(centroids[:, 0], centroids[:, 1], marker = 'x', s=80, linewidths=10, zorder=30)
	for i in range(len(X)):
		data = {}
		data['coordinate'] = i
		data['data'] = X[i]
		data['cluster'] = labels[i]
		list_cluster.append(data)
		index = str('%s%s'%(X[i][0], X[i][1])).replace('.','')
		if len(X[i]) > 2:
			plt.close()
		else:
			if index in point:
				point[index]+=', %s'%(str(i))
			else:
				point[index]=str(i)
				plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
		    	plt.text(X[i][0], X[i][1], '%s'%(point[index]))

	results['data_cluster'] = list_cluster
	results['plot'] = plt

	return results