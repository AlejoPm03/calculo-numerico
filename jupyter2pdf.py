import os
from datetime import date


def maketitle(title, author, subject):
	return '''
\\begin{titlepage}
    \\begin{center}
        \\vspace*{1cm}



        \\vspace{0.5cm}
        \\Large{Instituto Federal de Santa Catarina\\\\
        ''' +subject + '''}

        \\vspace{5.5cm}

        \\textbf{''' + title + '''}\\\\
        \\textbf{''' + author + '''}

        \\vfill

        Florianópolis\\\\
        ''' + str(date.today()) + '''

    \end{center}
\end{titlepage}
'''

def create_directory(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)

def get_notebook_files():
	files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.ipynb') and f != 'fix-latex.ipynb']
	return files

def select_files_to_convert(files):
	files_str = 'Files to convert to latex:'
	for i, f in enumerate(files):
		files_str += '\n' + str(f'{i+1}. {f}')
	files_to_convert = input(f"Enter the numbers of the files to convert separated by a space: \n {files_str}\n").split(' ')
	return [files[int(i)-1] for i in files_to_convert]

def convert_to_latex(files, latex_dir):
	for f in files:
		if os.path.exists(f'{latex_dir}/{f[:-6]}.tex'):
			overwrite = input(f'File {f[:-6]}.tex already exists, do you want to overwrite it? (y/n): ')
			if overwrite == 'y':
				os.system(f'jupyter nbconvert --to latex {f} --output-dir {latex_dir}')
		else:
			os.system(f'jupyter nbconvert --to latex {f} --output-dir {latex_dir}')

def fix_latex_files(files, latex_dir, fixed_files_dir, author, maketitle):
	for f in files:
		f = f[:-6] + '.tex'
		print(f'Fixing {f}')
		with open(f'{latex_dir}/{f}', 'r') as file:
			create_directory(fixed_files_dir)
			
			# Copy the files dir of the latex file
			os.system(f'cp -r {latex_dir}/{f[:-4] + "_files"} {fixed_files_dir}/')
			# Copy the assets folder
			os.system(f'cp -r assets {fixed_files_dir}/')

			title = input(f'Enter the title of the document {f[:-4]}: ')
			fixed_file_name = f'{author.replace(" ", "-")}-{title.replace(" ", "-")}.tex'
			if os.path.exists(f'{fixed_files_dir}/{fixed_file_name}'):
				os.remove(f'{fixed_files_dir}/{fixed_file_name}')
			with open(f'{fixed_files_dir}/{fixed_file_name}', 'w') as fixed_file:
				lines = file.readlines()
				lines[0] = lines[0].replace('[11pt]', '')
				for i, line in enumerate(lines):
					if '\\title' in line:
						line = '\\title{' + title + '}\n'
					elif '\\maketitle' in line:
						line = maketitle(title, author, subject)
					fixed_file.write(line)

def convert_to_pdf(input_dir, output_dir):
	files = [filename for filename in os.listdir(input_dir) if filename.endswith('.tex')]
	for f in files:
		create_directory(output_dir)
		convert = input(f'Convert {f[:-4]} to pdf? (y/n): ')
		if convert == 'n':
			continue
		if os.path.exists(f'{pdf_dir}/{f[:-4]}.pdf'):
			overwrite = input(f'File {f[:-4]}.pdf already exists, do you want to overwrite it? (y/n): ')
			if overwrite == 'n':
				continue
		os.system(f'tectonic -o {output_dir} {input_dir}/{f}')

def ask_for_author():
	authors = ['Alejo Perdomo Milar', 'João Mário C. I. Lago', 'Alejo Perdomo Milar e João Mário C. I. Lago']
	authors_str = 'Authors:\n'
	for i, author in enumerate(authors):
		authors_str += (f'{i+1}. {author}\n')
	author = input(f'Enter the author of the document: \n {authors_str}')
	return authors[int(author)-1]

def ask_for_subjects():
	subjects = ['Cálculo numérico']
	subjects_str = 'Subjects:\n'
	for i, subject in enumerate(subjects):
		subjects_str += (f'{i+1}. {subject}\n')
	subject = input(f'Enter the subject of the document: \n {subjects_str}')
	return subjects[int(subject)-1]


if __name__ == "__main__":
	latex_dir = 'latex_alejo'
	fixed_files_dir = latex_dir + '/fixed-files'
	pdf_dir = 'pdf_alejo'
	author = ask_for_author()
	subject = ask_for_subjects()

	create_directory(latex_dir)
	files = get_notebook_files()
	files_to_convert = select_files_to_convert(files)
	convert_to_latex(files_to_convert, latex_dir)
	fix_latex_files(files_to_convert, latex_dir, fixed_files_dir, author, maketitle)
	convert_to_pdf(fixed_files_dir, pdf_dir)
