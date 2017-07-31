# Import flask dependencies
from flask import Blueprint, request, render_template
from openpyxl import load_workbook
import string
import pandas as pd
import dbmodel as d

mod_select_column = Blueprint('selected_column', __name__, url_prefix='/mod_select_column')
mod_cleaning = Blueprint('cleaning', __name__, url_prefix='/mod_cleaning')

@mod_select_column.route('', methods=['POST'])
def select_column():
	# Setting title
	mainTitle = request.form["mainTitle"]
	subTitle = "Silahkan cleaning data"

	# Get table from input type selectedColumn
	selectedColumn = request.form["selectedColumn"]
	table = load_data_selected(selectedColumn)
	data = table[1]

	#Setting button and Command
	button = ['Cleaning Data', 'hidden','%smod_cleaning'%(str(request.url_root))] #request.url_root = ambil root host, format button = [nama button, url]
	command = "Tekan tombol %s agar data siap dilakukan cluster"%(button[0])

	return render_template('upload/tables.html',tables=[data.to_html(classes='Alumni')], text = [mainTitle, subTitle, command, selectedColumn], button=button)

@mod_cleaning.route('', methods = ['POST'])
def cleaning_data():
	# Setting title
	mainTitle = request.form["mainTitle"]
	subTitle = "Data berhasil melalui tahap cleaning"

	# Get table from input type selectedColumn
	selectedColumn = request.form["selectedColumn"]
	table = load_data_selected(selectedColumn)
	selectedColumn = '' #reset selected column

	# Cleaning data
	temp_data_clean = cleaning_str_to_float(table)
	data = temp_data_clean[1]

	header = {}
	for index, head in enumerate(table[0]):
		header[str(index)] = head

	# return str(data)

	# insert table to mongodb
	dbmodel = d.DBModel()
	result_insert_table = dbmodel.insert_cleaning_data("Alumni_UAD", "cleaning", data)
	result_insert_header = dbmodel.insert_header("Alumni_UAD", "header", header)

	#Setting button and Command
	command = "Lanjutkan ke tahap cluster, masukan jumlah cluster"
	button = ['Cluster', 'text','%smod_cluster'%(str(request.url_root))] #request.url_root = ambil root host, format button = [nama button, url]
	
	return render_template('upload/tables.html',tables=[data.to_html(classes='Alumni')], text = [mainTitle, subTitle, command, selectedColumn], button=button)

def load_data_selected(selectedColumn):
	# Load data dari file excel
	wb = load_workbook(filename = 'app/upload_data/DATA EXCEL.xlsx')
	sheet_ranges = wb['Sheet5']
	data = pd.DataFrame(sheet_ranges.values)

	# Ambil data berdasarkan kolom inputan
	selectedColumn = selectedColumn
	cols = selectedColumn.split(",")
	cols = list(map(int, cols)) # convert str to int
	data = data[cols] 

	# Setting header
	header = data.iloc[0].tolist() # ambil data baris pertama untuk dijadikan header
	data = data.drop([0]) # hapus data baris pertama
	data.columns = header

	table_data = [header, data]

	return table_data

def cleaning_str_to_float(table):
	for index in table[0]:
		replace_none = table[1][index].fillna(0)
		temp_str = replace_none.apply(str)
		str_replace = temp_str.str.replace(',','.')
		str_to_float = str_replace.apply(float)
		table[1][index] = str_to_float

	return table