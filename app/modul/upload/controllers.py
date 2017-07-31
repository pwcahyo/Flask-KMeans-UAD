# Import flask dependencies
from flask import Blueprint, request, render_template
from openpyxl import load_workbook
from werkzeug import secure_filename
import pandas as pd
import os

mod_upload = Blueprint('upload', __name__, url_prefix='/mod_upload')
mod_uploader = Blueprint('uploader', __name__, url_prefix='/mod_uploader')

mainTitle = "Data Alumni UAD"

@mod_upload.route('', methods = ['GET','POST'])
def upload_file():
   return render_template('upload/upload.html')
	
@mod_uploader.route('', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
   		subTitle = ("Pilih Kolom Data Cluster")
   		command = "Masukan urutan kolom yang akan dilakukan cluster (pisahkan degan koma)"
		f = request.files['file']
		f.save(os.path.join('app/upload_data', 'DATA EXCEL.xlsx'))
		wb = load_workbook(filename = 'app/upload_data/DATA EXCEL.xlsx')
		sheet_ranges = wb['Sheet5']
		data = pd.DataFrame(sheet_ranges.values)

		button = ['Pilih Kolom', 'text','%smod_select_column'%(str(request.url_root))] #request.url_root = ambil root host, format button = [nama button, url]
		return render_template('upload/tables.html',tables=[data.to_html(classes='Alumni')], text = [mainTitle, subTitle, command], button=button, data=data)